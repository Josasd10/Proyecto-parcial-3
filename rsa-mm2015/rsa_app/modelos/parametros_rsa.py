"""Datos utilizados por las operaciones RSA."""

from dataclasses import dataclass


@dataclass
class ParametrosRSA:
    """Conserva las entradas RSA y sus valores calculados."""

    p: int
    q: int
    e: int
    n: int
    phi: int
    d: int | None = None