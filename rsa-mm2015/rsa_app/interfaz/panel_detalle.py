"""Presentación de los datos y de los bloques calculados por el servicio RSA."""

import tkinter as tk
from tkinter import ttk

from rsa_app.modelos.resultado_desencriptacion import ResultadoDesencriptacion
from rsa_app.modelos.resultado_encriptacion import ResultadoEncriptacion


class PanelDetalle(ttk.Frame):
    """Muestra una operación sin repetir los cálculos de la capa matemática."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=12)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        self.titulo = tk.StringVar(value="Detalle del proceso")
        ttk.Label(self, textvariable=self.titulo, font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )

        self.resumen = tk.StringVar()
        etiqueta_resumen = ttk.Label(self, textvariable=self.resumen, justify="left")
        etiqueta_resumen.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        etiqueta_resumen.bind(
            "<Configure>",
            lambda evento: etiqueta_resumen.configure(wraplength=max(100, evento.width)),
        )

        marco_mensajes = ttk.Frame(self)
        marco_mensajes.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        marco_mensajes.columnconfigure(0, weight=1)
        self.texto_mensajes = tk.Text(
            marco_mensajes, height=3, width=40, wrap="none", state="disabled",
            font=("Consolas", 10), takefocus=True,
        )
        self.texto_mensajes.grid(row=0, column=0, sticky="ew")
        desplazamiento_texto = ttk.Scrollbar(
            marco_mensajes, orient="horizontal", command=self.texto_mensajes.xview
        )
        desplazamiento_texto.grid(row=1, column=0, sticky="ew")
        self.texto_mensajes.configure(xscrollcommand=desplazamiento_texto.set)

        marco_tabla = ttk.Frame(self)
        marco_tabla.grid(row=3, column=0, sticky="nsew")
        marco_tabla.columnconfigure(0, weight=1)
        marco_tabla.rowconfigure(0, weight=1)
        columnas = ("posicion", "pareja", "ascii1", "ascii2", "entrada", "salida", "relleno")
        self.tabla = ttk.Treeview(
            marco_tabla, columns=columnas, show="headings", height=7
        )
        for columna, titulo, ancho in (
            ("posicion", "Bloque", 65),
            ("pareja", "Pareja (· = espacio)", 155),
            ("ascii1", "ASCII 1", 80),
            ("ascii2", "ASCII 2", 80),
            ("entrada", "Entrada", 140),
            ("salida", "Salida", 140),
            ("relleno", "Relleno", 120),
        ):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, minwidth=ancho, anchor="center")
        self.tabla.grid(row=0, column=0, sticky="nsew")
        vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal = ttk.Scrollbar(
            marco_tabla, orient="horizontal", command=self.tabla.xview
        )
        horizontal.grid(row=1, column=0, sticky="ew")
        self.tabla.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)

        self.leyenda = tk.StringVar()
        etiqueta_leyenda = ttk.Label(self, textvariable=self.leyenda, justify="left")
        etiqueta_leyenda.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        etiqueta_leyenda.bind(
            "<Configure>",
            lambda evento: etiqueta_leyenda.configure(wraplength=max(100, evento.width)),
        )
        self.limpiar()

    def mostrar_encriptacion(self, resultado: ResultadoEncriptacion) -> None:
        """Presenta m -> c, incluidos los ceros iniciales de ambos bloques."""
        self._mostrar(resultado, desencriptacion=False)

    def mostrar_desencriptacion(self, resultado: ResultadoDesencriptacion) -> None:
        """Presenta c -> m, el exponente privado y el texto recuperado."""
        self._mostrar(resultado, desencriptacion=True)

    def _mostrar(
        self,
        resultado: ResultadoEncriptacion | ResultadoDesencriptacion,
        desencriptacion: bool,
    ) -> None:
        self.limpiar()
        parametros = resultado.parametros
        operacion = "Desencriptación" if desencriptacion else "Encriptación"
        self.titulo.set(f"Detalle de {operacion.lower()}")
        relleno = "Sí, un espacio al final" if resultado.tiene_relleno else "No"
        lineas = [
            f"p = {parametros.p}    q = {parametros.q}    e = {parametros.e}",
            f"n = {parametros.n}    phi = {parametros.phi}    "
            f"L = {resultado.longitud_original}    Relleno: {relleno}",
        ]
        if desencriptacion:
            lineas.append(f"d = {parametros.d}    Llave privada: ({parametros.d}, {parametros.n})")
        if not resultado.bloques:
            lineas.append("Mensaje vacío: C vacío, L = 0 y ningún bloque.")
        self.resumen.set("\n".join(lineas))

        nombre_mensaje = "Mensaje recuperado" if desencriptacion else "Mensaje original"
        original = resultado.mensaje_original
        con_relleno = resultado.mensaje_con_relleno
        self._poner_mensajes(
            f"{nombre_mensaje}: {original!r}\n"
            f"Espacios visibles: |{original.replace(' ', '·')}|\n"
            f"Texto de los bloques (con posible relleno): |{con_relleno.replace(' ', '·')}|"
        )
        self.tabla.heading("entrada", text="c (entrada)" if desencriptacion else "m (entrada)")
        self.tabla.heading("salida", text="m (recuperado)" if desencriptacion else "c (cifrado)")

        for indice, bloque in enumerate(resultado.bloques):
            entrada, salida = (
                (bloque.valor_cifrado, bloque.valor_original)
                if desencriptacion
                else (bloque.valor_original, bloque.valor_cifrado)
            )
            ultimo_con_relleno = resultado.tiene_relleno and indice == len(resultado.bloques) - 1
            self.tabla.insert(
                "", "end",
                values=(
                    bloque.posicion,
                    bloque.caracteres.replace(" ", "·"),
                    f"{bloque.codigos_ascii[0]:03d}",
                    f"{bloque.codigos_ascii[1]:03d}",
                    f"{entrada:06d}",
                    f"{salida:06d}",
                    "2.º carácter" if ultimo_con_relleno else "No",
                ),
            )
        self.leyenda.set(
            "Cada fila representa dos caracteres; ASCII 1 y ASCII 2 muestran sus códigos de tres dígitos. "
            "El símbolo · hace visibles todos los espacios. Solo el segundo carácter de la última fila "
            "marcada como relleno es el espacio añadido; los demás pertenecen al mensaje original. "
            "Las comillas y las barras de la vista superior son delimitadores de presentación."
        )

    def _poner_mensajes(self, texto: str) -> None:
        self.texto_mensajes.configure(state="normal")
        self.texto_mensajes.delete("1.0", "end")
        self.texto_mensajes.insert("1.0", texto)
        self.texto_mensajes.configure(state="disabled")
        self.texto_mensajes.xview_moveto(0)

    def limpiar(self) -> None:
        """Retira datos anteriores para no asociarlos con entradas nuevas."""
        self.titulo.set("Detalle del proceso")
        self.resumen.set("Ejecuta una operación para consultar sus parámetros y bloques.")
        self._poner_mensajes("")
        filas = self.tabla.get_children()
        if filas:
            self.tabla.delete(*filas)
        self.tabla.heading("entrada", text="Entrada")
        self.tabla.heading("salida", text="Salida")
        self.leyenda.set("Los bloques se muestran con seis dígitos, conservando los ceros iniciales.")
