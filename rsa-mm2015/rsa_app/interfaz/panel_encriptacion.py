"""Formulario de encriptación."""


import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from typing import Callable

from rsa_app.modelos.resultado_encriptacion import ResultadoEncriptacion


class PanelEncriptacion(ttk.Frame):
    """Recibe el mensaje y los parámetros, sin realizar cálculos RSA."""

    def __init__(
        self,
        master: tk.Misc,
        al_encriptar: Callable[[], None],
        al_cambiar: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(master, padding=12)
        self.al_cambiar = al_cambiar
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)
        self.variables = {
            nombre: tk.StringVar(master=self) for nombre in ("p", "q", "e")
        }
        self.salidas = {
            nombre: tk.StringVar(master=self)
            for nombre in ("cifrado", "longitud_original", "llave_publica")
        }
        self.aviso_copia = tk.StringVar(master=self)

        ttk.Label(self, text="Mensaje original M (se conservan todos sus espacios)").grid(
            row=0, column=0, sticky="w"
        )
        self.texto_mensaje = ScrolledText(
            self, height=3, width=64, wrap="word", font="TkFixedFont", undo=True
        )
        self.texto_mensaje.grid(row=1, column=0, sticky="nsew", pady=(4, 4))
        ttk.Label(
            self,
            text="ASCII imprimible 32 a 126: letras sin tildes, números, signos y espacios.",
        ).grid(row=2, column=0, sticky="w", pady=(0, 8))

        parametros = ttk.Frame(self)
        parametros.grid(row=3, column=0, sticky="ew")
        for columna, nombre in enumerate(("p", "q", "e")):
            parametros.columnconfigure(columna * 2 + 1, weight=1)
            ttk.Label(parametros, text=f"{nombre}:").grid(
                row=0, column=columna * 2, sticky="w", padx=(0 if columna == 0 else 12, 4)
            )
            ttk.Entry(parametros, textvariable=self.variables[nombre], width=16).grid(
                row=0, column=columna * 2 + 1, sticky="ew"
            )

        self.boton_encriptar = ttk.Button(self, text="Encriptar", command=al_encriptar)
        self.boton_encriptar.grid(row=4, column=0, sticky="w", pady=10)

        resultados = ttk.LabelFrame(self, text="Resultado de la encriptación", padding=10)
        resultados.grid(row=5, column=0, sticky="nsew")
        resultados.columnconfigure(0, weight=1)
        resultados.rowconfigure(1, weight=1)
        ttk.Label(resultados, text="Cifrado C (seis dígitos por bloque)").grid(
            row=0, column=0, sticky="w"
        )
        self.texto_resultado = ScrolledText(
            resultados, height=3, width=64, wrap="word", font="TkFixedFont", state="disabled"
        )
        self.texto_resultado.grid(row=1, column=0, sticky="nsew", pady=(4, 6))

        metadatos = ttk.Frame(resultados)
        metadatos.grid(row=2, column=0, sticky="ew")
        metadatos.columnconfigure(3, weight=1)
        ttk.Label(metadatos, text="Longitud L:").grid(row=0, column=0, sticky="w")
        ttk.Entry(
            metadatos, textvariable=self.salidas["longitud_original"], width=10, state="readonly"
        ).grid(row=0, column=1, sticky="w", padx=(5, 18))
        ttk.Label(metadatos, text="Llave pública (e, n):").grid(row=0, column=2, sticky="w")
        ttk.Entry(
            metadatos, textvariable=self.salidas["llave_publica"], width=28, state="readonly"
        ).grid(row=0, column=3, sticky="ew", padx=(5, 0))

        acciones = ttk.Frame(resultados)
        acciones.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        self.boton_copiar_cifrado = ttk.Button(
            acciones, text="Copiar C", command=lambda: self._copiar("cifrado", "C")
        )
        self.boton_copiar_cifrado.grid(row=0, column=0, padx=(0, 8))
        self.boton_copiar_longitud = ttk.Button(
            acciones, text="Copiar L", command=lambda: self._copiar("longitud_original", "L")
        )
        self.boton_copiar_longitud.grid(row=0, column=1)
        ttk.Label(acciones, textvariable=self.aviso_copia).grid(row=0, column=2, padx=12)
        self.limpiar_resultados()

        for variable in self.variables.values():
            variable.trace_add("write", self._entrada_cambiada)
        self.texto_mensaje.edit_modified(False)
        self.texto_mensaje.bind("<<Modified>>", self._texto_cambiado)

    def obtener_datos(self) -> dict[str, str]:
        """Excluye únicamente el salto de línea interno añadido por Tkinter."""
        return {
            "mensaje": self.texto_mensaje.get("1.0", "end-1c"),
            **{nombre: variable.get() for nombre, variable in self.variables.items()},
        }

    def cargar_datos(self, mensaje: str, p: str | int, q: str | int, e: str | int) -> None:
        """Carga, por ejemplo, las entradas del ejemplo del enunciado."""
        self.texto_mensaje.delete("1.0", "end")
        self.texto_mensaje.insert("1.0", mensaje)
        self.texto_mensaje.edit_modified(False)
        for nombre, valor in (("p", p), ("q", q), ("e", e)):
            self.variables[nombre].set(str(valor))
        self._entrada_cambiada()

    def mostrar_resultado(self, resultado: ResultadoEncriptacion) -> None:
        """Presenta exactamente las salidas recibidas del controlador."""
        self.salidas["cifrado"].set(resultado.cifrado)
        self.salidas["longitud_original"].set(str(resultado.longitud_original))
        self.salidas["llave_publica"].set(
            f"({resultado.parametros.e}, {resultado.parametros.n})"
        )
        self._poner_resultado(resultado.cifrado)
        self.aviso_copia.set("")
        self.boton_copiar_cifrado.state(["!disabled"])
        self.boton_copiar_longitud.state(["!disabled"])

    def limpiar_resultados(self) -> None:
        """Evita que una salida anterior se confunda con las entradas actuales."""
        for variable in self.salidas.values():
            variable.set("")
        self._poner_resultado("")
        self.aviso_copia.set("")
        self.boton_copiar_cifrado.state(["disabled"])
        self.boton_copiar_longitud.state(["disabled"])

    def _poner_resultado(self, texto: str) -> None:
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)
        self.texto_resultado.configure(state="disabled")

    def _entrada_cambiada(self, *_: object) -> None:
        self.limpiar_resultados()
        if self.al_cambiar is not None:
            self.al_cambiar()

    def _texto_cambiado(self, _evento: tk.Event) -> None:
        if self.texto_mensaje.edit_modified():
            self.texto_mensaje.edit_modified(False)
            self._entrada_cambiada()

    def _copiar(self, clave: str, etiqueta: str) -> None:
        try:
            self.clipboard_clear()
            self.clipboard_append(self.salidas[clave].get())
        except tk.TclError:
            messagebox.showerror("Portapapeles", "No se pudo copiar el resultado.", parent=self)
        else:
            self.aviso_copia.set(f"{etiqueta} copiado.")

