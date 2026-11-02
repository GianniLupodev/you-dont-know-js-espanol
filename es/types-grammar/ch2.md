# You Don't Know JS Yet: Types & Grammar - 2nd Edition
# Capítulo 2: Comportamientos de los Primitivos

| NOTA: |
| :--- |
| Trabajo en progreso |

Hasta ahora, hemos explorado siete value types primitivos incorporados en JS: `null`, `undefined`, `boolean`, `string`, `number`, `bigint`, y `symbol`.

El Capítulo 1 tuvo bastante para asimilar, mucho más complejo de lo que apuesto que la mayoría de los lectores esperaba. Si todavía estás recuperando el aliento después de leer todo eso, ¡no te preocupes por tomarte un pequeño descanso antes de continuar aquí!

Una vez que tengas la mente despejada y estés listo para seguir, metámonos en ciertos comportamientos que los value types implican para todos sus respectivos valores. Vamos a mirar con cuidado y más de cerca todos estos diversos comportamientos.

## Inmutabilidad de los Primitivos

Todos los valores primitivos son inmutables, lo que significa que nada en un programa JS puede acceder al contenido del valor y modificarlo de ninguna manera.

```js
myAge = 42;

// later:

myAge = 43;
```

La sentencia `myAge = 43` no cambia el valor. Reasigna un valor diferente `43` a `myAge`, reemplazando completamente el valor previo de `42`.

También se crean nuevos valores a través de diversas operaciones, pero de nuevo, estas no modifican el valor original:

```js
42 + 1;             // 43

"Hello" + "!";      // "Hello!"
```

Los valores `43` y `"Hello!"` son valores nuevos, distintos de los valores previos `42` y `"Hello"`, respectivamente.

Incluso un valor string, que parece meramente un array de caracteres -- y el contenido de los arrays suele ser mutable -- es inmutable:

```js
greeting = "Hello.";

greeting[5] = "!";

console.log(greeting);      // Hello.
```

| ADVERTENCIA: |
| :--- |
| En modo no estricto, asignar a una propiedad de solo lectura (como `greeting[5] = ..`) falla silenciosamente. En modo estricto, la asignación no permitida lanzará una excepción. |

La naturaleza inmutable de los valores primitivos no se ve afectada *de ninguna manera* por cómo se declara la variable o la propiedad del objeto que contiene el valor. Por ejemplo, ya sea que se use `const`, `let`, o `var` para declarar la variable `greeting` de arriba, el valor string que contiene es inmutable.

`const` no crea valores inmutables, declara variables que no pueden ser reasignadas (es decir, asignaciones inmutables) -- consulta el título "Scope & Closures" de esta serie para más información.

Una propiedad de un objeto puede marcarse como de solo lectura -- con el atributo de descriptor `writable: false`, como se discute en el título "Objects & Classes" de esta serie. Pero eso todavía no tiene ningún efecto sobre la naturaleza del valor, solo sobre impedir la reasignación de la propiedad.

### ¿Primitivos Con Propiedades?

Adicionalmente, las propiedades *no pueden* agregarse a ningún valor primitivo:

```js
greeting = "Hello.";

greeting.isRendered = true;

greeting.isRendered;        // undefined
```

Este fragmento parece estar agregando una propiedad `isRendered` al valor en `greeting`, pero esta asignación falla silenciosamente (incluso en modo estricto).

El acceso a propiedades no está permitido de ninguna manera en los valores primitivos nulos `null` y `undefined`. Pero las propiedades *sí pueden* ser accedidas en todos los demás valores primitivos -- sí, eso suena contraintuitivo.

Por ejemplo, todos los valores string tienen una propiedad de solo lectura `length`:

```js
greeting = "Hello.";

greeting.length;            // 6
```

`length` no puede ser establecida, pero puede ser accedida, y expone el número de code-units almacenados en el valor (consulta "JS Character Encodings" en el Capítulo 1), lo que a menudo significa el número de caracteres en el string.

| NOTA: |
| :--- |
| En cierto modo. Para la mayoría de los caracteres estándar, eso es verdad; un carácter es un code-point, que es un code-unit. Sin embargo, como se explicó en el Capítulo 1, los caracteres Unicode extendidos por encima del code-point `65535` se almacenarán como dos code-units (mitades surrogate). Por lo tanto, para cada uno de esos caracteres, `length` incluirá `2` en su conteo, aunque el carácter se imprima visualmente como un solo símbolo. |

Los valores primitivos no nulos también tienen un par de métodos incorporados estándar que pueden ser accedidos:

```js
greeting = "Hello.";

greeting.toString();    // "Hello." <-- redundant
greeting.valueOf();     // "Hello."
```

Adicionalmente, la mayoría de los value types primitivos definen sus propios métodos con comportamientos específicos inherentes a ese type. Los cubriremos más adelante en este capítulo.

| NOTA: |
| :--- |
| Como ya se mencionó brevemente en el Capítulo 1, técnicamente, este tipo de accesos a propiedades/métodos en valores primitivos se facilitan mediante un comportamiento coercitivo implícito llamado *auto-boxing*. Lo cubriremos en detalle en "Automatic Objects" en el Capítulo 3. |

## Asignaciones de Primitivos

Cualquier asignación de un valor primitivo de una variable/contenedor a otra es una *copia-por-valor*:

```js
myAge = 42;

yourAge = myAge;        // assigned by value-copy

myAge;                  // 42
yourAge;                // 42
```

Aquí, las variables `myAge` y `yourAge` tienen cada una su propia copia del valor number `42`.

| NOTA: |
| :--- |
| Dentro del engine de JS, *puede* ser el caso de que solo exista un valor `42` en memoria, y que el engine apunte ambas variables `myAge` y `yourAge` al valor compartido. Dado que los valores primitivos son inmutables, no hay peligro en que un engine de JS haga eso. Pero lo importante para nosotros como desarrolladores de JS es que, en nuestros programas, `myAge` y `yourAge` actúan como si tuvieran su propia copia de ese valor, en lugar de compartirlo. |

Si más adelante reasignamos `myAge` a `43` (cuando tengo un cumpleaños), eso no afecta al `42` que sigue asignado a `yourAge`:

```js
myAge++;            // sort of like: myAge = myAge + 1

myAge;              // 43
yourAge;            // 42 <-- unchanged
```

## Comportamientos de los Strings

Los valores string tienen una serie de comportamientos específicos que todo desarrollador de JS debería conocer.

### Acceso a Caracteres del String

Aunque los strings no son realmente arrays, JS permite el acceso al estilo de array `[ .. ]` de un carácter en un índice numérico (basado en `0`):

```js
greeting = "Hello!";

greeting[4];            // "o"
```

Si el valor/expresión entre los `[ .. ]` no se resuelve a un number, el valor será coercionado implícitamente a su representación numérica entera/completa (si es posible).

```js
greeting["4"];          // "o"
```

Si el valor/expresión se resuelve a un number fuera del rango entero de `0` - `length - 1` (o `NaN`), o si no es un value type number, el acceso será tratado en cambio como un acceso a propiedad con el nombre de propiedad equivalente en string. Si ese acceso a propiedad falla, el resultado es `undefined`.

| NOTA: |
| :--- |
|  Cubriremos la coerción en profundidad más adelante en el libro. |

### Iteración de Caracteres

Los strings no son arrays, pero ciertamente imitan a los arrays de cerca en muchos aspectos. Uno de esos comportamientos es que, al igual que los arrays, los strings son iterables. Esto significa que los caracteres (code-units) de un string pueden iterarse individualmente:

```js
myName = "Kyle";

for (let char of myName) {
    console.log(char);
}
// K
// y
// l
// e

chars = [ ...myName ];
chars;
// [ "K", "y", "l", "e" ]
```

