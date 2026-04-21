# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'invernadero_interfaz.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLCDNumber,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 740)
        self.actionExportar = QAction(MainWindow)
        self.actionExportar.setObjectName(u"actionExportar")
        self.actionSalir = QAction(MainWindow)
        self.actionSalir.setObjectName(u"actionSalir")
        self.actionAcerca_de = QAction(MainWindow)
        self.actionAcerca_de.setObjectName(u"actionAcerca_de")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupbox_monitoreo = QGroupBox(self.centralwidget)
        self.groupbox_monitoreo.setObjectName(u"groupbox_monitoreo")
        self.gridLayout_monitoreo = QGridLayout(self.groupbox_monitoreo)
        self.gridLayout_monitoreo.setObjectName(u"gridLayout_monitoreo")
        self.label_temperatura_titulo = QLabel(self.groupbox_monitoreo)
        self.label_temperatura_titulo.setObjectName(u"label_temperatura_titulo")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_temperatura_titulo.setFont(font)

        self.gridLayout_monitoreo.addWidget(self.label_temperatura_titulo, 0, 0, 1, 1)

        self.lcd_temperatura = QLCDNumber(self.groupbox_monitoreo)
        self.lcd_temperatura.setObjectName(u"lcd_temperatura")
        self.lcd_temperatura.setMinimumSize(QSize(100, 50))
        self.lcd_temperatura.setDigitCount(5)
        self.lcd_temperatura.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.gridLayout_monitoreo.addWidget(self.lcd_temperatura, 0, 1, 1, 1)

        self.label_temperatura_unidad = QLabel(self.groupbox_monitoreo)
        self.label_temperatura_unidad.setObjectName(u"label_temperatura_unidad")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_temperatura_unidad.setFont(font1)

        self.gridLayout_monitoreo.addWidget(self.label_temperatura_unidad, 0, 2, 1, 1)

        self.label_humedad_titulo = QLabel(self.groupbox_monitoreo)
        self.label_humedad_titulo.setObjectName(u"label_humedad_titulo")
        self.label_humedad_titulo.setFont(font)

        self.gridLayout_monitoreo.addWidget(self.label_humedad_titulo, 1, 0, 1, 1)

        self.lcd_humedad = QLCDNumber(self.groupbox_monitoreo)
        self.lcd_humedad.setObjectName(u"lcd_humedad")
        self.lcd_humedad.setMinimumSize(QSize(100, 50))
        self.lcd_humedad.setDigitCount(5)
        self.lcd_humedad.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.gridLayout_monitoreo.addWidget(self.lcd_humedad, 1, 1, 1, 1)

        self.label_humedad_unidad = QLabel(self.groupbox_monitoreo)
        self.label_humedad_unidad.setObjectName(u"label_humedad_unidad")
        self.label_humedad_unidad.setFont(font1)

        self.gridLayout_monitoreo.addWidget(self.label_humedad_unidad, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.groupbox_monitoreo)

        self.groupbox_control = QGroupBox(self.centralwidget)
        self.groupbox_control.setObjectName(u"groupbox_control")
        self.gridLayout_control = QGridLayout(self.groupbox_control)
        self.gridLayout_control.setObjectName(u"gridLayout_control")
        self.label_puerto = QLabel(self.groupbox_control)
        self.label_puerto.setObjectName(u"label_puerto")

        self.gridLayout_control.addWidget(self.label_puerto, 0, 0, 1, 1)

        self.combobox_puerto = QComboBox(self.groupbox_control)
        self.combobox_puerto.setObjectName(u"combobox_puerto")
        self.combobox_puerto.setMinimumSize(QSize(150, 0))

        self.gridLayout_control.addWidget(self.combobox_puerto, 0, 1, 1, 1)

        self.btn_conectar = QPushButton(self.groupbox_control)
        self.btn_conectar.setObjectName(u"btn_conectar")
        self.btn_conectar.setMinimumSize(QSize(120, 30))

        self.gridLayout_control.addWidget(self.btn_conectar, 0, 2, 1, 1)

        self.btn_desconectar = QPushButton(self.groupbox_control)
        self.btn_desconectar.setObjectName(u"btn_desconectar")
        self.btn_desconectar.setEnabled(False)
        self.btn_desconectar.setMinimumSize(QSize(120, 30))

        self.gridLayout_control.addWidget(self.btn_desconectar, 0, 3, 1, 1)

        self.btn_riego_manual = QPushButton(self.groupbox_control)
        self.btn_riego_manual.setObjectName(u"btn_riego_manual")
        self.btn_riego_manual.setEnabled(False)
        self.btn_riego_manual.setMinimumSize(QSize(0, 35))

        self.gridLayout_control.addWidget(self.btn_riego_manual, 1, 0, 1, 2)

        self.label_estado_bomba = QLabel(self.groupbox_control)
        self.label_estado_bomba.setObjectName(u"label_estado_bomba")
        self.label_estado_bomba.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_control.addWidget(self.label_estado_bomba, 1, 2, 1, 2)


        self.verticalLayout.addWidget(self.groupbox_control)

        self.groupbox_umbrales = QGroupBox(self.centralwidget)
        self.groupbox_umbrales.setObjectName(u"groupbox_umbrales")
        self.horizontalLayout_umbrales = QHBoxLayout(self.groupbox_umbrales)
        self.horizontalLayout_umbrales.setObjectName(u"horizontalLayout_umbrales")
        self.label_umbral_humedad = QLabel(self.groupbox_umbrales)
        self.label_umbral_humedad.setObjectName(u"label_umbral_humedad")

        self.horizontalLayout_umbrales.addWidget(self.label_umbral_humedad)

        self.spinbox_umbral_humedad = QSpinBox(self.groupbox_umbrales)
        self.spinbox_umbral_humedad.setObjectName(u"spinbox_umbral_humedad")
        self.spinbox_umbral_humedad.setMinimumSize(QSize(80, 0))
        self.spinbox_umbral_humedad.setMinimum(0)
        self.spinbox_umbral_humedad.setMaximum(100)
        self.spinbox_umbral_humedad.setValue(30)

        self.horizontalLayout_umbrales.addWidget(self.spinbox_umbral_humedad)

        self.btn_guardar_umbral = QPushButton(self.groupbox_umbrales)
        self.btn_guardar_umbral.setObjectName(u"btn_guardar_umbral")
        self.btn_guardar_umbral.setEnabled(False)

        self.horizontalLayout_umbrales.addWidget(self.btn_guardar_umbral)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_umbrales.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.groupbox_umbrales)

        self.groupbox_historial = QGroupBox(self.centralwidget)
        self.groupbox_historial.setObjectName(u"groupbox_historial")
        self.verticalLayout_historial = QVBoxLayout(self.groupbox_historial)
        self.verticalLayout_historial.setObjectName(u"verticalLayout_historial")
        self.table_historial = QTableWidget(self.groupbox_historial)
        if (self.table_historial.columnCount() < 4):
            self.table_historial.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_historial.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_historial.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_historial.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_historial.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table_historial.setObjectName(u"table_historial")
        self.table_historial.setMinimumSize(QSize(0, 200))
        self.table_historial.setAlternatingRowColors(True)
        self.table_historial.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_historial.setSortingEnabled(True)

        self.verticalLayout_historial.addWidget(self.table_historial)

        self.horizontalLayout_botones_historial = QHBoxLayout()
        self.horizontalLayout_botones_historial.setObjectName(u"horizontalLayout_botones_historial")
        self.btn_actualizar_historial = QPushButton(self.groupbox_historial)
        self.btn_actualizar_historial.setObjectName(u"btn_actualizar_historial")

        self.horizontalLayout_botones_historial.addWidget(self.btn_actualizar_historial)

        self.btn_exportar_historial = QPushButton(self.groupbox_historial)
        self.btn_exportar_historial.setObjectName(u"btn_exportar_historial")

        self.horizontalLayout_botones_historial.addWidget(self.btn_exportar_historial)

        self.btn_limpiar_historial = QPushButton(self.groupbox_historial)
        self.btn_limpiar_historial.setObjectName(u"btn_limpiar_historial")

        self.horizontalLayout_botones_historial.addWidget(self.btn_limpiar_historial)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_botones_historial.addItem(self.horizontalSpacer_2)


        self.verticalLayout_historial.addLayout(self.horizontalLayout_botones_historial)


        self.verticalLayout.addWidget(self.groupbox_historial)

        self.groupbox_estado = QGroupBox(self.centralwidget)
        self.groupbox_estado.setObjectName(u"groupbox_estado")
        self.groupbox_estado.setMaximumSize(QSize(16777215, 80))
        self.gridLayout_estado = QGridLayout(self.groupbox_estado)
        self.gridLayout_estado.setObjectName(u"gridLayout_estado")
        self.label_estado_conexion = QLabel(self.groupbox_estado)
        self.label_estado_conexion.setObjectName(u"label_estado_conexion")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_estado_conexion.setFont(font2)

        self.gridLayout_estado.addWidget(self.label_estado_conexion, 0, 0, 1, 1)

        self.label_ultimo_riego = QLabel(self.groupbox_estado)
        self.label_ultimo_riego.setObjectName(u"label_ultimo_riego")
        font3 = QFont()
        font3.setPointSize(10)
        self.label_ultimo_riego.setFont(font3)

        self.gridLayout_estado.addWidget(self.label_ultimo_riego, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupbox_estado)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.menuArchivo.addAction(self.actionExportar)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionSalir)
        self.menuAyuda.addAction(self.actionAcerca_de)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Invernadero Inteligente de Escritorio", None))
        self.actionExportar.setText(QCoreApplication.translate("MainWindow", u"Exportar datos...", None))
        self.actionSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.actionAcerca_de.setText(QCoreApplication.translate("MainWindow", u"Acerca de...", None))
        self.groupbox_monitoreo.setTitle(QCoreApplication.translate("MainWindow", u"Monitoreo en Tiempo Real", None))
        self.label_temperatura_titulo.setText(QCoreApplication.translate("MainWindow", u"Temperatura:", None))
        self.label_temperatura_unidad.setText(QCoreApplication.translate("MainWindow", u"\u00b0C", None))
        self.label_humedad_titulo.setText(QCoreApplication.translate("MainWindow", u"Humedad del suelo:", None))
        self.label_humedad_unidad.setText(QCoreApplication.translate("MainWindow", u"%", None))
        self.groupbox_control.setTitle(QCoreApplication.translate("MainWindow", u"Control del Sistema", None))
        self.label_puerto.setText(QCoreApplication.translate("MainWindow", u"Puerto Serial:", None))
        self.btn_conectar.setText(QCoreApplication.translate("MainWindow", u"Conectar ESP32", None))
        self.btn_desconectar.setText(QCoreApplication.translate("MainWindow", u"Desconectar", None))
        self.btn_riego_manual.setText(QCoreApplication.translate("MainWindow", u"Activar Riego Manual", None))
        self.label_estado_bomba.setText(QCoreApplication.translate("MainWindow", u"Estado bomba: Inactiva", None))
        self.groupbox_umbrales.setTitle(QCoreApplication.translate("MainWindow", u"Configuraci\u00f3n de Umbrales", None))
        self.label_umbral_humedad.setText(QCoreApplication.translate("MainWindow", u"Umbral de humedad m\u00ednima (%):", None))
        self.btn_guardar_umbral.setText(QCoreApplication.translate("MainWindow", u"Aplicar Configuraci\u00f3n", None))
        self.groupbox_historial.setTitle(QCoreApplication.translate("MainWindow", u"Historial de Datos", None))
        ___qtablewidgetitem = self.table_historial.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Fecha/Hora", None))
        ___qtablewidgetitem1 = self.table_historial.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Temperatura (\u00b0C)", None))
        ___qtablewidgetitem2 = self.table_historial.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Humedad (%)", None))
        ___qtablewidgetitem3 = self.table_historial.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Riego Activado", None))
        self.btn_actualizar_historial.setText(QCoreApplication.translate("MainWindow", u"Actualizar Historial", None))
        self.btn_exportar_historial.setText(QCoreApplication.translate("MainWindow", u"Exportar a CSV", None))
        self.btn_limpiar_historial.setText(QCoreApplication.translate("MainWindow", u"Limpiar Historial", None))
        self.groupbox_estado.setTitle(QCoreApplication.translate("MainWindow", u"Estado del Sistema", None))
        self.label_estado_conexion.setText(QCoreApplication.translate("MainWindow", u"Estado: Desconectado", None))
        self.label_ultimo_riego.setText(QCoreApplication.translate("MainWindow", u"\u00daltimo riego: --", None))
        self.menuArchivo.setTitle(QCoreApplication.translate("MainWindow", u"Archivo", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("MainWindow", u"Ayuda", None))
    # retranslateUi

