# You Don't Know JS Yet: Types & Grammar - 2nd Edition
# Capítulo 1: Valores Primitivos

| NOTA: |
| :--- |
| Trabajo en progreso |

En el Capítulo 1 del libro "Objects & Classes" de esta serie, confrontamos el error común de creer que "todo en JS es un objeto". Ahora volvemos a ese tema y, una vez más, desmentimos ese mito.

Aquí veremos los tipos de valor centrales de JS, específicamente los tipos que no son objetos, llamados *primitivos*.

## Tipos de Valor

JS no aplica types a las variables ni a las propiedades -- lo que yo llamo "tipos contenedores" -- sino que los valores en sí mismos tienen types -- lo que yo llamo "tipos de valor".

El lenguaje provee siete tipos de valor primitivos (no objeto) incorporados: [^PrimitiveValues]

* `undefined`
* `null`
* `boolean`
* `number`
* `bigint`
* `symbol`
* `string`

Estos tipos de valor definen colecciones de uno o más valores concretos, cada uno con un conjunto de comportamientos compartidos por todos los valores de cada type.

### Type-Of

El tipo de cualquier valor puede inspeccionarse mediante el operador `typeof`, que siempre devuelve un valor `string` que representa el tipo de valor JS subyacente:

```js
typeof true;            // "boolean"

typeof 42;              // "number"

typeof 42n;             // "bigint"

typeof Symbol("42");    // "symbol"
```

El operador `typeof`, cuando se usa sobre una variable en lugar de un valor, reporta el tipo de valor de *el valor contenido en la variable*:

```js
greeting = "Hello";
typeof greeting;        // "string"
```

Las variables de JS en sí mismas no tienen types. Contienen cualquier valor arbitrario, el cual, a su vez, tiene un tipo de valor.

### ¿No-objetos?

¿Qué hace específicamente que los 7 tipos de valor primitivos sean distintos de los tipos de valor objeto (y sus subtipos)? ¿Por qué no deberíamos simplemente considerarlos a todos como esencialmente *objetos* por debajo?

Considerá:

```js
myName = "Kyle";

myName.nickname = "getify";

console.log(myName.nickname);           // undefined
```

Este fragmento parece fallar silenciosamente al intentar agregar una propiedad `nickname` a un string primitivo. Tomado al pie de la letra, eso podría dar a entender que los primitivos son en realidad objetos por debajo, como muchos han afirmado (erróneamente) a lo largo de los años.

| ADVERTENCIA: |
| :--- |
| Uno podría explicar esa falla silenciosa como un ejemplo de *auto-boxing* (ver "Objetos Automáticos" en el Capítulo 3), donde el primitivo se convierte implícitamente en un objeto envoltorio de instancia `String` al intentar asignar la propiedad, y luego ese objeto interno se descarta una vez que la sentencia se completa. De hecho, dije exactamente eso en la primera edición de este libro. ¡Pero estaba equivocado; ups! |

Algo más profundo está en juego, como vemos en esta versión del fragmento anterior:

```js
"use strict";

myName = "Kyle";

myName.nickname = "getify";
// TypeError: Cannot create property 'nickname'
// on string 'Kyle'
```

¡Interesante! En strict-mode, JS impone una restricción que prohíbe asignar una nueva propiedad a un valor primitivo, como si lo promoviera implícitamente a un nuevo objeto.

En cambio, en modo no estricto, JS permite que la violación pase sin mención. ¿Y por qué? Porque strict-mode se agregó al lenguaje en ES5.1 (2011), más de 15 años después, y un cambio así habría roto programas existentes de no haberse definido como sensible a la nueva declaración strict-mode.

Entonces, ¿qué podemos concluir sobre la distinción entre primitivos y objetos? Los primitivos son valores a los que *no se les permite tener propiedades*; solo los objetos tienen permitido eso.

| TIP: |
| :--- |
| Esta distinción en particular parece contradecirse con expresiones como `"hello".length`; incluso en strict-mode, devuelve el valor esperado `5`. ¡Así que ciertamente *parece* que el string tiene una propiedad `length`! Pero, como se mencionó recién, la explicación correcta es el *auto-boxing*; cubriremos el tema en "Objetos Automáticos" en el Capítulo 3. |

## Valores Vacíos

Los types `null` y `undefined` típicamente representan un vacío o una ausencia de valor.

Desafortunadamente, el tipo de valor `null` tiene un resultado de `typeof` inesperado. En lugar de `"null"`, vemos:

```js
typeof null;            // "object"
```

No, eso no significa que `null` sea de algún modo una clase especial de objeto. Es solo una herencia de los primeros días de JS, que no puede cambiarse por la cantidad de código circulante que rompería.

El type `undefined` se reporta tanto para valores `undefined` explícitos como para cualquier lugar donde se encuentre un valor aparentemente faltante:

```js
typeof undefined;               // "undefined"

var whatever;

typeof whatever;                // "undefined"
typeof nonExistent;             // "undefined"

whatever = {};
typeof whatever.missingProp;    // "undefined"

whatever = [];
typeof whatever[10];            // "undefined"
```

| NOTA: |
| :--- |
| La expresión `typeof nonExistent` se refiere a una variable no declarada `nonExistent`. Normalmente, acceder a una referencia de variable no declarada provocaría una excepción, pero al operador `typeof` se le concede la capacidad especial de acceder de forma segura incluso a identificadores inexistentes y devolver tranquilamente `"undefined"` en lugar de lanzar una excepción. |

Sin embargo, cada type "vacío" respectivo tiene exactamente un valor, con el mismo nombre. Así que `null` es el único valor en el tipo de valor `null`, y `undefined` es el único valor en el tipo de valor `undefined`.

### Null'ish

Semánticamente, los types `null` y `undefined` representan ambos un vacío general, o la ausencia de otro valor afirmativo y significativo.

| NOTA: |
| :--- |
| A las operaciones de JS que se comportan igual tanto si encuentran `null` como `undefined` se las denomina "null'ish" (o "nullish"). ¡Supongo que "undefined'ish" se vería/sonaría demasiado raro! |

Para gran parte de JS, especialmente el código que escriben los desarrolladores, estos dos valores *nullish* son intercambiables; la decisión de usar/asignar intencionalmente `null` o `undefined` en un escenario dado depende de la situación y queda a criterio del desarrollador.

JS provee una serie de capacidades para ayudar a tratar los dos valores nullish como indistinguibles.

Por ejemplo, el operador `==` (comparación de igualdad coercitiva) trata específicamente a `null` y `undefined` como coercitivamente iguales entre sí, pero a ningún otro valor del lenguaje. Como tal, una verificación `.. == null` es segura de realizar si querés comprobar si un valor es específicamente `null` o `undefined`:

```js
if (greeting == null) {
    // greeting is nullish/empty
}
```

Otra adición (reciente) a JS es el operador `??` (coalescencia nullish):

```js
who = myName ?? "User";

// equivalent to:
who = (myName != null) ? myName : "User";
```

Como ilustra el equivalente ternario, `??` comprueba si `myName` es no-nullish y, de ser así, devuelve su valor. De lo contrario, devuelve el otro operando (aquí, `"User"`).

Junto con `??`, JS también agregó el operador `?.` (encadenamiento condicional nullish):

```js
record = {
    shippingAddress: {
        street: "123 JS Lane",
        city: "Browserville",
        state: "XY"
    }
};

console.log( record?.shippingAddress?.street );
// 123 JS Lane

console.log( record?.billingAddress?.street );
// undefined
```

El operador `?.` comprueba el valor inmediatamente precedente (a la izquierda) y, si es nullish, el operador se detiene y devuelve un valor `undefined`. De lo contrario, realiza el acceso a la propiedad con `.` sobre ese valor y continúa con la expresión.

Para que quede claro: `record?.` está diciendo, "comprobá `record` por nullish antes del acceso a propiedad con `.`". Adicionalmente, `billingAddress?.` está diciendo, "comprobá `billingAddress` por nullish antes del acceso a propiedad con `.`".

| ADVERTENCIA: |
| :--- |
| Algunos desarrolladores de JS creen que el más nuevo `?.` es superior a `.`, y que por lo tanto debería usarse casi siempre en lugar de `.`. Yo creo que esa es una perspectiva imprudente. En primer lugar, agrega ruido visual extra, lo cual solo debería hacerse si obtenés un beneficio de ello. En segundo lugar, deberías ser consciente de, y planificar para, el vacío de algún valor, para justificar el uso de `?.`. Si siempre esperás que un valor no-nullish esté presente en alguna expresión, usar `?.` para acceder a una propiedad en él no solo es innecesario/derrochador, sino que además podría potencialmente ocultar bugs futuros donde tu suposición de presencia de valor falló pero `?.` lo tapó. Como con la mayoría de las características en JS, usá `.` donde sea más apropiado, y usá `?.` donde sea más apropiado. Nunca sustituyas uno cuando el otro es más apropiado. |

