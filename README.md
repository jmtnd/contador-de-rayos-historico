# Contador de Rayos Histórico

Este proyecto permite descargar y analizar datos históricos de rayos (lightning) utilizando datos del satélite GOES (Geostationary Operational Environmental Satellite) a través del sistema GLM (Geostationary Lightning Mapper).

## Características

- **Descarga automática**: Descarga archivos NetCDF de rayos desde el bucket S3 de NOAA
- **Análisis geográfico**: Filtra rayos por ubicación específica (ej: Loreto, BCS)
- **Visualización**: Genera mapas detallados de la actividad de rayos
- **Múltiples satélites**: Soporte para GOES-16, GOES-17, GOES-18 y GOES-19
- **Conversión de zona horaria**: Maneja automáticamente la conversión de hora local a UTC

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
1. Selección del satélite GOES
2. Especificación de la fecha local
3. Configuración de la carpeta de destino
4. Descarga automática de archivos NetCDF
5. Opción para generar mapas de visualización

### Análisis de datos

Para analizar los archivos descargados:

```bash
python analyze_flashes.py
```

## Estructura del Proyecto

```
contador-de-rayos-historico/
├── download_glm_quicklook.py  # Script principal de descarga
├── analyze_flashes.py         # Script de análisis de datos
├── requirements.txt           # Dependencias de Python
├── README.md                 # Este archivo
└── glm_loreto_YYYYMMDD/      # Carpeta con archivos descargados
```

## Dependencias

- `xarray`: Para manejo de datos NetCDF
- `matplotlib`: Para visualización
- `cartopy`: Para mapas geográficos
- `numpy`: Para cálculos numéricos

## Fuente de Datos

Los datos provienen del [NOAA GOES Data Archive](https://www.ncei.noaa.gov/products/goes-r-terrestrial-weather-keys-products) y se acceden a través del bucket S3 público de NOAA.

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras. 