"""Ventana principal del programa."""


from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

from rsa_app.interfaz.panel_desencriptacion import PanelDesencriptacion
from rsa_app.interfaz.panel_detalle import PanelDetalle
from rsa_app.interfaz.panel_encriptacion import PanelEncriptacion
from rsa_app.modelos.resultado_desencriptacion import ResultadoDesencriptacion
from rsa_app.modelos.resultado_encriptacion import ResultadoEncriptacion

if TYPE_CHECKING:
    from rsa_app.controladores.controlador_rsa import ControladorRSA


class AplicacionRSA(tk.Tk):
    """Organiza los formularios y presenta los resultados y las validaciones."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Proyecto RSA | MM2015")
        self.geometry("1080x800")
        self.minsize(900, 720)
        self.controlador: ControladorRSA | None = None
        self.resultado_encriptacion: ResultadoEncriptacion | None = None
        self._operacion_en_curso: str | None = None
        self._hay_detalle = False

        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 19, "bold"))
        estilo.configure("TButton", padding=(10, 6))
        estilo.configure("Treeview", rowheight=28)

        contenedor = ttk.Frame(self, padding=16)
        contenedor.grid(sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(3, weight=1)
        ttk.Label(contenedor, text="Criptografía RSA", style="Titulo.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            contenedor,
            text="Ingresa los datos, ejecuta una operación y consulta su procedimiento.",
        ).grid(row=1, column=0, sticky="w", pady=(3, 12))

        herramientas = ttk.Frame(contenedor)
        herramientas.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        ttk.Button(
            herramientas, text="Cargar ejemplo del PDF", command=self.cargar_ejemplo
        ).grid(row=0, column=0, padx=(0, 8))
        self.boton_transferir = ttk.Button(
            herramientas, text="Pasar C y L a desencriptación",
            command=self.pasar_a_desencriptacion, state="disabled",
        )
        self.boton_transferir.grid(row=0, column=1, padx=(0, 8))
        self.boton_detalle = ttk.Button(
            herramientas, text="Ver detalle del proceso",
            command=self.ver_detalle, state="disabled",
        )
        self.boton_detalle.grid(row=0, column=2)

        self.pestanas = ttk.Notebook(contenedor)
        self.pestanas.grid(row=3, column=0, sticky="nsew")
        self.panel_encriptacion = PanelEncriptacion(
            self.pestanas, al_encriptar=self.solicitar_encriptacion,
            al_cambiar=lambda: self._entradas_modificadas("encriptacion"),
        )
        self.panel_desencriptacion = PanelDesencriptacion(
            self.pestanas, al_desencriptar=self.solicitar_desencriptacion,
            al_cambiar=lambda: self._entradas_modificadas("desencriptacion"),
        )
        self.panel_detalle = PanelDetalle(self.pestanas)
        self.pestanas.add(self.panel_encriptacion, text="  Encriptación  ")
        self.pestanas.add(self.panel_desencriptacion, text="  Desencriptación  ")
        self.pestanas.add(self.panel_detalle, text="  Detalle del proceso  ")
        self.estado = tk.StringVar(
            self, value="Listo. Puedes comenzar con el ejemplo de referencia."
        )
        ttk.Label(contenedor, textvariable=self.estado, wraplength=850).grid(
            row=4, column=0, sticky="ew", pady=(12, 0)
        )

    def conectar_controlador(self, controlador: ControladorRSA) -> None:
        """Recibe el controlador creado en el punto de entrada."""
        self.controlador = controlador

    def solicitar_encriptacion(self) -> None:
        """Entrega las entradas exactas del formulario al controlador."""
        self._operacion_en_curso = "encriptacion"
        self.panel_encriptacion.limpiar_resultados()
        self.resultado_encriptacion = None
        self.boton_transferir.configure(state="disabled")
        self._limpiar_detalle()
        if self.controlador is None:
            self.mostrar_error("La ventana aún no tiene un controlador conectado.")
            return
        self.controlador.encriptar(**self.panel_encriptacion.obtener_datos())

    def solicitar_desencriptacion(self) -> None:
        """Entrega C, L y los parámetros sin alterar su contenido."""
        self._operacion_en_curso = "desencriptacion"
        self.panel_desencriptacion.limpiar_resultados()
        self._limpiar_detalle()
        if self.controlador is None:
            self.mostrar_error("La ventana aún no tiene un controlador conectado.")
            return
        self.controlador.desencriptar(**self.panel_desencriptacion.obtener_datos())

    def mostrar_encriptacion(self, resultado: ResultadoEncriptacion) -> None:
        self.panel_encriptacion.mostrar_resultado(resultado)
        self.resultado_encriptacion = resultado
        self.boton_transferir.configure(state="normal")
        self.panel_detalle.mostrar_encriptacion(resultado)
        self._habilitar_detalle()
        self.estado.set("Encriptación completada. Conserva C y L para desencriptar.")
        self._operacion_en_curso = None

    def mostrar_desencriptacion(self, resultado: ResultadoDesencriptacion) -> None:
        self.panel_desencriptacion.mostrar_resultado(resultado)
        self.panel_detalle.mostrar_desencriptacion(resultado)
        self._habilitar_detalle()
        self.estado.set("Desencriptación completada. Se conservan los espacios originales.")
        self._operacion_en_curso = None

    def mostrar_error(self, mensaje: str) -> None:
        """Muestra la validación sin dejar salidas anteriores como válidas."""
        if self._operacion_en_curso == "encriptacion":
            self.panel_encriptacion.limpiar_resultados()
            self.resultado_encriptacion = None
            self.boton_transferir.configure(state="disabled")
        elif self._operacion_en_curso == "desencriptacion":
            self.panel_desencriptacion.limpiar_resultados()
        self._limpiar_detalle()
        self.estado.set("Revisa los datos: " + mensaje)
        self._operacion_en_curso = None
        messagebox.showerror("Datos inválidos", mensaje, parent=self)

    def cargar_ejemplo(self) -> None:
        """Carga los datos del enunciado para probar ambas operaciones."""
        self.panel_encriptacion.cargar_datos("RSA", 367, 373, 17)
        self.panel_desencriptacion.cargar_datos("026054 123875", 3, 367, 373, 17)
        self.pestanas.select(self.panel_encriptacion)
        self.estado.set("Ejemplo cargado: pulsa Encriptar para calcular sus resultados.")

    def pasar_a_desencriptacion(self) -> None:
        """Reutiliza los datos de la última encriptación válida."""
        resultado = self.resultado_encriptacion
        if resultado is None:
            return
        parametros = resultado.parametros
        self.panel_desencriptacion.cargar_datos(
            resultado.cifrado, resultado.longitud_original,
            parametros.p, parametros.q, parametros.e,
        )
        self.pestanas.select(self.panel_desencriptacion)
        self.estado.set("C, L, p, q y e cargados. Pulsa Desencriptar.")

    def ver_detalle(self) -> None:
        if self._hay_detalle:
            self.pestanas.select(self.panel_detalle)

    def _entradas_modificadas(self, operacion: str) -> None:
        if operacion == "encriptacion":
            self.resultado_encriptacion = None
            self.boton_transferir.configure(state="disabled")
        self._limpiar_detalle()
        if hasattr(self, "estado"):
            self.estado.set("Datos modificados. Ejecuta la operación para actualizar resultados.")

    def _limpiar_detalle(self) -> None:
        if hasattr(self, "panel_detalle"):
            self.panel_detalle.limpiar()
        self._hay_detalle = False
        self.boton_detalle.configure(state="disabled")

    def _habilitar_detalle(self) -> None:
        self._hay_detalle = True
        self.boton_detalle.configure(state="normal")
