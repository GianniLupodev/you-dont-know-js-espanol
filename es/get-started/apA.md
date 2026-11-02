# You Don't Know JS Yet: Get Started - 2nd Edition
# Apéndice A: Explorando más a fondo

En este apéndice vamos a explorar con un poco más de detalle algunos temas del texto principal de los capítulos. Pensá en este contenido como una vista previa opcional de algunos de los detalles más sutiles que se tratan a lo largo del resto de la serie de libros.

## Valores vs. Referencias

En el Capítulo 2 presentamos los dos tipos principales de valores: primitivos y objetos. Pero todavía no discutimos una diferencia clave entre ambos: cómo se asignan y se pasan estos valores.

En muchos lenguajes, quien desarrolla puede elegir entre asignar/pasar un valor como el valor en sí mismo, o como una referencia al valor. En JS, sin embargo, esta decisión está determinada por completo por el tipo de valor. Eso sorprende a muchas personas que vienen de otros lenguajes cuando empiezan a usar JS.

Si asignás/pasás el valor en sí mismo, el valor se copia. Por ejemplo:

```js
var myName = "Kyle";

var yourName = myName;
```

Acá, la variable `yourName` tiene una copia separada del string `"Kyle"` respecto del valor que está almacenado en `myName`. Eso es porque el valor es un primitivo, y los valores primitivos siempre se asignan/pasan como **copias de valor**.

Así es como podés demostrar que hay dos valores separados involucrados:

```js
var myName = "Kyle";

var yourName = myName;

myName = "Frank";

console.log(myName);
// Frank

console.log(yourName);
// Kyle
```

¿Ves cómo `yourName` no se vio afectada por la reasignación de `myName` a `"Frank"`? Eso es porque cada variable tiene su propia copia del valor.

En cambio, las referencias son la idea de que dos o más variables apuntan al mismo valor, de modo que modificar ese valor compartido se reflejaría al acceder a través de cualquiera de esas referencias. En JS, solo los valores de tipo objeto (arrays, objetos, funciones, etc.) se tratan como referencias.

Considerá:

```js
var myAddress = {
    street: "123 JS Blvd",
    city: "Austin",
    state: "TX"
};

var yourAddress = myAddress;

// I've got to move to a new house!
myAddress.street = "456 TS Ave";

console.log(yourAddress.street);
// 456 TS Ave
```

Como el valor asignado a `myAddress` es un objeto, se mantiene/asigna por referencia, y por lo tanto la asignación a la variable `yourAddress` es una copia de la referencia, no del valor objeto en sí mismo. Por eso el valor actualizado asignado a `myAddress.street` se refleja cuando accedemos a `yourAddress.street`. `myAddress` y `yourAddress` tienen copias de la referencia al único objeto compartido, así que una actualización en una es una actualización en ambas.

De nuevo, JS elige el comportamiento de copia-de-valor vs. copia-de-referencia según el tipo de valor. Los primitivos se mantienen por valor, los objetos se mantienen por referencia. No hay forma de anular esto en JS, en ninguna de las dos direcciones.

## Tantas formas de función

Recordá este fragmento de la sección "Funciones" del Capítulo 2:

```js
var awesomeFunction = function(coolThings) {
    // ..
    return amazingStuff;
};
```

La expresión de función de acá se denomina *expresión de función anónima*, ya que no tiene un identificador de nombre entre la palabra clave `function` y la lista de parámetros `(..)`. Este punto confunde a muchas personas que desarrollan en JS porque, a partir de ES6, JS realiza una "inferencia de nombre" sobre una función anónima:

```js
awesomeFunction.name;
// "awesomeFunction"
```

La propiedad `name` de una función revelará o bien su nombre dado directamente (en el caso de una declaración) o bien su nombre inferido en el caso de una expresión de función anónima. Ese valor generalmente lo usan las herramientas de desarrollo al inspeccionar un valor de función o al reportar un stack trace de error.

Así que incluso una expresión de función anónima *podría* obtener un nombre. Sin embargo, la inferencia de nombre solo ocurre en casos limitados, como cuando la expresión de función se asigna (con `=`). Si pasás una expresión de función como argumento a una llamada de función, por ejemplo, no ocurre inferencia de nombre; la propiedad `name` será un string vacío, y la consola de desarrollo normalmente reportará "(anonymous function)".

Incluso si se infiere un nombre, **sigue siendo una función anónima.** ¿Por qué? Porque el nombre inferido es un valor de string de metadatos, no un identificador disponible para referirse a la función. Una función anónima no tiene un identificador para usar que le permita referirse a sí misma desde adentro de sí misma—para recursión, para desvincular eventos, etc.

