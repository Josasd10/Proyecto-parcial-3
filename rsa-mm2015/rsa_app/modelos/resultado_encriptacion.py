"""Resultado completo de una encriptación."""

from dataclasses import dataclass

from rsa_app.modelos.bloque_rsa import BloqueRSA
from rsa_app.modelos.parametros_rsa import ParametrosRSA


@dataclass
class ResultadoEncriptacion:
    """Agrupa el cifrado y la información necesaria para explicarlo."""

    mensaje_original: str
    mensaje_con_relleno: str
    cifrado: str
    longitud_original: int
    tiene_relleno: bool
    parametros: ParametrosRSA
    bloques: list[BloqueRSA]