Los valores, como los strings y los arrays, son iterables (vía `...`, `for..of`, y `Array.from(..)`), si exponen un método productor de iteradores en la ubicación de propiedad de símbolo especial `Symbol.iterator` (consulta "Well-Known Symbols" en el Capítulo 1):

```js
myName = "Kyle";
it = myName[Symbol.iterator]();

it.next();      // { value: "K", done: false }
it.next();      // { value: "y", done: false }
it.next();      // { value: "l", done: false }
it.next();      // { value: "e", done: false }
it.next();      // { value: undefined, done: true }
```

| NOTA: |
| :--- |
| Los detalles del protocolo de iterador, incluyendo el hecho de que el resultado `{ value: "e" .. }` todavía muestra `done: false`, se cubren en detalle en el título "Sync & Async" de esta serie. |

### Cálculo de la Longitud

Como se mencionó en el Capítulo 1, los valores string tienen una propiedad `length` que expone automáticamente la longitud del string; esta propiedad solo puede ser accedida; los intentos de establecerla se ignoran silenciosamente.

El valor `length` reportado corresponde en cierto modo al número de caracteres en el string (en realidad, code-units), pero como vimos en el Capítulo 1, es más complejo cuando hay caracteres Unicode involucrados.

La mayoría de las personas distinguen visualmente los símbolos como caracteres separados; esta noción de un símbolo visual independiente se denomina *grafema*, o *clúster de grafemas*. Así que cuando contamos la "longitud" de un string, típicamente queremos decir que estamos contando el número de grafemas.

Pero no es así como la computadora trata los caracteres.

En JS, cada *carácter* es un code-unit (16 bits), con un valor de code-point igual o inferior a `65535`. La propiedad `length` de un string siempre cuenta el número de code-units en el valor del string, no de code-points. Un code-unit podría representar un solo carácter por sí mismo, o puede ser parte de un surrogate pair, o puede combinarse con un símbolo *combinante* adyacente, o ser parte de un clúster de grafemas. Como tal, `length` no coincide con la noción típica de contar caracteres/grafemas visuales.

Para acercarse más a una *longitud de grafemas* esperada/intuitiva para un string, el valor del string primero necesita ser normalizado con `normalize("NFC")` (consulta "Normalizing Unicode" en el Capítulo 1) para producir cualquier code-unit *compuesto* (donde sea posible), en caso de que algunos caracteres hayan sido originalmente almacenados *descompuestos* como code-units separados.

Por ejemplo:

```js
favoriteItem = "teléfono";
favoriteItem.length;            // 9 -- uh oh!

favoriteItem = favoriteItem.normalize("NFC");
favoriteItem.length;            // 8 -- phew!
```

Desafortunadamente, como vimos en el Capítulo 1, todavía tendremos la posibilidad de caracteres con code-point mayor a `65535`, y por lo tanto necesitando un surrogate pair para ser representados. Tales caracteres contarán doble en el `length`:

```js
// "☎" === "☎"
oldTelephone = "☎";
oldTelephone.length;            // 1

// "📱" === "\u{1F4F1}" === "📱"
cellphone = "📱";
cellphone.length;               // 2 -- oops!
```

¿Entonces qué hacemos?

Una solución es usar la iteración de caracteres (vía el operador `...`) como vimos en la sección anterior, ya que automáticamente devuelve cada carácter combinado de un surrogate pair:

```js
cellphone = "📱";
cellphone.length;               // 2 -- oops!
[ ...cellphone ].length;        // 1 -- phew!
```

Pero, desafortunadamente, los clústeres de grafemas (como se explicó en el Capítulo 1) meten otra traba más en el cálculo de la longitud de un string. Por ejemplo, si tomamos el emoji de pulgar hacia abajo (`"\u{1F44E}"`) y le agregamos el modificador de tono de piel para piel medio-oscura (`"\u{1F3FE}"`), obtenemos:

```js
// "👎🏾" = "\u{1F44E}\u{1F3FE}"
thumbsDown = "👎🏾";

thumbsDown.length;              // 4 -- oops!
[ ...thumbsDown ].length;       // 2 -- oops!
```

Como puedes ver, estos son dos code-points distintos (no un surrogate pair) que, en virtud de su orden y adyacencia, hacen que el renderizado Unicode de la computadora dibuje el símbolo de pulgar hacia abajo pero con un tono de piel más oscuro que el predeterminado. La longitud computada del string es por lo tanto `2`.

Haría falta replicar la mayor parte de la compleja lógica de renderizado Unicode de una plataforma para poder reconocer tales clústeres de code-points como un solo "carácter" a efectos del conteo de longitud. Hay bibliotecas que dicen hacerlo, pero no son necesariamente perfectas, y vienen con un costo considerable en términos de código extra.

| NOTA: |
| :--- |
| Como usuario de Twitter, podrías esperar poder poner 280 emojis de pulgar hacia abajo en un solo tweet, ya que parece un solo carácter. Twitter cuenta el `"👎"` (pulgar hacia abajo predeterminado), el `"👎🏾"` (pulgar hacia abajo con tono de piel medio-oscuro), e incluso el `"👩‍👩‍👦‍👦"` (clúster de grafemas de emoji de familia) todos como 2 caracteres cada uno, aunque sus respectivas longitudes de string (desde la perspectiva de JS) son `2`, `4`, y `7`; por lo tanto, solo puedes caber la mitad del número de emojis (140 en lugar de 280) en un tweet. De hecho, Twitter implementó este cambio en 2018 específicamente para nivelar el conteo de todos los caracteres Unicode, a 2 caracteres por símbolo. [^TwitterUnicode] Ese fue un cambio bienvenido para los usuarios de Twitter, especialmente para aquellos que quieren usar caracteres emoji que sean más representativos del género, tono de piel, etc., pretendidos. Aun así, *es* curioso que Twitter haya elegido contar todos los símbolos Unicode/emoji como 2 caracteres cada uno, en lugar del más intuitivo 1 carácter (grafema) cada uno. |

Contar la *longitud* de un string para que coincida con nuestras intuiciones humanas es una tarea notablemente desafiante, quizás más un arte que una ciencia. Podemos obtener aproximaciones aceptables en muchos casos, pero hay muchos otros casos que pueden confundir a nuestros programas.

### Internacionalización (i18n) y Localización (l10n)

Para servir a la creciente necesidad de que los programas JS operen como se espera en cualquier contexto de idioma/cultura internacional, el comité de ECMAScript también publica la ECMAScript Internationalization API. [^INTLAPI]

Un programa JS tiene por defecto un locale/idioma según el entorno que ejecuta el programa (página de navegador web, instancia de Node, etc). El locale en efecto afecta el ordenamiento (y las comparaciones de valores), el formateo, y varios otros comportamientos asumidos. Tales comportamientos alterados son quizás un poco más obvios con los strings, pero también pueden verse con los numbers (¡y las fechas!).

Pero los caracteres de los strings también pueden tener información de idioma/locale incrustada en ellos, lo cual tiene precedencia sobre el valor por defecto del entorno. Si el carácter del string es ambiguo/compartido en términos de su idioma/locale (como `"a"`), se usa la configuración por defecto del entorno.

Dependiendo del contenido del string, puede ser interpretado como ordenado de izquierda a derecha (LTR) o de derecha a izquierda (RTL). Como tal, muchos de los métodos de string que cubriremos más adelante usan descriptores lógicos en sus nombres, como "start", "end", "begin", "end", y "last", en lugar de términos direccionales como "left" y "right".

Por ejemplo, el hebreo y el árabe son ambos idiomas RTL comunes:

```js
hebrewHello = "\u{5e9}\u{5dc}\u{5d5}\u{5dd}";

console.log(hebrewHello);                       // שלום
```

¿Notas que el primer carácter listado en el literal del string (`"\u{5e9}"`) es en realidad el carácter más a la derecha cuando el string se renderiza?

