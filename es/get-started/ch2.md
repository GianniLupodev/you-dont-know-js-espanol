# You Don't Know JS Yet: Get Started - 2nd Edition
# Capítulo 2: Explorando JS

La mejor manera de aprender JS es empezar a escribir JS.

Para eso, necesitás saber cómo funciona el lenguaje, y en eso nos vamos a enfocar acá. Incluso si ya programaste en otros lenguajes antes, tomate tu tiempo para sentirte cómodo con JS, y asegurate de practicar cada parte.

Este capítulo no es una referencia exhaustiva de cada detalle de la sintaxis del lenguaje JS. Tampoco pretende ser un completo manual de "introducción a JS".

En cambio, solo vamos a recorrer algunas de las áreas temáticas principales del lenguaje. Nuestro objetivo es tener una mejor *sensación* de él, para poder avanzar escribiendo nuestros propios programas con más confianza. Vamos a volver sobre muchos de estos temas con sucesivamente más detalle a medida que avancés por el resto de este libro, y el resto de la serie.

Por favor, no esperes que este capítulo sea una lectura rápida. Es largo y hay un montón de detalles para masticar. Tomate tu tiempo.

| TIP: |
| :--- |
| Si todavía te estás familiarizando con JS, te sugiero que reserves bastante tiempo extra para trabajar a lo largo de este capítulo. Tomá cada sección y reflexioná y explorá el tema por un rato. Mirá programas JS existentes y compará lo que veas en ellos con el código y las explicaciones (¡y opiniones!) que se presentan acá. Vas a sacar mucho más provecho del resto del libro y de la serie con una base sólida sobre la *naturaleza* de JS. |

## Cada Archivo es un Programa

Casi todos los sitios web (aplicaciones web) que usás están compuestos por muchos archivos JS distintos (típicamente con la extensión de archivo .js). Es tentador pensar en todo el conjunto (la aplicación) como un solo programa. Pero JS lo ve de forma diferente.

En JS, cada archivo independiente es su propio programa separado.

La razón por la que esto importa gira principalmente en torno al manejo de errores. Como JS trata a los archivos como programas, un archivo puede fallar (durante el parseo/compilación o la ejecución) y eso no necesariamente va a impedir que el siguiente archivo sea procesado. Obviamente, si tu aplicación depende de cinco archivos .js, y uno de ellos falla, la aplicación en general probablemente va a operar solo parcialmente, en el mejor de los casos. Es importante asegurarse de que cada archivo funcione correctamente, y que en la medida de lo posible, manejen las fallas en otros archivos de la forma más elegante posible.

Puede sorprenderte considerar archivos .js separados como programas JS separados. Desde la perspectiva de tu uso de una aplicación, seguro parece un gran programa. Eso es porque la ejecución de la aplicación permite que estos *programas* individuales cooperen y actúen como un solo programa.

| NOTA: |
| :--- |
| Muchos proyectos usan herramientas de proceso de build que terminan combinando archivos separados del proyecto en un único archivo que se entrega a una página web. Cuando esto pasa, JS trata a este único archivo combinado como el programa entero. |

La única manera en que múltiples archivos .js independientes actúan como un solo programa es compartiendo su estado (y el acceso a su funcionalidad pública) a través del "scope global". Se mezclan en este espacio de nombres del scope global, de modo que en tiempo de ejecución actúan como un todo.

Desde ES6, JS también soporta un formato de módulo además del típico formato de programa JS independiente. Los módulos también están basados en archivos. Si un archivo se carga mediante un mecanismo de carga de módulos como una `import` statement o una etiqueta `<script type=module>`, todo su código se trata como un único módulo.

Aunque normalmente no pensarías en un módulo —una colección de estado y métodos expuestos públicamente para operar sobre ese estado— como un programa independiente, JS de hecho sigue tratando a cada módulo por separado. De manera similar a cómo el "scope global" permite que archivos independientes se mezclen en tiempo de ejecución, importar un módulo dentro de otro permite la interoperación en tiempo de ejecución entre ellos.

Sin importar qué patrón de organización de código (y mecanismo de carga) se use para un archivo (independiente o módulo), igual deberías pensar en cada archivo como su propio (mini) programa, que luego puede cooperar con otros (mini) programas para realizar las funciones de tu aplicación en general.

## Valores

La unidad de información más fundamental en un programa es un valor. Los valores son datos. Son la forma en que el programa mantiene el estado. Los valores vienen en dos formas en JS: **primitivo** y **objeto**.

Los valores se incrustan en los programas usando *literales*:

```js
greeting("My name is Kyle.");
```

En este programa, el valor `"My name is Kyle."` es un string literal primitivo; los strings son colecciones ordenadas de caracteres, normalmente usadas para representar palabras y oraciones.

Usé el carácter de comilla doble `"` para *delimitar* (rodear, separar, definir) el valor del string. Pero también podría haber usado el carácter de comilla simple `'`. La elección de qué carácter de comilla usar es enteramente estilística. Lo importante, por el bien de la legibilidad y mantenibilidad del código, es elegir uno y usarlo de forma consistente a lo largo del programa.

Otra opción para delimitar un string literal es usar el carácter de comilla invertida (back-tick) `` ` ``. Sin embargo, esta elección no es meramente estilística; también hay una diferencia de comportamiento. Considerá:

```js
console.log("My name is ${ firstName }.");
// My name is ${ firstName }.

console.log('My name is ${ firstName }.');
// My name is ${ firstName }.

