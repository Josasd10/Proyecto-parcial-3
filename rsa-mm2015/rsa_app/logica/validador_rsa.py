"""Validaciones de las entradas y del texto recuperado."""

import re

from rsa_app.errores import ErrorValidacion
from rsa_app.logica.aritmetica_modular import AritmeticaModular
from rsa_app.modelos.parametros_rsa import ParametrosRSA


class ValidadorRSA:
    """Comprueba los datos utilizados en ambas operaciones RSA."""

    @staticmethod
    def convertir_entero(valor: str | int, nombre: str) -> int:
        """Convierte una entrada de la interfaz a un entero."""
        if type(valor) is int:
            return valor

        if type(valor) is not str:
            raise ErrorValidacion(f"{nombre} debe ser un número entero.")

        texto = valor.strip()

        if re.fullmatch(r"[+-]?[0-9]+", texto) is None:
            raise ErrorValidacion(f"{nombre} debe ser un número entero.")

        try:
            return int(texto)
        except ValueError:
            raise ErrorValidacion(
                f"{nombre} no se pudo convertir a entero."
            ) from None

    @staticmethod
    def validar_parametros(
        p: str | int,
        q: str | int,
        e: str | int
    ) -> ParametrosRSA:
        """Valida las entradas RSA y devuelve sus valores calculados."""
        p = ValidadorRSA.convertir_entero(p, "p")
        q = ValidadorRSA.convertir_entero(q, "q")
        e = ValidadorRSA.convertir_entero(e, "e")

        if p < 2 or q < 2:
            raise ErrorValidacion(
                "p y q deben ser números primos mayores o iguales a 2."
            )

        if p == q:
            raise ErrorValidacion("p y q deben ser distintos.")

        n = p * q

        if not 126126 < n < 1000000:
            raise ErrorValidacion(
                "El producto n = p × q debe ser mayor que "
                "126126 y menor que 1000000."
            )

        if not AritmeticaModular.es_primo(p):
            raise ErrorValidacion("p debe ser un número primo.")

        if not AritmeticaModular.es_primo(q):
            raise ErrorValidacion("q debe ser un número primo.")

        phi = (p - 1) * (q - 1)

        if e <= 1:
            raise ErrorValidacion("e debe ser mayor que 1.")

        if AritmeticaModular.mcd_euclides(e, phi) != 1:
            raise ErrorValidacion(
                "e y phi deben ser coprimos: su MCD debe ser 1."
            )

        return ParametrosRSA(
            p=p,
            q=q,
            e=e,
            n=n,
            phi=phi
        )

    @staticmethod
    def validar_mensaje(mensaje: str) -> None:
        """Comprueba que todos los caracteres sean ASCII imprimibles."""
        if type(mensaje) is not str:
            raise ErrorValidacion("El mensaje debe ser texto.")

        for posicion, caracter in enumerate(mensaje, start=1):
            codigo = ord(caracter)

            if not 32 <= codigo <= 126:
                raise ErrorValidacion(
                    f"El carácter {caracter!r} en la posición "
                    f"{posicion} no está permitido. "
                    "Solo se admiten caracteres ASCII del 32 al 126."
                )

    @staticmethod
    def validar_cifrado(cifrado: str, n: int) -> list[int]:
        """Valida el formato del cifrado y devuelve sus bloques enteros."""
        if type(cifrado) is not str:
            raise ErrorValidacion("El cifrado debe ser texto.")

        # El texto vacío se representará con C vacío y L igual a cero.
        if cifrado == "":
            return []

        bloques = cifrado.split(" ")
        valores = []

        for posicion, bloque in enumerate(bloques, start=1):
            if re.fullmatch(r"[0-9]{6}", bloque) is None:
                raise ErrorValidacion(
                    f"El bloque {posicion} debe contener exactamente "
                    "seis dígitos del 0 al 9. Separa los bloques "
                    "con un único espacio, sin espacios al inicio "
                    "ni al final."
                )

            valor = int(bloque)

            if not 0 <= valor < n:
                raise ErrorValidacion(
                    f"El bloque {posicion} debe ser menor que n = {n}."
                )

            valores.append(valor)

        return valores

    @staticmethod
    def validar_longitud(
        longitud: str | int,
        cantidad_bloques: int
    ) -> int:
        """Comprueba la coherencia entre L y la cantidad de bloques."""
        longitud = ValidadorRSA.convertir_entero(longitud, "L")

        if cantidad_bloques == 0:
            if longitud != 0:
                raise ErrorValidacion(
                    "Si el cifrado está vacío, L debe ser cero."
                )

            return longitud

        longitud_par = 2 * cantidad_bloques
        longitud_impar = longitud_par - 1

        if longitud not in (longitud_par, longitud_impar):
            raise ErrorValidacion(
                f"Para {cantidad_bloques} bloques, L debe ser "
                f"{longitud_impar} o {longitud_par}."
            )

        return longitud

    @staticmethod
    def validar_texto_recuperado(
        texto: str,
        longitud_original: int
    ) -> None:
        """Valida el texto completo antes de retirar el relleno."""
        ValidadorRSA.validar_mensaje(texto)

        longitud_esperada = longitud_original

        if longitud_original % 2 != 0:
            longitud_esperada += 1

        if len(texto) != longitud_esperada:
            raise ErrorValidacion(
                "La cantidad de caracteres recuperados "
                "no coincide con la longitud indicada."
            )

        if longitud_original % 2 != 0:
            if not texto.endswith(" "):
                raise ErrorValidacion(
                    "Como L es impar, el último carácter recuperado "
                    "debe ser un espacio de relleno."
                )