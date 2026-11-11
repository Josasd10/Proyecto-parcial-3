"""Conversión entre texto y bloques numéricos para RSA."""

from rsa_app.errores import ErrorValidacion
from rsa_app.logica.validador_rsa import ValidadorRSA


class CodificadorASCII:
    """Convierte parejas de caracteres a números y viceversa."""

    @staticmethod
    def preparar_mensaje(mensaje: str) -> tuple[str, int, bool]:
        """Conserva la longitud original y agrega relleno si hace falta."""
        ValidadorRSA.validar_mensaje(mensaje)

        longitud_original = len(mensaje)
        tiene_relleno = longitud_original % 2 != 0

        if tiene_relleno:
            mensaje = mensaje + " "

        return mensaje, longitud_original, tiene_relleno

    @staticmethod
    def texto_a_bloques(
        mensaje: str
    ) -> list[tuple[str, tuple[int, int], int]]:
        """Convierte un texto de longitud par a bloques de dos caracteres."""
        ValidadorRSA.validar_mensaje(mensaje)

        if len(mensaje) % 2 != 0:
            raise ErrorValidacion(
                "El mensaje debe tener longitud par antes de formar bloques."
            )

        bloques = []

        for posicion in range(0, len(mensaje), 2):
            pareja = mensaje[posicion:posicion + 2]

            codigo_1 = ord(pareja[0])
            codigo_2 = ord(pareja[1])

            representacion = f"{codigo_1:03d}{codigo_2:03d}"
            valor = int(representacion)

            bloques.append(
                (pareja, (codigo_1, codigo_2), valor)
            )

        return bloques

    @staticmethod
    def bloque_a_texto(
        valor: int
    ) -> tuple[str, tuple[int, int]]:
        """Recupera los dos caracteres representados por un bloque."""
        if type(valor) is not int:
            raise ErrorValidacion(
                "El bloque recuperado debe ser un número entero."
            )

        if not 0 <= valor <= 999999:
            raise ErrorValidacion(
                "El bloque recuperado no se puede representar "
                "con seis dígitos."
            )

        representacion = f"{valor:06d}"

        codigo_1 = int(representacion[:3])
        codigo_2 = int(representacion[3:])

        if not (32 <= codigo_1 <= 126 and 32 <= codigo_2 <= 126):
            raise ErrorValidacion(
                f"El bloque {representacion} produce códigos ASCII "
                "fuera del rango permitido. Revisa el cifrado "
                "y los parámetros RSA."
            )

        pareja = chr(codigo_1) + chr(codigo_2)

        return pareja, (codigo_1, codigo_2)

    @staticmethod
    def retirar_relleno(
        mensaje: str,
        longitud_original: int
    ) -> str:
        """Retira únicamente el espacio añadido cuando L es impar."""
        if type(longitud_original) is not int:
            raise ErrorValidacion(
                "La longitud original debe ser un número entero."
            )

        if longitud_original < 0:
            raise ErrorValidacion(
                "La longitud original no puede ser negativa."
            )

        ValidadorRSA.validar_texto_recuperado(
            mensaje,
            longitud_original
        )

        if longitud_original % 2 != 0:
            return mensaje[:-1]

        return mensaje

    @staticmethod
    def formatear_cifrado(bloques: list[int]) -> str:
        """Representa cada bloque con seis dígitos separados por espacios."""
        bloques_formateados = []

        for valor in bloques:
            if type(valor) is not int:
                raise ErrorValidacion(
                    "Los bloques cifrados deben ser números enteros."
                )

            if not 0 <= valor <= 999999:
                raise ErrorValidacion(
                    "Cada bloque cifrado debe poder representarse "
                    "con seis dígitos."
                )

            bloques_formateados.append(f"{valor:06d}")

        return " ".join(bloques_formateados)