console.log(`My name is ${ firstName }.`);
// My name is Kyle.
```

Suponiendo que este programa ya definió una variable `firstName` con el valor de string `"Kyle"`, el string delimitado por `` ` `` entonces resuelve la expresión de la variable (indicada con `${ .. }`) a su valor actual. Esto se llama **interpolación**.

El string delimitado por la comilla invertida `` ` `` puede usarse sin incluir expresiones interpoladas, pero eso frustra todo el propósito de esa sintaxis alternativa de string literal:

```js
console.log(
    `Am I confusing you by omitting interpolation?`
);
// Am I confusing you by omitting interpolation?
```

El mejor enfoque es usar `"` o `'` (de nuevo, ¡elegí uno y quedate con él!) para los strings *a menos que necesites* interpolación; reservá `` ` `` solo para los strings que vayan a incluir expresiones interpoladas.

Además de los strings, los programas JS a menudo contienen otros valores literales primitivos como booleanos y números:

```js
while (false) {
    console.log(3.141592);
}
```

`while` representa un tipo de bucle, una manera de repetir operaciones *mientras* su condición sea verdadera.

En este caso, el bucle nunca va a correr (y no se va a imprimir nada), porque usamos el valor booleano `false` como condicional del bucle. `true` habría resultado en un bucle que sigue para siempre, ¡así que tené cuidado!

El número `3.141592` es, como quizás sepas, una aproximación del PI matemático a los primeros seis dígitos. Sin embargo, en lugar de incrustar semejante valor, típicamente usarías el valor predefinido `Math.PI` para ese propósito. Otra variación de los números es el tipo primitivo `bigint` (big-integer o entero grande), que se usa para almacenar números arbitrariamente grandes.

Los números se usan más a menudo en los programas para contar pasos, como las iteraciones de un bucle, y para acceder a información en posiciones numéricas (es decir, un índice de array). Vamos a cubrir arrays/objetos en un ratito, pero como ejemplo, si hubiera un array llamado `names`, podríamos acceder al elemento en su segunda posición así:

```js
console.log(`My name is ${ names[1] }.`);
// My name is Kyle.
```

Usamos `1` para el elemento en la segunda posición, en lugar de `2`, porque al igual que en la mayoría de los lenguajes de programación, los índices de array de JS están basados en 0 (`0` es la primera posición).

Además de strings, números y booleanos, otros dos valores *primitivos* en los programas JS son `null` y `undefined`. Si bien hay diferencias entre ellos (algunas históricas y otras contemporáneas), en su mayor parte ambos valores sirven al propósito de indicar la *vacuidad* (o ausencia) de un valor.

Muchos desarrolladores prefieren tratar a ambos de forma consistente de esta manera, es decir, asumiendo que los valores son indistinguibles. Si se tiene cuidado, esto a menudo es posible. Sin embargo, lo más seguro y mejor es usar solo `undefined` como el único valor vacío, ¡aunque `null` resulte atractivo por ser más corto de tipear!

```js
while (value != undefined) {
    console.log("Still got something!");
}
```

El último valor primitivo que hay que conocer es un symbol, que es un valor de propósito especial que se comporta como un valor oculto e imposible de adivinar. Los symbols se usan casi exclusivamente como claves especiales en objetos:

```js
hitchhikersGuide[ Symbol("meaning of life") ];
// 42
```

No vas a encontrar uso directo de symbols muy seguido en los programas JS típicos. Se usan principalmente en código de bajo nivel, como en librerías y frameworks.

### Arrays Y Objetos

Además de los primitivos, el otro tipo de valor en JS es un valor objeto.

Como se mencionó antes, los arrays son un tipo especial de objeto que está compuesto por una lista de datos ordenada e indexada numéricamente:

```js
var names = [ "Frank", "Kyle", "Peter", "Susan" ];

names.length;
// 4

names[0];
// Frank

names[1];
// Kyle
```

Los arrays de JS pueden contener cualquier tipo de valor, ya sea primitivo u objeto (incluyendo otros arrays). Como veremos hacia el final del Capítulo 3, incluso las funciones son valores que pueden contenerse en arrays u objetos.

| NOTA: |
| :--- |
| Las funciones, al igual que los arrays, son una clase especial (es decir, un sub-tipo) de objeto. Vamos a cubrir las funciones con más detalle en un rato. |

Los objetos son más generales: una colección desordenada y con claves de cualquier variedad de valores. En otras palabras, accedés al elemento por un nombre de ubicación de tipo string (es decir, "clave" o "propiedad") en lugar de por su posición numérica (como con los arrays). Por ejemplo:

```js
var me = {
    first: "Kyle",
    last: "Simpson",
    age: 39,
    specialties: [ "JS", "Table Tennis" ]
};

console.log(`My name is ${ me.first }.`);
```

Acá, `me` representa un objeto, y `first` representa el nombre de una ubicación de información en ese objeto (colección de valores). Otra opción de sintaxis que accede a la información en un objeto por su propiedad/clave usa los corchetes `[ ]`, como por ejemplo `me["first"]`.

### Determinación del Tipo de Valor

Para distinguir valores, el operador `typeof` te dice su tipo incorporado, si es primitivo, o `"object"` en caso contrario:

```js
typeof 42;                  // "number"
typeof "abc";               // "string"
typeof true;                // "boolean"
typeof undefined;           // "undefined"
typeof null;                // "object" -- oops, bug!
typeof { "a": 1 };          // "object"
typeof [1,2,3];             // "object"
typeof function hello(){};  // "function"
```

| ADVERTENCIA: |
| :--- |
| `typeof null` lamentablemente devuelve `"object"` en lugar del esperado `"null"`. Además, `typeof` devuelve el específico `"function"` para las funciones, pero no el esperado `"array"` para los arrays. |

