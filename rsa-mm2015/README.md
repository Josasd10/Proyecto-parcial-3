# Proyecto de criptografía RSA - MM2015

Programa en Python con interfaz gráfica Tkinter para encriptar y desencriptar
mensajes mediante RSA. Muestra los resultados y el procedimiento por bloques,
y conserva exactamente los espacios del mensaje original.

## Autores

- Jose Schumann
- Kevin Moreno

## Requisitos e instalación

- Python 3.10 o posterior con soporte Tcl/Tk.
- Versión de Python utilizada en las comprobaciones: **3.12.14**.
- Solo se utiliza la biblioteca estándar (`tkinter`, `tkinter.ttk`, `dataclasses`,
  `typing` y `re`). No se necesitan paquetes de pip; `requirements.txt` lo indica.

En Windows, abrir una terminal en la carpeta `rsa-mm2015` del repositorio y comprobar:

```powershell
python --version
python -m tkinter
```

El segundo comando abre una pequeña ventana de prueba. Si Python no incluye
Tkinter, reparar su instalación activando el componente Tcl/Tk. Tkinter no se
instala con `pip install tkinter`.

## Ejecución

Desde la carpeta `rsa-mm2015`:

```powershell
python main.py
```

Si se usa el lanzador de Python de Windows, puede sustituirse `python` por `py`.
En VS Code, seleccionar el intérprete de Python que tiene Tkinter y abrir una
terminal en esta carpeta. Ejecutar `main.py`, que conecta la ventana con el
controlador y comienza el bucle de eventos.

## Uso de la aplicación

La ventana contiene tres pestañas: **Encriptación**, **Desencriptación** y
**Detalle del proceso**. El botón **Cargar ejemplo del PDF** completa las entradas
del caso de referencia; los cálculos se realizan al pulsar Encriptar o Desencriptar.

### Encriptación

1. Escribir el mensaje M y los enteros p, q y e.
2. Pulsar **Encriptar**.
3. Consultar el cifrado **C**, la longitud original **L** y la llave pública **(e, n)**.
4. Usar los botones **Copiar C** y **Copiar L** para conservar ambos datos por separado.
5. Pulsar **Ver detalle del proceso** para consultar parámetros, caracteres y bloques.

Se aceptan únicamente caracteres ASCII imprimibles del 32 al 126: letras sin
tildes, números, signos y espacios. Las tildes, la ñ, las tabulaciones y los saltos
de línea se rechazan con un mensaje de validación. El programa no los reemplaza
ni elimina automáticamente.

Cada carácter ocupa tres dígitos ASCII; cada pareja forma un bloque de seis
dígitos. Si L es impar se agrega exactamente un espacio de relleno. Cada bloque
cifrado se muestra con seis dígitos, incluidos sus ceros iniciales, y los bloques
se separan con un único espacio. L se muestra por separado y no forma parte de C.

### Desencriptación

1. Ingresar C, L y los mismos valores p, q y e usados para encriptar.
2. También se puede pulsar **Pasar C y L a desencriptación** después de una
   encriptación válida; se transfieren C, L y los tres parámetros.
3. Pulsar **Desencriptar**.
4. Consultar el exponente privado **d** y el mensaje recuperado.
5. El resultado exacto se conserva en su campo. Una vista adicional representa
   cada espacio con `·` y muestra la longitud para hacer visibles los espacios
   originales. **Copiar mensaje** copia el texto real, con espacios, sin esos símbolos.
6. Consultar **Detalle del proceso** para ver los bloques cifrados de entrada y
   los bloques ASCII recuperados de salida.

Si L es impar, la lógica comprueba y retira solo el último espacio de relleno.
Si L es par, no retira caracteres. Los espacios originales del principio, del
final y entre palabras se conservan. No se aplica `strip()` ni `rstrip()` al mensaje.
El texto vacío se maneja, por convención de esta implementación, con C vacío y L = 0.

### Detalle del proceso y errores

En ambas operaciones se muestran p, q, e, n, phi, L, la presencia de relleno,
los textos exactos y con espacios visibles, los códigos ASCII de tres dígitos y
los bloques de entrada/salida con seis dígitos. En desencriptación también aparece d.
La última fila identifica el espacio de relleno cuando existe.

Las entradas inválidas producen una explicación en la ventana sin cerrar la
aplicación. Al modificar las entradas o recibir un error, se limpian las salidas
afectadas y el detalle anterior para evitar confundirlos con resultados nuevos.

## Ejemplo completo del enunciado

Las comillas de esta tabla delimitan los textos y no forman parte del mensaje.

| Dato | Valor |
| --- | --- |
| Mensaje M | `"RSA"` |
| p, q, e | `367`, `373`, `17` |
| n = p × q | `136891` |
| phi = (p - 1)(q - 1) | `136152` |
| MCD(e, phi) | `1` |
| Longitud original L | `3` |
| Texto con relleno | `"RSA "` (vista visible: `RSA·`) |
| Bloques originales | `082083 065032` |
| Cifrado C | `026054 123875` |
| Llave pública (e, n) | `(17, 136891)` |
| Exponente privado d | `8009` |
| Llave privada (d, n) | `(8009, 136891)` |
| Mensaje recuperado | `"RSA"` |