También existe una forma algo extraña del operador, `?.[`, no `?[`, para cuando necesitás usar acceso de estilo `[ .. ]` en lugar de acceso con `.`:

```js
record?.["shipping" + "Address"]?.state;    // XY
```

Otra variación más, denominada "llamada opcional", es `?.(`, y se usa cuando se llama condicionalmente a una función si el valor es no-nullish:

```js
// instead of:
//   if (someFunc) someFunc(42);
//
// or:
//   someFunc && someFunc(42);

someFunc?.(42);
```

El operador `?.(` parece estar comprobando si `someFunc(..)` es una función válida que puede ser llamada. ¡Pero no lo hace! Solo está comprobando que el valor sea no-nullish antes de intentar invocarlo. Si es algún otro tipo de valor no-nullish pero tampoco función, el intento de ejecución igual fallará con una excepción `TypeError`.

| ADVERTENCIA: |
| :--- |
| Debido a ese gotcha, me *disgusta mucho* esta forma del operador, y advierto a cualquiera que no lo use nunca. Creo que es una característica mal concebida que hace más daño (a JS mismo, y a los programas) que bien. Hay muy pocas características de JS de las que iría tan lejos como para decir, "nunca la uses". Pero esta es una de las partes verdaderamente *malas* del lenguaje, en mi opinión. |

### Distinct'ish

Es importante tener en cuenta que `null` y `undefined` *son* en realidad types distintos y, por lo tanto, `null` puede ser notablemente diferente de `undefined`. Podés, con cuidado, construir programas que mayormente los traten como indistinguibles. Pero eso requiere cuidado y disciplina por parte del desarrollador. Desde la perspectiva de JS, son más a menudo distintos.

Hay casos en los que `null` y `undefined` activarán comportamientos diferentes del lenguaje, lo cual es importante tener presente. No cubriremos todos los casos de forma exhaustiva aquí, pero acá hay un ejemplo:

```js
function greet(msg = "Hello") {
    console.log(msg);
}

greet();            // Hello
greet(undefined);   // Hello
greet("Hi");        // Hi

greet(null);        // null
```

La cláusula `= ..` en un parámetro se denomina el "valor por defecto del parámetro". Solo entra en acción y asigna su valor por defecto al parámetro si el argumento en esa posición está ausente, o es exactamente el valor `undefined`. Si pasás `null`, esa cláusula no se activa, y así `null` queda asignado al parámetro.

No hay una forma *correcta* o *incorrecta* de usar `null` o `undefined` en un programa. Así que la conclusión es: tené cuidado al elegir un valor u otro. Y si los estás usando de forma intercambiable, tené cuidado extra.

## Valores Boolean

El type `boolean` contiene dos valores: `false` y `true`.

En los "viejos tiempos", los lenguajes de programación, por convención, usaban `0` para significar `false` y `1` para significar `true`. Así que podés pensar en el type `boolean`, y en las palabras clave `false` y `true`, como un azúcar semántico conveniente por encima de los valores `0` y `1`:

```js
// isLoggedIn = 1;
isLoggedIn = true;

isComplete = 0;
// isComplete = false;
```

Los valores boolean son el modo en que toda la toma de decisiones ocurre en un programa JS:

```js
if (isLoggedIn) {
    // do something
}

while (!isComplete) {
    // keep going
}
```

El operador `!` niega/invierte un valor boolean al otro: `false` se vuelve `true`, y `true` se vuelve `false`.

## Valores String

El type `string` contiene cualquier valor que sea una colección de uno o más caracteres, delimitado (rodeado a ambos lados) por caracteres de comillas:

```js
myName = "Kyle";
```

JS no distingue un solo carácter como un type diferente como hacen algunos lenguajes; `"a"` es un string igual que `"abc"` lo es.