Aunque el hebreo es un idioma RTL, en realidad no escribes los caracteres en el literal del string en orden invertido (RTL) de la manera en que deberían renderizarse. Ingresas los caracteres en orden lógico, donde la posición `0` es el primer carácter, la posición `1` es el segundo carácter, etc. La capa de renderizado es donde los caracteres RTL se invierten para mostrarse en su orden correcto.

Eso también significa que si accedes a `hebrewHello[0]` (o `hebrewHello.charAt(0)`) -- para obtener el carácter en la posición `0` -- obtienes `"ש"` porque ese es lógicamente el primer carácter del string, no `"ם"` (lógicamente el último carácter del string). El acceso por posición de índice sigue la posición lógica, no la posición renderizada.

Aquí está el mismo ejemplo en otro idioma RTL, el árabe:

```js
arabicHello = "\u{631}\u{62d}\u{628}\u{627}";

console.log(arabicHello);                       // رحبا

console.log(arabicHello[0]);                    // ر
```

Los programas JS pueden forzar un idioma/locale específico, usando varias APIs de `Intl` como `Intl.Collator`: [^INTLCollator]

```js
germanStringSorter = new Intl.Collator("de");

listOfGermanWords = [ /* .. */ ];

germanStringSorter.compare("Hallo","Welt");
// -1 (or negative number)

// examples adapted from MDN:
//
germanStringSorter.compare("Z","z");
// 1 (or positive number)

caseFirstSorter = new Intl.Collator("de",{ caseFirst: "upper", });
caseFirstSorter.compare("Z","z");
// -1 (or negative number)
```

Los strings de múltiples palabras pueden segmentarse usando `Intl.Segmenter`: [^INTLSegmenter]

```js
arabicHelloWorld = "\u{645}\u{631}\u{62d}\u{628}\u{627} \
\u{628}\u{627}\u{644}\u{639}\u{627}\u{644}\u{645}";

console.log(arabicHelloWorld);      // مرحبا بالعالم

arabicSegmenter = new Intl.Segmenter("ar",{ granularity: "word" });

for (
    let { segment: word, isWordLike } of
    arabicSegmenter.segment(arabicHelloWorld)
) {
    if (isWordLike) {
        console.log(word);
    }
}
// مرحبا
//لعالم
```

| NOTA: |
| :--- |
| El método `segment(..)` (de instancias de `Intl.Segmenter`) devuelve un iterador JS estándar, que el bucle `for..of` aquí consume. Más sobre protocolos de iteración en el título "Sync & Async" de esta serie. |

### Comparación de Strings

Los valores string pueden compararse (tanto por igualdad como por ordenamiento relacional) con otros valores string, usando varios operadores incorporados. Es importante tener en cuenta que tales comparaciones son sensibles al contenido real del string, incluyendo especialmente los code-points subyacentes de los caracteres Unicode no-BPM.

Tanto la comparación por igualdad como la relacional distinguen entre mayúsculas y minúsculas, para cualquier carácter donde las mayúsculas y minúsculas estén bien definidas. Para hacer comparaciones que no distingan entre mayúsculas y minúsculas, normaliza primero la capitalización de ambos valores (con `toUpperCase()` o `toLowerCase()`).

#### Igualdad de Strings

Los operadores `===` y `==` (junto con sus contrapartes negadas `!==` y `!=`, respectivamente) son la forma más común en que se hacen las comparaciones de igualdad para valores primitivos, incluyendo los valores string:

```js
"my name" === "my n\x61me";               // true

"my name" !== String.raw`my n\x61me`;     // true
```

El operador `===`[^StrictEquality] -- a menudo referido como "igualdad estricta" -- primero verifica si los types coinciden, y si no, devuelve `false` de inmediato. Si los types coinciden, entonces verifica si los valores son los mismos; para los strings, esto es una comparación code-unit por code-unit, de principio a fin.

A pesar del nombre "estricto", hay matices en `===` (como el manejo de `-0` y `NaN`), pero los cubriremos más adelante.

##### Igualdad Coercitiva

En contraste, el operador `==`[^LooseEquality] -- a menudo referido como "igualdad flexible" -- realiza *igualdad coercitiva*: si los value types de los dos operandos no coinciden, `==` primero coerciona uno o ambos operandos hasta que los value types *sí* coincidan, y luego pasa la comparación internamente a `===`.

La coerción es un tema extremadamente importante -- es una parte inherente del sistema de types de JS, uno de los 3 pilares del lenguaje -- pero solo vamos a introducirla brevemente aquí en este capítulo, y la revisitaremos en detalle más adelante.

| NOTA: |
| :--- |
| Puede que hayas escuchado la explicación a menudo citada, pero no obstante inexacta, de que la diferencia entre `==` y `===` es que `==` compara los valores mientras que `==` compara tanto los valores como los types. No es verdad, y puedes leer la especificación tú mismo para verificarlo -- tanto los algoritmos de especificación `isStrictlyEqual(..)` como `isLooselyEqual(..)` están enlazados como footnotes en los párrafos anteriores. Para resumir, sin embargo: tanto `==` como `===` conocen y son sensibles a los types de los operandos. Si los types de los operandos son los mismos, ambos operadores hacen literalmente exactamente lo mismo; si los types difieren, `==` fuerza la coerción hasta que los types coincidan, mientras que `===` devuelve `false` inmediatamente. |

Es extremadamente común que los desarrolladores afirmen que el operador `==` es confuso y demasiado difícil de usar sin sorpresas (de ahí la preferencia casi universal por `===`). Pienso que eso es totalmente una tontería, y de hecho, los desarrolladores de JS deberían usar `==` por defecto (y evitar `===` si es posible). Pero necesitamos mucha más discusión para respaldar una afirmación tan controversial; retén tus objeciones hasta que la revisitemos más adelante.

Por ahora, para ganar algo de intuición sobre la naturaleza coercitiva de `==`, la observación más esclarecedora es que si los types no coinciden, `==` *prefiere* la comparación numérica. Eso significa que intentará convertir ambos operandos a numbers, y luego realizar la verificación de igualdad (igual que `===`).

Así que, en lo que respecta a nuestra discusión presente, la igualdad real de strings *solo puede* verificarse si ambos operandos ya son strings:

```js
// actual string equality check (via === internally):
"42" == "42";           // true
```

`==` en realidad no realiza verificaciones de igualdad de strings por sí mismo. Si los value types de los operandos son ambos strings, `==` simplemente pasa la comparación a `===`. Si no son ambos strings, los pasos coercitivos en `==` reducirán la coincidencia de la comparación a numérica en lugar de string:

```js
// numeric (not string!) equality check:
42 == "42";             // true
```

Cubriremos la igualdad numérica más adelante en este capítulo.

##### Igualdad *Realmente* Estricta

Además de `==` y `===`, JS provee la utilidad `Object.is(..)`, que devuelve `true` si ambos argumentos son *exactamente idénticos*, y `false` en caso contrario (sin excepciones ni matices):

```js
Object.is("42",42);             // false

Object.is("42","\x34\x32");     // true
```

Dado que `===` agrega un `=` al final de `==` para hacerlo más estricto en comportamiento, hago una especie de medio chiste de que la utilidad `Object.is(..)` es como un operador `====` (un cuarto `=` agregado), ¡para el tipo de verificación de igualdad realmente-verdaderamente-estricta-sin-excepciones!

Dicho eso, `===` (y `==` en virtud de su delegación interna a `===`) son *extremadamente predecibles*, sin excepciones raras, cuando se trata de comparar dos valores que ya son realmente strings. Recomiendo encarecidamente usar `==` para tales verificaciones (o `===`), y reservar `Object.is(..)` para los casos límite (que son numéricos).

#### Comparaciones Relacionales de Strings

Además de las verificaciones de igualdad entre strings, JS soporta comparaciones relacionales entre valores primitivos, como los strings: `<`, `<=`, `>`, y `>=`.

