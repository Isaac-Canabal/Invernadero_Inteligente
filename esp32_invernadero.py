from machine import Pin, ADC, I2C
import dht
import time
import sys
import uselect

DHT_PIN = 4
SUELO_ADC_PIN = 10
RELE_PIN = 18
BTN1_PIN = 15
BTN2_PIN = 16
LCD_SDA = 14
LCD_SCL = 13
LCD_ADDR = 0x27
LCD_COLS = 16
LCD_ROWS = 2

DEBOUNCE_MS = 60
SENSOR_INTERVAL_MS = 2000
LOOP_DELAY_MS = 20
AUTO_RIEGO_S = 1.5
MANUAL_RIEGO_S = 2.0

umbral_humedad = 30
bomba_activa = False
ultimo_sensor_ms = 0
ultimo_riego_ms = 0
bloqueo_riego_ms = 15000

sensor_temp_hum = dht.DHT22(Pin(DHT_PIN))
sensor_humedad_suelo = ADC(Pin(SUELO_ADC_PIN))
sensor_humedad_suelo.atten(ADC.ATTN_11DB)
rele_bomba = Pin(RELE_PIN, Pin.OUT)
rele_bomba.value(0)

class DebouncedButton:
    def __init__(self, pin_number, debounce_ms=50, pull_up=True):
        mode = Pin.PULL_UP if pull_up else Pin.PULL_DOWN
        self.pin = Pin(pin_number, Pin.IN, mode)
        self.debounce_ms = debounce_ms
        self.pull_up = pull_up
        self.last_raw = self.pin.value()
        self.stable_state = self.last_raw
        self.last_change_ms = time.ticks_ms()

    def update(self):
        now = time.ticks_ms()
        raw = self.pin.value()
        pressed_event = False
        released_event = False

        if raw != self.last_raw:
            self.last_raw = raw
            self.last_change_ms = now

        if time.ticks_diff(now, self.last_change_ms) >= self.debounce_ms:
            if raw != self.stable_state:
                previous = self.stable_state
                self.stable_state = raw
                if self.pull_up:
                    if previous == 1 and self.stable_state == 0:
                        pressed_event = True
                    elif previous == 0 and self.stable_state == 1:
                        released_event = True
                else:
                    if previous == 0 and self.stable_state == 1:
                        pressed_event = True
                    elif previous == 1 and self.stable_state == 0:
                        released_event = True
        return pressed_event, released_event

btn1 = DebouncedButton(BTN1_PIN, debounce_ms=DEBOUNCE_MS, pull_up=True)
btn2 = DebouncedButton(BTN2_PIN, debounce_ms=DEBOUNCE_MS, pull_up=True)

lcd = None
poll = uselect.poll()
poll.register(sys.stdin, uselect.POLLIN)

def init_lcd():
    global lcd
    try:
        i2c = I2C(0, scl=Pin(LCD_SCL), sda=Pin(LCD_SDA), freq=400000)
        dispositivos = i2c.scan()
        print("I2C scan:", [hex(x) for x in dispositivos])
        from i2c_lcd import I2cLcd
        lcd = I2cLcd(i2c, LCD_ADDR, LCD_ROWS, LCD_COLS)
        lcd.clear()
        lcd.putstr("Invernadero OK\nIniciando...")
        print("LCD inicializado correctamente")
    except Exception as e:
        lcd = None
        print("No se pudo inicializar LCD:", e)

def lcd_write(line1="", line2=""):
    if lcd is None:
        return
    try:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(str(line1)[:LCD_COLS])
        lcd.move_to(0, 1)
        lcd.putstr(str(line2)[:LCD_COLS])
    except Exception as e:
        print("Error escribiendo LCD:", e)

def leer_sensores():
    try:
        sensor_temp_hum.measure()
        temperatura = sensor_temp_hum.temperature()
        humedad_ambiente = sensor_temp_hum.humidity()
        valor_adc = sensor_humedad_suelo.read()
        humedad_suelo = 100 - ((valor_adc / 4095) * 100)
        humedad_suelo = max(0, min(100, humedad_suelo))
        return temperatura, humedad_ambiente, humedad_suelo, valor_adc
    except Exception as e:
        print("Error al leer sensores:", e)
        return None, None, None, None