Compará la forma de la expresión de función anónima con:

```js
// let awesomeFunction = ..
// const awesomeFunction = ..
var awesomeFunction = function someName(coolThings) {
    // ..
    return amazingStuff;
};

awesomeFunction.name;
// "someName"
```

Esta expresión de función es una *expresión de función nombrada*, ya que el identificador `someName` está asociado directamente con la expresión de función en tiempo de compilación; la asociación con el identificador `awesomeFunction` igual no ocurre hasta el tiempo de ejecución, en el momento de ese statement. Esos dos identificadores no tienen por qué coincidir; a veces tiene sentido que sean diferentes, y otras veces es mejor que sean iguales.

Notá también que el nombre explícito de la función, el identificador `someName`, tiene precedencia al asignar un *nombre* para la propiedad `name`.

¿Las expresiones de función deberían ser nombradas o anónimas? Las opiniones varían muchísimo al respecto. La mayoría de quienes desarrollan tienden a no preocuparse por usar funciones anónimas. Son más cortas, y sin duda más comunes en la amplia esfera del código JS que anda dando vueltas.

En mi opinión, si una función existe en tu programa, tiene un propósito; de lo contrario, ¡sacala! Y si tiene un propósito, tiene un nombre natural que describe ese propósito.

Si una función tiene un nombre, vos, quien escribe el código, deberías incluir ese nombre en el código, para que quien lo lee no tenga que inferir ese nombre leyendo y ejecutando mentalmente el código fuente de esa función. Incluso un cuerpo de función trivial como `x * 2` hay que leerlo para inferir un nombre como "double" o "multBy2"; ese breve trabajo mental extra es innecesario cuando podrías tomarte un segundo para nombrar la función "double" o "multBy2" *una sola vez*, ahorrándole a quien lee ese trabajo mental repetido cada vez que se lea en el futuro.

Hay, lamentablemente en algunos aspectos, muchas otras formas de definición de función en JS a principios de 2020 (¡quizás más en el futuro!).

Acá hay algunas formas de declaración más:

```js
// generator function declaration
function *two() { .. }

// async function declaration
async function three() { .. }

// async generator function declaration
async function *four() { .. }

// named function export declaration (ES6 modules)
export function five() { .. }
```

Y acá hay algunas más de las (¡muchas!) formas de expresión de función:

```js
// IIFE
(function(){ .. })();
(function namedIIFE(){ .. })();

// asynchronous IIFE
(async function(){ .. })();
(async function namedAIIFE(){ .. })();

// arrow function expressions
var f;
f = () => 42;
f = x => x * 2;
f = (x) => x * 2;
f = (x,y) => x * y;
f = x => ({ x: x * 2 });
f = x => { return x * 2; };
f = async x => {
    var y = await doSomethingAsync(x);
    return y * 2;
};
someOperation( x => x * 2 );
// ..
```

Tené en cuenta que las arrow function expressions son **sintácticamente anónimas**, lo que significa que la sintaxis no provee una forma de dar un identificador de nombre directo a la función. La expresión de función puede obtener un nombre inferido, pero solo si es una de las formas de asignación, no en la forma (¡más común!) de ser pasada como argumento de una llamada de función (como en la última línea del fragmento).

Como no creo que las funciones anónimas sean una buena idea para usar con frecuencia en tus programas, no soy fanático de usar la forma de arrow function `=>`. Este tipo de función en realidad tiene un propósito específico (es decir, manejar la palabra clave `this` de forma léxica), pero eso no significa que debamos usarla para cada función que escribimos. Usá la herramienta más apropiada para cada trabajo.

Las funciones también se pueden especificar en definiciones de clase y en definiciones de objetos literales. Normalmente se las denomina "métodos" cuando están en estas formas, aunque en JS este término no tiene mucha diferencia observable respecto de "función":

```js
class SomethingKindaGreat {
    // class methods
    coolMethod() { .. }   // no commas!
    boringMethod() { .. }
}

var EntirelyDifferent = {
    // object methods
    coolMethod() { .. },   // commas!
    boringMethod() { .. },

    // (anonymous) function expression property
    oldSchool: function() { .. }
};
```

¡Uf! Esa es un montón de formas distintas de definir funciones.

Acá no hay ningún atajo simple; simplemente tenés que construir familiaridad con todas las formas de función para poder reconocerlas en el código existente y usarlas apropiadamente en el código que escribís. ¡Estudialas de cerca y practicá!

