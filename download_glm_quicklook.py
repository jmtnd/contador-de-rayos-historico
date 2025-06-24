import os
import subprocess
from datetime import datetime, timedelta

# --- Configuración ---
BASE_S3_PATH = "GLM-L2-LCFA"

# --- Funciones auxiliares ---
def julian_day(year, month, day):
    dt = datetime(year, month, day)
    return dt.timetuple().tm_yday

def list_available_nc(bucket, year, jday, hour):
    s3_dir = f"s3://{bucket}/{BASE_S3_PATH}/{year}/{jday:03d}/{hour:02d}/"
    print(f"Buscando NetCDF disponibles en: {s3_dir}")
    result = subprocess.run([
        "aws", "s3", "ls", s3_dir, "--no-sign-request"
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error al listar archivos: {result.stderr}")
        return []
    files = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) == 4 and parts[3].endswith(".nc"):
            files.append(parts[3])
    return files

def extract_minute_from_filename(fname):
    # Ejemplo: OR_GLM-L2-LCFA_G19_s20251530002000_e20251530002200_c20251530002219.nc
    # Extrae el minuto de inicio (los dos dígitos después de la hora)
    try:
        s = fname.split('_')[4]  # s20251530002000
        minute = int(s[11:13])
        return minute
    except Exception:
        return None

def download_file(bucket, s3_key, dest_folder, year, jday, hour):
    url = f"s3://{bucket}/{BASE_S3_PATH}/{year}/{jday:03d}/{hour:02d}/{s3_key}"
    dest = os.path.join(dest_folder, os.path.basename(s3_key))
    print(f"Descargando: {url}")
    result = subprocess.run([
        "aws", "s3", "cp", url, dest, "--no-sign-request"
    ], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✔ Guardado en {dest}")
    else:
        print(f"✗ No se pudo descargar {url}\n{result.stderr}")

def plot_flashes(dest_folder):
    try:
        import xarray as xr
        import matplotlib.pyplot as plt
        import cartopy.crs as ccrs
        import numpy as np
        from pathlib import Path
    except ImportError:
        print("Faltan dependencias. Instala con: pip install xarray matplotlib cartopy")
        return
    folder = Path(dest_folder)
    files = sorted(folder.glob("*.nc"))
    if not files:
        print("No se encontraron archivos NetCDF en la carpeta para graficar.")
        return
    print("Procesando archivos para graficar flashes...")

    # Coordenadas del punto de interés (Loreto)
    target_lat = 26.00586
    target_lon = -111.35247
    
    # Rango de 100 km
    lat_range = 0.9
    lon_range = 0.9
    
    all_lats = []
    all_lons = []
    
    for f in files:
        with xr.open_dataset(f) as ds:
            if 'flash_lat' in ds and 'flash_lon' in ds:
                all_lats.extend(ds['flash_lat'].values)
                all_lons.extend(ds['flash_lon'].values)

    if not all_lats:
        print("No se encontraron datos de flashes en los archivos.")
        return

    lats = np.array(all_lats)
    lons = np.array(all_lons)
    total_flashes = len(lats)

    # Filtrar flashes dentro del radio de 100km
    nearby_mask = (lons >= target_lon - lon_range) & (lons <= target_lon + lon_range) & \
                  (lats >= target_lat - lat_range) & (lats <= target_lat + lat_range)
    nearby_flash_count = np.sum(nearby_mask)
    
    print(f"\n--- Análisis de Rayos ---")
    print(f"Total de flashes detectados (en todo el dominio): {total_flashes}")
    print(f"Flashes dentro de ~100 km de Loreto: {nearby_flash_count}")
    print("--------------------------")

    # --- Mapa 1: Detallado en Loreto ---
    fig1, ax1 = plt.subplots(figsize=(12, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax1.set_title(f'Análisis Detallado en Loreto, BCS\n{nearby_flash_count} flashes en un radio de ~100 km', fontsize=14, fontweight='bold')
    ax1.coastlines(resolution='10m', color='black')
    
    # Graficar solo flashes cercanos
    if nearby_flash_count > 0:
        ax1.scatter(lons[nearby_mask], lats[nearby_mask], s=30, c='red', alpha=0.7, transform=ccrs.PlateCarree())

    # Marcar punto de interés y radio
    ax1.scatter(target_lon, target_lat, s=200, c='blue', marker='*', zorder=10, label='Loreto')
    circle_lons = target_lon + lon_range * np.cos(np.linspace(0, 2 * np.pi, 100))
    circle_lats = target_lat + lat_range * np.sin(np.linspace(0, 2 * np.pi, 100))
    ax1.plot(circle_lons, circle_lats, 'b--', linewidth=2, transform=ccrs.PlateCarree(), label='Radio ~100 km')
    
    ax1.set_extent([target_lon - lon_range, target_lon + lon_range, target_lat - lat_range, target_lat + lat_range])
    ax1.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
    ax1.legend()
    plt.show()

    # --- Mapa 2: Contexto General ---
    if total_flashes > 0:
        print("\nMostrando mapa de contexto general para ubicar la tormenta...")
        fig2, ax2 = plt.subplots(figsize=(12, 10), subplot_kw={'projection': ccrs.PlateCarree()})
        ax2.set_title(f'Mapa de Contexto - {total_flashes} flashes totales detectados', fontsize=14, fontweight='bold')
        ax2.coastlines(resolution='50m', color='black')
        ax2.add_feature(ccrs.cartopy.feature.BORDERS, linestyle=':')
        
        # Graficar todos los flashes
        ax2.scatter(lons, lats, s=5, c='red', alpha=0.5, transform=ccrs.PlateCarree())
        
        # Dibujar el recuadro del mapa detallado
        rect_lons = [target_lon - lon_range, target_lon + lon_range, target_lon + lon_range, target_lon - lon_range, target_lon - lon_range]
        rect_lats = [target_lat - lat_range, target_lat - lat_range, target_lat + lat_range, target_lat + lat_range, target_lat - lat_range]
        ax2.plot(rect_lons, rect_lats, 'b-', linewidth=2, transform=ccrs.PlateCarree(), label='Zona de Loreto')
        
        ax2.set_extent([-118, -105, 22, 33]) # Vista del Noroeste de México
        ax2.gridlines(draw_labels=True)
        ax2.legend()
        plt.show()
    else:
        print("No se generó mapa de contexto porque no se detectaron flashes.")

# --- Interfaz de usuario ---
def main():
    print("Descarga de archivos NetCDF GLM para un DÍA LOCAL COMPLETO")
    
    # --- Selección de Satélite ---
    print("Selecciona el satélite a consultar:")
    print("1: GOES-19 (más moderno, operativo desde ~2024)")
    print("2: GOES-18 (operativo desde ~2022)")
    print("3: GOES-17 (operativo desde ~2018)")
    print("4: GOES-16 (Este, puede no tener cobertura)")
    
    satellite_choice = input("Opción (1-4): ").strip()
    
    if satellite_choice == '2':
        BUCKET = "noaa-goes18"
    elif satellite_choice == '3':
        BUCKET = "noaa-goes17"
    elif satellite_choice == '4':
        BUCKET = "noaa-goes16"
    else:
        BUCKET = "noaa-goes19" # Por defecto GOES-19
        
    print(f"Consultando el bucket: {BUCKET}")

    # --- Petición de fecha local ---
    print("\nIntroduce la fecha local de interés:")
    year = int(input("Año (YYYY): "))
    month = int(input("Mes (1-12): "))
    day = int(input("Día (1-31) de Loreto: "))
    
    # --- Conversión de hora local de Loreto (UTC-7) a rangos UTC ---
    local_start = datetime(year, month, day, 0, 0)
    utc_start = local_start + timedelta(hours=7)
    utc_end = utc_start + timedelta(days=1)
    
    print(f"\nBuscando datos para el día {year}-{month}-{day} en Loreto...")
    print(f"Esto corresponde al intervalo UTC: {utc_start.strftime('%Y-%m-%d %H:%M')} a {utc_end.strftime('%Y-%m-%d %H:%M')}")
    
    dest_folder = input(f"Carpeta destino (ej: ./glm_loreto_{year}{month:02d}{day:02d}): ").strip() or f"./glm_loreto_{year}{month:02d}{day:02d}"
    os.makedirs(dest_folder, exist_ok=True)

    # --- Búsqueda en los días UTC correspondientes ---
    all_day_files = []
    current_utc_day = utc_start
    while current_utc_day < utc_end:
        jday = current_utc_day.timetuple().tm_yday
        
        # Iterar sobre las horas del día UTC actual
        start_hour = current_utc_day.hour if current_utc_day.date() == utc_start.date() else 0
        end_hour = utc_end.hour if current_utc_day.date() == utc_end.date() else 24

        for hour in range(start_hour, end_hour):
            files_in_hour = list_available_nc(BUCKET, current_utc_day.year, jday, hour)
            if files_in_hour:
                for f in files_in_hour:
                    all_day_files.append((f, current_utc_day.year, jday, hour))
        
        current_utc_day += timedelta(days=1)
        # Asegurarnos de no pasarnos del día final
        current_utc_day = datetime(current_utc_day.year, current_utc_day.month, current_utc_day.day)

    if not all_day_files:
        print(f"No se encontraron archivos NetCDF para el día local {year}-{month}-{day}.")
        return

    print(f"\nSe encontraron un total de {len(all_day_files)} archivos para el día local especificado.")
    
    resp_download = input(f"¿Deseas descargar los {len(all_day_files)} archivos? (s/n): ").strip().lower()
    if resp_download != 's':
        print("Descarga cancelada.")
        return
        
    print("Descargando...")
    for f, f_year, f_jday, f_hour in all_day_files:
        download_file(BUCKET, f, dest_folder, f_year, f_jday, f_hour)
    print("Descarga finalizada.")

    # Opción para graficar
    resp_plot = input("¿Deseas mostrar un mapa de los flashes detectados? (s/n): ").strip().lower()
    if resp_plot == 's':
        plot_flashes(dest_folder)

if __name__ == "__main__":
    main() 