def enviar_datos_serial(temperatura, humedad_suelo):
    print("TEMP:{:.1f},HUM:{:.1f}".format(temperatura, humedad_suelo))

def activar_riego(duracion_s, motivo):
    global bomba_activa, ultimo_riego_ms
    if bomba_activa:
        return
    print("Activando riego ({}): {} s".format(motivo, duracion_s))
    lcd_write("Riego {}".format(motivo[:9]), "Bomba encendida")
    bomba_activa = True
    rele_bomba.value(1)
    time.sleep(duracion_s)
    rele_bomba.value(0)
    bomba_activa = False
    ultimo_riego_ms = time.ticks_ms()
    print("Riego completado")
    lcd_write("Riego completo", "Bomba apagada")

def procesar_comando_serial():
    global umbral_humedad
    if not poll.poll(0):
        return
    try:
        comando = sys.stdin.readline().strip()
        if not comando:
            return
        print("CMD:", comando)
        if comando == "RIEGO_ON":
            activar_riego(AUTO_RIEGO_S, "auto")
        elif comando == "RIEGO_MANUAL":
            activar_riego(MANUAL_RIEGO_S, "manual")
        elif comando.startswith("SET_UMBRAL:"):
            try:
                umbral_humedad = int(comando.split(":", 1)[1])
                print("Umbral actualizado a {}%".format(umbral_humedad))
                lcd_write("Umbral nuevo", "{}%".format(umbral_humedad))
            except Exception:
                print("Error al actualizar umbral")
    except Exception as e:
        print("Error leyendo comando:", e)

def verificar_riego_automatico(humedad_suelo):
    if humedad_suelo is None or bomba_activa:
        return
    ahora = time.ticks_ms()
    if time.ticks_diff(ahora, ultimo_riego_ms) < bloqueo_riego_ms:
        return
    if humedad_suelo < umbral_humedad:
        print("Humedad baja detectada. Activando riego automatico...")
        activar_riego(AUTO_RIEGO_S, "auto")

def manejar_botones():
    presionado1, _ = btn1.update()
    presionado2, _ = btn2.update()
    if presionado1:
        print("Boton 1: riego manual")
        activar_riego(MANUAL_RIEGO_S, "manual")
    if presionado2:
        print("Boton 2: cambio de pantalla")
        lcd_write("Sistema activo", "Boton 2 OK")

def actualizar_pantalla_sensores(temp, hum_amb, hum_suelo):
    if temp is None:
        lcd_write("Error sensores", "Revisar DHT/ADC")
        return
    linea1 = "T:{:.1f}C H:{:.0f}%".format(temp, hum_amb)
    linea2 = "Suelo:{:.0f}%".format(hum_suelo)
    lcd_write(linea1, linea2)

def loop_principal():
    global ultimo_sensor_ms
    print("Iniciando sistema de invernadero inteligente...")
    lcd_write("Invernadero", "Sistema listo")
    while True:
        procesar_comando_serial()
        manejar_botones()
        ahora = time.ticks_ms()
        if time.ticks_diff(ahora, ultimo_sensor_ms) >= SENSOR_INTERVAL_MS:
            ultimo_sensor_ms = ahora
            temperatura, humedad_ambiente, humedad_suelo, valor_adc = leer_sensores()
            if temperatura is not None:
                enviar_datos_serial(temperatura, humedad_suelo)
                actualizar_pantalla_sensores(temperatura, humedad_ambiente, humedad_suelo)
                verificar_riego_automatico(humedad_suelo)
            else:
                actualizar_pantalla_sensores(None, None, None)
        time.sleep_ms(LOOP_DELAY_MS)

try:
    init_lcd()
    loop_principal()
except KeyboardInterrupt:
    print("\nPrograma detenido")
    rele_bomba.value(0)
    lcd_write("Sistema detenido", "Bomba apagada")
except Exception as e:
    rele_bomba.value(0)
    print("Error fatal:", e)
    lcd_write("Error fatal", str(e)[:16])