Convertir de un tipo de valor a otro, como de string a número, se denomina en JS "coerción". Vamos a cubrir esto con más detalle más adelante en este capítulo.

Los valores primitivos y los valores objeto se comportan de forma diferente cuando se asignan o se pasan por ahí. Vamos a cubrir estos detalles en el Apéndice A, "Valores vs Referencias."

## Declarar y Usar Variables

Para ser explícito sobre algo que puede no haber sido obvio en la sección anterior: en los programas JS, los valores pueden aparecer ya sea como valores literales (como ilustran muchos de los ejemplos anteriores), o pueden contenerse en variables; pensá en las variables simplemente como contenedores de valores.

Las variables tienen que ser declaradas (creadas) para poder usarse. Hay varias formas de sintaxis que declaran variables (es decir, "identificadores"), y cada forma tiene distintos comportamientos implícitos.

Por ejemplo, considerá la `var` statement:

```js
var myName = "Kyle";
var age;
```

La palabra clave `var` declara una variable para ser usada en esa parte del programa, y opcionalmente permite una asignación inicial de un valor.

Otra palabra clave similar es `let`:

```js
let myName = "Kyle";
let age;
```

La palabra clave `let` tiene algunas diferencias respecto de `var`, siendo la más obvia que `let` permite un acceso más limitado a la variable que `var`. Esto se llama "block scoping" (scope de bloque) en oposición al scope regular o de función.

Considerá:

```js
var adult = true;

if (adult) {
    var myName = "Kyle";
    let age = 39;
    console.log("Shhh, this is a secret!");
}

console.log(myName);
// Kyle

console.log(age);
// Error!
```

El intento de acceder a `age` fuera de la `if` statement resulta en un error, porque `age` tenía un scope de bloque limitado al `if`, mientras que `myName` no.

El block-scoping es muy útil para limitar cuán extendidas están las declaraciones de variables en nuestros programas, lo que ayuda a prevenir el solapamiento accidental de sus nombres.

Pero `var` sigue siendo útil en el sentido de que comunica "esta variable va a ser vista por un scope más amplio (el de toda la función)". Ambas formas de declaración pueden ser apropiadas en cualquier parte dada de un programa, dependiendo de las circunstancias.

| NOTA: |
| :--- |
| Es muy común sugerir que `var` debería evitarse en favor de `let` (¡o `const`!), generalmente por una confusión percibida sobre cómo ha funcionado el comportamiento de scope de `var` desde el comienzo de JS. Creo que este es un consejo excesivamente restrictivo y en definitiva poco útil. Asume que sos incapaz de aprender y usar una característica correctamente en combinación con otras características. ¡Creo que *podés* y *deberías* aprender cualquier característica disponible, y usarla donde sea apropiado! |

Una tercera forma de declaración es `const`. Es como `let` pero tiene una limitación adicional: se le debe dar un valor en el momento en que se declara, y no se le puede reasignar un valor diferente más tarde.

Considerá:

```js
const myBirthday = true;
let age = 39;

if (myBirthday) {
    age = age + 1;    // OK!
    myBirthday = false;  // Error!
}
```

A la constante `myBirthday` no se le permite ser reasignada.

Las variables declaradas con `const` no son "inmutables", simplemente no pueden ser reasignadas. No es aconsejable usar `const` con valores objeto, porque esos valores igual pueden cambiarse aunque la variable no pueda reasignarse. Esto lleva a una potencial confusión más adelante, así que creo que es sabio evitar situaciones como:

```js
const actors = [
    "Morgan Freeman", "Jennifer Aniston"
];

actors[2] = "Tom Cruise";   // OK :(
actors = [];                // Error!
```

El mejor uso semántico de un `const` es cuando tenés un valor primitivo simple al que querés darle un nombre útil, como usar `myBirthday` en lugar de `true`. Esto hace que los programas sean más fáciles de leer.

| TIP: |
| :--- |
| ¡Si te quedás usando `const` solo con valores primitivos, evitás cualquier confusión entre reasignación (no permitida) vs. mutación (permitida)! Esa es la forma más segura y mejor de usar `const`. |

Además de `var` / `let` / `const`, hay otras formas sintácticas que declaran identificadores (variables) en varios scopes. Por ejemplo:

```js
function hello(myName) {
    console.log(`Hello, ${ myName }.`);
}

hello("Kyle");
// Hello, Kyle.
```

El identificador `hello` se crea en el scope exterior, y también se asocia automáticamente de modo que referencia a la función. Pero el parámetro nombrado `myName` se crea solo dentro de la función, y por lo tanto solo es accesible dentro del scope de esa función. `hello` y `myName` se comportan generalmente como si estuvieran declarados con `var`.

Otra sintaxis que declara una variable es una cláusula `catch`:

```js
try {
    someError();
}
catch (err) {
    console.log(err);
}
```

El `err` es una variable con scope de bloque que existe solo dentro de la cláusula `catch`, como si hubiera sido declarada con `let`.

## Funciones

La palabra "función" tiene una variedad de significados en programación. Por ejemplo, en el mundo de la Programación Funcional, "función" tiene una definición matemática precisa e implica un estricto conjunto de reglas a las que atenerse.

En JS, deberíamos considerar que "función" toma el significado más amplio de otro término relacionado: "procedimiento". Un procedimiento es una colección de statements que puede invocarse una o más veces, puede recibir algunas entradas, y puede devolver una o más salidas.

Desde los primeros días de JS, la definición de una función se veía así:

