"""
Código para ESP32-S3
Invernadero Inteligente - Lado del microcontrolador
MicroPython

Conexiones:
- DHT11/DHT22: GPIO 4
- Sensor humedad suelo (FC-28 / YL-69):
  - A0 (Salida analógica): GPIO 34 (ADC)
  - D0 (Salida digital): GPIO 35 (Entrada digital)
- Bomba de agua (Relé): GPIO 5
- LCD I2C: SDA=GPIO 21, SCL=GPIO 22
- Botones: GPIO 15, GPIO 16
"""

from machine import Pin, ADC, I2C, Timer
import dht
import time

# Configuración de pines
sensor_temp_hum = dht.DHT22(Pin(4))  # Instanciado para DHT22

# Sensor de humedad del suelo con 4 pines (VCC, GND, D0, A0)
# A0 se conecta al pin analógico GPIO 34 (ADC)
sensor_humedad_suelo_analog = ADC(Pin(34))
sensor_humedad_suelo_analog.atten(ADC.ATTN_11DB)  # Rango completo 0-3.3V

# D0 se conecta a un pin digital de entrada (ej: GPIO 35)
sensor_humedad_suelo_digital = Pin(35, Pin.IN)

rele_bomba = Pin(5, Pin.OUT)
rele_bomba.value(0)  # Bomba apagada inicialmente

boton1 = Pin(15, Pin.IN, Pin.PULL_UP)
boton2 = Pin(16, Pin.IN, Pin.PULL_UP)

# Configuración I2C para LCD (opcional)
try:
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    print("LCD I2C inicializado")
except:
    print("No se pudo inicializar LCD")

# Variables globales
umbral_humedad = 30  # Porcentaje mínimo de humedad
tiempo_riego = 3  # Segundos que dura el riego
bomba_activa = False

def leer_sensores():
    """
    Se leen los valores de temperatura, humedad ambiente y humedad del suelo (A0 analógico y D0 digital).
    Retorna: (temperatura, humedad_ambiente, humedad_suelo_analog, humedad_suelo_digital)
    """
    try:
        # Se lee el sensor DHT
        sensor_temp_hum.measure()
        temperatura = sensor_temp_hum.temperature()
        humedad_ambiente = sensor_temp_hum.humidity()
        
        # Se lee el sensor de humedad del suelo en su salida analógica (A0)
        # El sensor FC-28 da valores entre 0 (seco) y 4095 (húmedo)
        # Se convierte a porcentaje
        valor_adc = sensor_humedad_suelo_analog.read()
        humedad_suelo_analog = 100 - ((valor_adc / 4095) * 100)  # Invertir para que 100% sea húmedo
        
        # Se lee el sensor de humedad del suelo en su salida digital (D0)
        # El pin D0 se pone en LOW (0) cuando detecta suficiente humedad y HIGH (1) cuando está seco
        humedad_suelo_digital = sensor_humedad_suelo_digital.value()
        
        return temperatura, humedad_ambiente, humedad_suelo_analog, humedad_suelo_digital
    
    except Exception as e:
        print(f"Error al leer sensores: {e}")
        return None, None, None, None

def activar_riego(duracion=3):
    """
    Se activa la bomba de riego durante un tiempo determinado.
    
    Args:
        duracion (int): Segundos que debe estar activa la bomba
    """
    global bomba_activa
    print("Activando riego...")
    rele_bomba.value(1)
    bomba_activa = True
    time.sleep(duracion)
    rele_bomba.value(0)
    bomba_activa = False
    print("Riego completado")

def enviar_datos_serial(temperatura, humedad_suelo_analog, humedad_suelo_digital):
    """
    Se envían los datos por serial en formato: TEMP:25.5,HUM:45.2,HUM_DIG:0
    
    Args:
        temperatura (float): Temperatura en °C
        humedad_suelo_analog (float): Humedad del suelo en % (analógica)
        humedad_suelo_digital (int): Estado digital del sensor (D0)
    """
    print(f"TEMP:{temperatura:.1f},HUM:{humedad_suelo_analog:.1f},HUM_DIG:{humedad_suelo_digital}")

def procesar_comando(comando):
    """
    Se procesan los comandos recibidos desde la interfaz Python.
    
    Args:
        comando (str): Comando recibido
    """
    global umbral_humedad
    
    comando = comando.strip()
    
    if comando == "RIEGO_ON":
        activar_riego(tiempo_riego)
    
    elif comando == "RIEGO_MANUAL":
        activar_riego(5)  # Riego manual por 5 segundos
    
    elif comando.startswith("SET_UMBRAL:"):
        try:
            nuevo_umbral = int(comando.split(':')[1])
            umbral_humedad = nuevo_umbral
            print(f"Umbral actualizado a {umbral_humedad}%")
        except:
            print("Error al actualizar umbral")

def verificar_riego_automatico(humedad_suelo):
    """
    Se verifica si se debe activar el riego automático según el umbral.
    
    Args:
        humedad_suelo (float): Humedad actual del suelo
    """
    global bomba_activa
    
    if humedad_suelo < umbral_humedad and not bomba_activa:
        print("Humedad baja detectada. Activando riego automático...")
        activar_riego(tiempo_riego)

def loop_principal():
    """
    Bucle principal del programa.
    """
    print("Iniciando sistema de invernadero inteligente...")
    
    while True:
        # Se leen los sensores
        temperatura, humedad_ambiente, humedad_suelo_analog, humedad_suelo_digital = leer_sensores()
        
        if temperatura is not None:
            # Se envían los datos por serial (incluyendo la lectura analógica A0 y la digital D0)
            enviar_datos_serial(temperatura, humedad_suelo_analog, humedad_suelo_digital)
            
            # Se verifica si se debe activar el riego automático usando la lectura analógica
            verificar_riego_automatico(humedad_suelo_analog)
        
        # Se verifica si hay comandos entrantes por serial
        # Nota: En MicroPython, sys.stdin.read() puede bloquear
        # Implementar lectura no bloqueante según sea necesario
        
        # Se verifica el estado de los botones
        if boton1.value() == 0:  # Botón presionado (pull-up)
            print("Botón 1 presionado: Riego manual")
            activar_riego(5)
            time.sleep(0.3)  # Debounce
        
        if boton2.value() == 0:
            print("Botón 2 presionado")
            # Implementar funcionalidad adicional
            time.sleep(0.3)
        
        time.sleep(1)  # Esperar 1 segundo antes de la siguiente lectura

# Iniciar el programa
try:
    loop_principal()
except KeyboardInterrupt:
    print("\nPrograma detenido")
    rele_bomba.value(0)  # Asegurar que la bomba esté apagada