Las operaciones `<` (menor-que) y `>` (mayor-que) comparan dos valores string lexicográficamente -- como ordenarías palabras en un diccionario -- y por lo tanto deberían ser bastante autoexplicativas:

```js
"hello" < "world";          // true
```

| NOTA: |
| :--- |
| Como se mencionó antes, el programa JS en ejecución tiene un locale por defecto, y estos operadores comparan según ese locale. |

Al igual que `==`, los operadores `<` y `>` son numéricamente coercitivos. Cualquier valor que no sea number es coercionado a number. Así que la única manera de hacer una comparación relacional con strings es asegurarse de que ambos operandos ya sean valores string.

Quizás de forma algo sorprendente, `<` y `>` no tienen un equivalente de comparación estricta, de la manera en que `===` evita la coerción de `==`. Estos operadores siempre son coercitivos (cuando los types no coinciden), y no hay manera en JS de evitar eso.

¿Entonces qué pasa cuando ambos valores son strings *con apariencia numérica*?

```js
"100" < "11";               // true
```

Numéricamente, por supuesto, `100` *no debería ser* menor que `11`.

Pero las comparaciones relacionales entre dos strings usan el ordenamiento lexicográfico. Así que el segundo carácter `"0"` (en `"100"`) es menor que el segundo `"1"` (en `"11"`), y por lo tanto `"100"` se ordenaría en un *diccionario* antes que `"11"`. Los operadores relacionales solo coercionan a numbers si los types de los operandos no son ya strings.

Los operadores `<=` (menor-o-igual) y `>=` (mayor-o-igual) son efectivamente una abreviatura de una verificación compuesta.

```js
"hello" <= "hello";                             // true
("hello" < "hello") || ("hello" == "hello");    // true

"hello" >= "hello";                             // true
("hello" > "hello") || ("hello" == "hello");    // true
```

| NOTA: |
| :--- |
| Aquí hay un interesante matiz de la especificación: JS en realidad no define las operaciones subyacentes de mayor-que (para `>`) o mayor-o-igual (para `>=`). En cambio, las define invirtiendo los argumentos de sus contrapartes complementarias *menor-que*. Así que `x > y` es tratado por JS esencialmente como `y <= x`, y `x >= y` es tratado por JS esencialmente como `y < x`. ¡Así que JS solo necesita especificar cómo funcionan `<` y `==`, y por lo tanto obtiene `>` y `>=` gratis! |

##### Comparaciones Relacionales Conscientes del Locale

Como mencioné hace un momento, los operadores relacionales asumen y usan el locale actual en efecto. Sin embargo, a veces puede ser útil forzar un locale específico para las comparaciones (como cuando se ordena una lista de strings).

JS provee el método `localCompare(..)` en los strings de JS para este propósito:

```js
"hello".localeCompare("world");
// -1 (or negative number)

"world".localeCompare("hello","en");
// 1 (or positive number)

"hello".localeCompare("hello","en",{ ignorePunctuation: true });
// 0

// examples from MDN:
//
// in German, ä sorts before z
"ä".localeCompare("z","de");
// -1 (or negative number) // a negative value

// in Swedish, ä sorts after z
"ä".localeCompare("z","sv");
// 1 (or positive number)
```

Los argumentos segundo y tercero opcionales de `localeCompare(..)` controlan qué locale usar, vía la API `Intl.Collator`[^INTLCollatorApi], como se cubrió anteriormente.

Podrías usar `localeCompare(..)` al ordenar un array de strings:

```js
studentNames = [
    "Lisa",
    "Kyle",
    "Jason"
];

// Array::sort() mutates the array in place
studentNames.sort(function alphabetizeNames(name1,name2){
    return name1.localeCompare(name2);
});

studentNames;
// [ "Jason", "Kyle", "Lisa" ]
```

Pero como se discutió antes, una forma más directa (y ligeramente más performante al ordenar muchos strings) es usar `Intl.Collator` directamente:

```js
studentNames = [
    "Lisa",
    "Kyle",
    "Jason"
];

nameSorter = new Intl.Collator("en");

// Array::sort() mutates the array in place
studentNames.sort(nameSorter.compare);

studentNames;
// [ "Jason", "Kyle", "Lisa" ]
```

### Concatenación de Strings

Dos o más valores string pueden concatenarse (combinarse) en un nuevo valor string, usando el operador `+`:

```js
greeting = "Hello, " + "Kyle!";

greeting;               // Hello, Kyle!
```

El operador `+` actuará como una concatenación de strings si cualquiera de los dos operandos (valores en los lados izquierdo o derecho del operador) ya es un string (incluso un string vacío `""`).

Si un operando es un string y el otro no lo es, el que no es un string será coercionado a su representación en string a efectos de la concatenación:

```js
userCount = 7;

status = "There are " + userCount + " users online";

status;         // There are 7 users online
```

La concatenación de strings de este tipo es esencialmente la interpolación de datos dentro del string, que es el propósito principal de los template literals (consulta el Capítulo 1). Así que el siguiente código tendrá el mismo resultado pero generalmente se considera el enfoque más preferido:

```js
userCount = 7;

status = `There are ${userCount} users online`;

status;         // There are 7 users online
```

Otras opciones para la concatenación de strings incluyen `"one".concat("two","three")` y `[ "one", "two", "three" ].join("")`, pero este tipo de enfoques solo son preferibles cuando el número de strings a concatenar depende de condiciones/cómputo en tiempo de ejecución. Si el string tiene un conjunto de contenido fijo/conocido, como arriba, los template literals son la mejor opción.

### Métodos de los Valores String

Los valores string proveen un montón de métodos adicionales específicos de strings (como propiedades):

* `charAt(..)`: produce un nuevo valor string en el índice numérico, similar a `[ .. ]`; a diferencia de `[ .. ]`, el resultado siempre es un string, ya sea el carácter en la posición `0` (si es un number válido fuera del rango de índices), o el string vacío `""` (si falta el índice o es inválido)

* `at(..)` es similar a `charAt(..)`, pero los índices negativos cuentan hacia atrás desde el final del string

* `charCodeAt(..)`: devuelve el code-unit numérico (consulta "JS Character Encodings" en el Capítulo 1) en el índice especificado

* `codePointAt(..)`: devuelve el code-point completo que comienza en el índice especificado; si se encuentra un surrogate pair allí, se devuelve el carácter completo (code-point)

* `substr(..)` / `substring(..)` / `slice(..)`: producen un nuevo valor string que representa un rango de caracteres del string original; estos difieren en cómo se especifican o determinan los índices de inicio/fin del rango

* `toUpperCase()`: produce un nuevo valor string que está todo en caracteres mayúsculas

* `toLowerCase()`: produce un nuevo valor string que está todo en caracteres minúsculas

* `toLocaleUpperCase()` / `toLocaleLowerCase()`: usan mapeos de locale para las operaciones de mayúsculas o minúsculas

* `concat(..)`: produce un nuevo valor string que es la concatenación del string original y todos los valores string pasados como argumentos

* `indexOf(..)`: busca un valor string argumento en el string original, opcionalmente comenzando desde la posición especificada en el segundo argumento; devuelve la posición de índice basada en `0` si se encuentra, o `-1` si no se encuentra

* `lastIndexOf(..)`: como `indexOf(..)` pero, desde el final del string (derecha en locales LTR, izquierda en locales RTL)

* `includes(..)`: similar a `indexOf(..)` pero devuelve un resultado boolean

* `search(..)`: similar a `indexOf(..)` pero con una coincidencia de expresión regular según se especifique

* `trimStart()` / `trimEnd()` / `trim()`: producen un nuevo valor string con el espacio en blanco recortado del inicio del string (izquierda en locales LTR, derecha en locales RTL), o del final del string (derecha en locales LTR, izquierda en locales RTL), o de ambos