```js
function awesomeFunction(coolThings) {
    // ..
    return amazingStuff;
}
```

Esto se llama una function declaration (declaración de función) porque aparece como una statement por sí misma, no como una expression dentro de otra statement. La asociación entre el identificador `awesomeFunction` y el valor de la función ocurre durante la fase de compilación del código, antes de que ese código se ejecute.

En contraste con una statement de function declaration, una function expression puede definirse y asignarse así:

```js
// let awesomeFunction = ..
// const awesomeFunction = ..
var awesomeFunction = function(coolThings) {
    // ..
    return amazingStuff;
};
```

Esta función es una expression que se asigna a la variable `awesomeFunction`. A diferencia de la forma de function declaration, una function expression no se asocia con su identificador hasta esa statement durante el tiempo de ejecución.

Es sumamente importante notar que en JS, las funciones son valores que pueden asignarse (como se muestra en este fragmento) y pasarse por ahí. De hecho, las funciones de JS son un tipo especial del tipo de valor objeto. No todos los lenguajes tratan a las funciones como valores, pero es esencial que un lenguaje soporte el patrón de programación funcional, como lo hace JS.

Las funciones de JS pueden recibir entrada de parámetros:

```js
function greeting(myName) {
    console.log(`Hello, ${ myName }!`);
}

greeting("Kyle");   // Hello, Kyle!
```

En este fragmento, `myName` se llama un parámetro, que actúa como una variable local dentro de la función. Las funciones pueden definirse para recibir cualquier cantidad de parámetros, desde ninguno en adelante, como te parezca conveniente. A cada parámetro se le asigna el valor del argumento que pasás en esa posición (`"Kyle"`, acá) de la llamada.

Las funciones también pueden devolver valores usando la palabra clave `return`:

```js
function greeting(myName) {
    return `Hello, ${ myName }!`;
}

var msg = greeting("Kyle");

console.log(msg);   // Hello, Kyle!
```

Solo podés hacer `return` de un único valor, pero si tenés más valores para devolver, podés envolverlos en un solo objeto/array.

Como las funciones son valores, pueden asignarse como propiedades en objetos:

```js
var whatToSay = {
    greeting() {
        console.log("Hello!");
    },
    question() {
        console.log("What's your name?");
    },
    answer() {
        console.log("My name is Kyle.");
    }
};

whatToSay.greeting();
// Hello!
```

En este fragmento, se incluyen referencias a tres funciones (`greeting()`, `question()` y `answer()`) en el objeto contenido por `whatToSay`. Cada función puede llamarse accediendo a la propiedad para recuperar el valor de referencia de la función. Compará este estilo directo de definir funciones en un objeto con la sintaxis de `class` más sofisticada que se discute más adelante en este capítulo.

Hay muchas formas variadas que toman las `function`s en JS. Nos sumergimos en estas variaciones en el Apéndice A, "Tantas Formas de Funciones."

## Comparaciones

Tomar decisiones en los programas requiere comparar valores para determinar su identidad y su relación entre sí. JS tiene varios mecanismos para habilitar la comparación de valores, así que miremos más de cerca cada uno.

### Igual...ito

La comparación más común en los programas JS hace la pregunta: "¿Este valor X es *el mismo que* ese valor Y?". ¿Qué significa realmente "el mismo que" para JS, sin embargo?

Por razones ergonómicas e históricas, el significado es más complicado que el obvio tipo de coincidencia de *identidad exacta*. A veces una comparación de igualdad pretende una coincidencia *exacta*, pero otras veces la comparación deseada es un poco más amplia, permitiendo una coincidencia *muy similar* o *intercambiable*. En otras palabras, debemos ser conscientes de las sutiles diferencias entre una comparación de **igualdad** (equality) y una comparación de **equivalencia** (equivalence).

Si pasaste algo de tiempo trabajando con JS y leyendo sobre él, seguramente viste el llamado operador "triple-igual" `===`, también descrito como el operador de "igualdad estricta". Eso parece bastante directo, ¿no? Seguramente, "estricto" significa estricto, como en estrecho y *exacto*.

No *exacta*mente.

Sí, la mayoría de los valores que participan en una comparación de igualdad `===` van a encajar con esa misma intuición de *exactamente igual*. Considerá algunos ejemplos:

```js
3 === 3.0;              // true
"yes" === "yes";        // true
null === null;          // true
false === false;        // true

42 === "42";            // false
"hello" === "Hello";    // false
true === 1;             // false
0 === null;             // false
"" === null;            // false
null === undefined;     // false
```

| NOTA: |
| :--- |
| Otra forma en que a menudo se describe la comparación de igualdad de `===` es "chequear tanto el valor como el tipo". En varios de los ejemplos que vimos hasta ahora, como `42 === "42"`, el *tipo* de ambos valores (número, string, etc.) parece ser el factor distintivo. Sin embargo, hay más que eso. **Todas** las comparaciones de valores en JS consideran el tipo de los valores que se comparan, no *solo* el operador `===`. Específicamente, `===` no permite ningún tipo de conversión de tipo (es decir, "coerción") en su comparación, mientras que otras comparaciones de JS *sí* permiten coerción. |

Pero el operador `===` sí tiene algo de sutileza, un hecho que muchos desarrolladores JS pasan por alto, en su perjuicio. El operador `===` está diseñado para *mentir* en dos casos de valores especiales: `NaN` y `-0`. Considerá:

```js
NaN === NaN;            // false
0 === -0;               // true
```

