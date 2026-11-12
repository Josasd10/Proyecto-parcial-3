"""Formulario de desencriptación y representación fiel del mensaje."""

import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from typing import Callable

from rsa_app.modelos.resultado_desencriptacion import ResultadoDesencriptacion


class PanelDesencriptacion(ttk.Frame):
    """Recibe C, L y los parámetros; presenta el texto sin quitar espacios."""

    def __init__(
        self,
        master: tk.Misc,
        al_desencriptar: Callable[[], None],
        al_cambiar: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(master, padding=12)
        self.al_cambiar = al_cambiar
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)
        self.variables = {
            nombre: tk.StringVar(master=self)
            for nombre in ("longitud_original", "p", "q", "e")
        }
        self.salidas = {
            nombre: tk.StringVar(master=self) for nombre in ("d", "mensaje_visible")
        }
        self.aviso_copia = tk.StringVar(master=self)
        self.longitud_recuperada = tk.StringVar(master=self)
        self._mensaje_original = ""

        ttk.Label(self, text="Cifrado C (bloques de seis dígitos separados por un espacio)").grid(
            row=0, column=0, sticky="w"
        )
        self.texto_cifrado = ScrolledText(
            self, height=3, width=64, wrap="word", font="TkFixedFont", undo=True
        )
        self.texto_cifrado.grid(row=1, column=0, sticky="nsew", pady=(4, 4))
        ttk.Label(
            self, text="Conserva los ceros iniciales de C e ingresa la longitud original L."
        ).grid(row=2, column=0, sticky="w", pady=(0, 8))

        parametros = ttk.Frame(self)
        parametros.grid(row=3, column=0, sticky="ew")
        for columna, nombre in enumerate(("longitud_original", "p", "q", "e")):
            parametros.columnconfigure(columna * 2 + 1, weight=1)
            ttk.Label(parametros, text="L:" if nombre == "longitud_original" else f"{nombre}:").grid(
                row=0, column=columna * 2, sticky="w", padx=(0 if columna == 0 else 12, 4)
            )
            ttk.Entry(parametros, textvariable=self.variables[nombre], width=12).grid(
                row=0, column=columna * 2 + 1, sticky="ew"
            )

        self.boton_desencriptar = ttk.Button(
            self, text="Desencriptar", command=al_desencriptar
        )
        self.boton_desencriptar.grid(row=4, column=0, sticky="w", pady=10)

        resultados = ttk.LabelFrame(self, text="Resultado de la desencriptación", padding=10)
        resultados.grid(row=5, column=0, sticky="nsew")
        resultados.columnconfigure(0, weight=1)
        resultados.rowconfigure(2, weight=1)
        fila_d = ttk.Frame(resultados)
        fila_d.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(fila_d, text="Exponente privado d:").grid(row=0, column=0, sticky="w")
        ttk.Entry(fila_d, textvariable=self.salidas["d"], width=20, state="readonly").grid(
            row=0, column=1, sticky="w", padx=6
        )
        ttk.Label(fila_d, textvariable=self.longitud_recuperada).grid(row=0, column=2, padx=12)
        ttk.Label(resultados, text="Mensaje original M (texto exacto)").grid(
            row=1, column=0, sticky="w"
        )
        self.texto_resultado = ScrolledText(
            resultados, height=2, width=64, wrap="word", font="TkFixedFont", state="disabled"
        )
        self.texto_resultado.grid(row=2, column=0, sticky="nsew", pady=(4, 6))

        ttk.Label(resultados, text="Vista de espacios: cada · representa un espacio original.").grid(
            row=3, column=0, sticky="w"
        )
        self.entrada_mensaje_visible = ttk.Entry(
            resultados, textvariable=self.salidas["mensaje_visible"], state="readonly",
            font="TkFixedFont",
        )
        self.entrada_mensaje_visible.grid(row=4, column=0, sticky="ew", pady=(4, 0))
        barra_visible = ttk.Scrollbar(
            resultados, orient="horizontal", command=self.entrada_mensaje_visible.xview
        )
        barra_visible.grid(row=5, column=0, sticky="ew")
        self.entrada_mensaje_visible.configure(xscrollcommand=barra_visible.set)

        acciones = ttk.Frame(resultados)
        acciones.grid(row=6, column=0, sticky="ew", pady=(8, 0))
        self.boton_copiar_mensaje = ttk.Button(
            acciones, text="Copiar mensaje exacto", command=self._copiar_mensaje
        )
        self.boton_copiar_mensaje.grid(row=0, column=0, sticky="w")
        ttk.Label(acciones, textvariable=self.aviso_copia).grid(row=0, column=1, padx=12)
        self.limpiar_resultados()

        for variable in self.variables.values():
            variable.trace_add("write", self._entrada_cambiada)
        self.texto_cifrado.edit_modified(False)
        self.texto_cifrado.bind("<<Modified>>", self._texto_cambiado)

    def obtener_datos(self) -> dict[str, str]:
        """Conserva C tal como se ingresó para que el validador revise su formato."""
        return {
            "cifrado": self.texto_cifrado.get("1.0", "end-1c"),
            **{nombre: variable.get() for nombre, variable in self.variables.items()},
        }

    def cargar_datos(
        self, cifrado: str, longitud_original: str | int,
        p: str | int, q: str | int, e: str | int,
    ) -> None:
        """Carga C, L y los parámetros, conservando los ceros iniciales."""
        self.texto_cifrado.delete("1.0", "end")
        self.texto_cifrado.insert("1.0", cifrado)
        self.texto_cifrado.edit_modified(False)
        for nombre, valor in (
            ("longitud_original", longitud_original), ("p", p), ("q", q), ("e", e)
        ):
            self.variables[nombre].set(str(valor))
        self._entrada_cambiada()

    def mostrar_resultado(self, resultado: ResultadoDesencriptacion) -> None:
        """Mantiene el mensaje real separado de la visualización de sus espacios."""
        self._mensaje_original = resultado.mensaje_original
        self.salidas["d"].set(str(resultado.parametros.d))
        self.salidas["mensaje_visible"].set(resultado.mensaje_original.replace(" ", "·"))
        self.longitud_recuperada.set(f"Caracteres recuperados: {len(resultado.mensaje_original)}")
        self._poner_resultado(resultado.mensaje_original)
        self.aviso_copia.set("")
        self.boton_copiar_mensaje.state(["!disabled"])

    def limpiar_resultados(self) -> None:
        """Borra las salidas al editar datos o recibir una validación fallida."""
        self._mensaje_original = ""
        for variable in self.salidas.values():
            variable.set("")
        self.longitud_recuperada.set("")
        self.aviso_copia.set("")
        self._poner_resultado("")
        self.boton_copiar_mensaje.state(["disabled"])

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
        if self.texto_cifrado.edit_modified():
            self.texto_cifrado.edit_modified(False)
            self._entrada_cambiada()

    def _copiar_mensaje(self) -> None:
        try:
            self.clipboard_clear()
            self.clipboard_append(self._mensaje_original)
        except tk.TclError:
            messagebox.showerror("Portapapeles", "No se pudo copiar el mensaje.", parent=self)
        else:
            self.aviso_copia.set("Mensaje exacto copiado.")
