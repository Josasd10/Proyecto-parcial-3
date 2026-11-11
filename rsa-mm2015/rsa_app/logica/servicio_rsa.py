"""Operaciones completas de encriptación y desencriptación RSA."""

from rsa_app.logica.aritmetica_modular import AritmeticaModular
from rsa_app.logica.codificador_ascii import CodificadorASCII
from rsa_app.logica.validador_rsa import ValidadorRSA
from rsa_app.modelos.bloque_rsa import BloqueRSA
from rsa_app.modelos.resultado_desencriptacion import (
    ResultadoDesencriptacion
)
from rsa_app.modelos.resultado_encriptacion import (
    ResultadoEncriptacion
)


class ServicioRSA:
    """Coordina la lógica RSA sin depender de la interfaz gráfica."""

    @staticmethod
    def encriptar(
        mensaje: str,
        p: str | int,
        q: str | int,
        e: str | int
    ) -> ResultadoEncriptacion:
        """Encripta un mensaje y conserva el detalle del proceso."""
        parametros = ValidadorRSA.validar_parametros(p, q, e)

        (
            mensaje_con_relleno,
            longitud_original,
            tiene_relleno
        ) = CodificadorASCII.preparar_mensaje(mensaje)

        bloques_texto = CodificadorASCII.texto_a_bloques(
            mensaje_con_relleno
        )

        bloques = []
        valores_cifrados = []

        for posicion, datos in enumerate(bloques_texto, start=1):
            pareja, codigos_ascii, valor_original = datos

            valor_cifrado = AritmeticaModular.exponenciacion_modular(
                valor_original,
                parametros.e,
                parametros.n
            )

            bloques.append(
                BloqueRSA(
                    posicion=posicion,
                    caracteres=pareja,
                    codigos_ascii=codigos_ascii,
                    valor_original=valor_original,
                    valor_cifrado=valor_cifrado
                )
            )

            valores_cifrados.append(valor_cifrado)

        cifrado = CodificadorASCII.formatear_cifrado(
            valores_cifrados
        )

        return ResultadoEncriptacion(
            mensaje_original=mensaje,
            mensaje_con_relleno=mensaje_con_relleno,
            cifrado=cifrado,
            longitud_original=longitud_original,
            tiene_relleno=tiene_relleno,
            parametros=parametros,
            bloques=bloques
        )

    @staticmethod
    def desencriptar(
        cifrado: str,
        longitud_original: str | int,
        p: str | int,
        q: str | int,
        e: str | int
    ) -> ResultadoDesencriptacion:
        """Desencripta los bloques y recupera el mensaje exacto."""
        parametros = ValidadorRSA.validar_parametros(p, q, e)

        valores_cifrados = ValidadorRSA.validar_cifrado(
            cifrado,
            parametros.n
        )

        longitud_original = ValidadorRSA.validar_longitud(
            longitud_original,
            len(valores_cifrados)
        )

        d = AritmeticaModular.inverso_modular(
            parametros.e,
            parametros.phi
        )

        parametros.d = d

        bloques = []
        parejas_recuperadas = []

        for posicion, valor_cifrado in enumerate(
            valores_cifrados,
            start=1
        ):
            valor_original = AritmeticaModular.exponenciacion_modular(
                valor_cifrado,
                d,
                parametros.n
            )

            pareja, codigos_ascii = CodificadorASCII.bloque_a_texto(
                valor_original
            )

            bloques.append(
                BloqueRSA(
                    posicion=posicion,
                    caracteres=pareja,
                    codigos_ascii=codigos_ascii,
                    valor_original=valor_original,
                    valor_cifrado=valor_cifrado
                )
            )

            parejas_recuperadas.append(pareja)

        mensaje_con_relleno = "".join(parejas_recuperadas)

        mensaje_original = CodificadorASCII.retirar_relleno(
            mensaje_con_relleno,
            longitud_original
        )

        return ResultadoDesencriptacion(
            cifrado=cifrado,
            mensaje_con_relleno=mensaje_con_relleno,
            mensaje_original=mensaje_original,
            longitud_original=longitud_original,
            tiene_relleno=longitud_original % 2 != 0,
            parametros=parametros,
            bloques=bloques
        )