En el caso de `NaN`, el operador `===` *miente* y dice que una ocurrencia de `NaN` no es igual a otro `NaN`. En el caso de `-0` (sí, ¡este es un valor real y distinto que podés usar intencionalmente en tus programas!), el operador `===` *miente* y dice que es igual al valor regular `0`.

Como la *mentira* sobre tales comparaciones puede ser molesta, lo mejor es evitar usar `===` para ellas. Para las comparaciones de `NaN`, usá la utilidad `Number.isNaN(..)`, que no *miente*. Para la comparación de `-0`, usá la utilidad `Object.is(..)`, que tampoco *miente*. `Object.is(..)` también puede usarse para chequeos de `NaN` que no *mienten*, si lo preferís. Graciosamente, podrías pensar en `Object.is(..)` como el "cuádruple-igual" `====`, ¡la comparación realmente-realmente-estricta!

Hay razones históricas y técnicas más profundas para estas *mentiras*, pero eso no cambia el hecho de que `===` no es en realidad una comparación *estrictamente y exactamente igual*, en el sentido más *estricto*.

La historia se vuelve aún más complicada cuando consideramos las comparaciones de valores objeto (no primitivos). Considerá:

```js
[ 1, 2, 3 ] === [ 1, 2, 3 ];    // false
{ a: 42 } === { a: 42 }         // false
(x => x * 2) === (x => x * 2)   // false
```

¿Qué está pasando acá?

Puede parecer razonable asumir que un chequeo de igualdad considera la *naturaleza* o el *contenido* del valor; después de todo, `42 === 42` considera el valor real `42` y lo compara. Pero cuando se trata de objetos, una comparación que tiene en cuenta el contenido generalmente se denomina "igualdad estructural".

JS no define `===` como *igualdad estructural* para los valores objeto. En cambio, `===` usa *igualdad de identidad* para los valores objeto.

En JS, todos los valores objeto se contienen por referencia (ver "Valores vs Referencias" en el Apéndice A), se asignan y se pasan por copia-de-referencia, **y** para nuestra discusión actual, se comparan por igualdad de referencia (identidad). Considerá:

```js
var x = [ 1, 2, 3 ];

// assignment is by reference-copy, so
// y references the *same* array as x,
// not another copy of it.
var y = x;

y === x;              // true
y === [ 1, 2, 3 ];    // false
x === [ 1, 2, 3 ];    // false
```

En este fragmento, `y === x` es true porque ambas variables contienen una referencia al mismo array inicial. Pero las comparaciones `=== [1,2,3]` fallan ambas porque `y` y `x`, respectivamente, se están comparando con nuevos arrays *diferentes* `[1,2,3]`. La estructura y el contenido del array no importan en esta comparación, solo la **identidad de referencia**.

JS no provee un mecanismo para la comparación de igualdad estructural de valores objeto, solo la comparación de identidad de referencia. Para hacer una comparación de igualdad estructural, vas a necesitar implementar los chequeos vos mismo.

Pero cuidado, es más complicado de lo que vas a suponer. Por ejemplo, ¿cómo determinarías si dos referencias de función son "estructuralmente equivalentes"? Incluso convertir a string para comparar el texto de su código fuente no tendría en cuenta cosas como el closure. ¡JS no provee la comparación de igualdad estructural porque es casi intratable manejar todos los casos límite!

### Comparaciones Coercitivas

Coerción significa que un valor de un tipo se convierte a su respectiva representación en otro tipo (en la medida de lo posible). Como discutiremos en el Capítulo 4, la coerción es un pilar central del lenguaje JS, no una característica opcional que pueda razonablemente evitarse.

Pero donde la coerción se encuentra con los operadores de comparación (como la igualdad), lamentablemente la confusión y la frustración surgen más a menudo que no.

Pocas características de JS atraen más ira en la comunidad JS en general que el operador `==`, generalmente llamado el operador de "igualdad laxa" (loose equality). La mayoría de todo lo que se escribe y del discurso público sobre JS condena a este operador como mal diseñado y peligroso/plagado de bugs cuando se usa en los programas JS. Incluso el propio creador del lenguaje, Brendan Eich, ha lamentado que se haya diseñado como un gran error.

Por lo que puedo ver, la mayor parte de esta frustración viene de una lista bastante corta de casos límite confusos, pero un problema más profundo es la concepción errónea extremadamente extendida de que realiza sus comparaciones sin considerar los tipos de los valores comparados.

El operador `==` realiza una comparación de igualdad de manera similar a cómo lo hace `===`. De hecho, ambos operadores consideran el tipo de los valores que se comparan. Y si la comparación es entre el mismo tipo de valor, tanto `==` como `===` **hacen exactamente lo mismo, sin ninguna diferencia en absoluto.**

Si los tipos de valor que se comparan son diferentes, `==` se diferencia de `===` en que permite la coerción antes de la comparación. En otras palabras, ambos quieren comparar valores de tipos iguales, pero `==` permite conversiones de tipo *primero*, y una vez que los tipos se convirtieron para ser iguales en ambos lados, entonces `==` hace lo mismo que `===`. En lugar de "igualdad laxa", el operador `==` debería describirse como "igualdad coercitiva".

Considerá:

```js
42 == "42";             // true
1 == true;              // true
```

En ambas comparaciones, los tipos de valor son diferentes, así que el `==` hace que los valores no numéricos (`"42"` y `true`) se conviertan a números (`42` y `1`, respectivamente) antes de que se hagan las comparaciones.

Simplemente ser consciente de esta naturaleza de `==` —que prefiere las comparaciones numéricas primitivas— te ayuda a evitar la mayoría de los casos límite problemáticos, como mantenerte alejado de trampas como `"" == 0` o `0 == false`.