* `repeat(..)`: produce un nuevo string con el valor del string original repetido el número de veces especificado

* `split(..)`: produce un array de valores string separados en los límites de string o expresión regular especificados

* `padStart(..)` / `padEnd(..)`: producen un nuevo valor string con relleno (por defecto " " espacio en blanco, pero puede sobrescribirse) aplicado ya sea al inicio (izquierda en locales LTR, derecha en locales RTL) o al final (derecha en locales LTR, izquierda en locales RTL), de modo que el resultado final del string tenga al menos una longitud especificada

* `startsWith(..)` / `endsWith(..)`: verifican ya sea el inicio (izquierda en locales LTR, derecha en locales RTL) o el final (derecha en locales LTR) del string original para el valor string argumento; devuelven un resultado boolean

* `match(..)` / `matchAll(..)`: devuelven un resultado similar a array de coincidencia de expresión regular contra el string original

* `replace(..)`: devuelve un nuevo string con un reemplazo del string original, de una o más ocurrencias coincidentes de la coincidencia de expresión regular especificada

* `normalize(..)`: produce un nuevo string con la normalización Unicode (consulta "Unicode Normalization" en el Capítulo 1) habiendo sido realizada sobre el contenido

* `localCompare(..)`: función que compara dos strings según el locale actual (útil para ordenar); devuelve un number negativo (usualmente `-1` pero no garantizado) si el valor del string original viene antes que el valor del string argumento lexicográficamente, un number positivo (usualmente `1` pero no garantizado) si el valor del string original viene después del valor del string argumento lexicográficamente, y `0` si los dos strings son idénticos

* `anchor()`, `big()`, `blink()`, `bold()`, `fixed()`, `fontcolor()`, `fontsize()`, `italics()`, `link()`, `small()`, `strike()`, `sub()`, y `sup()`: históricamente, estos eran útiles para generar fragmentos de string HTML; ahora están obsoletos y deberían evitarse

| ADVERTENCIA: |
| :--- |
| Muchos de los métodos descritos arriba dependen de índices de posición. Como se mencionó antes en la sección "Cálculo de la Longitud", estas posiciones dependen del contenido interno del valor del string, lo que significa que si está presente un carácter Unicode extendido y ocupa dos slots de code-unit, eso contará como dos posiciones de índice en lugar de una. No tener en cuenta los code-units *descompuestos*, los surrogate pairs, y los clústeres de grafemas es una fuente común de bugs en el manejo de strings en JS. |

Todos estos métodos de string pueden llamarse directamente sobre un valor literal, o sobre una variable/propiedad que contiene un valor string. Cuando corresponde, producen un nuevo valor string en lugar de modificar el valor string existente (ya que los strings son inmutables):

```js
"all these letters".toUpperCase();      // ALL THESE LETTERS

greeting = "Hello!";
greeting.repeat(2);                     // Hello!Hello!
greeting;                               // Hello!
```

### Ayudantes Estáticos de `String`

Las siguientes funciones utilitarias de string se proveen directamente en el objeto `String`, en lugar de como métodos en los valores string individuales:

* `String.fromCharCode(..)` / `String.fromCodePoint(..)`: producen un string a partir de uno o más argumentos que representan los code-units (`fromCharCode(..)`) o los code-points completos (`fromCodePoint(..)`)

* `String.raw(..)`: una función template-tag por defecto que permite la interpolación en un template literal pero impide que las secuencias de escape de caracteres sean parseadas, de modo que permanecen en sus caracteres de entrada individuales *crudos* del literal

Además, la mayoría de los valores (especialmente los primitivos) pueden ser coercionados explícitamente a su equivalente en string pasándolos a la función `String(..)` (sin la palabra clave `new`). Por ejemplo:

```js
String(true);           // "true"
String(42);             // "42"
String(Infinity);       // "Infinity"
String(undefined);      // "undefined"
```

Cubriremos mucho más detalle sobre tales coerciones de type en un capítulo posterior.

## Comportamientos de los Numbers

Los numbers se usan para una variedad de tareas en nuestros programas, pero mayormente para cómputos matemáticos. Presta mucha atención a cómo se comportan los numbers en JS, para asegurarte de que los resultados sean los esperados.

### Imprecisión de Punto Flotante

Necesitamos revisitar nuestra discusión sobre IEEE-754 del Capítulo 1.

Uno de los clásicos escollos de cualquier sistema numérico IEEE-754 en cualquier lenguaje de programación -- ¡NO EXCLUSIVO DE JS! -- es que no todas las operaciones y valores pueden encajar prolijamente en las representaciones IEEE-754.

La ilustración más común es:

```js
point3a = 0.1 + 0.2;
point3b = 0.3;

point3a;                        // 0.30000000000000004
point3b;                        // 0.3

point3a === point3b;            // false <-- oops!
```

La operación `0.1 + 0.2` termina creando un error de punto flotante (deriva), donde el valor almacenado es en realidad `0.30000000000000004`.

Las respectivas representaciones en bits son:

```
// 0.30000000000000004
00111111110100110011001100110011
00110011001100110011001100110100

// 0.3
00111111110100110011001100110011
00110011001100110011001100110011
```

Si miras de cerca esos patrones de bits, solo los últimos 2 bits difieren, de `00` a `11`. ¡Pero eso es suficiente para que esos dos numbers sean desiguales!

De nuevo, solo para reforzar: este comportamiento **NO ES DE NINGUNA MANERA** exclusivo de JS. Así es exactamente como funcionará cualquier lenguaje de programación conforme a IEEE-754 en el mismo escenario. Como afirmé arriba, la mayoría de todos los lenguajes de programación usan IEEE-754, y por lo tanto todos sufrirán este mismo destino.

La tentación de burlarse de JS por `0.1 + 0.2 !== 0.3` es fuerte, lo sé. Pero aquí es completamente una tontería.

| NOTA: |
| :--- |
| Prácticamente todos los programadores necesitan ser conscientes de IEEE-754 y asegurarse de ser cuidadosos con este tipo de escollos. Es algo asombroso, de manera decepcionante, lo pocos de ellos que tienen alguna idea de cómo funciona IEEE-754. Si te has tomado tu tiempo leyendo y entendiendo estos conceptos hasta ahora, ¡ahora estás en ese raro pequeño porcentaje que realmente hizo el esfuerzo de entender los numbers en sus programas! |

#### Umbral Epsilon

Un consejo común para sortear tal imprecisión de punto flotante usa este valor number *muy pequeño* definido por JS:

```js
Number.EPSILON;                 // 2.220446049250313e-16
```

*Epsilon* es la diferencia más pequeña que JS puede representar entre `1` y el siguiente valor mayor que `1`. Si bien este valor técnicamente depende de la implementación/plataforma, generalmente es alrededor de `2.2E-16`, o `2^-52`.

Para quienes no prestan suficiente atención a los detalles aquí -- ¡incluyendo mi yo del pasado! -- generalmente se asume que cualquier desviación en la precisión de punto flotante de una sola operación nunca debería ser mayor que `Number.EPSILON`. Así, en teoría, podemos usar `Number.EPSILON` como un valor de tolerancia *muy pequeño* para asegurar que las comparaciones de igualdad de numbers sean *seguras*:

```js
function safeNumberEquals(a,b) {
    return Math.abs(a - b) < Number.EPSILON;
}

point3a = 0.1 + 0.2;
point3b = 0.3;

// are these safely "equal"?
safeNumberEquals(point3a,point3b);      // true
```

| ADVERTENCIA: |
| :--- |
| En el libro "Types & Grammar" de la primera edición, efectivamente recomendé exactamente este enfoque. Estaba equivocado. Debería haber investigado el tema más de cerca. |

Pero, resulta que, este enfoque no es seguro en absoluto:

