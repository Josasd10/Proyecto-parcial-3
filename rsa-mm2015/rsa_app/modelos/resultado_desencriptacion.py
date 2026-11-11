"""Resultado completo de una desencriptación."""

from dataclasses import dataclass

from rsa_app.modelos.bloque_rsa import BloqueRSA
from rsa_app.modelos.parametros_rsa import ParametrosRSA


@dataclass
class ResultadoDesencriptacion:
    """Agrupa el mensaje recuperado y el detalle de la operación."""

    cifrado: str
    mensaje_con_relleno: str
    mensaje_original: str
    longitud_original: int
    tiene_relleno: bool
    parametros: ParametrosRSA
    bloques: list[BloqueRSA]