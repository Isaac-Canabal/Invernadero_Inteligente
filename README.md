# Invernadero Inteligente de Escritorio

Sistema de monitoreo y control automatizado para plantas usando ESP32-S3 y Python.

## Estructura del Proyecto

```
invernadero_inteligente/
├── main.py                    # Aplicación principal Python
├── ui_invernadero.py          # Interfaz generada por Qt Designer
├── invernadero_interfaz.ui    # Archivo de diseño Qt
├── esp32_invernadero.py       # Código MicroPython para ESP32
└── README.md                  # Este archivo
```

## Requisitos

### Hardware
- ESP32-S3 DevKit
- Sensor DHT11 o DHT22 (temperatura y humedad ambiente)
- Sensor FC-28 o YL-69 (humedad del suelo)
- Bomba de agua sumergible 3-5V
- Relé de 1 canal
- LCD 16x2 con módulo I2C (opcional)
- 2 pulsadores
- Cables y protoboard

### Software - PC
- Python 3.8 o superior
- PySide6
- pyserial


## Instalación

### 1. Instalar dependencias Python

```bash
pip install PySide6 pyserial
```

O puedes ejecutar pip install -r requirements.txt para instalar las dependencias.

### 2. Cargar código en el ESP32

1. Instalar Thonny IDE o esptool
2. Flashear MicroPython en el ESP32-S3
3. Cargar el archivo `esp32_invernadero.py` al ESP32
4. Configurar para que se ejecute al inicio

### 3. Ejecutar la aplicación

```bash
python main.py
o 
py main.py
```

## Uso

### Conexión
1. Conectar el ESP32 al puerto USB
2. Seleccionar el puerto serial en la interfaz
3. Hacer clic en "Conectar ESP32"

### Funciones disponibles

**Monitoreo en Tiempo Real**
- Visualización de temperatura actual
- Visualización de humedad del suelo
- Actualización automática cada segundo

**Control Manual**
- Activar riego manual con el botón correspondiente
- Configurar umbral de humedad (0-100%)
- Aplicar nueva configuración al ESP32

**Historial**
- Visualizar últimas 100 lecturas
- Exportar historial completo a CSV
- Limpiar base de datos

## Protocolo de Comunicación Serial

### Formato de datos ESP32 → PC
```
TEMP:25.5,HUM:45.2,HUM_DIG:0
```
*(Donde `HUM` es el porcentaje de humedad analógico y `HUM_DIG` es el estado digital del sensor: 0 para húmedo y 1 para seco).*

### Comandos PC → ESP32
```
RIEGO_ON          # Activar riego por defecto (3s)
RIEGO_MANUAL      # Activar riego manual (5s)
SET_UMBRAL:30     # Configurar umbral de humedad al 30%
```

## Conexiones ESP32

```
DHT11/22          → GPIO 4
Humedad suelo A0  → GPIO 34 (ADC)
Humedad suelo D0  → GPIO 35 (Entrada Digital)
Relé bomba        → GPIO 5
LCD SDA           → GPIO 21
LCD SCL           → GPIO 22
Botón 1           → GPIO 15 (pull-up interno)
Botón 2           → GPIO 16 (pull-up interno)
```

## Base de Datos

El sistema crea automáticamente una base de datos SQLite (`invernadero.db`) con la siguiente estructura:

```sql
CREATE TABLE historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora TEXT NOT NULL,
    temperatura REAL,
    humedad REAL,
    riego_activado INTEGER DEFAULT 0
);
```

## Solución de Problemas

### No detecta el puerto serial
- Instalar drivers CH340 o CP2102 según el chip USB del ESP32
- En Linux: agregar usuario al grupo `dialout`
  ```bash
  sudo usermod -a -G dialout $USER
  ```

### La bomba no se activa
- Verificar conexión del relé
- Verificar voltaje de alimentación de la bomba
- Revisar polaridad del relé

### Lecturas erráticas
- Calibrar sensor de humedad del suelo
- Verificar conexiones de sensores
- Agregar resistencias pull-up si es necesario

## Autores

- Isaac David Canabal Martínez
- Diego José Barón
- Santiago Andrés Carballo Manchego
- Emmanuel David Angulo González

## Curso

Computación e Interfaces - NRC: 1475 - 1476  
Ingeniería de Sistemas y Computación
