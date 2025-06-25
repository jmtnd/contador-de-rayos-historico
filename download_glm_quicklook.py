import os
import subprocess
from datetime import datetime, timedelta

# --- Configuración ---
BASE_S3_PATH = "GLM-L2-LCFA"

# Base de datos de ciudades principales
CITIES_DB = {
    "loreto": {"name": "Loreto, BCS", "lat": 26.00586, "lon": -111.35247, "timezone": -7},
    "la_paz": {"name": "La Paz, BCS", "lat": 24.1426, "lon": -110.3129, "timezone": -7},
    "cabos": {"name": "Los Cabos, BCS", "lat": 23.0597, "lon": -109.6977, "timezone": -7},
    "mexicali": {"name": "Mexicali, BC", "lat": 32.6648, "lon": -115.4679, "timezone": -8},
    "tijuana": {"name": "Tijuana, BC", "lat": 32.5149, "lon": -117.0382, "timezone": -8},
    "ensenada": {"name": "Ensenada, BC", "lat": 31.8667, "lon": -116.6167, "timezone": -8},
    "hermosillo": {"name": "Hermosillo, Son", "lat": 29.0729, "lon": -110.9559, "timezone": -7},
    "guaymas": {"name": "Guaymas, Son", "lat": 27.9194, "lon": -110.8978, "timezone": -7},
    "ciudad_obregon": {"name": "Ciudad Obregón, Son", "lat": 27.4864, "lon": -109.9408, "timezone": -7},
    "navojoa": {"name": "Navojoa, Son", "lat": 27.0814, "lon": -109.4461, "timezone": -7},
    "culiacan": {"name": "Culiacán, Sin", "lat": 24.7994, "lon": -107.3897, "timezone": -7},
    "mazatlan": {"name": "Mazatlán, Sin", "lat": 23.2494, "lon": -106.4111, "timezone": -7},
    "guadalajara": {"name": "Guadalajara, Jal", "lat": 20.6597, "lon": -103.3496, "timezone": -6},
    "monterrey": {"name": "Monterrey, NL", "lat": 25.6866, "lon": -100.3161, "timezone": -6},
    "ciudad_juarez": {"name": "Ciudad Juárez, Chih", "lat": 31.6904, "lon": -106.4244, "timezone": -7},
    "chihuahua": {"name": "Chihuahua, Chih", "lat": 28.6353, "lon": -106.0889, "timezone": -7},
    "durango": {"name": "Durango, Dgo", "lat": 24.0225, "lon": -104.6578, "timezone": -6},
    "zacatecas": {"name": "Zacatecas, Zac", "lat": 22.7709, "lon": -102.5832, "timezone": -6},
    "aguascalientes": {"name": "Aguascalientes, Ags", "lat": 21.8853, "lon": -102.2916, "timezone": -6},
    "san_luis_potosi": {"name": "San Luis Potosí, SLP", "lat": 22.1565, "lon": -100.9855, "timezone": -6},
    "leon": {"name": "León, Gto", "lat": 21.1250, "lon": -101.6860, "timezone": -6},
    "queretaro": {"name": "Querétaro, Qro", "lat": 20.5888, "lon": -100.3899, "timezone": -6},
    "toluca": {"name": "Toluca, Mex", "lat": 19.2833, "lon": -99.6533, "timezone": -6},
    "puebla": {"name": "Puebla, Pue", "lat": 19.0413, "lon": -98.2062, "timezone": -6},
    "veracruz": {"name": "Veracruz, Ver", "lat": 19.1738, "lon": -96.1342, "timezone": -6},
    "oaxaca": {"name": "Oaxaca, Oax", "lat": 17.0732, "lon": -96.7266, "timezone": -6},
    "tuxtla": {"name": "Tuxtla Gutiérrez, Chis", "lat": 16.7519, "lon": -93.1167, "timezone": -6},
    "villahermosa": {"name": "Villahermosa, Tab", "lat": 17.9892, "lon": -92.9281, "timezone": -6},
    "merida": {"name": "Mérida, Yuc", "lat": 20.9674, "lon": -89.5926, "timezone": -6},
    "cancun": {"name": "Cancún, QR", "lat": 21.1743, "lon": -86.8466, "timezone": -5},
    "chetu": {"name": "Chetumal, QR", "lat": 18.5141, "lon": -88.3038, "timezone": -5},
    "campeche": {"name": "Campeche, Camp", "lat": 19.8301, "lon": -90.5349, "timezone": -6},
    "ciudad_victoria": {"name": "Ciudad Victoria, Tamps", "lat": 23.7417, "lon": -99.1456, "timezone": -6},
    "tampico": {"name": "Tampico, Tamps", "lat": 22.2553, "lon": -97.8686, "timezone": -6},
    "reynosa": {"name": "Reynosa, Tamps", "lat": 26.0421, "lon": -98.2737, "timezone": -6},
    "matamoros": {"name": "Matamoros, Tamps", "lat": 25.8690, "lon": -97.5027, "timezone": -6},
    "nuevo_laredo": {"name": "Nuevo Laredo, Tamps", "lat": 27.4763, "lon": -99.5163, "timezone": -6},
    "saltillo": {"name": "Saltillo, Coah", "lat": 25.4383, "lon": -100.9737, "timezone": -6},
    "torreon": {"name": "Torreón, Coah", "lat": 25.5428, "lon": -103.4067, "timezone": -6},
    "monclova": {"name": "Monclova, Coah", "lat": 26.9103, "lon": -101.4222, "timezone": -6},
    "piedras_negras": {"name": "Piedras Negras, Coah", "lat": 28.7000, "lon": -100.5231, "timezone": -6},
    "acapulco": {"name": "Acapulco, Gro", "lat": 16.8531, "lon": -99.8237, "timezone": -6},
    "chilpancingo": {"name": "Chilpancingo, Gro", "lat": 17.5506, "lon": -99.5058, "timezone": -6},
    "morelia": {"name": "Morelia, Mich", "lat": 19.7008, "lon": -101.1844, "timezone": -6},
    "zamora": {"name": "Zamora, Mich", "lat": 19.9833, "lon": -102.2833, "timezone": -6},
    "colima": {"name": "Colima, Col", "lat": 19.2433, "lon": -103.7247, "timezone": -6},
    "manzanillo": {"name": "Manzanillo, Col", "lat": 19.0500, "lon": -104.3167, "timezone": -6}
}

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