Quizás estés pensando: "Ah, bueno, simplemente voy a evitar siempre cualquier comparación de igualdad coercitiva (usando `===` en su lugar) para evitar esos casos límite". Eh, perdón, eso no es tan probable como esperarías.

Hay una muy buena posibilidad de que uses operadores de comparación relacional como `<`, `>` (e incluso `<=` y `>=`).

Al igual que `==`, estos operadores van a actuar como si fueran "estrictos" si los tipos que se comparan relacionalmente ya coinciden, pero van a permitir la coerción primero (generalmente, a números) si los tipos difieren.

Considerá:

```js
var arr = [ "1", "10", "100", "1000" ];
for (let i = 0; i < arr.length && arr[i] < 500; i++) {
    // will run 3 times
}
```

La comparación `i < arr.length` está "a salvo" de la coerción porque `i` y `arr.length` siempre son números. La comparación `arr[i] < 500` invoca coerción, sin embargo, porque los valores de `arr[i]` son todos strings. Esas comparaciones se convierten entonces en `1 < 500`, `10 < 500`, `100 < 500` y `1000 < 500`. Como esa cuarta es false, el bucle se detiene después de su tercera iteración.

Estos operadores relacionales típicamente usan comparaciones numéricas, excepto en el caso en que **ambos** valores que se comparan ya son strings; en este caso, usan comparación alfabética (como de diccionario) de los strings:

```js
var x = "10";
var y = "9";

x < y;      // true, watch out!
```

No hay manera de hacer que estos operadores relacionales eviten la coerción, aparte de simplemente no usar nunca tipos no coincidentes en las comparaciones. Eso quizás sea admirable como objetivo, pero igual es bastante probable que te encuentres con un caso donde los tipos *puedan* diferir.

El enfoque más sabio no es evitar las comparaciones coercitivas, sino abrazarlas y aprender sus entretelones.

Las comparaciones coercitivas surgen en otros lugares de JS, como en los condicionales (`if`, etc.), sobre los que vamos a volver en el Apéndice A, "Comparación Condicional Coercitiva."

## Cómo Organizamos en JS

Dos patrones principales para organizar el código (datos y comportamiento) se usan ampliamente a lo largo del ecosistema JS: clases y módulos. Estos patrones no son mutuamente excluyentes; muchos programas pueden usar y usan ambos. Otros programas van a quedarse con un solo patrón, ¡o incluso ninguno!

En algunos aspectos, estos patrones son muy diferentes. Pero curiosamente, en otros sentidos, son simplemente dos caras de la misma moneda. Ser competente en JS requiere entender ambos patrones y dónde son apropiados (¡y dónde no!).

### Clases

Los términos "orientado a objetos", "orientado a clases" y "clases" están todos muy cargados de detalle y matices; no son universales en su definición.

Vamos a usar acá una definición común y en cierto modo tradicional, la más probablemente familiar para quienes tienen experiencia en lenguajes "orientados a objetos" como C++ y Java.

Una clase en un programa es la definición de un "tipo" de estructura de datos personalizada que incluye tanto datos como comportamientos que operan sobre esos datos. Las clases definen cómo funciona semejante estructura de datos, pero las clases no son en sí mismas valores concretos. Para obtener un valor concreto que puedas usar en el programa, una clase debe ser *instanciada* (con la palabra clave `new`) una o más veces.

Considerá:

```js
class Page {
    constructor(text) {
        this.text = text;
    }

    print() {
        console.log(this.text);
    }
}

class Notebook {
    constructor() {
        this.pages = [];
    }

    addPage(text) {
        var page = new Page(text);
        this.pages.push(page);
    }

    print() {
        for (let page of this.pages) {
            page.print();
        }
    }
}

var mathNotes = new Notebook();
mathNotes.addPage("Arithmetic: + - * / ...");
mathNotes.addPage("Trigonometry: sin cos tan ...");

mathNotes.print();
// ..
```

En la clase `Page`, los datos son un string de texto almacenado en una propiedad miembro `this.text`. El comportamiento es `print()`, un método que vuelca el texto a la consola.

Para la clase `Notebook`, los datos son un array de instancias de `Page`. El comportamiento es `addPage(..)`, un método que instancia nuevas páginas `Page` y las agrega a la lista, así como `print()` (que imprime todas las páginas en el notebook).

La statement `mathNotes = new Notebook()` crea una instancia de la clase `Notebook`, y `page = new Page(text)` es donde se crean las instancias de la clase `Page`.

El comportamiento (los métodos) solo puede llamarse sobre las instancias (no sobre las clases en sí), como `mathNotes.addPage(..)` y `page.print()`.

El mecanismo de `class` permite empaquetar datos (`text` y `pages`) para organizarlos junto con sus comportamientos (por ejemplo, `addPage(..)` y `print()`). El mismo programa podría haberse construido sin ninguna definición de `class`, pero probablemente habría estado mucho menos organizado, habría sido más difícil de leer y razonar, y más susceptible a bugs y a un mantenimiento deficiente.

#### Herencia de Clases

Otro aspecto inherente al diseño tradicional "orientado a clases", aunque un poco menos usado comúnmente en JS, es la "herencia" (y el "polimorfismo"). Considerá:

```js
class Publication {
    constructor(title,author,pubDate) {
        this.title = title;
        this.author = author;
        this.pubDate = pubDate;
    }

    print() {
        console.log(`
            Title: ${ this.title }
            By: ${ this.author }
            ${ this.pubDate }
        `);
    }
}
```

