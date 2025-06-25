# Contador de Rayos Histórico

Este proyecto permite descargar y analizar datos históricos de rayos (lightning) utilizando datos del satélite GOES (Geostationary Operational Environmental Satellite) a través del sistema GLM (Geostationary Lightning Mapper).

## Características

- **Descarga automática**: Descarga archivos NetCDF de rayos desde el bucket S3 de NOAA
- **Análisis geográfico**: Filtra rayos por ubicación específica (cualquier ciudad de México o coordenadas personalizadas)
- **Visualización**: Genera mapas detallados de la actividad de rayos
- **Múltiples satélites**: Soporte para GOES-16, GOES-17, GOES-18 y GOES-19
- **Conversión de zona horaria**: Maneja automáticamente la conversión de hora local a UTC
- **Base de datos de ciudades**: Incluye más de 50 ciudades principales de México con coordenadas precisas
- **Coordenadas personalizadas**: Permite ingresar cualquier ubicación específica

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/jmtnd/contador-de-rayos-historico.git
cd contador-de-rayos-historico
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Asegúrate de tener AWS CLI instalado para acceder a los datos S3:
```bash
# En macOS con Homebrew
brew install awscli
```

## Uso

### Descarga de datos

Ejecuta el script principal para descargar datos de rayos:

```bash
python download_glm_quicklook.py
```

El script te guiará a través de:
1. **Selección de ubicación**:
   - Opción 1: Buscar por ciudad predefinida (más de 50 ciudades de México)
   - Opción 2: Ingresar coordenadas personalizadas
2. Selección del satélite GOES
3. Especificación de la fecha local
4. Configuración de la carpeta de destino
5. Descarga automática de archivos NetCDF
6. Opción para generar mapas de visualización

### Análisis de datos

Para analizar los archivos descargados:

```bash
python analyze_flashes.py
```

Este script también permite seleccionar cualquier ubicación y analiza los flashes detectados en un radio de ~50 km.

## Ciudades Disponibles

El proyecto incluye una base de datos con más de 50 ciudades principales de México, organizadas por región:

### Baja California
- Tijuana, Mexicali, Ensenada

### Baja California Sur
- Loreto, La Paz, Los Cabos

### Sonora
- Hermosillo, Guaymas, Ciudad Obregón, Navojoa

### Sinaloa
- Culiacán, Mazatlán

### Chihuahua
- Ciudad Juárez, Chihuahua

### Coahuila
- Saltillo, Torreón, Monclova, Piedras Negras

### Nuevo León
- Monterrey

### Tamaulipas
- Ciudad Victoria, Tampico, Reynosa, Matamoros, Nuevo Laredo

### Y muchas más...
- Durango, Zacatecas, Aguascalientes, San Luis Potosí, Guanajuato, Querétaro, México, Jalisco, Colima, Michoacán, Guerrero, Puebla, Veracruz, Oaxaca, Chiapas, Tabasco, Yucatán, Quintana Roo, Campeche

## Estructura del Proyecto

```
contador-de-rayos-historico/
├── download_glm_quicklook.py  # Script principal de descarga
├── analyze_flashes.py         # Script de análisis de datos
├── requirements.txt           # Dependencias de Python
├── README.md                 # Este archivo
└── glm_[ciudad]_YYYYMMDD/    # Carpetas con archivos descargados
```

## Dependencias

- `xarray`: Para manejo de datos NetCDF
- `matplotlib`: Para visualización
- `cartopy`: Para mapas geográficos
- `numpy`: Para cálculos numéricos

## Fuente de Datos

Los datos provienen del [NOAA GOES Data Archive](https://www.ncei.noaa.gov/products/goes-r-terrestrial-weather-keys-products) y se acceden a través del bucket S3 público de NOAA.

## Características Técnicas

- **Zonas horarias**: Manejo automático de zonas horarias de México (UTC-5 a UTC-8)
- **Detección automática**: El sistema detecta automáticamente la zona horaria basada en la longitud
- **Nombres de carpetas**: Se generan automáticamente basados en la ciudad seleccionada
- **Mapas adaptativos**: Los mapas de contexto se ajustan automáticamente según la ubicación

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras. 