def get_location_info():
    """Obtiene información de ubicación del usuario"""
    print("\n=== SELECCIÓN DE UBICACIÓN ===")
    print("1. Buscar por ciudad predefinida")
    print("2. Ingresar coordenadas personalizadas")
    
    choice = input("Opción (1-2): ").strip()
    
    if choice == "1":
        return select_city()
    elif choice == "2":
        return input_coordinates()
    else:
        print("Opción inválida, usando coordenadas personalizadas...")
        return input_coordinates()

def select_city():
    """Permite seleccionar una ciudad de la base de datos"""
    print("\n--- Ciudades disponibles ---")
    
    # Agrupar ciudades por región
    regions = {
        "Baja California": ["tijuana", "mexicali", "ensenada"],
        "Baja California Sur": ["loreto", "la_paz", "cabos"],
        "Sonora": ["hermosillo", "guaymas", "ciudad_obregon", "navojoa"],
        "Sinaloa": ["culiacan", "mazatlan"],
        "Chihuahua": ["ciudad_juarez", "chihuahua"],
        "Coahuila": ["saltillo", "torreon", "monclova", "piedras_negras"],
        "Nuevo León": ["monterrey"],
        "Tamaulipas": ["ciudad_victoria", "tampico", "reynosa", "matamoros", "nuevo_laredo"],
        "Durango": ["durango"],
        "Zacatecas": ["zacatecas"],
        "Aguascalientes": ["aguascalientes"],
        "San Luis Potosí": ["san_luis_potosi"],
        "Guanajuato": ["leon"],
        "Querétaro": ["queretaro"],
        "México": ["toluca"],
        "Jalisco": ["guadalajara"],
        "Colima": ["colima", "manzanillo"],
        "Michoacán": ["morelia", "zamora"],
        "Guerrero": ["acapulco", "chilpancingo"],
        "Puebla": ["puebla"],
        "Veracruz": ["veracruz"],
        "Oaxaca": ["oaxaca"],
        "Chiapas": ["tuxtla"],
        "Tabasco": ["villahermosa"],
        "Yucatán": ["merida"],
        "Quintana Roo": ["cancun", "chetu"],
        "Campeche": ["campeche"]
    }
    
    # Mostrar regiones
    for i, (region, cities) in enumerate(regions.items(), 1):
        print(f"{i:2d}. {region}")
    
    region_choice = input("\nSelecciona la región (número): ").strip()
    
    try:
        region_idx = int(region_choice) - 1
        region_names = list(regions.keys())
        if 0 <= region_idx < len(region_names):
            selected_region = region_names[region_idx]
            region_cities = regions[selected_region]
            
            print(f"\n--- Ciudades en {selected_region} ---")
            for i, city_key in enumerate(region_cities, 1):
                city_info = CITIES_DB[city_key]
                print(f"{i:2d}. {city_info['name']}")
            
            city_choice = input("\nSelecciona la ciudad (número): ").strip()
            try:
                city_idx = int(city_choice) - 1
                if 0 <= city_idx < len(region_cities):
                    selected_city_key = region_cities[city_idx]
                    return CITIES_DB[selected_city_key]
                else:
                    print("Opción inválida, usando Loreto por defecto...")
                    return CITIES_DB["loreto"]
            except ValueError:
                print("Opción inválida, usando Loreto por defecto...")
                return CITIES_DB["loreto"]
        else:
            print("Opción inválida, usando Loreto por defecto...")
            return CITIES_DB["loreto"]
    except ValueError:
        print("Opción inválida, usando Loreto por defecto...")
        return CITIES_DB["loreto"]

