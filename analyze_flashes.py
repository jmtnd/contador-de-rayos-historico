import xarray as xr
import numpy as np
from pathlib import Path

def analyze_flashes(folder_path):
    """
    Analiza los archivos NetCDF GLM para extraer información de flashes
    y filtrar por proximidad a Loreto.
    """
    
    # Coordenadas de Loreto
    loreto_lat = 26.00586  # 26°00'21.1"N
    loreto_lon = -111.35247  # 111°21'08.9"W
    
    # Rango de filtrado (±0.5° ≈ 50 km)
    lat_range = 0.5
    lon_range = 0.5
    
    print(f"Analizando archivos NetCDF en: {folder_path}")
    print(f"Punto de referencia: Loreto ({loreto_lat}°N, {loreto_lon}°W)")
    print(f"Rango de filtrado: ±{lat_range}° (≈50 km)")
    print("-" * 60)
    
    # Buscar archivos .nc
    folder = Path(folder_path)
    files = sorted(folder.glob("*.nc"))
    
    if not files:
        print("No se encontraron archivos .nc en la carpeta especificada.")
        return
    
    print(f"Encontrados {len(files)} archivos NetCDF:")
    for f in files:
        print(f"  - {f.name}")
    
    # Leer y concatenar todos los archivos
    print("\nProcesando archivos...")
    try:
        # Usar combine='nested' y concat_dim para evitar problemas de concatenación
        ds = xr.open_mfdataset(files, combine='nested', concat_dim="number_of_flashes")
        
        # Extraer coordenadas
        lats = ds.flash_lat.values
        lons = ds.flash_lon.values
        
        total_flashes = len(lats)
        print(f"\nTotal de flashes detectados: {total_flashes}")
        
        # Filtrar flashes cercanos a Loreto
        mask = (
            (lats >= loreto_lat - lat_range) & 
            (lats <= loreto_lat + lat_range) &
            (lons >= loreto_lon - lon_range) & 
            (lons <= loreto_lon + lon_range)
        )
        
        nearby_flashes = mask.sum()
        print(f"Flashes dentro de ±{lat_range}° de Loreto: {nearby_flashes}")
        
        # Mostrar coordenadas de todos los flashes
        print(f"\nCoordenadas de todos los flashes detectados:")
        print("Latitud\t\tLongitud\t\tDistancia a Loreto (km)")
        print("-" * 70)
        
        for i, (lat, lon) in enumerate(zip(lats, lons)):
            # Calcular distancia aproximada
            dlat = lat - loreto_lat
            dlon = lon - loreto_lon
            distance_km = np.sqrt((dlat * 111)**2 + (dlon * 111 * np.cos(np.radians(loreto_lat)))**2)
            
            # Marcar si está cerca
            marker = "★" if mask[i] else " "
            print(f"{lat:.6f}\t{lon:.6f}\t{distance_km:.1f} km {marker}")
        
        # Resumen de flashes cercanos
        if nearby_flashes > 0:
            print(f"\n=== RESUMEN DE FLASHES CERCANOS A LORETO ===")
            nearby_lats = lats[mask]
            nearby_lons = lons[mask]
            
            for i, (lat, lon) in enumerate(zip(nearby_lats, nearby_lons)):
                dlat = lat - loreto_lat
                dlon = lon - loreto_lon
                distance_km = np.sqrt((dlat * 111)**2 + (dlon * 111 * np.cos(np.radians(loreto_lat)))**2)
                print(f"Flash {i+1}: {lat:.6f}°N, {lon:.6f}°W (a {distance_km:.1f} km de Loreto)")
        
        # Estadísticas adicionales
        if total_flashes > 0:
            print(f"\n=== ESTADÍSTICAS ===")
            print(f"Rango latitudinal: {lats.min():.6f}° a {lats.max():.6f}°")
            print(f"Rango longitudinal: {lons.min():.6f}° a {lons.max():.6f}°")
            print(f"Porcentaje cerca de Loreto: {(nearby_flashes/total_flashes)*100:.1f}%")
        
        ds.close()
        
    except Exception as e:
        print(f"Error al procesar los archivos: {e}")
        print("Intentando método alternativo...")
        
        # Método alternativo: procesar archivos uno por uno
        all_lats = []
        all_lons = []
        
        for f in files:
            try:
                ds = xr.open_dataset(f)
                if 'flash_lat' in ds and 'flash_lon' in ds:
                    all_lats.extend(ds.flash_lat.values.tolist())
                    all_lons.extend(ds.flash_lon.values.tolist())
                ds.close()
            except Exception as e:
                print(f"Error al leer {f.name}: {e}")
        
        if all_lats and all_lons:
            lats = np.array(all_lats)
            lons = np.array(all_lons)
            
            total_flashes = len(lats)
            print(f"\nTotal de flashes detectados: {total_flashes}")
            
            # Aplicar el mismo filtro
            mask = (
                (lats >= loreto_lat - lat_range) & 
                (lats <= loreto_lat + lat_range) &
                (lons >= loreto_lon - lon_range) & 
                (lons <= loreto_lon + lon_range)
            )
            
            nearby_flashes = mask.sum()
            print(f"Flashes dentro de ±{lat_range}° de Loreto: {nearby_flashes}")
            
            # Mostrar coordenadas
            print(f"\nCoordenadas de todos los flashes detectados:")
            for i, (lat, lon) in enumerate(zip(lats, lons)):
                dlat = lat - loreto_lat
                dlon = lon - loreto_lon
                distance_km = np.sqrt((dlat * 111)**2 + (dlon * 111 * np.cos(np.radians(loreto_lat)))**2)
                marker = "★" if mask[i] else " "
                print(f"{lat:.6f}\t{lon:.6f}\t{distance_km:.1f} km {marker}")

if __name__ == "__main__":
    # Puedes cambiar esta ruta por la carpeta donde están tus archivos .nc
    folder_path = input("Ingresa la ruta de la carpeta con archivos .nc (ej: ./glm_nc): ").strip()
    if not folder_path:
        folder_path = "./glm_nc"
    
    analyze_flashes(folder_path) 