Esta clase `Publication` define un conjunto de comportamiento común que cualquier publicación podría necesitar.

Ahora consideremos tipos más específicos de publicación, como `Book` y `BlogPost`:

```js
class Book extends Publication {
    constructor(bookDetails) {
        super(
            bookDetails.title,
            bookDetails.author,
            bookDetails.pubDate
        );
        this.publisher = bookDetails.publisher;
        this.ISBN = bookDetails.ISBN;
    }

    print() {
        super.print();
        console.log(`
            Publisher: ${ this.publisher }
            ISBN: ${ this.ISBN }
        `);
    }
}

class BlogPost extends Publication {
    constructor(title,author,pubDate,URL) {
        super(title,author,pubDate);
        this.URL = URL;
    }

    print() {
        super.print();
        console.log(this.URL);
    }
}
```

Tanto `Book` como `BlogPost` usan la cláusula `extends` para *extender* la definición general de `Publication` e incluir comportamiento adicional. La llamada `super(..)` en cada constructor delega al constructor de la clase padre `Publication` para su trabajo de inicialización, y luego hacen cosas más específicas según su respectivo tipo de publicación (es decir, "sub-clase" o "clase hija").

Ahora considerá el uso de estas clases hijas:

```js
var YDKJS = new Book({
    title: "You Don't Know JS",
    author: "Kyle Simpson",
    pubDate: "June 2014",
    publisher: "O'Reilly",
    ISBN: "123456-789"
});

YDKJS.print();
// Title: You Don't Know JS
// By: Kyle Simpson
// June 2014
// Publisher: O'Reilly
// ISBN: 123456-789

var forAgainstLet = new BlogPost(
    "For and against let",
    "Kyle Simpson",
    "October 27, 2014",
    "https://davidwalsh.name/for-and-against-let"
);

forAgainstLet.print();
// Title: For and against let
// By: Kyle Simpson
// October 27, 2014
// https://davidwalsh.name/for-and-against-let
```

Notá que ambas instancias de las clases hijas tienen un método `print()`, que fue una sobrescritura del método `print()` *heredado* de la clase padre `Publication`. Cada uno de esos métodos `print()` sobrescritos de las clases hijas llama a `super.print()` para invocar la versión heredada del método `print()`.

El hecho de que tanto el método heredado como el sobrescrito puedan tener el mismo nombre y coexistir se llama *polimorfismo*.

La herencia es una herramienta poderosa para organizar datos/comportamiento en unidades lógicas separadas (clases), pero permitiendo que la clase hija coopere con el padre accediendo/usando su comportamiento y sus datos.

### Módulos

El patrón de módulo tiene esencialmente el mismo objetivo que el patrón de clase, que es agrupar datos y comportamiento juntos en unidades lógicas. También, al igual que las clases, los módulos pueden "incluir" o "acceder" a los datos y comportamientos de otros módulos, en aras de la cooperación.

Pero los módulos tienen algunas diferencias importantes respecto de las clases. Lo más notable es que la sintaxis es enteramente distinta.

#### Módulos Clásicos

ES6 agregó una forma de sintaxis de módulo a la sintaxis nativa de JS, que vamos a ver en un momento. Pero desde los primeros días de JS, los módulos fueron un patrón importante y común que se aprovechó en incontables programas JS, incluso sin una sintaxis dedicada.

Las características distintivas clave de un *módulo clásico* son una función exterior (que corre al menos una vez), que devuelve una "instancia" del módulo con una o más funciones expuestas que pueden operar sobre los datos internos (ocultos) de la instancia del módulo.

Como un módulo de esta forma es *solo una función*, y llamarla produce una "instancia" del módulo, otra descripción para estas funciones es "fábricas de módulos" (module factories).

Considerá la forma de módulo clásico de las clases `Publication`, `Book` y `BlogPost` anteriores:

```js
function Publication(title,author,pubDate) {
    var publicAPI = {
        print() {
            console.log(`
                Title: ${ title }
                By: ${ author }
                ${ pubDate }
            `);
        }
    };

    return publicAPI;
}

function Book(bookDetails) {
    var pub = Publication(
        bookDetails.title,
        bookDetails.author,
        bookDetails.publishedOn
    );

    var publicAPI = {
        print() {
            pub.print();
            console.log(`
                Publisher: ${ bookDetails.publisher }
                ISBN: ${ bookDetails.ISBN }
            `);
        }
    };

    return publicAPI;
}

function BlogPost(title,author,pubDate,URL) {
    var pub = Publication(title,author,pubDate);

    var publicAPI = {
        print() {
            pub.print();
            console.log(URL);
        }
    };

    return publicAPI;
}
```

Comparando estas formas con las formas de `class`, hay más similitudes que diferencias.

La forma de `class` almacena los métodos y los datos en una instancia de objeto, a la que se debe acceder con el prefijo `this.`. Con los módulos, los métodos y los datos se acceden como variables identificadoras en el scope, sin ningún prefijo `this.`.

Con `class`, la "API" de una instancia es implícita en la definición de la clase; además, todos los datos y métodos son públicos. Con la función fábrica de módulo, creás y devolvés explícitamente un objeto con cualquier método expuesto públicamente, y cualquier dato u otros métodos no referenciados permanecen privados dentro de la función fábrica.

Hay otras variaciones de esta forma de función fábrica que son bastante comunes a lo largo de JS, incluso en 2020; podés toparte con estas formas en distintos programas JS: AMD (Asynchronous Module Definition), UMD (Universal Module Definition) y CommonJS (los módulos clásicos estilo Node.js). Las variaciones son menores (no del todo compatibles). Sin embargo, todas estas formas se basan en los mismos principios básicos.