def input_coordinates():
    """Permite al usuario ingresar coordenadas personalizadas"""
    print("\n--- Coordenadas personalizadas ---")
    print("Ingresa las coordenadas de la ubicación de interés:")
    
    try:
        lat = float(input("Latitud (ej: 26.00586): "))
        lon = float(input("Longitud (ej: -111.35247): "))
        
        # Determinar zona horaria aproximada basada en la longitud
        if lon < -102:  # Zona horaria del Pacífico
            timezone = -8
        elif lon < -90:  # Zona horaria de la Montaña
            timezone = -7
        else:  # Zona horaria del Este
            timezone = -6
        
        # Permitir al usuario ajustar la zona horaria
        print(f"Zona horaria detectada: UTC{timezone:+d}")
        custom_timezone = input("¿Deseas cambiar la zona horaria? (s/n): ").strip().lower()
        
        if custom_timezone == 's':
            timezone = int(input("Nueva zona horaria (ej: -7): "))
        
        city_name = input("Nombre de la ubicación (ej: Mi Ciudad): ").strip() or "Ubicación personalizada"
        
        return {
            "name": city_name,
            "lat": lat,
            "lon": lon,
            "timezone": timezone
        }
    except ValueError:
        print("Error en las coordenadas, usando Loreto por defecto...")
        return CITIES_DB["loreto"]

def plot_flashes(dest_folder, location_info):
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

    # Coordenadas del punto de interés
    target_lat = location_info["lat"]
    target_lon = location_info["lon"]
    location_name = location_info["name"]
    
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
    print(f"Flashes dentro de ~100 km de {location_name}: {nearby_flash_count}")
    print("--------------------------")

    # --- Mapa 1: Detallado en la ubicación ---
    fig1, ax1 = plt.subplots(figsize=(12, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax1.set_title(f'Análisis Detallado en {location_name}\n{nearby_flash_count} flashes en un radio de ~100 km', fontsize=14, fontweight='bold')
    ax1.coastlines(resolution='10m', color='black')
    
    # Graficar solo flashes cercanos
    if nearby_flash_count > 0:
        ax1.scatter(lons[nearby_mask], lats[nearby_mask], s=30, c='red', alpha=0.7, transform=ccrs.PlateCarree())

    # Marcar punto de interés y radio
    ax1.scatter(target_lon, target_lat, s=200, c='blue', marker='*', zorder=10, label=location_name)
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
        ax2.plot(rect_lons, rect_lats, 'b-', linewidth=2, transform=ccrs.PlateCarree(), label=f'Zona de {location_name}')
        
        # Ajustar extensión basada en la ubicación
        if target_lon < -100:  # Oeste de México
            ax2.set_extent([-118, -95, 15, 35])
        elif target_lon < -90:  # Centro de México
            ax2.set_extent([-105, -85, 15, 35])
        else:  # Este de México
            ax2.set_extent([-95, -75, 15, 35])
        
        ax2.gridlines(draw_labels=True)
        ax2.legend()
        plt.show()
    else:
        print("No se generó mapa de contexto porque no se detectaron flashes.")

# --- Interfaz de usuario ---
def main():
    print("Descarga de archivos NetCDF GLM para un DÍA LOCAL COMPLETO")
    
    # --- Selección de ubicación ---
    location_info = get_location_info()
    print(f"\nUbicación seleccionada: {location_info['name']}")
    print(f"Coordenadas: {location_info['lat']:.6f}, {location_info['lon']:.6f}")
    print(f"Zona horaria: UTC{location_info['timezone']:+d}")
    
    # --- Selección de Satélite ---
    print("\nSelecciona el satélite a consultar:")
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
    print(f"\nIntroduce la fecha local de {location_info['name']}:")
    year = int(input("Año (YYYY): "))
    month = int(input("Mes (1-12): "))
    day = int(input("Día (1-31): "))
    
    # --- Conversión de hora local a rangos UTC ---
    local_start = datetime(year, month, day, 0, 0)
    utc_start = local_start + timedelta(hours=abs(location_info['timezone']))
    utc_end = utc_start + timedelta(days=1)
    
    print(f"\nBuscando datos para el día {year}-{month}-{day} en {location_info['name']}...")
    print(f"Esto corresponde al intervalo UTC: {utc_start.strftime('%Y-%m-%d %H:%M')} a {utc_end.strftime('%Y-%m-%d %H:%M')}")
    
    # Crear nombre de carpeta basado en la ubicación
    safe_name = location_info['name'].replace(' ', '_').replace(',', '').replace('.', '')
    default_folder = f"./glm_{safe_name.lower()}_{year}{month:02d}{day:02d}"
    dest_folder = input(f"Carpeta destino (ej: {default_folder}): ").strip() or default_folder
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
        plot_flashes(dest_folder, location_info)

if __name__ == "__main__":
    main() 