Los strings pueden delimitarse con comillas dobles (`"`), comillas simples (`'`), o acentos graves (`` ` ``). El delimitador de cierre siempre debe coincidir con el delimitador de apertura.

Los strings tienen una longitud intrínseca que corresponde a cuántos code-points -- en realidad, code-units, más sobre eso en un momento -- contienen.

```js
myName = "Kyle";

myName.length;      // 4
```

Esto no necesariamente corresponde a la cantidad de caracteres visibles presentes entre los delimitadores de inicio y fin (es decir, el literal string). A veces puede ser un poco confuso mantener clara la diferencia entre un literal string y el valor string subyacente, así que prestá mucha atención.

| NOTA: |
| :--- |
| Cubriremos el cálculo de longitud de strings en detalle, en el Capítulo 2. |

### Codificaciones de Caracteres de JS

¿Qué tipo de codificación de caracteres usa JS para los caracteres de los strings?

Probablemente hayas oído de "Unicode" y quizás incluso de "UTF-8" (8 bits) o "UTF-16" (16 bits). Si sos como yo (antes de hacer la investigación que me llevó escribir este texto), tal vez simplemente lo pasaste por alto y decidiste que eso es todo lo que necesitás saber sobre las codificaciones de caracteres en los strings de JS.

Pero... no lo es. Ni por asomo.

Resulta que necesitás entender cómo funcionan una variedad de aspectos de Unicode, e incluso considerar conceptos de UCS-2 (Universal Character Set de 2 bytes), que es similar a UTF-16, pero no exactamente lo mismo. [^UTFUCS]

Unicode define todos los "caracteres" que podemos representar universalmente en programas de computadora, asignando un número específico a cada uno, llamado code-points. Estos números van desde `0` hasta un máximo de `1114111` (`10FFFF` en hexadecimal).

La notación estándar para caracteres Unicode es `U+` seguido de 4 a 6 caracteres hexadecimales. Por ejemplo, el `❤` (símbolo de corazón) es el code-point `10084` (`2764` en hexadecimal), y por lo tanto se nota con `U+2764`.

El primer grupo de 65.535 code points en Unicode se llama el BMP (Basic Multilingual Plane). Todos estos pueden representarse con 16 bits (2 bytes). Al representar caracteres Unicode del BMP, es bastante directo, ya que *entran* prolijamente en caracteres UTF-16 individuales de JS.

Todos los demás code points están agrupados en 16 planos llamados "planos suplementarios" o "planos astrales". Estos code-points requieren más de 16 bits para representarse -- 21 bits para ser exactos -- así que al representar caracteres extendidos/suplementarios por encima del BMP, JS en realidad almacena estos code-points como un par de dos code units adyacentes de 16 bits, llamados *mitades sustitutas* (o *pares sustitutos*).

Por ejemplo, el code point Unicode `127878` (hexadecimal `1F386`) es `🎆` (símbolo de fuegos artificiales). JS lo almacena en un valor string como dos code units de mitad sustituta: `U+D83C` y `U+DF86`. Tené en cuenta que estas dos partes del carácter completo *no* se sostienen por sí solas; solo son válidas/significativas cuando se emparejan inmediatamente adyacentes una a la otra.

Esto tiene implicancias en la longitud de los strings, porque un solo carácter visible como el símbolo de fuegos artificiales `🎆`, cuando está en un string de JS, se cuenta como 2 caracteres a efectos de la longitud del string.

Revisitaremos los caracteres Unicode en un momento, y luego cubriremos los desafíos de calcular la longitud de los strings en el Capítulo 2.

### Secuencias de Escape

Si se usan `"` o `'` para delimitar un literal string, los contenidos solo se analizan en busca de *secuencias de escape de caracteres*: `\` seguido de uno o más caracteres que JS reconoce y analiza con un significado especial. Cualquier otro carácter en un string que no se analice como secuencia de escape (de un solo carácter o de varios) se inserta tal cual en el valor string.

Para las secuencias de escape de un solo carácter, los siguientes caracteres se reconocen después de un `\`: `b`, `f`, `n`, `r`, `t`, `v`, `0`, `'`, `"`, y `\`. Por ejemplo, `\n` significa nueva línea, `\t` significa tabulación, etc.

Si un `\` va seguido de cualquier otro carácter (excepto `x` y `u` -- explicados abajo), como por ejemplo `\k`, esa secuencia se interpreta como que el `\` es un escape innecesario, que por lo tanto se descarta, dejando solo el carácter literal en sí (`k`).

Para incluir un `"` en medio de un literal string delimitado por `"`, usá la secuencia de escape `\"`. De manera similar, si estás incluyendo un carácter `'` en medio de un literal string delimitado por `'`, usá la secuencia de escape `\'`. En cambio, un `'` *no* necesita ser escapado dentro de un string delimitado por `"`, ni viceversa.

```js
myTitle = "Kyle Simpson (aka, \"getify\"), former O'Reilly author";

console.log(myTitle);
// Kyle Simpson (aka, "getify"), former O'Reilly author
```

En texto, la barra inclinada `/` es la más común. Pero ocasionalmente necesitás una barra invertida `\`. Para incluir un carácter de barra invertida `\` literal sin que actúe como el inicio de una secuencia de escape de caracteres, usá la `\\` (doble barra invertida).

Entonces, ¿como qué se analizaría `\\\` (tres barras invertidas) en un string? Las primeras dos `\` serían una secuencia de escape `\\`, insertando así un solo carácter `\` en el valor string, y la `\` restante simplemente escaparía cualquier carácter que venga inmediatamente después.

Un lugar donde las barras invertidas aparecen comúnmente es en las rutas de archivos de Windows, que usan el separador `\` en lugar del separador `/` usado en las rutas de estilo linux/unix:

```js
windowsFontsPath =
    "C:\\Windows\\Fonts\\";

console.log(windowsFontsPath);
// C:\Windows\Fonts\"
```

| TIP: |
| :--- |
| ¿Qué hay de cuatro barras invertidas `\\\\` en un literal string? Bueno, eso son simplemente dos secuencias de escape `\\` una al lado de la otra, así que resulta en dos barras invertidas adyacentes (`\\`) en el valor string subyacente. Quizás reconozcas que hay un patrón de regla par/impar en juego. Así, deberías poder descifrar cualquier cantidad impar (`\\\\\`, `\\\\\\\\\`, etc) o par (`\\\\\\`, `\\\\\\\\\\`, etc) de barras invertidas en un literal string. |

#### Continuación de Línea

El carácter `\` seguido de un carácter de nueva línea real (no solo la `n` literal) es un caso especial, y crea lo que se llama una continuación de línea:

```js
greeting = "Hello \
Friends!";

console.log(greeting);
// Hello Friends!
```

Como podés ver, la nueva línea al final de la línea `greeting = ` está inmediatamente precedida por un `\`, lo que permite que este literal string continúe en la línea siguiente. Sin el `\` de escape antes de ella, una nueva línea -- la nueva línea real, no la secuencia de escape de caracteres `\n` -- que aparezca en un literal string delimitado por `"` o `'` en realidad produciría un error de análisis de sintaxis de JS.

Debido a que el `\` de fin de línea convierte el carácter de nueva línea en una continuación de línea, el carácter de nueva línea se omite del string, como lo muestra la salida de `console.log(..)`.

| NOTA: |
| :--- |
| Esta característica de continuación de línea a menudo se denomina "strings multilínea", pero creo que esa es una etiqueta confusa. Como podés ver, el valor string en sí no tiene múltiples líneas, solo fue definido a lo largo de múltiples líneas mediante las continuaciones de línea. Un string multilínea en realidad tendría múltiples líneas en el valor subyacente. Revisitaremos este tema más adelante en este capítulo cuando cubramos los Template Literals. |

### Escapes de Varios Caracteres

Las secuencias de escape de varios caracteres pueden ser secuencias hexadecimales o Unicode.

Las secuencias de escape hexadecimales se usan para codificar cualquiera de los caracteres ASCII base (códigos 0-255), y se ven como `\x` seguido de exactamente dos caracteres hexadecimales (`0-9` y `a-f` / `A-F` -- sin distinción de mayúsculas/minúsculas). Por ejemplo, `A9` o `a9` son el valor decimal `169`, que corresponde a:

```js
copyright = "\xA9";  // or "\xa9"

console.log(copyright);     // ©
```

Para cualquier carácter normal que pueda escribirse en un teclado, como `"a"`, suele ser más legible simplemente especificar el carácter literal, en lugar de una representación hexadecimal más ofuscada:

```js
"a" === "\x61";             // true
```

#### Unicode En Strings

Las secuencias de escape Unicode por sí solas pueden codificar cualquiera de los caracteres del BMP de Unicode. Se ven como `\u` seguido de exactamente cuatro caracteres hexadecimales.

Por ejemplo, la secuencia de escape `©` (o `©`) corresponde a ese mismo símbolo `©`, mientras que `☺` (o `☺`) corresponde al carácter Unicode con code-point `9786`: `☺` (símbolo de carita sonriente).

Cuando se reconoce cualquier secuencia de escape de caracteres (sin importar la longitud), el único carácter que representa se inserta en el string, en lugar de los caracteres separados originales. Así, en el string `"☺"`, hay solo un carácter (carita sonriente), no seis caracteres individuales.

Pero como se explicó antes, muchos code-points Unicode están muy por encima de `65535`. Por ejemplo, `1F4A9` (o `1f4a9`) es el code-point decimal `128169`, que corresponde al gracioso símbolo `💩` (montón de caca).

Pero `Ὂ9` no funcionaría para incluir este carácter en un string, ya que se analizaría como la secuencia de escape Unicode `Ὂ`, seguida de un carácter `9` literal. Para abordar esta limitación, se introdujo una variación de las secuencias de escape Unicode que permite una cantidad arbitraria de caracteres hexadecimales después del `\u`, rodeándolos con llaves `{ .. }`:

```js
myReaction = "\u{1F4A9}";

console.log(myReaction);
// 💩
```

¿Recordás la discusión anterior sobre los caracteres Unicode extendidos (no-BMP) y las *mitades sustitutas*? El mismo `💩` también podría definirse con dos code-units explícitos, que forman un par sustituto:

```js
myReaction = "💩";

console.log(myReaction);
// 💩
```

Las tres representaciones de este mismo carácter se almacenan internamente por JS de forma idéntica, y son indistinguibles:

```js
"💩" === "\u{1F4A9}";                // true
"\u{1F4A9}" === "💩";     // true
```

Aunque a JS no le importa de qué manera se represente tal carácter en tu programa, considerá cuidadosamente las diferencias de legibilidad al escribir tu código.

| NOTA: |
| :--- |
| Aunque `💩` parece un solo carácter, su representación interna afecta cosas como el cálculo de longitud de un string que contenga ese carácter. Cubriremos el cálculo de longitud de strings en el Capítulo 2. |

##### Normalización Unicode

Otra complicación en el manejo de strings Unicode es que incluso ciertos caracteres individuales del BMP pueden representarse de distintas formas.

Por ejemplo, el carácter `"é"` puede representarse ya sea como sí mismo (code-point `233`, es decir `\xe9` o `é` o `\u{e9}`), o como la combinación de dos code-points: el carácter `"e"` (code-point `101`, es decir `\x65`, `e`, `\u{65}`) y la *tilde combinante* (code-point `769`, es decir `́`, `\u{301}`).

Considerá:

```js
eTilde1 = "é";
eTilde2 = "é";
eTilde3 = "é";

console.log(eTilde1);       // é
console.log(eTilde2);       // é
console.log(eTilde3);       // é
```

El literal string asignado a `eTilde3` en este fragmento almacena la marca de acento como un símbolo de *marca combinante* separado. Al igual que los pares sustitutos, una marca combinante solo tiene sentido en conexión con el símbolo al que está adyacente (usualmente después).

El renderizado del símbolo Unicode debería ser el mismo sin importar nada, pero cómo se almacena internamente el carácter `"é"` afecta cosas como el cálculo de `length` del string que lo contiene, así como la comparación de igualdad y relacional (más sobre esto en el Capítulo 2):

```js
eTilde1.length;             // 2
eTilde2.length;             // 1
eTilde3.length;             // 2

eTilde1 === eTilde2;        // false
eTilde1 === eTilde3;        // true
```

Un desafío particular es que podés copiar y pegar un string con un carácter `"é"` visible en él, y ese carácter que copiaste puede haber estado en la forma *compuesta* o *descompuesta*. Pero no hay manera visual de distinguirlo, y aun así el valor string subyacente en el literal será diferente:

```js
"é" === "é";           // false!!
```

Esta diferencia de representación interna puede ser bastante desafiante si no se planifica cuidadosamente. Afortunadamente, JS provee un método utilitario `normalize(..)` en los strings para ayudar:

```js
eTilde1 = "é";
eTilde2 = "\u{e9}";
eTilde3 = "\u{65}\u{301}";

eTilde1.normalize("NFC") === eTilde2;
eTilde2.normalize("NFD") === eTilde3;
```

El modo de normalización `"NFC"` combina code-points adyacentes en el code-point *compuesto* (si es posible), mientras que el modo de normalización `"NFD"` divide un solo code-point en sus code-points *descompuestos* (si es posible).

Y en realidad puede haber más de dos code-points *descompuestos* individuales que conforman un solo code-point *compuesto* -- por ejemplo, un solo carácter podría tener varias marcas diacríticas aplicadas.

Al trabajar con strings Unicode que serán comparados, ordenados o analizados por longitud, es muy importante tener presente la normalización Unicode, y usarla donde sea necesario.

##### Clusters de Grafemas Unicode

Una complicación final del manejo de strings Unicode es el soporte para el agrupamiento de múltiples code-points adyacentes en un solo símbolo visualmente distinto, denominado un *grafema* (o un *cluster de grafemas*).

Un ejemplo sería un emoji de familia como `"👩‍👩‍👦‍👦"`, que en realidad está compuesto de 7 code-points que todos se agrupan juntos en un solo símbolo visual.

Considerá:

```js
familyEmoji = "\u{1f469}\u{200d}\u{1f469}\u{200d}\u{1f466}\u{200d}\u{1f466}";

familyEmoji;            // 👩‍👩‍👦‍👦
```

Este emoji *no* es un solo code-point Unicode registrado, y como tal, no hay ninguna *normalización* que pueda realizarse para componer estos 7 code-points separados en una sola entidad. La lógica de renderizado visual para tales símbolos compuestos es bastante compleja, mucho más allá de lo que la mayoría de los desarrolladores de JS quieren incrustar en nuestros programas. Existen librerías para manejar parte de esta lógica, pero suelen ser grandes y aun así no necesariamente cubren todos los matices/variaciones.

A diferencia de los pares sustitutos y las marcas combinantes, los símbolos en los clusters de grafemas de hecho pueden actuar como caracteres independientes, pero tienen el comportamiento combinante especial cuando se colocan adyacentes entre sí.

Este tipo de complejidad afecta significativamente los cálculos de longitud, la comparación, el ordenamiento, y muchas otras operaciones comunes orientadas a strings.

### Template Literals

Mencioné antes que los strings pueden alternativamente delimitarse con acentos graves `` `..` ``:

```js
myName = `Kyle`;
```

Todas las mismas reglas para las codificaciones de caracteres, las secuencias de escape de caracteres, y las longitudes aplican a este tipo de strings.

Sin embargo, los contenidos de estos literales de plantilla (template literals) adicionalmente se analizan en busca de una secuencia delimitadora especial `${ .. }`, que marca una expresión a evaluar e interpolar en el valor string en esa ubicación:

```js
myName = `Kyle`;

greeting = `Hello, ${myName}!`;

console.log(greeting);      // Hello, Kyle!
```

Todo lo que está entre las `{ .. }` en un template literal de este tipo es una expresión arbitraria de JS. Puede ser variables simples como `myName`, o programas complejos de JS, o cualquier cosa intermedia (¡incluso otra expresión de template literal!).

| TIP: |
| :--- |
| A esta característica comúnmente se la llama "template literals" o "template strings", pero creo que eso es confuso. "Template" (plantilla) usualmente significa, en contextos de programación, un conjunto reutilizable de texto que puede reevaluarse con datos diferentes. Por ejemplo, los *motores de plantillas* para páginas, las plantillas de email para campañas de newsletter, etc. Esta característica de JS no es reutilizable. Es un literal, y produce un solo valor inmediato (usualmente un string). Podés poner tal valor en una función, y llamar a la función múltiples veces. Pero entonces la función está actuando como la plantilla, no el literal en sí. Yo prefiero en cambio referirme a esta característica como *literales interpolados*, o el gracioso diminutivo: *interpoliterales*. Simplemente creo que ese nombre es más precisamente descriptivo. |

Los template literals también tienen un comportamiento interesantemente diferente respecto de las nuevas líneas, comparados con los strings clásicos delimitados por `"` o `'`. Recordá que, para esos strings, una continuación de línea requería un `\` al final de cada línea, justo antes de una nueva línea. ¡No es así con los template literals!

```js
myPoem = `
Roses are red
Violets are blue
C3PO's a funny robot
and so R2.`;

console.log(myPoem);
//
// Roses are red
// Violets are blue
// C3PO's a funny robot
// and so R2.
```

Las continuaciones de línea con template literals *no requieren* escape. Sin embargo, eso significa que la nueva línea es parte del string, incluso la primera nueva línea de arriba. En otras palabras, `myPoem` arriba contiene un verdadero *string multilínea*, como se muestra. No obstante, si escapás con `\` el final de cualquier línea en un template literal, la nueva línea se omitirá, igual que con los strings que no son template literals.

Los template literals usualmente resultan en un valor string, pero no siempre. Una forma de template literal que puede verse algo extraña se llama *tagged template literal* (template literal etiquetado):

```js
price = formatCurrency`The cost is: ${totalCost}`;
```

Aquí, `formatCurrency` es una etiqueta aplicada al valor template literal, que en realidad invoca `formatCurrency(..)` como función, pasándole los literales string y las expresiones interpoladas analizadas del valor. Esta función puede entonces ensamblarlos de la manera que considere conveniente -- como formatear un valor `number` como moneda en el locale actual -- y devolver cualquier valor, string o de otro tipo, que quiera.

Así que los tagged template literals no siempre son strings; pueden ser cualquier valor. Pero los template literals sin etiqueta *siempre serán* strings.

Algunos desarrolladores de JS creen que los strings de template literal sin etiqueta son los mejores para usar en *todos* los strings, incluso si no se usa ninguna interpolación de expresiones ni múltiples líneas. Yo disiento. Creo que solo deberían usarse al interpolar (o hacer multilínea).

| TIP: |
| :--- |
| El principio que siempre aplico al hacer tales determinaciones: usá la característica/herramienta más cercana a lo que necesitás, y la menos capaz, para cualquier tarea. |

Más aún, hay unos pocos lugares donde los strings de estilo `` `..` `` están prohibidos. Por ejemplo, el pragma `"use strict"` no puede usar acentos graves, o el pragma se ignorará silenciosamente (y así el programa correrá accidentalmente en modo no estricto). Además, este estilo de strings no puede usarse en nombres de propiedades entrecomillados de literales de objeto, patrones de destructuring, ni en la cláusula de especificador de módulo `import .. from ..` de los ES Module.

Mi postura: usá strings delimitados por `` `..` `` donde esté permitido, pero solo cuando se necesite interpolación/multilínea; y seguí usando strings delimitados por `".."` o `'..'` para todo lo demás.

## Valores Number

El type `number` contiene cualquier valor numérico (número entero o decimal), como `-42` o `3.1415926`. Estos valores son representados por el engine de JS como valores binarios de punto flotante de doble precisión IEEE-754 de 64 bits. [^IEEE754]

Los `number` de JS son siempre decimales; los números enteros (es decir, "integers") no se almacenan de una manera diferente/especial. Un "integer" almacenado como valor `number` meramente no tiene nada distinto de cero en su porción fraccionaria; `42` es así indistinguible en JS de `42.0` y `42.000000`.

Podemos usar `Number.isInteger(..)` para determinar si un valor `number` tiene alguna fracción distinta de cero o no:

```js
Number.isInteger(42);           // true
Number.isInteger(42.0);         // true
Number.isInteger(42.000000);    // true

Number.isInteger(42.0000001);   // false
```

### Parsing vs Coercion

Si un valor string contiene contenidos de apariencia numérica, es posible que necesites convertir de ese valor string a un `number`, para propósitos de operación matemática.

Sin embargo, es muy importante distinguir entre la conversión por parsing y la conversión por coercion.

Podemos convertir por parsing con las utilidades incorporadas de JS `parseInt(..)` o `parseFloat(..)`:

```js
someNumericText = "123.456";

parseInt(someNumericText,10);               // 123
parseFloat(someNumericText);                // 123.456

parseInt("42",10) === parseFloat("42");     // true

parseInt("512px");                          // 512
```

| NOTA: |
| :--- |
| El parsing solo es relevante para valores string, ya que es una operación carácter por carácter (de izquierda a derecha). No tiene sentido parsear los contenidos de un `boolean`, ni parsear los contenidos de un `number` o un `null`; no hay nada que parsear. Si pasás cualquier cosa que no sea un valor string a `parseInt(..)` / `parseFloat(..)`, esas utilidades primero convierten ese valor a string y luego intentan parsearlo. Eso es casi con certeza problemático (conduce a bugs) o derrochador -- `parseInt(42)` es tonto, y `parseInt(42.3)` es un abuso de `parseInt(..)` para hacer el trabajo de `Math.floor(..)`. |

El parsing extrae los caracteres de apariencia numérica del valor string, y los coloca en un valor `number`, deteniéndose una vez que encuentra un carácter no numérico (por ejemplo, que no sea `-`, `.` o `0`-`9`). Si el parsing falla en el primer carácter, ambas utilidades devuelven el valor especial `NaN` (ver "Invalid Number" más abajo), indicando que la operación fue inválida y falló.

Cuando `parseInt(..)` encuentra el `.` en `"123.456"`, se detiene, usando solo el `123` en el valor `number` resultante. `parseFloat(..)`, en cambio, acepta este carácter `.`, y sigue parseando un float con cualesquiera dígitos decimales que haya después del `.`.

La utilidad `parseInt(..)` específicamente toma como segundo argumento opcional -- pero *en realidad*, más bien necesario -- el `radix`: la base numérica a asumir para interpretar los caracteres del string para el `number` (rango `2` - `36`). `10` es para números estándar en base 10, `2` es para binario, `8` es para octal, y `16` es para hexadecimal. Cualquier otro `radix` inusual, como `23`, asume dígitos en orden, `0` - `9` seguidos de la ordenación de caracteres `a` - `z` (sin distinción de mayúsculas/minúsculas). Si el radix especificado está fuera del rango `2` - `36`, `parseInt(..)` falla como inválido y devuelve el valor `NaN`.

Si se omite el `radix`, el comportamiento de `parseInt(..)` es bastante matizado y confuso, en el sentido de que intenta hacer una mejor conjetura para un radix, basándose en lo que ve en el primer carácter. Esto históricamente ha llevado a muchos bugs sutiles, así que nunca confíes en la autoadivinanza por defecto; siempre especificá un radix explícito (como `10` en las llamadas de arriba).

`parseFloat(..)` siempre parsea con un radix de `10`, así que no acepta segundo argumento.

| ADVERTENCIA: |
| :--- |
| Una diferencia sorprendente entre `parseInt(..)` y `parseFloat(..)` es que `parseInt(..)` no parseará completamente la notación científica (por ejemplo, `"1.23e+5"`), deteniéndose en cambio en el `.` ya que no es válido para integers; de hecho, incluso `"1e+5"` se detiene en la `"e"`. `parseFloat(..)`, por otro lado, parsea completamente la notación científica como se espera. |

En contraste con la conversión por parsing, la conversión por coercion es un tipo de operación de todo-o-nada. O bien los contenidos completos del string se reconocen como numéricos (integer o punto flotante), o la conversión completa falla (resultando en `NaN` -- de nuevo, ver "Invalid Number" más adelante en este capítulo).

La conversión por coercion puede hacerse explícitamente con la función `Number(..)` (sin la palabra clave `new`) o con el operador unario `+` delante del valor:

```js
someNumericText = "123.456";

Number(someNumericText);        // 123.456
+someNumericText;               // 123.456

Number("512px");                // NaN
+"512px";                       // NaN
```

### Otras Representaciones Numéricas

Además de definir números usando los numerales tradicionales en base 10 (`0`-`9`), JS soporta definir literales numéricos solo de números enteros en otras tres bases: binario (base 2), octal (base 8), y hexadecimal (base 16).

```js
// binary
myAge = 0b101010;
myAge;              // 42

// octal
myAge = 0o52;
myAge;              // 42

// hexadecimal
myAge = 0x2a;
myAge;              // 42
```

Como podés ver, los prefijos `0b` (binario), `0o` (octal), y `0x` (hexadecimal) señalan la definición de números en las diferentes bases, pero los decimales no están permitidos en estos literales numéricos.

| NOTA: |
| :--- |
| La sintaxis de JS permite también los prefijos `0B`, `0O`, y `0X`. Sin embargo, por favor no uses nunca esas formas de prefijo en mayúsculas. Creo que cualquier persona sensata estaría de acuerdo: `0O` es mucho más fácil de confundir a simple vista que `0o` (que, de por sí, es un poco visualmente ambiguo a simple vista). ¡Quedate siempre con las formas de prefijo en minúsculas! |

Es importante darse cuenta de que no estás definiendo un *número diferente*, solo usando una forma diferente para producir el mismo valor numérico subyacente.

Por defecto, JS representa el valor numérico subyacente en modo de salida/string con la forma estándar en base 10. Sin embargo, los valores `number` tienen un método incorporado `toString(..)` que produce una representación string en cualquier base/radix especificado (al igual que con `parseInt(..)`, en el rango `2` - `36`):

```js
myAge = 42;

myAge.toString(2);          // "101010"
myAge.toString(8);          // "52"
myAge.toString(16);         // "2a"
myAge.toString(23);         // "1j"
myAge.toString(36);         // "16"
```

Podés hacer un round-trip de cualquier representación string de radix arbitrario de vuelta a un `number` usando `parseInt(..)`, con el radix apropiado:

```js
myAge = 42;

parseInt(myAge.toString("23"),23);      // 42
```

Otra forma permitida para especificar literales numéricos es usando notación científica:

```js
myAge = 4.2E1;      // or 4.2e1 or 4.2e+1

myAge;              // 42
```

`4.2E1` (o `4.2e1`) significa `4.2 * (10 ** 1)` (`10` elevado a la `1`). El exponente puede opcionalmente tener un signo `+` o `-`. Si se omite el signo, se asume que es `+`. Un exponente negativo hace el número más pequeño (mueve el decimal hacia la izquierda) en lugar de más grande (moviendo el decimal hacia la derecha):

```js
4.2E-3;             // 0.0042
```

Esta forma de notación científica es especialmente útil para la legibilidad al especificar potencias más grandes de `10`:

```js
someBigPowerOf10 = 1000000000;

// vs:

someBigPowerOf10 = 1e9;
```

Por defecto, JS representará (por ejemplo, como valores string, etc) los números muy grandes o muy pequeños -- específicamente, si los valores requieren más de 21 dígitos de precisión -- usando esta misma notación científica:

```js
ratherBigNumber = 123 ** 11;
ratherBigNumber.toString();     // "9.748913698143826e+22"

prettySmallNumber = 123 ** -11;
prettySmallNumber.toString();   // "1.0257553107587752e-23"
```

Los números con valores absolutos más pequeños (más cercanos a `0`) que estos umbrales igual pueden forzarse a la forma de notación científica (como strings):

```js
plainBoringNumber = 42;

plainBoringNumber.toExponential();      // "4.2e+1"
plainBoringNumber.toExponential(0);     // "4e+1"
plainBoringNumber.toExponential(4);     // "4.2000e+1"
```

El argumento opcional de `toExponential(..)` especifica la cantidad de dígitos decimales a incluir en la representación string.

Otra comodidad de legibilidad para especificar literales numéricos en el código es la capacidad de insertar `_` como separador de dígitos donde sea conveniente/significativo hacerlo. Por ejemplo:

```js
someBigPowerOf10 = 1_000_000_000;

totalCostInPennies = 123_45;  // vs 12_345
```

La decisión de usar `12345` (sin separador), `12_345` (como "12.345"), o `123_45` (como "123,45") queda enteramente a criterio del autor del código; JS ignora los separadores. Pero según el contexto, `123_45` podría ser más significativo semánticamente (en términos de legibilidad) que el más tradicional estilo de agrupamiento de tres dígitos desde la derecha separados por comas imitado con `12_345`.

### Representaciones Binarias Bit a Bit IEEE-754

IEEE-754[^IEEE754] es un estándar técnico para la representación binaria de números decimales. Es ampliamente usado por la mayoría de los lenguajes de programación de computadoras, incluyendo JS, Python, Ruby, etc.

No voy a cubrirlo exhaustivamente, pero creo que una breve introducción a cómo funcionan los números en lenguajes como JS está más que justificada, dado lo pocos programadores que tienen *alguna* familiaridad con ello.

En IEEE-754 de 64 bits -- llamado de "doble precisión", porque originalmente IEEE-754 solía ser de 32 bits, ¡y ahora es el doble de eso! -- los 64 bits se dividen en tres secciones: 52 bits para el valor base del número (es decir, "fracción", "mantisa", o "significando"), 11 bits para el exponente al que elevar `2` antes de multiplicar, y 1 bit para el signo del valor final.

| NOTA: |
| :--- |
| Dado que solo 52 de los 64 bits se usan en realidad para representar el valor base, `number` no tiene en realidad `2^64` valores en él. Según la especificación para el type `number`[^NumberType], la cantidad de valores es precisamente `2^64 - 2^53 + 3`, o alrededor de 18 trillones, repartidos aproximadamente de manera uniforme entre números positivos y negativos. |

Estos bits están dispuestos de izquierda a derecha, así (S = Bit de Signo, E = Bit de Exponente, M = Bit de Mantisa):

```js
SEEEEEEEEEEEMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
```

Así, el número `42` (o `42.000000`) estaría representado por estos bits:

```
// 42:
01000000010001010000000000000000
00000000000000000000000000000000
```

El bit de signo es `0`, lo que significa que el número es positivo (`1` significa negativo).

El exponente de 11 bits es el binario `10000000100`, que en base 10 es `1028`. Pero en IEEE-754, este valor se interpreta como almacenado sin signo con un "sesgo de exponente" de `1023`, lo que significa que estamos desplazando hacia arriba el rango del exponente de `-1022:1023` a `1:2046` (donde `0` y `2047` están reservados para representaciones especiales). Así, tomamos `1028` y le restamos el sesgo `1023`, lo que da un exponente efectivo de `5`. Elevamos `2` a ese valor (`2^5`), dando `32`.

| NOTA: |
| :--- |
| Si al restar `1023` del valor del exponente se obtiene un negativo (por ejemplo, `-3`), eso igual se interpreta como el exponente de `2`; elevar `2` a números negativos solo produce valores cada vez más pequeños. |

Los 52 bits restantes nos dan el valor base `01010000...`, interpretado como el decimal binario `1.0101000...` (con todos ceros a la derecha). Convirtiendo *eso* a base 10, obtenemos `1.3125000...`. Finalmente, entonces, multiplicá eso por el `32` ya calculado a partir del exponente. El resultado: `42`.

Como quizás puedas darte cuenta ahora, este estándar de representación numérica IEEE-754 se llama "punto flotante" porque el punto decimal "flota" de un lado a otro a lo largo de los bits, dependiendo del valor de exponente especificado.

El número `42.0000001`, que solo difiere de `42.000000` por apenas `0.0000001`, estaría representado por estos bits:

```
// 42.0000001:
01000000010001010000000000000000
00000000110101101011111110010101
```

¡Fijate cómo el patrón de bits anterior y este difieren en bastantes bits en las posiciones finales! La fracción decimal binaria que contiene todos esos bits `1` extra (`1.010100000000...01011111110010101`) se convierte a base 10 como `1.31250000312500003652`, que multiplicado por `32` nos da exactamente `42.0000001`.

Revisitaremos más detalles sobre la (im)precisión del punto flotante en el Capítulo 2. ¡Pero ahora entendés *un poco más* sobre cómo funciona IEEE-754!

### Límites de Number

Como quizás resulte evidente ahora que viste cómo funciona IEEE-754, los 52 bits del valor base del número deben compartirse, representando tanto la porción del número entero (si la hay) como la porción decimal (si la hay) del valor `number` previsto. Esencialmente, cuanto más grande sea la porción del número entero a representar, menos bits quedan disponibles para la porción decimal, y viceversa.

El valor más grande que puede almacenarse con precisión en el type `number` se expone como `Number.MAX_VALUE`:

```js
Number.MAX_VALUE;           // 1.7976931348623157e+308
```

Quizás esperes que ese valor sea un valor decimal, dada la representación. Pero mirando más de cerca, `1.79E308` es (aproximadamente) `2^1024 - 1`. Eso parece mucho más como si debiera ser un integer, ¿no? Podemos verificar:

```js
Number.isInteger(Number.MAX_VALUE);         // true
```

¿Pero qué pasa si vas por encima del valor máximo?

```js
Number.MAX_VALUE === (Number.MAX_VALUE + 1);
// true -- oops!

Number.MAX_VALUE === (Number.MAX_VALUE + 10000000);
// true
```

Entonces, ¿es `Number.MAX_VALUE` realmente el valor más grande representable en JS? Es ciertamente el valor `number` *finito* más grande.

IEEE-754 define un valor infinito especial, que JS expone como `Infinity`; también hay un `-Infinity` en el otro extremo lejano de la recta numérica. Los valores pueden ser testeados para ver si son finitos o infinitos:

```js
Number.isFinite(Number.MAX_VALUE);  // true

Number.isFinite(Infinity);          // false
Number.isFinite(-Infinity);         // false
```

Nunca podés contar hacia arriba (con `+ 1`) desde `Number.MAX_VALUE` hasta `Infinity`, sin importar cuánto tiempo dejes correr el programa, porque la operación `+ 1` en realidad no está incrementando más allá del valor tope `Number.MAX_VALUE`.

Sin embargo, las operaciones aritméticas de JS (`+`, `*`, e incluso `/`) definitivamente pueden desbordar el type `number` por el extremo superior, en cuyo caso `Infinity` es el resultado:

```js
Number.MAX_VALUE + 1E291;           // 1.7976931348623157e+308
Number.MAX_VALUE + 1E292;           // Infinity

Number.MAX_VALUE * 1.0000000001;    // Infinity

1 / 1E-308;                         // 1e+308
1 / 1E-309;                         // Infinity
```

| TIP: |
| :--- |
| Lo inverso no es cierto: una operación aritmética sobre un valor infinito *nunca* producirá un valor finito. |

Yendo de lo muy grande a lo muy, muy pequeño -- en realidad, lo más cercano a cero, ¡lo que no es lo mismo que ir muy, muy negativo! -- el valor decimal absoluto más pequeño que teóricamente podrías almacenar en el type `number` sería `2^-1022` (¿recordás el rango del exponente de IEEE-754?), o alrededor de `2E-308`. Sin embargo, los engines de JS tienen permitido por la especificación variar en sus representaciones internas para este límite inferior. Cualquiera sea el límite inferior efectivo del engine, se expondrá como `Number.MIN_VALUE`:

```js
Number.MIN_VALUE;               // 5e-324 <-- usually!
```

La mayoría de los engines de JS parecen tener un valor mínimo representable alrededor de `5E-324` (aproximadamente `2^-1074`). Dependiendo del engine y/o la plataforma, puede exponerse un valor diferente. Tené cuidado con cualquier lógica de programa que dependa de tales valores dependientes de la implementación.

### Límites de Enteros Seguros

Dado que `Number.MAX_VALUE` es un integer, podrías suponer que es el integer más grande del lenguaje. Pero eso no es realmente preciso.

El integer más grande que podés almacenar con precisión en el type `number` es `2^53 - 1`, o `9007199254740991`, que es *mucho más pequeño* que `Number.MAX_VALUE` (alrededor de `2^1024 - 1`). Este valor especial más seguro se expone como `Number.MAX_SAFE_INTEGER`:

```js
maxInt = Number.MAX_SAFE_INTEGER;

maxInt;             // 9007199254740991

maxInt + 1;         // 9007199254740992

maxInt + 2;         // 9007199254740992
```

Hemos visto que pueden aparecer integers más grandes que `9007199254740991`. Sin embargo, esos integers más grandes no son "seguros", en el sentido de que la precisión/exactitud empieza a desmoronarse cuando hacés operaciones con ellos. Como se muestra arriba, las expresiones `maxInt + 1` y `maxInt + 2` ambas dan erróneamente el mismo resultado, ilustrando el peligro al exceder el límite `Number.MAX_SAFE_INTEGER`.

¿Pero cuál es el integer seguro más pequeño?

Dependiendo de cómo interpretes "más pequeño", podrías responder ya sea `0` o... `Number.MIN_SAFE_INTEGER`:

```js
Number.MIN_SAFE_INTEGER;    // -9007199254740991
```

Y JS provee una utilidad para determinar si un valor es un integer en este rango seguro (`-2^53 + 1` - `2^53 - 1`):

```js
Number.isSafeInteger(2 ** 53);      // false
Number.isSafeInteger(2 ** 53 - 1);  // true
```

### Ceros Dobles

Puede sorprenderte saber que JS tiene dos ceros: `0`, y `-0` (cero negativo). ¿Pero qué demonios es un "cero negativo"? [^SignedZero] Un matemático seguramente se resistiría a tal noción.

Esto no es solo una peculiaridad graciosa de JS; está impuesto por la especificación IEEE-754[^IEEE754]. Todos los números de punto flotante tienen signo, incluido el cero. Y aunque JS en cierto modo oculta la existencia de `-0`, es completamente posible producirlo y detectarlo:

```js
function isNegZero(v) {
    return v == 0 && (1 / v) == -Infinity;
}

regZero = 0 / 1;
negZero = 0 / -1;

regZero === negZero;        // true -- oops!
Object.is(-0,regZero);      // false -- phew!
Object.is(-0,negZero);      // true

isNegZero(regZero);         // false
isNegZero(negZero);         // true
```

Quizás te preguntes por qué alguna vez necesitaríamos algo como `-0`. Puede ser útil cuando se usan números para representar tanto la magnitud del movimiento (velocidad) de algún elemento (como un personaje de juego o una animación) como también su dirección (por ejemplo, negativo = izquierda, positivo = derecha).

Sin tener un valor de cero con signo, no podrías saber hacia qué dirección estaba apuntando tal elemento en el momento en que quedó en reposo.

| NOTA: |
| :--- |
| Si bien JS define un cero con signo en el type `number`, no hay un cero con signo correspondiente en el type numérico `bigint`. Como tal, `-0n` simplemente se interpreta como `0n`, y los dos son indistinguibles. |

### Invalid Number

Las operaciones matemáticas a veces pueden producir un resultado inválido. Por ejemplo:

```js
42 / "Kyle";            // NaN
```

Probablemente sea obvio, pero si intentás dividir un número por un string, esa es una operación matemática inválida.

Otro tipo de operación numérica inválida es intentar convertir coercitivamente un valor que no se asemeja a algo numérico a un `number`. Como se discutió antes, podemos hacerlo con la función `Number(..)` o con el operador unario `+`:

```js
myAge = Number("just a number");

myAge;                  // NaN

+undefined;             // NaN
```

Todas esas operaciones inválidas (matemáticas o coercitivas/numéricas) producen el valor `number` especial llamado `NaN`.

La raíz histórica de "NaN" (de la especificación IEEE-754[^IEEE754]) es como acrónimo de "Not a Number" (No es un número). Técnicamente, hay alrededor de 9 cuatrillones de valores en el espacio numérico IEEE-754 de 64 bits designados como "NaN", pero JS los trata a todos de forma indistinguible como el único valor `NaN`.

Desafortunadamente, ese significado de *no es un número* produce confusión, ya que `NaN` es *absolutamente* un `number`.

| TIP: |
| :--- |
| ¡¿Por qué `NaN` es un `number`?! Pensá en lo opuesto: ¿qué pasaría si una operación matemática/numérica, como `+` o `/`, produjera un valor no-`number` (como `null`, `undefined`, etc)? ¿No sería eso realmente extraño e inesperado? ¿Qué pasaría si lanzaran excepciones, de modo que tuvieras que hacer `try..catch` en toda tu matemática? El único comportamiento sensato es que las operaciones numéricas/matemáticas deberían *siempre* producir un `number`, incluso si ese valor es inválido porque provino de una operación inválida. |

Para evitar tal confusión, prefiero fuertemente definir "NaN" como cualquiera de los siguientes en su lugar:

* "iNvalid Number" (Número iNválido)
* "Not actual Number" (No es un Número real)
* "Not available Number" (No hay Número disponible)
* "Not applicable Number" (Número No aplicable)

`NaN` es un valor especial en JS, en el sentido de que es el único valor del lenguaje que carece de la *propiedad de identidad* -- nunca es igual a sí mismo.

```js
NaN === NaN;            // false
```

Así que, desafortunadamente, el operador `===` no puede comprobar un valor para ver si es `NaN`. Pero hay algunas maneras de hacerlo:

```js
politicianIQ = "nothing" / Infinity;

Number.isNaN(politicianIQ);         // true

Object.is(NaN,politicianIQ);        // true
[ NaN ].includes(politicianIQ);     // true
```

Acá hay un hecho de prácticamente todos los programas de JS, te des cuenta o no: `NaN` pasa. En serio, casi todos los programas que hacen alguna matemática o conversiones numéricas están sujetos a que aparezca `NaN`.

Si no estás comprobando apropiadamente `NaN` en tus programas donde hacés matemática o conversiones numéricas, puedo decir con cierto grado de certeza: probablemente tengas un bug numérico en algún lugar de tu programa, y simplemente todavía no te ha mordido (¡que vos sepas!).

| ADVERTENCIA: |
| :--- |
| JS originalmente proveyó una función global llamada `isNaN(..)` para la comprobación de `NaN`, pero desafortunadamente tiene un bug de coercion de larga data. `isNaN("Kyle")` devuelve `true`, aunque el valor string `"Kyle"` definitivamente *no* es el valor `NaN`. Esto se debe a que la función global `isNaN(..)` fuerza a cualquier argumento no-`number` a coercionarse a un `number` primero, antes de comprobar `NaN`. Coercionar `"Kyle"` a un `number` produce `NaN`, ¡así que ahora la función ve un `NaN` y devuelve `true`! Esta función global `isNaN(..)` con bug todavía existe en JS, pero nunca debería usarse. Al comprobar `NaN`, siempre usá `Number.isNaN(..)`, `Object.is(..)`, etc. |

## Valores BigInteger

Como el integer seguro máximo en los `number` de JS es `9007199254740991` (ver arriba), un límite relativamente tan bajo puede presentar un problema si un programa JS necesita realizar matemática de integers más grandes, o incluso solo contener valores como IDs de integer de 64 bits (por ejemplo, los IDs de Tweets de Twitter).

Por esa razón, JS provee el type alternativo `bigint` (BigInteger), que puede almacenar integers arbitrariamente grandes (teóricamente no limitados, excepto por la memoria finita de la máquina y/o la implementación de JS).

Para distinguir un `bigint` de un valor `number` entero, que de otro modo ambos se verían igual (`42`), JS requiere un sufijo `n` en los valores `bigint`:

```js
myAge = 42n;        // this is a bigint, not a number

myKidsAge = 11;     // this is a number, not a bigint
```

Ilustremos la falta de límite superior del `bigint`:

```js
Number.MAX_SAFE_INTEGER;        // 9007199254740991

Number.MAX_SAFE_INTEGER + 2;    // 9007199254740992 -- oops!

myBigInt = 9007199254740991n;

myBigInt + 2n;                  // 9007199254740993n -- phew!

myBigInt ** 2n;                 // 81129638414606663681390495662081n
```

Como podés ver, el tipo de valor `bigint` es capaz de hacer aritmética precisa por encima del límite de integer del tipo de valor `number`.

| ADVERTENCIA: |
| :--- |
| ¿Notaste que el operador `+` requirió `.. + 2n` en lugar de solo `.. + 2`? No podés mezclar los tipos de valor `number` y `bigint` en la misma expresión. Esta restricción es molesta, pero protege a tu programa de operaciones matemáticas inválidas que darían resultados inesperados no obvios. |

Un valor `bigint` también puede crearse con la función `BigInt(..)`; por ejemplo, para convertir un valor `number` entero a un `bigint`:

```js
myAge = 42n;

inc = 1;

myAge += BigInt(inc);

myAge;              // 43n
```

| ADVERTENCIA: |
| :--- |
| Aunque pueda parecer contraintuitivo para algunos lectores, `BigInt(..)` *siempre* se llama sin la palabra clave `new`. Si se usa `new`, se lanzará una excepción. |

Ese es definitivamente uno de los usos más comunes de la función `BigInt(..)`: convertir `number`s a `bigint`s, para propósitos de operación matemática.

Pero no es tan infrecuente representar valores de integer grandes como strings, especialmente si esos valores llegan al entorno de JS desde otros entornos de lenguaje, o mediante ciertos formatos de intercambio, que en sí mismos no soportan valores de estilo `bigint`.

Como tal, `BigInt(..)` es útil para coercionar esos valores string a `bigint`s:

```js
myBigInt = BigInt("12345678901234567890");

myBigInt;                       // 12345678901234567890n
```

A diferencia de `parseInt(..)`, si algún carácter en el string es no numérico (dígitos `0-9` o `-`), incluyendo `.` o incluso un carácter de sufijo `n` al final, se lanzará una excepción. En otras palabras, `BigInt(..)` es una conversión por coercion de todo-o-nada, no una conversión por parsing.

| NOTA: |
| :--- |
| Creo que es absurdo que `BigInt(..)` no acepte el carácter `n` al final al coercionar strings (y así efectivamente ignorarlo). Hice un fuerte lobby por ese comportamiento, en el proceso de TC39, pero finalmente fue denegado. En mi opinión, ahora es una pequeñísima verruga gotcha en JS, pero una verruga al fin. |

## Valores Symbol

El type `symbol` contiene valores especiales opacos llamados "symbols". Estos valores solo pueden crearse mediante la función `Symbol(..)`:

```js
secret = Symbol("my secret");
```

| ADVERTENCIA: |
| :--- |
| Al igual que con `BigInt(..)`, la función `Symbol(..)` debe llamarse sin la palabra clave `new`. |

El string `"my secret"` pasado a la llamada de la función `Symbol(..)` *no* es el valor symbol en sí, aunque parezca así. Es meramente una etiqueta descriptiva opcional, usada solo para propósitos de depuración, en beneficio del desarrollador.

El valor subyacente devuelto por `Symbol(..)` es una clase especial de valor que se resiste a que el programa/desarrollador inspeccione cualquier cosa sobre su representación subyacente. Eso es lo que quiero decir con "opaco".

| NOTA: |
| :--- |
| Podrías pensar en los symbols como si fueran números integer que se incrementan monótonamente -- de hecho, eso es similar a cómo al menos algunos engines de JS los implementan. Pero el engine de JS nunca expondrá ninguna representación del valor subyacente de un symbol de ninguna manera que vos o el programa puedan ver. |

Los symbols están garantizados por el engine de JS de ser únicos (solo dentro del programa en sí), y son inadivinables. En otras palabras, un valor symbol duplicado nunca puede crearse en un programa.

Quizás te estés preguntando en este punto para qué se usan los symbols.

Un uso típico es como valores "especiales" que el desarrollador distingue de cualesquiera otros valores que podrían colisionar accidentalmente. Por ejemplo:

```js
EMPTY = Symbol("not set yet");
myNickname = EMPTY;

// later:

if (myNickname == EMPTY) {
    // ..
}
```

Aquí, he definido un valor `EMPTY` especial e inicializado `myNickname` con él. Más tarde, compruebo si todavía es ese valor especial, y entonces realizo alguna acción si es así. Podría no querer haber usado `null` o `undefined` para tales propósitos, ya que otro desarrollador podría pasar uno de esos valores comunes incorporados. `EMPTY`, en cambio, aquí es un valor único e inadivinable que solo yo he definido y sobre el que tengo control y acceso.

Quizás aún más comúnmente, los symbols a menudo se usan como propiedades especiales (meta-) en los objetos:

```js
myInfo = {
    name: "Kyle Simpson",
    nickname: "getify",
    age: 42
};

// later:
PRIVATE_ID = Symbol("private unique ID, don't touch!");

myInfo[PRIVATE_ID] = generateID();
```

Es importante notar que las propiedades symbol igual son visibles públicamente en cualquier objeto; no son *en realidad* privadas. Pero se tratan como especiales y apartadas de la colección normal de propiedades del objeto. Es similar a si en cambio hubiera hecho:

```js
Object.defineProperty(myInfo,"__private_id_dont_touch",{
    value: generateID(),
    enumerable: false,
});
```

Solo por convención, la mayoría de los desarrolladores saben que si un nombre de propiedad está prefijado con `_` (¡o aún más, `__`!), eso significa que es "pseudo-privado" y que hay que dejarlo tranquilo a menos que realmente se supone que deban acceder a él.

Los symbols básicamente sirven para el mismo caso de uso, pero un poco más ergonómicamente que el enfoque de prefijado.

### Well-Known Symbols (WKS)

JS predefine un conjunto de symbols, denominados *well-known symbols* (WKS), que representan ciertos ganchos especiales de metaprogramación en los objetos. Estos symbols se almacenan como propiedades estáticas en el objeto de función `Symbol`. Por ejemplo:

```js
myInfo = {
    // ..
};

String(myInfo);         // [object Object]

myInfo[Symbol.toStringTag] = "my-info";
String(myInfo);         // [object my-info]
```

`Symbol.toStringTag` es un well-known symbol para acceder y sobrescribir la representación string por defecto de un objeto plano (`"[object Object]"`), reemplazando la parte `"Object"` con un valor diferente (por ejemplo, `"my-info"`).

Ver el libro "Objects & Classes" de esta serie para más información sobre los Well-Known Symbols y la metaprogramación.

### Registro Global de Symbols

A menudo, querés mantener los valores symbol privados, como dentro del scope de un módulo. Pero ocasionalmente, querés exponerlos para que sean accesibles globalmente a lo largo de todos los archivos de un programa JS.

En lugar de solo adjuntarlos como variables globales (es decir, propiedades en el objeto `globalThis`), JS provee un *espacio de nombres global* alternativo donde registrar symbols:

```js
// retrieve if already registered,
// otherwise register
PRIVATE_ID = Symbol.for("private-id");

// elsewhere:

privateIDKey = Symbol.keyFor(PRIVATE_ID);
privateIDKey;           // "private-id"

// elsewhere:

// retrieve symbol from registry undeer
// specified key
privateIDSymbol = Symbol.for(privateIDKey);
```

El valor pasado a `Symbol.for(..)` *no* es el mismo que el pasado a `Symbol(..)`. `Symbol.for(..)` espera una *clave* única bajo la cual registrar el symbol en el registro global, mientras que `Symbol(..)` opcionalmente acepta una etiqueta descriptiva (no necesariamente única).

Si el registro no tiene un symbol bajo esa *clave* especificada, se crea un nuevo symbol (sin etiqueta descriptiva) y se registra automáticamente allí. De lo contrario, `Symbol.for(..)` devuelve cualquier symbol previamente registrado que esté bajo esa *clave*.

Yendo en la dirección opuesta, si tenés el valor symbol en sí, y querés recuperar la *clave* bajo la cual está registrado, `Symbol.keyFor(..)` toma el symbol en sí como entrada, y devuelve la *clave* (si la hay). Eso es útil en caso de que sea más conveniente pasar el valor string de la *clave* que el symbol en sí.

### ¿Objeto o Primitivo?

A diferencia de otros primitivos como `42`, donde podés crear múltiples copias del mismo valor, los symbols *sí* actúan más como referencias de objeto específicas en el sentido de que siempre son completamente únicos (a efectos de asignación de valor y comparación de igualdad). La especificación también categoriza la función `Symbol()` bajo la sección de "Objetos Fundamentales", llamando a la función un "constructor", e incluso definiendo su propiedad `prototype`.

Sin embargo, como se mencionó antes, `new` no puede usarse con `Symbol(..)`; esto es similar al "constructor" `BigInt()`. Sabemos claramente que los valores `bigint` son primitivos, así que los valores `symbol` parecen ser del mismo *tipo*.

Y en la sección "Terms and Definitions" de la especificación, lista symbol como un valor primitivo. [^PrimitiveValues] Más aún, los valores en sí se usan en los programas de JS como primitivos en lugar de como objetos. Por ejemplo, los symbols se usan principalmente como claves en los objetos -- ¡sabemos que los objetos no pueden usar otros valores de objeto como claves! -- junto con los strings, que también son primitivos.

Como se mencionó antes, algunos engines de JS incluso implementan internamente los symbols como integers únicos que se incrementan monótonamente (¡primitivos!).

Finalmente, como se explicó al principio de este capítulo, sabemos que a los valores primitivos *no se les permite* tener propiedades asignadas, sino que se les hace *auto-boxing* (ver "Objetos Automáticos" en el Capítulo 3) internamente al type de objeto envoltorio correspondiente para facilitar el acceso a propiedades/métodos. Los symbols siguen todos estos comportamientos exactos, igual que todos los demás primitivos.

Considerado todo esto, creo que los symbols son *mucho más* parecidos a primitivos que a objetos, así que así es como los presento en este libro.

## Los Primitivos Son Tipos Incorporados

Ahora hemos profundizado en los siete tipos de valor primitivos (no objeto) que JS provee automáticamente incorporados.

Antes de pasar a discutir el tipo de valor objeto incorporado de JS, queremos echar un vistazo más de cerca a los tipos de comportamientos que podemos esperar de los valores de JS. Lo haremos en profundidad, en el próximo capítulo.

[^PrimitiveValues]: "4.4.5 primitive value", ECMAScript 2022 Language Specification; https://tc39.es/ecma262/#sec-primitive-value ; Accessed August 2022

[^UTFUCS]: "JavaScript’s internal character encoding: UCS-2 or UTF-16?"; Mathias Bynens; January 20 2012; https://mathiasbynens.be/notes/javascript-encoding ; Accessed July 2022

[^IEEE754]: "IEEE-754"; https://en.wikipedia.org/wiki/IEEE_754 ; Accessed July 2022

[^NumberType]: "6.1.6.1 The Number Type", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-ecmascript-language-types-number-type ; Accessed August 2022

[^SignedZero]: "Signed Zero", Wikipedia; https://en.wikipedia.org/wiki/Signed_zero ; Accessed August 2022