```js
point3a = 10.1 + 0.2;
point3b = 10.3;

safeNumberEquals(point3a,point3b);      // false :(
```

Bueno... ¡qué lástima!

Desafortunadamente, `Number.EPSILON` solo funciona como un umbral de error "seguramente igual" para ciertos numbers/operaciones pequeños, y en otros casos, es demasiado pequeño, y produce falsos negativos.

Podrías escalar `Number.EPSILON` por algún factor para producir un umbral más grande que evite falsos negativos pero que todavía filtre toda la desviación de punto flotante en tu programa. Pero qué factor usar es enteramente una decisión de juicio manual basada en qué magnitud de valores, y operaciones sobre ellos, implicará tu programa. No hay forma automática de computar un umbral confiable y universal.

A menos que realmente sepas lo que estás haciendo, simplemente *no* deberías usar este enfoque del umbral `Number.EPSILON` en absoluto.

| TIP: |
| :--- |
| Si te gustaría leer más detalles y consejos sólidos sobre este tema, recomiendo encarecidamente leer este post. [^EpsilonBad] Pero si no podemos usar `Number.EPSILON` para evitar los peligros de la desviación de punto flotante, ¿qué hacemos? Si puedes evitar el punto flotante por completo escalando todos tus numbers hacia arriba de modo que sean todos enteros (o bigints) mientras realizas matemáticas, hazlo. Solo trata con valores decimales cuando tengas que mostrar/representar un valor final después de que toda la matemática esté hecha. Si eso no es posible/práctico, usa una biblioteca de emulación de decimales de precisión arbitraria y evita los valores number por completo. O haz tus matemáticas en otro entorno de programación externo que no esté basado en IEEE-754. |

### Comparación Numérica

Al igual que los strings, los valores number pueden compararse (tanto por igualdad como por ordenamiento relacional) usando los mismos operadores.

Recuerda que no importa qué forma tome el valor number cuando se especifica como literal (base-10, octal, hexadecimal, exponencial, etc), el valor subyacente almacenado es lo que se comparará. También ten en cuenta los problemas de imprecisión de punto flotante discutidos en la sección anterior, ya que las comparaciones serán sensibles al contenido binario exacto.

#### Igualdad Numérica

Al igual que los strings, las comparaciones de igualdad para numbers usan ya sea los operadores `==` / `===` o `Object.is(..)`. También recuerda que si los types de ambos operandos son los mismos, `==` se comporta idénticamente a `===`.

```js
42 == 42;                   // true
42 === 42;                  // true

42 == 43;                   // false
42 === 43;                  // false

Object.is(42,42);           // true
Object.is(42,43);           // false
```

Para la igualdad coercitiva `==` (cuando los types de los operandos no coinciden), si cualquiera de los operandos no es un valor string, `==` prefiere una verificación de igualdad numérica (lo que significa que ambos operandos son coercionados a numbers).

```js
// numeric (not string!) comparison
42 == "42";                 // true
```

En este fragmento, la igualdad coercitiva coerciona `"42"` a `42`, no al revés (`42` a `"42"`). Una vez que ambos types son number, entonces sus valores se comparan por igualdad exacta, igual que lo haría `===`.

Recuerda que JS no distingue entre valores como `42`, `42.0`, y `42.000000`; por debajo, son todos lo mismo. Como no sorprende, las verificaciones de igualdad `==` y `===` lo verifican:

```js
42 == 42.0;                 // true
42.0 == 42.00000;           // true
42.00 === 42.000;           // true
```

La intuición que probablemente tienes es que, si dos numbers son literalmente los mismos, son iguales. Y así es como JS lo interpreta. Pero `0.3` no es literalmente lo mismo que el resultado de `0.1 + 0.2`, porque (como vimos antes), este último produce un valor subyacente que está *muy cerca* de `0.3`, pero no es exactamente idéntico.

Lo interesante es que los dos valores están *tan cerca* que su diferencia es menor que el umbral `Number.EPSILON`, así que JS en realidad no puede representar esa diferencia *con precisión*.

Podrías entonces pensar, al menos informalmente, que tales numbers de JS deberían ser "iguales", ya que la diferencia entre ellos es demasiado pequeña para representar. Pero fíjate: JS *sí puede* representar que *hay* una diferencia, razón por la cual ves ese `4` justo al final del decimal cuando JS evalúa `0.1 + 0.2`. Y *podrías* escribir el literal number `0.00000000000000004` (es decir, `4e-17`), siendo esa la diferencia entre `0.3` y `0.1 + 0.2`.

Lo que JS no puede hacer, con sus numbers de punto flotante IEEE-754, es representar un number tan pequeño de una manera lo suficientemente *precisa* como para que las operaciones sobre él produzcan resultados esperados. Es demasiado pequeño para ser representado completa y apropiadamente en el type number que JS provee.

Así que `0.1 + 0.2 == 0.3` se resuelve a `false`, porque hay una diferencia entre los dos valores, aunque JS no pueda representar con precisión o hacer nada con un valor tan pequeño como esa diferencia.

También, como vimos con los strings, los operadores `!=` (no-igual coercitivo) y `!==` (no-igual estricto) funcionan con numbers. `x != y` es básicamente `!(x == y)`, y `x !== y` es básicamente `!(x === y)`.

Hay dos excepciones frustrantes en la igualdad numérica (ya sea que uses `==` o `===`):

```js
NaN === NaN;                // false -- ugh!
-0 === 0;                   // true -- ugh!
```

`NaN` nunca es igual a sí mismo (incluso con `===`), y `-0` siempre es igual a `0` (incluso con `===`). A veces sorprende a la gente que incluso `===` tenga estas dos excepciones.

Sin embargo, la verificación de igualdad `Object.is(..)` no tiene ninguna de estas excepciones, así que para comparaciones de igualdad con `NaN` y `-0`, evita los operadores `==` / `===` y usa `Object.is(..)` -- o para `NaN` específicamente, `Number.isNaN(..)`.

#### Comparaciones Relacionales Numéricas

Al igual que con los valores string, los operadores relacionales de JS (`<`, `<=`, `>`, y `>=`) operan con numbers. Las operaciones `<` (menor-que) y `>` (mayor-que) deberían ser bastante autoexplicativas:

```js
41 < 42;                    // true

0.1 + 0.2 > 0.3;            // true (ugh, IEEE-754)
```

Recuerda: al igual que `==`, los operadores `<` y `>` también son coercitivos, lo que significa que cualquier valor que no sea number es coercionado a number -- a menos que ambos operandos ya sean strings, como vimos antes. No hay operadores de comparación relacional estrictos.

Si estás haciendo comparaciones relacionales entre numbers, la única manera de evitar la coerción es asegurarte de que las comparaciones siempre tengan dos numbers. De lo contrario, estos operadores harán comparaciones *relacionales coercitivas* similares a cómo `==` realiza comparaciones de *igualdad coercitiva*.

### Operadores Matemáticos

Como afirmé antes, la razón principal para tener numbers en un lenguaje de programación es realizar operaciones matemáticas con ellos. Así que hablemos de cómo lo hacemos.

Los operadores aritméticos básicos son `+` (suma), `-` (resta), `*` (multiplicación), y `/` (división). También están disponibles los operadores `**` (exponenciación) y `%` (módulo, es decir, *resto de división*). También hay formas `+=`, `-=`, `*=`, `/=`, `**=`, y `%=` de los operadores, que adicionalmente asignan el resultado de vuelta al operando izquierdo -- debe ser un objetivo de asignación válido como una variable o propiedad.

| NOTA: |
| :--- |
| Como ya hemos visto, el operador `+` está sobrecargado para funcionar tanto con numbers como con strings. Cuando uno o ambos operandos es un string, el resultado es una concatenación de strings (incluyendo coercionar cualquier operando a string si es necesario). Pero si ninguno de los operandos es un string, el resultado es una suma numérica, como se espera. |

