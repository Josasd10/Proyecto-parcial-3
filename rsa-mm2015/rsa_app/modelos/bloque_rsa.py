"""Información de un bloque durante el proceso RSA."""

from dataclasses import dataclass


@dataclass
class BloqueRSA:
    """Conserva la representación de una pareja de caracteres."""

    posicion: int
    caracteres: str
    codigos_ascii: tuple[int, int]
    valor_original: int
    valor_cifrado: int