Para desencriptar, ingresar C = `026054 123875`, L = `3`, p = `367`, q = `373`
y e = `17`. La primera pareja `RS` se representa como `082083`; la segunda
pareja es `A` más un espacio de relleno, representada como `065032`.

Ejemplo adicional de conservación de espacios: el mensaje `" A "` tiene L = 3.
La vista visible del resultado debe ser `·A·`, y el texto copiado debe contener
un espacio antes de A y otro después.

Para demostrar un error, cambiar q a `367` y ejecutar la operación: debe indicar
que p y q deben ser distintos, sin presentar una salida correcta ni cerrar la ventana.

## Estructura y conexión con el controlador

Los archivos de interfaz ya tienen estos nombres en el repositorio:

| Archivo | Clase o función | Responsabilidad |
| --- | --- | --- |
| `main.py` | `main()` | Crea la ventana y el controlador; los conecta e inicia `mainloop`. |
| `rsa_app/interfaz/aplicacion_rsa.py` | `AplicacionRSA` | Organiza las pestañas y conecta eventos/resultados. |
| `rsa_app/interfaz/panel_encriptacion.py` | `PanelEncriptacion` | Entradas de encriptación y resultados C, L y llave pública. |
| `rsa_app/interfaz/panel_desencriptacion.py` | `PanelDesencriptacion` | Entradas de desencriptación, d y texto exacto recuperado. |
| `rsa_app/interfaz/panel_detalle.py` | `PanelDetalle` | Parámetros, ASCII, relleno y tabla de bloques. |
| `rsa_app/controladores/controlador_rsa.py` | `ControladorRSA` | Llama al servicio y comunica resultados o errores. |
| `rsa_app/logica/servicio_rsa.py` | `ServicioRSA` | Coordina las operaciones RSA. |

`main.py` proporciona al controlador las funciones `mostrar_encriptacion`,
`mostrar_desencriptacion` y `mostrar_error` de la ventana. Los formularios
entregan sus entradas como texto mediante `obtener_datos()`. La interfaz no
implementa de nuevo la lógica matemática ni cambia las validaciones existentes.

## Algoritmos matemáticos

Se encuentran en `rsa_app/logica/aritmetica_modular.py`, clase `AritmeticaModular`:

- `es_primo`: comprueba divisibilidad hasta la raíz cuadrada, usando
  `divisor * divisor <= numero`.
- `mcd_euclides`: calcula el MCD mediante divisiones y residuos sucesivos.
- `bezout_matricial`: obtiene los coeficientes de Bézout con actualizaciones de
  una matriz; `inverso_modular` usa el coeficiente correspondiente para obtener d.
- `exponenciacion_modular`: aplica cuadrados sucesivos y reduce módulo n durante
  el cálculo para evitar construir la potencia completa.

Estos algoritmos propios no se sustituyen por `math.gcd`, `pow` con módulo,
`pow` para inversos ni bibliotecas criptográficas. Las conversiones ASCII se
realizan en `rsa_app/logica/codificador_ascii.py` con `ord`, `chr` y formato de texto.

`rsa_app/logica/validador_rsa.py` comprueba p y q primos distintos,
`126126 < n < 1000000`, e entero mayor que 1 y coprimo con phi. No exige que e
sea primo ni menor que phi. También valida ASCII, formato y rango de C,
coherencia de L y espacio final de relleno.

## Comprobaciones

Para ejecutar las comprobaciones de la lógica y del controlador que ya incluye
el repositorio:

```powershell
python verificar_rsa.py
```

Cubren la recuperación exacta de mensajes pares/impares, letras, números,
signos, espacios consecutivos, al principio y al final, texto vacío, el ejemplo
del enunciado y sus ceros iniciales. Comprueban el rechazo de primos iguales,
exponentes no coprimos, caracteres no admitidos, bloques mal formados o fuera
de rango y longitudes inconsistentes. También verifican callbacks del controlador.

Para la interfaz, verificar el recorrido Encriptar → pasar C y L → Desencriptar,
el portapapeles, el detalle de ambas operaciones, los mensajes de validación y
la limpieza de resultados al editar datos. Repetir el ejemplo y `" A "` para
comprobar que los espacios visibles y el texto copiado coinciden.

En esta versión se ejecutaron las comprobaciones anteriores de lógica y
controlador y una prueba de integración con widgets reales de Tkinter
(Python 3.12.14, Tcl/Tk 8.6.12). La integración comprobó el ejemplo del PDF,
diez mensajes (incluidos espacios, mensaje vacío y texto largo), doce entradas
inválidas, el detalle en ambas direcciones y la limpieza de salidas al editar.
También comprobó exponentes válidos compuestos o mayores que phi y el contenido
exacto enviado por los botones de copia, con el acceso al portapapeles sustituido
durante la prueba. Todas esas comprobaciones finalizaron correctamente.

## Video demostrativo: 