Todos estos operadores matemáticos son *binarios*, lo que significa que esperan dos operandos de valor, uno a cada lado del operador; todos esperan que los operandos sean valores number. Si uno o ambos operandos no son numbers, el/los operando(s) que no es/son number es/son coercionado(s) a numbers para realizar la operación. Cubriremos la coerción en detalle en un capítulo posterior.

Considera:

```js
40 + 2;                 // 42
44 - 2;                 // 42
21 * 2;                 // 42
84 / 2;                 // 42
7 ** 2;                 // 49
49 % 2;                 // 1

40 + "2";               // "402" (string concatenation)
44 - "2";               // 42 (because "2" is coerced to 2)
21 * "2";               // 42 (..ditto..)
84 / "2";               // 42 (..ditto..)
"7" ** "2";             // 49 (both operands are coerced to numbers)
"49" % "2";             // 1 (..ditto..)
```

Los operadores `+` y `-` también vienen en una forma *unaria*, lo que significa que solo tienen un operando; de nuevo, se espera que el operando sea un number, y es coercionado a number si no lo es:

```js
+42;                    // 42
-42;                    // -42

+"42";                  // 42
-"42";                  // -42
```

Puede que hayas notado que `-42` parece ser simplemente un literal numérico "cuarenta y dos negativo". Eso no es del todo correcto. Un matiz de la sintaxis de JS es que no reconoce literales numéricos negativos. En cambio, JS trata esto como un literal numérico positivo `42` que está precedido, y negado, por el operador unario `-` delante de él.

Entonces, de manera algo sorprendente:

```js
-42;                    // -42
- 42;                   // -42
-
    42;                 // -42
```

Como puedes ver, el espacio en blanco (e incluso las nuevas líneas) están permitidos entre el operador unario `-` y su operando; en realidad, esto es verdad para todos los operadores y operandos.

#### Incremento y Decremento

Hay otros dos operadores numéricos unarios: `++` (incremento) y `--` decremento. Ambos realizan su respectiva operación y luego reasignan el resultado al operando -- debe ser un objetivo de asignación válido como una variable o propiedad.

Puedes pensar en cierto modo en `++` como equivalente a `+= 1`, y `--` como equivalente a `-= 1`:

```js
myAge = 42;

myAge++;
myAge;                  // 43

numberOfHeadHairs--;
```

Sin embargo, estos son operadores especiales en el sentido de que pueden aparecer en una posición postfija (después del operando), como arriba, o en una posición prefija (antes del operando):

```js
myAge = 42;

++myAge;
myAge;                  // 43

--numberofHeadHairs;
```

Puede parecer peculiar que las posiciones prefija y postfija parezcan dar el mismo resultado (incrementar o decrementar) en tales ejemplos. La diferencia es sutil, y no está relacionada con el resultado reasignado final. Revisitaremos estos operadores en particular en un capítulo posterior para profundizar en las diferencias posicionales.

### Operadores Bit a Bit

JS provee varios operadores bit a bit para realizar operaciones a nivel de bit sobre valores number.

Sin embargo, estas operaciones de bit no se realizan contra el patrón de bits empaquetado de los numbers IEEE-754 (consulta el Capítulo 1). En cambio, el number operando primero se convierte a un *entero* con signo de 32 bits, se realiza la operación de bit, y luego el resultado se convierte de vuelta en un number IEEE-754.

Ten en cuenta que, al igual que cualquier otro operador de primitivos, estos solo computan nuevos valores, sin modificar realmente un valor en su lugar.

* `&` (AND bit a bit): Realiza una operación AND con cada bit correspondiente de los dos operandos; `42 & 36 === 32` (es decir, `0b00...101010 & 0b00...100100 === 0b00..100000`)

* `|` (OR bit a bit): Realiza una operación OR con cada bit correspondiente de los dos operandos; `42 | 36 === 46` (es decir, `0b00...101010 | 0b00...100100 === 0b00...101110`)

* `^` (XOR bit a bit): Realiza una operación XOR (OR-eXclusivo) con cada bit correspondiente de los dos operandos; `42 ^ 36 === 14` (es decir, `0b00...101010 ^ 0b00...100100 === 0b00...001110`)

* `~` (NOT bit a bit): Realiza una operación NOT contra los bits de un solo operando; `~42 === -43` (es decir, `~0b00...101010 === 0b11...010101`); usando complemento a 2, el entero con signo tiene el primer bit establecido en `1` lo que significa negativo, y el resto de los bits (cuando se vuelven a invertir, según el complemento a 2, que es la inversión de bits del complemento a 1 y luego sumar `1`) sería `43` (`0b10...101011`); el equivalente de `~` en la aritmética de numbers decimales es `~x === -(x + 1)`, así que `~42 === -43`

* `<<` (desplazamiento a la izquierda): Realiza un desplazamiento a la izquierda de los bits del operando izquierdo por la cantidad de bits especificada por el operando derecho; `42 << 3 == 336` (es decir, `0b00...101010 << 3 === 0b00...101010000`)

* `>>` (desplazamiento a la derecha): Realiza un desplazamiento a la derecha con propagación de signo de los bits del operando izquierdo por la cantidad de bits especificada por el operando derecho, descartando los bits que caen por el lado derecho; sea cual sea el bit más a la izquierda (`0`, o `1` es negativo) se copia como bits a la izquierda (preservando así el signo del valor original en el resultado); `42 >> 3 === 5` (es decir, `0b00..101010 >> 3 === 0b00...000101`)

* `>>>` (desplazamiento a la derecha con relleno de cero, es decir, desplazamiento a la derecha sin signo): Realiza el mismo desplazamiento a la derecha que `>>`, pero rellena con `0` los bits desplazados que entran por el lado izquierdo en lugar de copiar el bit más a la izquierda (ignorando así el signo del valor original en el resultado); `42 >>> 3 === 5` pero `-43 >>> 3 === 536870906` (es decir, `0b11...010101 >>> 3 === 0b0001...111010`)

* `&=`, `|=`, `<<=`, `>>=`, y `>>>=` (operadores bit a bit con asignación): Realizan la operación bit a bit correspondiente, pero luego asignan el resultado al operando izquierdo (que debe ser un objetivo de asignación válido, como una variable o propiedad, no solo un valor literal); nota que `~=` falta en la lista, porque no existe tal operador de "negación binaria con asignación"

Honestamente, las operaciones bit a bit no son muy comunes en JS. Pero a veces puedes ver una sentencia como:

```js
myGPA = 3.54;

myGPA | 0;              // 3
```

Dado que los operadores bit a bit actúan solo sobre enteros de 32 bits, la operación `| 0` trunca (es decir, `Math.trunc(..)`) cualquier valor decimal, dejando solo el entero.

| ADVERTENCIA: |
| :--- |
| Un concepto erróneo común es que `| 0` es como *floor* (es decir, `Math.floor(..)`). El resultado de `| 0` coincide con `Math.floor(..)` en numbers positivos, pero difiere en numbers negativos, porque por definición estándar, *floor* es una operación que redondea hacia abajo hacia `-Infinity`. `| 0` simplemente descarta los bits decimales, lo que es de hecho truncamiento. |

### Métodos de los Valores Number

Los valores number proveen los siguientes métodos (como propiedades) para operaciones específicas de numbers:

* `toExponential(..)`: produce una representación en string del number usando notación científica (p. ej., `"4.2e+1"`)

* `toFixed(..)`: produce una representación en string en notación no-científica del number con el número especificado de lugares decimales (redondeando o rellenando con ceros según sea necesario)

* `toPrecision(..)`: como `toFixed(..)`, excepto que aplica el argumento numérico como el número de dígitos significativos (es decir, precisión) incluyendo tanto el número entero como los lugares decimales si los hay

* `toLocaleString(..)`: produce una representación en string del number según el locale actual