## Comparación condicional coercitiva

Sí, el nombre de esa sección es todo un trabalenguas. ¿Pero de qué estamos hablando? Estamos hablando de expresiones condicionales que necesitan realizar comparaciones orientadas a la coerción para tomar sus decisiones.

Los statements `if` y el ternario `? :`, así como las cláusulas de prueba en los bucles `while` y `for`, todos realizan una comparación implícita de valores. Pero ¿de qué tipo? ¿Es "estricta" o "coercitiva"? Ambas, en realidad.

Considerá:

```js
var x = 1;

if (x) {
    // will run!
}

while (x) {
    // will run, once!
    x = false;
}
```

Podrías pensar en estas expresiones condicionales `(x)` así:

```js
var x = 1;

if (x == true) {
    // will run!
}

while (x == true) {
    // will run, once!
    x = false;
}
```

En este caso específico —el valor de `x` siendo `1`— ese modelo mental funciona, pero no es preciso de forma más general. Considerá:

```js
var x = "hello";

if (x) {
    // will run!
}

if (x == true) {
    // won't run :(
}
```

Ups. Entonces, ¿qué está haciendo en realidad el statement `if`? Este es el modelo mental más preciso:

```js
var x = "hello";

if (Boolean(x) == true) {
    // will run
}

// which is the same as:

if (Boolean(x) === true) {
    // will run
}
```

Como la función `Boolean(..)` siempre devuelve un valor de tipo boolean, el `==` vs `===` en este fragmento es irrelevante; ambos harán lo mismo. Pero lo importante es ver que, antes de la comparación, ocurre una coerción, desde cualquier tipo que `x` tenga en ese momento hacia boolean.

Simplemente no podés escapar de las coerciones en las comparaciones de JS. Ponete las pilas y aprendelas.

## "Clases" prototipales

En el Capítulo 3 presentamos los prototypes y mostramos cómo podemos vincular objetos a través de una cadena de prototype.

Otra forma de conectar dichos vínculos de prototype sirvió como predecesora (honestamente, fea) de la elegancia del sistema `class` de ES6 (ver el Capítulo 2, "Clases"), y se denomina clases prototipales.

| TIP: |
| :--- |
| ¡Aunque este estilo de código es bastante infrecuente en JS hoy en día, sigue siendo desconcertantemente común que te pregunten sobre él en entrevistas de trabajo! |

Primero recordemos el estilo de codificación con `Object.create(..)`:

```js
var Classroom = {
    welcome() {
        console.log("Welcome, students!");
    }
};

var mathClass = Object.create(Classroom);

mathClass.welcome();
// Welcome, students!
```

Acá, un objeto `mathClass` está vinculado a través de su prototype a un objeto `Classroom`. A través de este vínculo, la llamada de función `mathClass.welcome()` se delega al método definido en `Classroom`.

El patrón de clase prototipal habría etiquetado este comportamiento de delegación como "herencia", y alternativamente lo habría definido (con el mismo comportamiento) así:

```js
function Classroom() {
    // ..
}

Classroom.prototype.welcome = function hello() {
    console.log("Welcome, students!");
};

var mathClass = new Classroom();

mathClass.welcome();
// Welcome, students!
```

Todas las funciones, por defecto, referencian un objeto vacío en una propiedad llamada `prototype`. A pesar de la nomenclatura confusa, este **no** es el *prototype* de la función (donde la función está vinculada por prototype), sino más bien el objeto prototype al cual *vincular* cuando se crean otros objetos llamando a la función con `new`.

Agregamos una propiedad `welcome` sobre ese objeto vacío (llamado `Classroom.prototype`), apuntando a la función `hello()`.

Luego `new Classroom()` crea un nuevo objeto (asignado a `mathClass`), y lo vincula por prototype al objeto `Classroom.prototype` existente.

Aunque `mathClass` no tiene una propiedad/función `welcome()`, delega exitosamente a la función `Classroom.prototype.welcome()`.

Este patrón de "clase prototipal" ahora se desaconseja fuertemente, en favor de usar el mecanismo `class` de ES6:

```js
class Classroom {
    constructor() {
        // ..
    }

    welcome() {
        console.log("Welcome, students!");
    }
}

var mathClass = new Classroom();

mathClass.welcome();
// Welcome, students!
```

Por debajo, se conecta el mismo vínculo de prototype, pero esta sintaxis `class` encaja con el patrón de diseño orientado a clases de forma mucho más limpia que las "clases prototipales".
