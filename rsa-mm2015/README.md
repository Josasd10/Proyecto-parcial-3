# Proyecto RSA - MM2015

Estructura inicial del proyecto del Parcial 3 de Matemática Discreta 1.

**Estado:** clases vacías con `pass` y su responsabilidad documentada. No se han implementado algoritmos, validaciones ni interfaz gráfica.

## Entorno previsto

- Python 3.10 o posterior.
- Interfaz con `tkinter` de la biblioteca estándar.
- Sin dependencias externas previstas; `requirements.txt` lo deja indicado.
- Autor o autores: pendiente de completar.

## Inicio provisional

Desde esta carpeta:

```powershell
python main.py
```

Por ahora solo imprime un aviso de que la estructura está creada. La ventana se conectará al punto de entrada cuando se implemente `AplicacionRSA`.

Para comprobar que la instalación de Python incluye Tkinter:

```powershell
python -m tkinter
```

## Clases previstas

| Archivo dentro de `rsa_app/` | Clase | Responsabilidad pendiente |
| --- | --- | --- |
| `modelos/parametros_rsa.py` | `ParametrosRSA` | Representar p, q, e, n, phi y d. |
| `modelos/bloque_rsa.py` | `BloqueRSA` | Registrar pareja, ASCII y valores del bloque. |
| `modelos/resultado_encriptacion.py` | `ResultadoEncriptacion` | Conservar C, L, relleno, parámetros y pasos. |
| `modelos/resultado_desencriptacion.py` | `ResultadoDesencriptacion` | Conservar el mensaje exacto, d y los pasos. |
| `logica/aritmetica_modular.py` | `AritmeticaModular` | Implementar primalidad, MCD, inverso y exponenciación modular. |
| `logica/validador_rsa.py` | `ValidadorRSA` | Validar entradas y texto recuperado. |
| `logica/codificador_ascii.py` | `CodificadorASCII` | Convertir caracteres y parejas; agregar y retirar relleno. |
| `logica/servicio_rsa.py` | `ServicioRSA` | Coordinar encriptación y desencriptación. |
| `errores.py` | `ErrorValidacion` | Comunicar errores de entrada a la interfaz. |
| `controladores/controlador_rsa.py` | `ControladorRSA` | Conectar formularios, servicio y resultados. |
| `interfaz/aplicacion_rsa.py` | `AplicacionRSA` | Crear la ventana principal con Tkinter. |
| `interfaz/panel_encriptacion.py` | `PanelEncriptacion` | Recibir M, p, q, e y mostrar C, L y la llave pública. |
| `interfaz/panel_desencriptacion.py` | `PanelDesencriptacion` | Recibir C, L, p, q, e y mostrar d y M. |
| `interfaz/panel_detalle.py` | `PanelDetalle` | Mostrar parámetros, ASCII, relleno y bloques del proceso. |

La lógica no deberá importar componentes de la interfaz. El controlador conectará ambas partes. Las clases podrán ajustarse durante la implementación; el enunciado no exige una arquitectura específica.

## Reglas que deberá cubrir la implementación

- p y q enteros, primos distintos; `126126 < n < 1000000`.
- e entero mayor que 1 y coprimo con phi; no imponer que e sea primo ni menor que phi.
- ASCII imprimible del 32 al 126, conservando todos los espacios originales.
- Tres dígitos por carácter y dos caracteres por bloque.
- Si L es impar, agregar un único espacio de relleno.
- Cada bloque cifrado se representa con seis dígitos y los bloques se separan por espacios.
- Para k > 0 bloques, L debe ser `2*k` o `2*k - 1`; cada bloque cifrado debe ser menor que n.
- Al recuperar el texto, validar ambos códigos ASCII y el espacio de relleno cuando corresponda. Retirar únicamente ese espacio; no utilizar `strip()` ni `rstrip()` para eliminar relleno.
- Implementar los algoritmos propios: no sustituirlos por `math.gcd`, `pow` con módulo o para inversos, ni bibliotecas criptográficas. Tampoco calcular la potencia completa para reducirla al final.
- Mostrar n, phi, L, relleno, ASCII y bloques; también d al desencriptar.
- Presentar errores comprensibles sin cerrar la aplicación inesperadamente.

## Ejemplo para verificar más adelante

Datos de referencia del enunciado; todavía no se han calculado con este proyecto:

