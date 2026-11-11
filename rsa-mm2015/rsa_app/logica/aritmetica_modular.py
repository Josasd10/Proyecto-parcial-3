"""Algoritmos matemáticos propios para el proyecto RSA."""


class AritmeticaModular:
    """Agrupa los algoritmos matemáticos utilizados por RSA."""

    @staticmethod
    def es_primo(numero: int) -> bool:
        """Determina si un entero es primo."""
        if type(numero) is not int:
            raise TypeError("El número debe ser entero.")

        if numero < 2:
            return False

        divisor = 2

        while divisor * divisor <= numero:
            if numero % divisor == 0:
                return False

            divisor += 1

        return True

    @staticmethod
    def mcd_euclides(a: int, b: int) -> int:
        """Calcula el MCD de dos enteros positivos mediante Euclides."""
        for valor in (a, b):
            if type(valor) is not int:
                raise TypeError("Las entradas deben ser enteros.")

            if valor <= 0:
                raise ValueError("Las entradas deben ser positivas.")

        while b != 0:
            residuo = a % b
            a = b
            b = residuo

        return a

    @staticmethod
    def bezout_matricial(a: int, b: int) -> tuple[int, int]:
        """Devuelve coeficientes x, y tales que a*x + b*y = MCD(a, b)."""
        for valor in (a, b):
            if type(valor) is not int:
                raise TypeError("Las entradas deben ser enteros.")

            if valor <= 0:
                raise ValueError("Las entradas deben ser positivas.")

        matriz = [
            [1, 0],
            [0, 1]
        ]

        while b != 0:
            cociente = a // b

            matriz = [
                matriz[1][:],
                [
                    matriz[0][0] - cociente * matriz[1][0],
                    matriz[0][1] - cociente * matriz[1][1]
                ]
            ]

            residuo = a % b
            a = b
            b = residuo

        return matriz[0][0], matriz[0][1]

    @staticmethod
    def inverso_modular(a: int, modulo: int) -> int:
        """Obtiene el inverso de a módulo modulo mediante Bézout."""
        for valor in (a, modulo):
            if type(valor) is not int:
                raise TypeError("Las entradas deben ser enteros.")

        if a <= 0:
            raise ValueError("El número debe ser positivo.")

        if modulo < 2:
            raise ValueError("El módulo debe ser al menos 2.")

        if AritmeticaModular.mcd_euclides(a, modulo) != 1:
            raise ValueError(
                "No existe inverso modular: los números no son coprimos."
            )

        x, _ = AritmeticaModular.bezout_matricial(a, modulo)

        return x % modulo

    @staticmethod
    def exponenciacion_modular(
        base: int,
        exponente: int,
        modulo: int
    ) -> int:
        """Calcula base^exponente módulo modulo por cuadrados sucesivos."""
        for valor in (base, exponente, modulo):
            if type(valor) is not int:
                raise TypeError("Las entradas deben ser enteros.")

        if base < 0:
            raise ValueError("La base no puede ser negativa.")

        if exponente < 0:
            raise ValueError("El exponente no puede ser negativo.")

        if modulo < 2:
            raise ValueError("El módulo debe ser al menos 2.")

        resultado = 1
        base = base % modulo

        while exponente > 0:
            if exponente % 2 != 0:
                resultado = (resultado * base) % modulo

            base = (base * base) % modulo
            exponente = exponente // 2

        return resultado