```js
myAge = 42;

myAge.toExponential(3);         // "4.200e+1"
```

Un matiz particular de la sintaxis de JS es que `.` puede ser ambiguo al tratar con literales number y el acceso a propiedades/métodos.

Si un `.` viene inmediatamente (sin espacio en blanco) después de un dígito de un literal numérico, y no hay ya un `.` decimal en el valor number, se asume que el `.` está comenzando la porción decimal del number. Pero si la posición del `.` inequívocamente *no* es parte del literal numérico, entonces siempre se trata como un acceso a propiedad.

```js
42 .toExponential(3);           // "4.200e+1"
```

Aquí, el espacio en blanco desambigua el `.`, designándolo como un acceso a propiedad/método. Quizás es más común/preferido usar `(..)` en lugar de espacio en blanco para tal desambiguación:

```js
(42).toExponential(3);          // "4.200e+1"
```

Un efecto de apariencia inusual de esta regla de gramática de parseo de JS:

```js
42..toExponential(3);           // "4.200e+1"
```

Llamado el idiom del "doble-punto", el primer `.` en esta expresión es un decimal, y por lo tanto el segundo `.` inequívocamente *no* es un decimal, sino más bien un acceso a propiedad/método.

También, nota que no hay dígitos después del primer `.`; es sintaxis perfectamente legal dejar un `.` final en un literal numérico:

```js
myAge = 41. + 1.;

myAge;                          // 42
```

Los valores de type `bigint` no pueden tener decimales, así que el parseo es inequívoco de que un `.` después de un literal (con la `n` final) siempre es un acceso a propiedad:

```js
42n.toString();                 // 42
```

### Propiedades Estáticas de `Number`

* `Number.EPSILON`: El valor más pequeño posible entre `1` y el siguiente number más alto

* `Number.NaN`: Lo mismo que el símbolo global `NaN`, el number inválido especial

* `Number.MIN_SAFE_INTEGER` / `Number.MAX_SAFE_INTEGER`: Los enteros positivo y negativo con el mayor valor absoluto (más lejanos de `0`)

* `Number.MIN_VALUE` / `Number.MAX_VALUE`: El mínimo (valor positivo más cercano a `0`) y el máximo (valor positivo más lejano de `0`) representable por el type number

* `Number.NEGATIVE_INFINITY` / `Number.POSITIVE_INFINITY`: Lo mismo que los globales `-Infinity` e `Infinity`, los valores que representan los valores más grandes (no-finitos) más lejanos de `0`

### Ayudantes Estáticos de `Number`

* `Number.isFinite(..)`: devuelve un boolean que indica si el valor es finito -- un number que no es `NaN`, ni uno de los dos infinitos

* `Number.isInteger(..)` / `Number.isSafeInteger(..)`: ambos devuelven booleans que indican si el valor es un number entero sin lugares decimales, y si está dentro del rango *seguro* para enteros (`-2^53 + 1` - `2^53 - 1`)

* `Number.isNaN(..)`: La versión con el bug corregido de la utilidad global `isNaN(..)`, que identifica si el argumento provisto es el valor especial `NaN`

* `Number.parseFloat(..)` / `Number.parseInt(..)`: utilidades para parsear valores string en busca de dígitos numéricos, de izquierda a derecha, hasta el final del string o el primer carácter no-flotante (o no-entero) que se encuentre

### Espacio de Nombres Estático `Math`

Dado que el uso principal de los valores number es realizar operaciones matemáticas, JS incluye muchas constantes matemáticas estándar y utilidades de operación en el espacio de nombres `Math`.

Hay un montón de estas, así que omitiré listar cada una. Pero aquí hay algunas con fines ilustrativos:

```js
Math.PI;                        // 3.141592653589793

// absolute value
Math.abs(-32.6);                // 32.6

// rounding
Math.round(-32.6);              // -33

// min/max selection
Math.min(100,Math.max(0,42));   // 42
```

A diferencia de `Number`, que también es la función `Number(..)` (para la coerción de numbers), `Math` es solo un objeto que contiene estas propiedades y utilidades de función estáticas; no puede ser llamado como una función.

| ADVERTENCIA: |
| :--- |
| Un miembro peculiar del espacio de nombres `Math` es `Math.random()`, para producir un valor de punto flotante aleatorio entre `0` y `1.0`. Es inusual considerar la generación de numbers aleatorios -- una tarea que es inherentemente con estado/con efectos secundarios -- como una operación matemática. También ha sido durante mucho tiempo un footgun en términos de seguridad, ya que el generador de numbers pseudo-aleatorios (PRNG) que JS usa *no* es seguro (puede predecirse) desde una perspectiva de criptografía. La plataforma web intervino hace varios años con la API más segura `crypto.getRandomValues(..)` (basada en un mejor PRNG), que llena un typed-array con bits aleatorios que pueden interpretarse como uno o más enteros (de magnitud máxima especificada por el type). El uso de `Math.random()` está universalmente desaconsejado ahora. |

### Los BigInts y los Numbers No Se Mezclan

Como cubrimos en el Capítulo 1, los valores de type number y type bigint no pueden mezclarse en las mismas operaciones. Eso puede hacerte tropezar incluso si estás haciendo un simple incremento del valor (como en un bucle):

```js
myAge = 42n;

myAge + 1;                  // TypeError thrown!
myAge += 1;                 // TypeError thrown!

myAge + 1n;                 // 43n
myAge += 1n;                // 43n

myAge++;
myAge;                      // 44n
```

Como tal, si estás usando ambos valores number y bigint en tus programas, necesitarás coercionar manualmente un value type al otro con cierta regularidad. La función `BigInt(..)` (sin la palabra clave `new`) puede coercionar un valor number a bigint. Viceversa, para ir en la otra dirección de bigint a number, usa la función `Number(..)` (de nuevo, sin la palabra clave `new`):

```js
BigInt(42);                 // 42n

Number(42n);                // 42
```

Ten en cuenta sin embargo: coercionar entre estos types tiene cierto riesgo:

```js
BigInt(4.2);                // RangeError thrown!
BigInt(NaN);                // RangeError thrown!
BigInt(Infinity);           // RangeError thrown!

Number(2n ** 1024n);        // Infinity
```

## Los Primitivos Son Fundacionales

A lo largo de los últimos dos capítulos, nos hemos metido a fondo en cómo se comportan los valores primitivos en JS. Apuesto a que más de unos pocos lectores estaban, como yo, listos para saltarse estos temas. Pero ahora, con suerte, ves la importancia de entender estos conceptos.

Sin embargo, la historia no termina aquí. ¡Para nada! En el próximo capítulo, dirigiremos nuestra atención a entender los object types de JS (objetos, arrays, etc).

[^TwitterUnicode]: "New update to the Twitter-Text library: Emoji character count"; Andy Piper; Oct 2018; https://twittercommunity.com/t/new-update-to-the-twitter-text-library-emoji-character-count/114607 ; Accedido en Julio 2022

[^INTLAPI]: ECMAScript 2022 Internationalization API Specification; https://402.ecma-international.org/9.0/ ; Accedido en Agosto 2022

[^INTLCollator]: "Intl.Collator", MDN; https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator ; Accedido en Agosto 2022

[^INTLSegmenter]: "Intl.Segmenter", MDN; https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter ; Accedido en Agosto 2022

[^StrictEquality]: "7.2.16 IsStrictlyEqual(x,y)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-isstrictlyequal ; Accedido en Agosto 2022

[^LooseEquality]: "7.2.15 IsLooselyEqual(x,y)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-islooselyequal ; Accedido en Agosto 2022

[^EpsilonBad]: "PLEASE don't follow the code recipe in the accepted answer", Stack Overflow; Daniel Scott; July 2019; https://stackoverflow.com/a/56967003/228852 ; Accedido en Agosto 2022