```text
M = "RSA"
p = 367
q = 373
e = 17
n = 136891
phi = 136152
L = 3
Texto con relleno = "RSA "
Bloques = 082083 065032
C = 026054 123875
d = 8009
Texto recuperado = "RSA"
```

El panel de encriptación mostrará C y L por separado. Para desencriptar se ingresarán ambos junto con p, q y e. La longitud original permitirá distinguir el relleno de los espacios del mensaje.

## Pendientes antes de entregar

- Implementar las clases y conectar `main.py` con la ventana.
- Verificar mensajes pares e impares, mayúsculas y minúsculas, números, signos, espacios consecutivos y espacios originales al inicio y al final.
- Verificar bloques cifrados con ceros iniciales.
- Verificar el rechazo de parámetros inválidos, caracteres no admitidos, cifrados mal formados o fuera de rango y longitudes inconsistentes.
- Documentar las comprobaciones realizadas y la versión concreta de Python utilizada.
- Completar autores, instrucciones definitivas y video demostrativo.

El repositorio se inicializa localmente con Git. La publicación en un servicio remoto queda pendiente.


## Lógica RSA

La lógica está implementada en Python y separada de la interfaz gráfica.

### Algoritmos matemáticos

En `rsa_app/logica/aritmetica_modular.py` se encuentran:

- `es_primo`: comprueba divisibilidad hasta la raíz cuadrada del número,
  utilizando la condición `divisor * divisor <= numero`.
- `mcd_euclides`: calcula el máximo común divisor mediante residuos sucesivos.
- `bezout_matricial`: obtiene los coeficientes de Bézout mediante
  actualizaciones de una matriz.
- `inverso_modular`: comprueba que los números sean coprimos y utiliza
  el coeficiente de Bézout para obtener el inverso.
- `exponenciacion_modular`: utiliza cuadrados sucesivos y reduce módulo n
  durante el cálculo, sin construir primero la potencia completa.

Estos algoritmos no utilizan `math.gcd`, `pow` ni bibliotecas criptográficas.

### Validación y representación del texto

`ValidadorRSA` comprueba las entradas numéricas, la primalidad de p y q,
el rango de n y que e sea mayor que 1 y coprimo con phi.

También comprueba los caracteres ASCII permitidos, el formato y rango
de los bloques cifrados y la coherencia entre L y la cantidad de bloques.

`CodificadorASCII` representa cada carácter mediante tres dígitos
y agrupa dos caracteres por bloque. Si la longitud original es impar,
agrega exactamente un espacio de relleno.

Al desencriptar se verifica ese espacio y se retira únicamente el último
carácter. Los espacios originales se conservan.

Como convención del programa, el mensaje vacío se representa con cifrado
vacío y longitud cero.

### Operaciones completas

`ServicioRSA.encriptar` devuelve un `ResultadoEncriptacion` con el cifrado,
la longitud original, los parámetros y el detalle de los bloques.

`ServicioRSA.desencriptar` calcula el exponente privado y devuelve un
`ResultadoDesencriptacion` con el mensaje recuperado y el detalle del proceso.

`ControladorRSA` recibe las entradas de la interfaz, llama al servicio
y comunica resultados o mensajes de validación mediante funciones
proporcionadas por la ventana.

### Ejemplo de referencia

- Mensaje: `"RSA"`
- p: 367
- q: 373
- e: 17
- n: 136891
- phi: 136152
- Longitud original L: 3
- Mensaje con relleno: `"RSA "`
- Bloques originales: `082083 065032`
- Cifrado C: `026054 123875`
- Exponente privado d: 8009
- Mensaje recuperado: `"RSA"`

Para desencriptar deben conservarse C y L e ingresarse junto con p, q y e.

### Comprobaciones de la lógica

Desde la carpeta `rsa-mm2015`, ejecutar:

    python verificar_rsa.py

Se comprueban la recuperación exacta de mensajes pares e impares,
mayúsculas y minúsculas, números, signos, espacios consecutivos,
espacios al inicio y al final y el mensaje vacío.

También se comprueba el ejemplo del enunciado, incluyendo los ceros
iniciales del cifrado, y el rechazo de primos iguales, exponentes
no coprimos, caracteres no admitidos, bloques mal formados,
bloques fuera de rango y longitudes inconsistentes.

La comprobación del controlador verifica que las operaciones válidas
comuniquen resultados y que las inválidas comuniquen errores.

La interfaz gráfica requiere una comprobación adicional después
de su integración.