"""Conexión entre la interfaz gráfica y el servicio RSA."""

from typing import Callable

from rsa_app.errores import ErrorValidacion
from rsa_app.logica.servicio_rsa import ServicioRSA
from rsa_app.modelos.resultado_desencriptacion import (
    ResultadoDesencriptacion
)
from rsa_app.modelos.resultado_encriptacion import (
    ResultadoEncriptacion
)


class ControladorRSA:
    """Procesa las solicitudes de la interfaz y comunica sus resultados."""

    def __init__(
        self,
        mostrar_encriptacion: Callable[
            [ResultadoEncriptacion], None
        ],
        mostrar_desencriptacion: Callable[
            [ResultadoDesencriptacion], None
        ],
        mostrar_error: Callable[[str], None]
    ) -> None:
        """Recibe las funciones de la interfaz que mostrarán las salidas."""
        self.mostrar_encriptacion = mostrar_encriptacion
        self.mostrar_desencriptacion = mostrar_desencriptacion
        self.mostrar_error = mostrar_error

    def encriptar(
        self,
        mensaje: str,
        p: str | int,
        q: str | int,
        e: str | int
    ) -> None:
        """Solicita la encriptación y comunica el resultado o la validación."""
        try:
            resultado = ServicioRSA.encriptar(
                mensaje=mensaje,
                p=p,
                q=q,
                e=e
            )
        except ErrorValidacion as error:
            self.mostrar_error(str(error))
            return

        self.mostrar_encriptacion(resultado)

    def desencriptar(
        self,
        cifrado: str,
        longitud_original: str | int,
        p: str | int,
        q: str | int,
        e: str | int
    ) -> None:
        """Solicita la desencriptación y comunica su resultado o validación."""
        try:
            resultado = ServicioRSA.desencriptar(
                cifrado=cifrado,
                longitud_original=longitud_original,
                p=p,
                q=q,
                e=e
            )
        except ErrorValidacion as error:
            self.mostrar_error(str(error))
            return

        self.mostrar_desencriptacion(resultado)
        