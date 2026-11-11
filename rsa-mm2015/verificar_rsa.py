"""Comprobación integrada de la lógica RSA."""

from rsa_app.errores import ErrorValidacion
from rsa_app.logica.servicio_rsa import ServicioRSA


def verificar_recuperacion() -> None:
    """Comprueba mensajes y la conservación exacta de sus espacios."""
    mensajes = [
        "RSA",
        "AB",
        "Hola Mundo",
        "Numeros 123 y signos !?",
        "  Inicio",
        "Final  ",
        "Dos  espacios",
        " A ",
        "   ",
        ""
    ]

    for mensaje in mensajes:
        encriptacion = ServicioRSA.encriptar(
            mensaje, 367, 373, 17
        )

        desencriptacion = ServicioRSA.desencriptar(
            encriptacion.cifrado,
            encriptacion.longitud_original,
            367,
            373,
            17
        )

        assert desencriptacion.mensaje_original == mensaje, (
            f"No se recuperó exactamente el mensaje: {mensaje!r}"
        )

    print("Recuperación exacta: correcta.")


def verificar_ejemplo_referencia() -> None:
    """Comprueba los resultados proporcionados en el enunciado."""
    encriptacion = ServicioRSA.encriptar("RSA", 367, 373, 17)

    assert encriptacion.parametros.n == 136891
    assert encriptacion.parametros.phi == 136152
    assert encriptacion.longitud_original == 3
    assert encriptacion.mensaje_con_relleno == "RSA "
    assert encriptacion.cifrado == "026054 123875"

    desencriptacion = ServicioRSA.desencriptar(
        encriptacion.cifrado,
        encriptacion.longitud_original,
        367,
        373,
        17
    )

    assert desencriptacion.parametros.d == 8009
    assert desencriptacion.mensaje_original == "RSA"

    print("Ejemplo del enunciado: correcto.")


def verificar_validaciones() -> None:
    """Comprueba que las operaciones rechacen entradas inválidas."""
    casos = [
        (
            "Primos iguales",
            lambda: ServicioRSA.encriptar("RSA", 367, 367, 17)
        ),
        (
            "Exponente no coprimo",
            lambda: ServicioRSA.encriptar("RSA", 367, 373, 2)
        ),
        (
            "Caracter no admitido",
            lambda: ServicioRSA.encriptar("Hola ñ", 367, 373, 17)
        ),
        (
            "Bloque mal formado",
            lambda: ServicioRSA.desencriptar(
                "26054 123875", 3, 367, 373, 17
            )
        ),
        (
            "Bloque fuera de rango",
            lambda: ServicioRSA.desencriptar(
                "999999", 2, 367, 373, 17
            )
        ),
        (
            "Longitud inconsistente",
            lambda: ServicioRSA.desencriptar(
                "026054 123875", 1, 367, 373, 17
            )
        )
    ]

    for nombre, operacion in casos:
        try:
            operacion()
        except ErrorValidacion:
            print(f"Validación correcta: {nombre}.")
        else:
            raise AssertionError(
                f"Se aceptó una entrada inválida: {nombre}."
            )

def verificar_controlador() -> None:
    """Comprueba la comunicación de resultados y errores con la interfaz."""
    from rsa_app.controladores.controlador_rsa import ControladorRSA

    encriptaciones = []
    desencriptaciones = []
    errores = []

    controlador = ControladorRSA(
        mostrar_encriptacion=encriptaciones.append,
        mostrar_desencriptacion=desencriptaciones.append,
        mostrar_error=errores.append
    )

    # Las entradas numéricas llegan como texto desde los formularios.
    controlador.encriptar("RSA", "367", "373", "17")

    assert len(encriptaciones) == 1
    assert encriptaciones[0].cifrado == "026054 123875"
    assert errores == []

    controlador.desencriptar(
        "026054 123875", "3", "367", "373", "17"
    )

    assert len(desencriptaciones) == 1
    assert desencriptaciones[0].mensaje_original == "RSA"
    assert desencriptaciones[0].parametros.d == 8009
    assert errores == []

    # Una operación inválida debe informar el error sin generar resultados.
    controlador.encriptar("RSA", "367", "367", "17")

    assert len(errores) == 1
    assert len(encriptaciones) == 1

    controlador.desencriptar(
        "026054 123875", "1", "367", "373", "17"
    )

    assert len(errores) == 2
    assert len(desencriptaciones) == 1

    print("Controlador: resultados y errores comunicados correctamente.")

if __name__ == "__main__":
    verificar_recuperacion()
    verificar_ejemplo_referencia()
    verificar_validaciones()
    verificar_controlador()

    print("Todas las comprobaciones finalizaron correctamente.")