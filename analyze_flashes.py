import xarray as xr
import numpy as np
from pathlib import Path

# Base de datos de ciudades principales (misma que en download_glm_quicklook.py)
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
        
        city_name = input("Nombre de la ubicación (ej: Mi Ciudad): ").strip() or "Ubicación personalizada"
        
        return {
            "name": city_name,
            "lat": lat,
            "lon": lon,
            "timezone": -7  # Valor por defecto, no se usa en análisis
        }
    except ValueError:
        print("Error en las coordenadas, usando Loreto por defecto...")
        return CITIES_DB["loreto"]

def analyze_flashes(folder_path, location_info):
    """
    Analiza los archivos NetCDF GLM para extraer información de flashes
    y filtrar por proximidad a la ubicación especificada.
    """
    
    # Coordenadas del punto de referencia
    target_lat = location_info["lat"]
    target_lon = location_info["lon"]
    location_name = location_info["name"]
    
    # Rango de filtrado (±0.5° ≈ 50 km)
    lat_range = 0.5
    lon_range = 0.5
    
    print(f"Analizando archivos NetCDF en: {folder_path}")
    print(f"Punto de referencia: {location_name} ({target_lat}°N, {target_lon}°W)")
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
        
        # Filtrar flashes cercanos a la ubicación
        mask = (
            (lats >= target_lat - lat_range) & 
            (lats <= target_lat + lat_range) &
            (lons >= target_lon - lon_range) & 
            (lons <= target_lon + lon_range)
        )
        
        nearby_flashes = mask.sum()
        print(f"Flashes dentro de ±{lat_range}° de {location_name}: {nearby_flashes}")
        
        # Mostrar coordenadas de todos los flashes
        print(f"\nCoordenadas de todos los flashes detectados:")
        print("Latitud\t\tLongitud\t\tDistancia a {location_name} (km)")
        print("-" * 70)
        
        for i, (lat, lon) in enumerate(zip(lats, lons)):
            # Calcular distancia aproximada
            dlat = lat - target_lat
            dlon = lon - target_lon
            distance_km = np.sqrt((dlat * 111)**2 + (dlon * 111 * np.cos(np.radians(target_lat)))**2)
            
            # Marcar si está cerca
            marker = "★" if mask[i] else " "
            print(f"{lat:.6f}\t{lon:.6f}\t{distance_km:.1f} km {marker}")
        
        # Resumen de flashes cercanos
        if nearby_flashes > 0:
            print(f"\n=== RESUMEN DE FLASHES CERCANOS A {location_name.upper()} ===")
            nearby_lats = lats[mask]
            nearby_lons = lons[mask]
            
            for i, (lat, lon) in enumerate(zip(nearby_lats, nearby_lons)):
                dlat = lat - target_lat
                dlon = lon - target_lon
                distance_km = np.sqrt((dlat * 111)**2 + (dlon * 111 * np.cos(np.radians(target_lat)))**2)
                print(f"Flash {i+1}: {lat:.6f}°N, {lon:.6f}°W (a {distance_km:.1f} km de {location_name})")
        
        # Estadísticas adicionales
        if total_flashes > 0:
            print(f"\n=== ESTADÍSTICAS ===")
            print(f"Rango latitudinal: {lats.min():.6f}° a {lats.max():.6f}°")
            print(f"Rango longitudinal: {lons.min():.6f}° a {lons.max():.6f}°")
            print(f"Porcentaje cerca de {location_name}: {(nearby_flashes/total_flashes)*100:.1f}%")
        
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
                (lats >= target_lat - lat_range) & 
                (lats <= target_lat + lat_range) &
                (lons >= target_lon - lon_range) & 
                (lons <= target_lon + lon_range)
            )
            
            nearby_flashes = mask.sum()
            print(f"Flashes dentro de ±{lat_range}° de {location_name}: {nearby_flashes}")
            
            # Mostrar coordenadas
            print(f"\nCoordenadas de todos los flashes detectados:")
            for i, (lat, lon) in enumerate(zip(lats, lons)):
                dlat = lat - target_lat
                dlon = lon - target_lon
                distance_km = np.sqrt((dlat * 111)**2 + (dlon * 111 * np.cos(np.radians(target_lat)))**2)
                marker = "★" if mask[i] else " "
                print(f"{lat:.6f}\t{lon:.6f}\t{distance_km:.1f} km {marker}")

if __name__ == "__main__":
    print("Análisis de archivos NetCDF GLM para cualquier ubicación")
    
    # Obtener información de ubicación
    location_info = get_location_info()
    print(f"\nUbicación seleccionada: {location_info['name']}")
    print(f"Coordenadas: {location_info['lat']:.6f}, {location_info['lon']:.6f}")
    
    # Obtener ruta de la carpeta
    folder_path = input("\nIngresa la ruta de la carpeta con archivos .nc (ej: ./glm_nc): ").strip()
    if not folder_path:
        folder_path = "./glm_nc"
    
    analyze_flashes(folder_path, location_info) 