"""Punto de entrada de la aplicación gráfica RSA."""

from rsa_app.controladores.controlador_rsa import ControladorRSA
from rsa_app.interfaz.aplicacion_rsa import AplicacionRSA


def main() -> None:
    """Crea la ventana, conecta el controlador e inicia el bucle de eventos."""
    aplicacion = AplicacionRSA()
    controlador = ControladorRSA(
        mostrar_encriptacion=aplicacion.mostrar_encriptacion,
        mostrar_desencriptacion=aplicacion.mostrar_desencriptacion,
        mostrar_error=aplicacion.mostrar_error,
    )
    aplicacion.conectar_controlador(controlador)
    aplicacion.mainloop()


if __name__ == "__main__":
    main()
