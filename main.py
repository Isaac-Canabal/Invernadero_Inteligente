#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Invernadero Inteligente de Escritorio
Sistema de monitoreo y control automatizado para plantas
Curso: Computación e Interfaces
"""

import sys
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QTimer
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from ui_invernadero import Ui_MainWindow


class InvernaderoInteligente(QMainWindow):
    """
    Clase principal que maneja la interfaz y lógica del invernadero inteligente.
    Se encarga de la comunicación serial con el ESP32, actualización de la interfaz
    y almacenamiento de datos en la base de datos.
    """
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Configuración del puerto serial
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        
        # Timer para actualización periódica de datos
        self.timer_actualizacion = QTimer()
        self.timer_actualizacion.timeout.connect(self.leer_datos_serial)
        
        # Variables de estado
        self.conectado = False
        self.umbral_humedad = 30
        
        # Inicialización del sistema
        self.inicializar_base_datos()
        self.cargar_puertos_disponibles()
        self.conectar_senales()
        
    def conectar_senales(self):
        """
        Se conectan las señales de los widgets a sus respectivas funciones.
        """
        self.ui.btn_conectar.clicked.connect(self.conectar_esp32)
        self.ui.btn_desconectar.clicked.connect(self.desconectar_esp32)
        self.ui.btn_riego_manual.clicked.connect(self.activar_riego_manual)
        self.ui.btn_guardar_umbral.clicked.connect(self.guardar_umbral)
        self.ui.btn_actualizar_historial.clicked.connect(self.cargar_historial)
        self.ui.btn_exportar_historial.clicked.connect(self.exportar_historial)
        self.ui.btn_limpiar_historial.clicked.connect(self.limpiar_historial)
        self.ui.actionSalir.triggered.connect(self.close)
        self.ui.actionAcerca_de.triggered.connect(self.mostrar_acerca_de)
        
    def inicializar_base_datos(self):
        """
        Se crea la base de datos SQLite y la tabla de historial si no existen.
        """
        try:
            self.conn = sqlite3.connect('invernadero.db')
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historial (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_hora TEXT NOT NULL,
                    temperatura REAL,
                    humedad REAL,
                    riego_activado INTEGER DEFAULT 0
                )
            ''')
            self.conn.commit()
            print("Base de datos inicializada correctamente")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error al inicializar base de datos: {e}")
    
    def cargar_puertos_disponibles(self):
        """
        Se escanean y cargan los puertos seriales disponibles en el sistema.
        """
        self.ui.combobox_puerto.clear()
        puertos = QSerialPortInfo.availablePorts()
        
        for puerto in puertos:
            self.ui.combobox_puerto.addItem(puerto.portName())
        
        if self.ui.combobox_puerto.count() == 0:
            self.ui.combobox_puerto.addItem("No hay puertos disponibles")
            self.ui.btn_conectar.setEnabled(False)
        else:
            self.ui.btn_conectar.setEnabled(True)
    
    def conectar_esp32(self):
        """
        Se establece la conexión serial con el ESP32.
        """
        puerto_seleccionado = self.ui.combobox_puerto.currentText()
        
        if puerto_seleccionado == "No hay puertos disponibles":
            QMessageBox.warning(self, "Advertencia", "No hay puertos seriales disponibles")
            return
        
        self.serial.setPortName(puerto_seleccionado)
        
        if self.serial.open(QSerialPort.ReadWrite):
            self.conectado = True
            self.ui.label_estado_conexion.setText("Estado: Conectado")
            self.ui.btn_conectar.setEnabled(False)
            self.ui.btn_desconectar.setEnabled(True)
            self.ui.btn_riego_manual.setEnabled(True)
            self.ui.btn_guardar_umbral.setEnabled(True)
            self.ui.combobox_puerto.setEnabled(False)
            
            # Se inicia el timer para leer datos cada segundo
            self.timer_actualizacion.start(1000)
            
            QMessageBox.information(self, "Éxito", f"Conectado al puerto {puerto_seleccionado}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudo conectar al puerto {puerto_seleccionado}")
    
    def desconectar_esp32(self):
        """
        Se cierra la conexión serial con el ESP32.
        """
        self.timer_actualizacion.stop()
        self.serial.close()
        self.conectado = False
        
        self.ui.label_estado_conexion.setText("Estado: Desconectado")
        self.ui.btn_conectar.setEnabled(True)
        self.ui.btn_desconectar.setEnabled(False)
        self.ui.btn_riego_manual.setEnabled(False)
        self.ui.btn_guardar_umbral.setEnabled(False)
        self.ui.combobox_puerto.setEnabled(True)
        
        QMessageBox.information(self, "Desconectado", "Conexión cerrada correctamente")
    
    def leer_datos_serial(self):
        """
        Se leen los datos enviados por el ESP32 a través del puerto serial.
        Se espera recibir datos en formato: TEMP:25.5,HUM:45.2
        """
        if not self.serial.canReadLine():
            return
        
        try:
            datos = self.serial.readLine().data().decode('utf-8').strip()
            
            # Se parsean los datos recibidos
            if "TEMP:" in datos and "HUM:" in datos:
                partes = datos.split(',')
                temperatura = float(partes[0].split(':')[1])
                humedad = float(partes[1].split(':')[1])
                
                # Se actualiza la interfaz
                self.ui.lcd_temperatura.display(f"{temperatura:.1f}")
                self.ui.lcd_humedad.display(f"{humedad:.1f}")
                
                self.ui.statusbar.showMessage("Conexión activa")
                print(f"Lectura serial -> Temp: {temperatura}°C, Humedad Suelo: {humedad}%")
                
                # Se verifica si se debe activar el riego automático
                riego_activado = 0
                if humedad < self.umbral_humedad:
                    self.enviar_comando("RIEGO_ON")
                    self.ui.label_estado_bomba.setText("Estado bomba: Activa")
                    riego_activado = 1
                    self.actualizar_ultimo_riego()
                else:
                    self.ui.label_estado_bomba.setText("Estado bomba: Inactiva")
                
                # Se guardan los datos en la base de datos
                self.guardar_lectura(temperatura, humedad, riego_activado)
                
        except Exception as e:
            print(f"Error al leer datos serial: {e}")
    
    def enviar_comando(self, comando):
        """
        Se envía un comando al ESP32 a través del puerto serial.
        
        Args:
            comando (str): Comando a enviar (ej: "RIEGO_ON", "RIEGO_OFF", "SET_UMBRAL:30")
        """
        if self.conectado:
            self.serial.write(f"{comando}\n".encode('utf-8'))
            print(f"Comando enviado: {comando}")
    
    def activar_riego_manual(self):
        """
        Se activa el riego de forma manual mediante un comando al ESP32.
        """
        respuesta = QMessageBox.question(
            self, 
            "Riego Manual", 
            "¿Desea activar el riego manual?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            self.enviar_comando("RIEGO_MANUAL")
            self.ui.label_estado_bomba.setText("Estado bomba: Activa (Manual)")
            self.actualizar_ultimo_riego()
            
            # Se registra en la base de datos
            temperatura = self.ui.lcd_temperatura.value()
            humedad = self.ui.lcd_humedad.value()
            self.guardar_lectura(temperatura, humedad, 1)
    
    def guardar_umbral(self):
        """
        Se guarda el nuevo umbral de humedad y se envía al ESP32.
        """
        self.umbral_humedad = self.ui.spinbox_umbral_humedad.value()
        self.enviar_comando(f"SET_UMBRAL:{self.umbral_humedad}")
        QMessageBox.information(self, "Éxito", f"Umbral actualizado a {self.umbral_humedad}%")
    
    def guardar_lectura(self, temperatura, humedad, riego_activado):
        """
        Se guarda una lectura de sensores en la base de datos.
        
        Args:
            temperatura (float): Temperatura medida en °C
            humedad (float): Humedad del suelo en %
            riego_activado (int): 1 si se activó el riego, 0 si no
        """
        try:
            cursor = self.conn.cursor()
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO historial (fecha_hora, temperatura, humedad, riego_activado) VALUES (?, ?, ?, ?)",
                (fecha_hora, temperatura, humedad, riego_activado)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al guardar lectura: {e}")
    
    def cargar_historial(self):
        """
        Se carga el historial de lecturas desde la base de datos y se muestra en la tabla.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT fecha_hora, temperatura, humedad, riego_activado FROM historial ORDER BY id DESC LIMIT 100"
            )
            registros = cursor.fetchall()
            
            self.ui.table_historial.setRowCount(len(registros))
            
            for fila, registro in enumerate(registros):
                self.ui.table_historial.setItem(fila, 0, QTableWidgetItem(registro[0]))
                self.ui.table_historial.setItem(fila, 1, QTableWidgetItem(f"{registro[1]:.1f}"))
                self.ui.table_historial.setItem(fila, 2, QTableWidgetItem(f"{registro[2]:.1f}"))
                estado_riego = "Sí" if registro[3] == 1 else "No"
                self.ui.table_historial.setItem(fila, 3, QTableWidgetItem(estado_riego))
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar historial: {e}")
    
    def exportar_historial(self):
        """
        Se exporta el historial completo a un archivo CSV.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM historial ORDER BY id DESC")
            registros = cursor.fetchall()
            
            nombre_archivo = f"historial_invernadero_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write("ID,Fecha/Hora,Temperatura (°C),Humedad (%),Riego Activado\n")
                for registro in registros:
                    archivo.write(f"{registro[0]},{registro[1]},{registro[2]},{registro[3]},{registro[4]}\n")
            
            QMessageBox.information(self, "Éxito", f"Historial exportado a {nombre_archivo}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar historial: {e}")
    
    def limpiar_historial(self):
        """
        Se eliminan todos los registros del historial de la base de datos.
        """
        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            "¿Está seguro de que desea eliminar todo el historial?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM historial")
                self.conn.commit()
                self.ui.table_historial.setRowCount(0)
                QMessageBox.information(self, "Éxito", "Historial eliminado correctamente")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error al limpiar historial: {e}")
    
    def actualizar_ultimo_riego(self):
        """
        Se actualiza la etiqueta de último riego con la fecha y hora actual.
        """
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.label_ultimo_riego.setText(f"Último riego: {fecha_hora}")
    
    def mostrar_acerca_de(self):
        """
        Se muestra un cuadro de diálogo con información sobre el proyecto.
        """
        QMessageBox.about(
            self,
            "Acerca de",
            "Invernadero Inteligente de Escritorio\n\n"
            "Curso: Computación e Interfaces\n"
            "NRC: 1475 - 1476\n\n"
            "Desarrollado con ESP32, Python y PySide6\n"
            "Sistema de monitoreo y control automatizado para plantas"
        )
    
    def closeEvent(self, event):
        """
        Se ejecuta al cerrar la aplicación. Se cierra la conexión serial y la base de datos.
        """
        if self.conectado:
            self.serial.close()
        
        if hasattr(self, 'conn'):
            self.conn.close()
        
        event.accept()


def main():
    """
    Función principal que inicia la aplicación.
    """
    app = QApplication(sys.argv)
    ventana = InvernaderoInteligente()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