Considerá también el uso (es decir, la "instanciación") de estas funciones fábrica de módulos:

```js
var YDKJS = Book({
    title: "You Don't Know JS",
    author: "Kyle Simpson",
    publishedOn: "June 2014",
    publisher: "O'Reilly",
    ISBN: "123456-789"
});

YDKJS.print();
// Title: You Don't Know JS
// By: Kyle Simpson
// June 2014
// Publisher: O'Reilly
// ISBN: 123456-789

var forAgainstLet = BlogPost(
    "For and against let",
    "Kyle Simpson",
    "October 27, 2014",
    "https://davidwalsh.name/for-and-against-let"
);

forAgainstLet.print();
// Title: For and against let
// By: Kyle Simpson
// October 27, 2014
// https://davidwalsh.name/for-and-against-let
```

La única diferencia observable acá es la ausencia del uso de `new`, llamando a las fábricas de módulos como funciones normales.

#### Módulos ES

Los módulos ES (ESM), introducidos al lenguaje JS en ES6, están pensados para servir prácticamente al mismo espíritu y propósito que los *módulos clásicos* recién descritos, teniendo especialmente en cuenta variaciones y casos de uso importantes de AMD, UMD y CommonJS.

El enfoque de implementación, sin embargo, difiere significativamente.

Primero, no hay una función envolvente para *definir* un módulo. El contexto envolvente es un archivo. Los ESM están siempre basados en archivos; un archivo, un módulo.

Segundo, no interactuás con la "API" de un módulo explícitamente, sino que usás la palabra clave `export` para agregar una variable o un método a su definición de API pública. Si algo se define en un módulo pero no se hace `export`, entonces permanece oculto (tal como con los *módulos clásicos*).

Tercero, y quizás lo más notablemente distinto de los patrones discutidos previamente, no "instanciás" un módulo ES, simplemente lo hacés `import` para usar su única instancia. Los ESM son, en efecto, "singletons", en el sentido de que solo hay una instancia creada, en el primer `import` en tu programa, y todos los demás `import` simplemente reciben una referencia a esa misma instancia única. Si tu módulo necesita soportar múltiples instanciaciones, tenés que proveer una función fábrica *al estilo de módulo clásico* en tu definición de ESM para ese propósito.

En nuestro ejemplo en curso, asumimos múltiple instanciación, así que los siguientes fragmentos van a mezclar tanto ESM como *módulos clásicos*.

Considerá el archivo `publication.js`:

```js
function printDetails(title,author,pubDate) {
    console.log(`
        Title: ${ title }
        By: ${ author }
        ${ pubDate }
    `);
}

export function create(title,author,pubDate) {
    var publicAPI = {
        print() {
            printDetails(title,author,pubDate);
        }
    };

    return publicAPI;
}
```

Para importar y usar este módulo, desde otro módulo ES como `blogpost.js`:

```js
import { create as createPub } from "publication.js";

function printDetails(pub,URL) {
    pub.print();
    console.log(URL);
}

export function create(title,author,pubDate,URL) {
    var pub = createPub(title,author,pubDate);

    var publicAPI = {
        print() {
            printDetails(pub,URL);
        }
    };

    return publicAPI;
}
```

Y finalmente, para usar este módulo, lo importamos dentro de otro módulo ES como `main.js`:

```js
import { create as newBlogPost } from "blogpost.js";

var forAgainstLet = newBlogPost(
    "For and against let",
    "Kyle Simpson",
    "October 27, 2014",
    "https://davidwalsh.name/for-and-against-let"
);

forAgainstLet.print();
// Title: For and against let
// By: Kyle Simpson
// October 27, 2014
// https://davidwalsh.name/for-and-against-let
```

| NOTA: |
| :--- |
| La cláusula `as newBlogPost` en la `import` statement es opcional; si se omite, se importaría una función de nivel superior simplemente llamada `create(..)`. En este caso, la estoy renombrando por el bien de la legibilidad; su nombre de fábrica más genérico `create(..)` se vuelve más descriptivo semánticamente de su propósito como `newBlogPost(..)`. |

Como se muestra, los módulos ES pueden usar *módulos clásicos* internamente si necesitan soportar múltiple instanciación. Alternativamente, podríamos haber expuesto una `class` desde nuestro módulo en lugar de una función fábrica `create(..)`, con prácticamente el mismo resultado. Sin embargo, dado que a esa altura ya estás usando ESM, recomendaría quedarse con los *módulos clásicos* en lugar de `class`.

Si tu módulo solo necesita una única instancia, podés saltarte las capas extra de complejidad: hacé `export` de sus métodos públicos directamente.

## La Madriguera del Conejo se Profundiza

Como se prometió al comienzo de este capítulo, acabamos de dar un vistazo a una amplia superficie de las partes principales del lenguaje JS. Tu cabeza quizás todavía esté dando vueltas, ¡pero eso es completamente natural después de semejante chorro de información!

Incluso con este "breve" repaso de JS, cubrimos o insinuamos un montón de detalles que deberías considerar cuidadosamente y asegurarte de sentirte cómodo con ellos. Hablo en serio cuando sugiero: releé este capítulo, quizás varias veces.

En el próximo capítulo, vamos a profundizar mucho más en algunos aspectos importantes de cómo funciona JS en su núcleo. Pero antes de seguir esa madriguera del conejo más hondo, asegurate de haberte tomado el tiempo adecuado para digerir completamente lo que acabamos de cubrir acá.
