#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QTimer
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from ui_invernadero import Ui_MainWindow

class InvernaderoInteligente(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)

        self.timer_actualizacion = QTimer()
        self.timer_actualizacion.timeout.connect(self.leer_datos_serial)

        self.conectado = False
        self.umbral_humedad = 30

        self.inicializar_base_datos()
        self.cargar_puertos_disponibles()
        self.conectar_senales()

    def conectar_senales(self):
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
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error al inicializar base de datos: {e}")

    def cargar_puertos_disponibles(self):
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
            self.timer_actualizacion.start(200)
            QMessageBox.information(self, "Éxito", f"Conectado al puerto {puerto_seleccionado}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudo conectar al puerto {puerto_seleccionado}")

    def desconectar_esp32(self):
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
        while self.serial.canReadLine():
            try:
                datos = self.serial.readLine().data().decode('utf-8', errors='ignore').strip()
                if not datos:
                    continue

                print(f"RX: {datos}")

                if "TEMP:" in datos and "HUM:" in datos:
                    partes = datos.split(',')
                    temperatura = float(partes[0].split(':')[1])
                    humedad = float(partes[1].split(':')[1])

                    self.ui.lcd_temperatura.display(f"{temperatura:.1f}")
                    self.ui.lcd_humedad.display(f"{humedad:.1f}")

                    riego_activado = 0
                    if humedad < self.umbral_humedad:
                        self.ui.label_estado_bomba.setText("Estado bomba: Activa (Auto)")
                        riego_activado = 1
                        self.actualizar_ultimo_riego()
                    else:
                        self.ui.label_estado_bomba.setText("Estado bomba: Inactiva")

                    self.guardar_lectura(temperatura, humedad, riego_activado)

                elif "Riego completado" in datos:
                    self.ui.label_estado_bomba.setText("Estado bomba: Inactiva")

                elif "Activando riego" in datos:
                    if "manual" in datos:
                        self.ui.label_estado_bomba.setText("Estado bomba: Activa (Manual)")
                    else:
                        self.ui.label_estado_bomba.setText("Estado bomba: Activa (Auto)")

            except Exception as e:
                print(f"Error al leer datos serial: {e}")

    def enviar_comando(self, comando):
        if self.conectado:
            enviados = self.serial.write(f"{comando}\n".encode('utf-8'))
            self.serial.flush()
            print(f"TX: {comando} ({enviados} bytes)")

    def activar_riego_manual(self):
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
            temperatura = self.ui.lcd_temperatura.value()
            humedad = self.ui.lcd_humedad.value()
            self.guardar_lectura(temperatura, humedad, 1)

    def guardar_umbral(self):
        self.umbral_humedad = self.ui.spinbox_umbral_humedad.value()
        self.enviar_comando(f"SET_UMBRAL:{self.umbral_humedad}")
        QMessageBox.information(self, "Éxito", f"Umbral actualizado a {self.umbral_humedad}%")

    def guardar_lectura(self, temperatura, humedad, riego_activado):
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
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.label_ultimo_riego.setText(f"Último riego: {fecha_hora}")

    def mostrar_acerca_de(self):
        QMessageBox.about(
            self,
            "Acerca de",
            "Invernadero Inteligente de Escritorio\n\n"
            "Desarrollado con ESP32, Python y PySide6\n"
            "Sistema de monitoreo y control automatizado para plantas"
        )

    def closeEvent(self, event):
        if self.conectado:
            self.serial.close()
        if hasattr(self, 'conn'):
            self.conn.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    ventana = InvernaderoInteligente()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
