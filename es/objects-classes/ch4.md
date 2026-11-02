# You Don't Know JS Yet: Objects & Classes - 2nd Edition
# Capítulo 4: This Funciona

| NOTA: |
| :--- |
| Trabajo en progreso |

Hasta ahora hemos visto usar bastante la palabra clave `this`, pero en realidad no hemos profundizado para entender exactamente cómo funciona en JS. Es hora de hacerlo.

Pero para entender correctamente `this` en JS, necesitas dejar de lado cualquier preconcepto que puedas tener, especialmente suposiciones provenientes de cómo funciona `this` en otros lenguajes de programación en los que puedas tener experiencia.

Esto es lo más importante que hay que entender sobre `this`: la determinación de qué valor (usualmente, objeto) apunta `this` no se hace en tiempo de autoría, sino que se determina en tiempo de ejecución. Eso significa que no puedes simplemente mirar una función `this`-aware (incluso un method en una definición de `class`) y saber con certeza qué contendrá `this` mientras esa función se ejecuta.

En cambio, tienes que encontrar cada lugar donde se invoca la función, y mirar *cómo* se invoca (ni siquiera importa *dónde*). Esa es la única manera de responder completamente a qué apuntará `this`.

De hecho, una misma función `this`-aware puede invocarse de al menos cuatro maneras diferentes, y cualquiera de esos enfoques terminará asignando un `this` distinto para esa invocación de función en particular.

Así que la pregunta típica que podríamos hacernos al leer código -- "¿A qué apunta `this` en la función?" -- no es en realidad una pregunta válida. La pregunta que realmente tienes que hacerte es: "Cuando la función se invoca de cierta manera, ¿qué `this` se asignará para esa invocación?"

Si tu cerebro ya se está retorciendo con solo leer esta introducción del capítulo... ¡bien! Acomódate para un recableado de cómo piensas sobre `this` en JS.

## This Aware

Usé la frase `this`-aware hace un momento. Pero, ¿qué quiero decir exactamente con eso?

Cualquier función que tenga una palabra clave `this` dentro.

Si una función no tiene `this` en ningún lado, entonces las reglas de cómo se comporta `this` no afectan a esa función de ninguna manera. Pero si *sí* tiene aunque sea un solo `this`, entonces no puedes de ninguna manera determinar cómo se comportará la función sin averiguar, para cada invocación de la función, a qué apuntará `this`.

Es como si la palabra clave `this` fuera un marcador de posición en una plantilla. La sustitución del valor de ese marcador de posición no se determina cuando escribimos el código; se determina mientras el código se está ejecutando.

Podrías pensar que estoy jugando con las palabras acá. Por supuesto, cuando escribes el programa, escribes todas las llamadas a cada función, así que ya determinaste qué va a ser `this` cuando escribiste el código, ¿verdad? ¡¿Verdad?!

¡No tan rápido!

En primer lugar, no siempre escribes todo el código que invoca tu(s) función(es). Tu(s) función(es) `this`-aware podrían pasarse como callback(s) a algún otro código, ya sea en tu base de código, o en un framework/utilidad de terceros, o incluso dentro de un mecanismo nativo incorporado del lenguaje o del entorno que aloja tu programa.

Pero incluso dejando de lado el paso de funciones como callbacks, varios mecanismos en JS permiten comportamientos condicionales en tiempo de ejecución para determinar qué valor (de nuevo, usualmente objeto) se asignará al `this` de una invocación de función en particular. Así que aunque hayas escrito todo ese código, *en el mejor de los casos* tendrás que ejecutar mentalmente las distintas condiciones/caminos que terminan afectando la invocación de la función.

¿Y por qué importa todo esto?

Porque no eres solo tú, el autor del código, quien necesita descifrar estas cosas. Es *cada lector* de tu código, para siempre. Si alguien (incluso tu futuro yo) quiere leer un fragmento de código que define una función `this`-aware, eso inevitablemente significa que, para entender y predecir completamente su comportamiento, esa persona tendrá que encontrar, leer y entender cada una de las invocaciones de esa función.

### This Confuses Me

Ahora bien, para ser justos, eso ya es parcialmente cierto si consideramos los parámetros de una función. Para entender cómo va a funcionar una función, necesitamos saber qué se le está pasando. Así que cualquier función con al menos un parámetro es, en un sentido similar, *argument*-aware -- es decir, qué argumento(s) se pasa(n) y se asigna(n) a los parámetros de la función.

Pero con los parámetros, a menudo tenemos un poco más de pista desde la propia función sobre qué harán y contendrán los parámetros.

A menudo vemos los nombres de los parámetros declarados justo en el encabezado de la función, lo que contribuye mucho a explicar su naturaleza/propósito. Y si hay valores por defecto para los parámetros, a menudo los vemos declarados en línea con cláusulas `= loquesea`. Más aún, dependiendo del estilo de código del autor, podríamos ver en las primeras líneas de la función un conjunto de lógica que se aplica a estos parámetros; esto podría ser aserciones sobre los valores (valores no permitidos, etc), o incluso modificaciones (conversión de tipos, formateo, etc).

En realidad, `this` se parece mucho a un parámetro de una función, pero es un parámetro implícito en lugar de uno explícito. No ves ninguna señal de que `this` vaya a usarse, en ningún lado del encabezado de la función. Tienes que leer todo el cuerpo de la función para ver si `this` aparece en algún lado.

El nombre del "parámetro" siempre es `this`, así que no obtenemos mucha pista sobre su naturaleza/propósito a partir de un nombre tan general. De hecho, históricamente hay mucha confusión sobre qué se supone que significa "this". Y rara vez vemos mucho (si es que algo) hecho para validar/convertir/etc el valor de `this` aplicado a una invocación de función. De hecho, prácticamente todo el código `this`-aware que he visto simplemente asume alegremente que el "parámetro" `this` está conteniendo exactamente el valor que se espera. ¡Hablando de **una trampa para bugs inesperados!**

### So What Is This?

Si `this` es un parámetro implícito, ¿cuál es su propósito? ¿Qué se está pasando?

Con suerte ya has leído el libro "Scope & Closures" de esta serie. Si no, te animo enérgicamente a volver y leer ese una vez que termines este. En ese libro, expliqué extensamente cómo funcionan los scopes (¡y los closures!), una característica especialmente importante de las funciones.

El lexical scope (incluyendo todas las variables sobre las que se hace closure) representa un contexto *estático* contra el cual se evalúan las referencias a identificadores léxicos de la función. Es fijo/estático porque en tiempo de autoría, cuando colocas funciones y declaraciones de variables en varios scopes (anidados), esas decisiones son fijas, y no se ven afectadas por ninguna condición de tiempo de ejecución.

En contraste, un lenguaje de programación diferente podría ofrecer scope *dinámico*, donde el contexto para las referencias a variables de una función no se determina por decisiones en tiempo de autoría sino por condiciones en tiempo de ejecución. Tal sistema sería, sin duda, más flexible que el contexto estático -- aunque con la flexibilidad a menudo viene la complejidad.

Para ser claros: el scope en JS es siempre y únicamente léxico y *estático* (si ignoramos trucos del non-strict mode como `eval(..)` y `with`). Sin embargo, una de las cosas verdaderamente poderosas de JS es que ofrece otro mecanismo con flexibilidad y capacidades similares al scope *dinámico*.

El mecanismo `this` es, en efecto, contexto *dinámico* (no scope); es cómo una función `this`-aware puede invocarse dinámicamente contra diferentes contextos -- ¡algo que es imposible con los identificadores de closure y lexical scope!

### Why Is This So Implicit?

Podrías preguntarte por qué algo tan importante como un contexto *dinámico* se maneja como una entrada implícita a una función, en lugar de ser un argumento explícito que se pasa.

Esa es una pregunta muy importante, pero no es una que podamos responder del todo, todavía. Aférrate a esa pregunta, eso sí.

### Can We Get On With This?

Entonces, ¿por qué me he explayado tanto sobre *este* tema por un par de páginas ya? Lo entiendes, ¿verdad? Estás listo para seguir adelante.

Mi punto es que tú, el autor del código, y todos los demás lectores del código incluso años o décadas en el futuro, necesitan ser `this`-aware. Esa es la elección, la carga, que impones sobre la lectura de tal código. Y sí, eso vale para la elección de usar `class` (ver Capítulo 3), ya que la mayoría de los methods de clase serán `this`-aware por necesidad.

Sé consciente de *esta* elección de `this` en el código que escribes. Hazlo intencionalmente, y hazlo de tal manera que produzca más beneficio en el resultado que carga. Asegúrate de que el uso de `this` en tu código *justifique su propio peso*.

Déjame ponerlo de *esta* manera: no uses código `this`-aware a menos que realmente puedas justificarlo, y hayas sopesado cuidadosamente los costos. Solo porque hayas visto muchos ejemplos de código lanzando `this` por todos lados en el código de otros, no significa que `this` pertenezca en *este* código que estás escribiendo.

El mecanismo `this` en JS, emparejado con la delegación de `[[Prototype]]`, es un pilar extremadamente poderoso del lenguaje. Pero como dice el cliché: "un gran poder conlleva una gran responsabilidad". Anecdóticamente, aunque realmente me gusta y aprecio *este* pilar de JS, probablemente menos del 5% del código JS que escribo lo usa. Y cuando lo hago, es con moderación. No es mi capacidad de JS por defecto, a la que recurro primero.

## This Is It!

OK, basta de la conferencia verborrágica. Estás listo para sumergirte en el código de `this`, ¿verdad?

Volvamos (y extendamos) a `Point2d` del Capítulo 3, pero solo como un objeto con propiedades de datos y funciones sobre él, en lugar de usar `class`:

```js
var point = {
    x: null,
    y: null,

    init(x,y) {
        this.x = x;
        this.y = y;
    },
    rotate(angleRadians) {
        var rotatedX = this.x * Math.cos(angleRadians) -
            this.y * Math.sin(angleRadians);
        var rotatedY = this.x * Math.sin(angleRadians) +
            this.y * Math.cos(angleRadians);
        this.x = rotatedX;
        this.y = rotatedY;
    },
    toString() {
        return `(${this.x},${this.y})`;
    },
};
```

Como puedes ver, las funciones `init(..)`, `rotate(..)` y `toString()` son `this`-aware. Podrías tener la costumbre de asumir que la referencia `this` obviamente siempre contendrá el objeto `point`. Pero eso no está garantizado de ninguna manera.

Sigue recordándote a medida que avanzas por el resto de este capítulo: el valor de `this` para una función se determina por *cómo* se invoca la función. Eso significa que no puedes mirar la definición de la función, ni dónde se define la función (¡ni siquiera la `class` que la contiene!). De hecho, ni siquiera importa desde dónde se llama la función.

Solo necesitamos mirar *cómo* se llaman las funciones; ese es el único factor que importa.

### Implicit Context Invocation

Considera esta llamada:

```js
point.init(3,4);
```

Estamos invocando la función `init(..)`, pero fíjate en el `point.` delante de ella. Este es un binding de *contexto implícito*. Le dice a JS: invoca la función `init(..)` con `this` referenciando a `point`.

Esa es la manera *normal* en que esperaríamos que funcione un `this`, y esa es también una de las maneras más comunes en que invocamos funciones. Así que la invocación típica nos da el resultado intuitivo. ¡Eso es algo bueno!

### Default Context Invocation

Pero, ¿qué pasa si hacemos esto?

```js
const init = point.init;
init(3,4);
```

Podrías asumir que obtendríamos el mismo resultado que el fragmento anterior. Pero no es así como funciona la asignación de `this` en JS.

El *call-site* de la función es `init(3,4)`, que es diferente de `point.init(3,4)`. Cuando no hay *contexto implícito* (`point.`), ni ningún otro tipo de mecanismo de asignación de `this`, ocurre la asignación de *contexto por defecto*.

¿A qué referenciará `this` cuando `init(3,4)` se invoque de esa manera?

*Depende.*

Uh oh. ¿Depende? Eso suena confuso.

No te preocupes, no es tan malo como suena. La asignación de *contexto por defecto* depende de si el código está en strict mode o no. Pero por suerte, prácticamente todo el código JS en estos días se está ejecutando en strict mode; por ejemplo, ESM (ES Modules) siempre se ejecuta en strict mode, al igual que el código dentro de un bloque `class`. Y prácticamente todo el código JS transpilado (vía Babel, TypeScript, etc) está escrito para declarar strict mode.

Así que casi todo el tiempo, el código JS moderno se estará ejecutando en strict mode, y por lo tanto el contexto de *asignación por defecto* no "dependerá" de nada; es bastante sencillo: `undefined`. ¡Eso es todo!

| NOTA: |
| :--- |
| Ten en cuenta: `undefined` no significa "no definido"; significa "definido con el valor especial vacío `undefined`". Lo sé, lo sé... el nombre y el significado no coinciden. Es el equipaje heredado del lenguaje, para ti. (encogiéndose de hombros) |

Eso significa que `init(3,4)`, si se ejecuta en strict mode, lanzaría una excepción. ¿Por qué? Porque la referencia `this.x` en `init(..)` es un acceso a la propiedad `.x` sobre `undefined` (es decir, `undefined.x`), lo cual no está permitido:

```js
"use strict";

var point = { /* .. */ };

const init = point.init;
init(3,4);
// TypeError: Cannot set properties of
// undefined (setting 'x')
```

Detente un momento y considera: ¿por qué elegiría JS poner por defecto el contexto en `undefined`, de modo que cualquier invocación de *contexto por defecto* de una función `this`-aware falle con tal excepción?

Porque una función `this`-aware **siempre necesita un `this`**. La invocación `init(3,4)` no está proporcionando un `this`, así que eso *es* un error, y *debería* lanzar una excepción para que el error pueda corregirse. La lección: ¡nunca invoques una función `this`-aware sin proporcionarle un `this`!

Solo para completar: en el menos común non-strict mode, el *contexto por defecto* es el objeto global -- JS lo define como `globalThis`, que en el JS de navegador es esencialmente un alias de `window`, y en Node es `global`. Así que, cuando `init(3,4)` se ejecuta en non-strict mode, la expresión `this.x` es `globalThis.x` -- también conocida como `window.x` en el navegador, o `global.x` en Node. Por lo tanto, `globalThis.x` queda establecido en `3` y `globalThis.y` queda establecido en `4`.

```js
// no strict-mode here, beware!

var point = { /* .. */ };

const init = point.init;
init(3,4);

globalThis.x;   // 3
globalThis.y;   // 4
point.x;        // null
point.y;        // null
```

Eso es desafortunado, porque es casi seguro que *no* es el resultado deseado. No solo es malo si es una variable global, sino que tampoco está cambiando la propiedad en nuestro objeto `point`, así que los bugs del programa están garantizados.

| ADVERTENCIA: |
| :--- |
| ¡Ay! Nadie quiere variables globales accidentales creadas implícitamente desde todas partes del código. La lección: ¡asegúrate siempre de que tu código se esté ejecutando en strict mode! |

### Explicit Context Invocation

Las funciones pueden invocarse alternativamente con *contexto explícito*, usando las utilidades incorporadas `call(..)` o `apply(..)`:

```js
var point = { /* .. */ };

const init = point.init;

init.call( point, 3, 4 );
// or: init.apply( point, [ 3, 4 ] )

point.x;        // 3
point.y;        // 4
```

`init.call(point,3,4)` es efectivamente lo mismo que `point.init(3,4)`, en el sentido de que ambos asignan `point` como el contexto de `this` para la invocación de `init(..)`.

| NOTA: |
| :--- |
| Tanto la utilidad `call(..)` como `apply(..)` toman como su primer argumento un valor de contexto para `this`; eso casi siempre es un objeto, pero técnicamente puede ser cualquier valor (number, string, etc). La utilidad `call(..)` toma los argumentos subsiguientes y los pasa a la función invocada, mientras que `apply(..)` espera que su segundo argumento sea un array de valores para pasar como argumentos. |

Podría parecer incómodo contemplar invocar una función con el estilo de asignación de *contexto explícito* (`call(..)` / `apply(..)`) en tu programa. Pero es más útil de lo que podría ser obvio a primera vista.

Recordemos el fragmento original:

```js
var point = {
    x: null,
    y: null,

    init(x,y) {
        this.x = x;
        this.y = y;
    },
    rotate(angleRadians) { /* .. */ },
    toString() {
        return `(${this.x},${this.y})`;
    },
};

point.init(3,4);

var anotherPoint = {};
point.init.call( anotherPoint, 5, 6 );

point.x;                // 3
point.y;                // 4
anotherPoint.x;         // 5
anotherPoint.y;         // 6
```

¿Estás viendo lo que hice ahí?

Quería definir `anotherPoint`, pero no quería repetir las definiciones de esas funciones `init(..)` / `rotate(..)` / `toString()` de `point`. Así que "tomé prestada" una referencia de función, `point.init`, y establecí explícitamente el objeto vacío `anotherPoint` como el contexto de `this`, vía `call(..)`.

Cuando `init(..)` se está ejecutando en ese momento, `this` dentro de ella referenciará a `anotherPoint`, y por eso las propiedades `x` / `y` (valores `5` / `6`, respectivamente) quedan establecidas ahí.

Cualquier función `this`-aware puede tomarse prestada de esta manera: `point.rotate.call(anotherPoint, ..)`, `point.toString.call(anotherPoint)`.

#### Revisiting Implicit Context Invocation

Otro enfoque para compartir comportamiento entre `point` y `anotherPoint` habría sido:

```js
var point = { /* .. */ };

var anotherPoint = {
    init: point.init,
    rotate: point.rotate,
    toString: point.toString,
};

anotherPoint.init(5,6);

anotherPoint.x;         // 5
anotherPoint.y;         // 6
```

Esta es otra manera de "tomar prestadas" las funciones, agregando referencias compartidas a las funciones en cualquier objeto destino (por ejemplo, `anotherPoint`). La invocación en el call-site `anotherPoint.init(5,6)` es el estilo más natural/ergonómico que se apoya en la asignación de *contexto implícito*.

Puede parecer que este enfoque es un poco más limpio, comparando `anotherPoint.init(5,6)` con `point.init.call(anotherPoint,5,6)`.

Pero la principal desventaja es tener que modificar cualquier objeto destino con tales referencias de función compartidas, lo que puede ser verboso, manual y propenso a errores. A veces tal enfoque es aceptable, pero muchas otras veces, la asignación de *contexto explícito* con `call(..)` / `apply(..)` es más preferible.

### New Context Invocation

Hasta ahora hemos visto tres maneras diferentes de asignación de contexto en el call-site de la función: *por defecto*, *implícito* y *explícito*.

Una cuarta manera de llamar a una función, y asignar el `this` para esa invocación, es con la palabra clave `new`:

```js
var point = {
    // ..

    init: function() { /* .. */ }

    // ..
};

var anotherPoint = new point.init(3,4);

anotherPoint.x;     // 3
anotherPoint.y;     // 4
```

| TIP: |
| :--- |
| Este ejemplo tiene un poco de matiz por explicar. La forma `init: function() { .. }` mostrada aquí -- específicamente, una function expression asignada a una propiedad -- es requerida para que la función pueda llamarse válidamente con la palabra clave `new`. De fragmentos anteriores, la forma concisa de method `init() { .. }` define una función que *no puede* llamarse con `new`. |

Típicamente has visto `new` usado con `class` para crear instancias. Pero como mecanismo subyacente del lenguaje JS, `new` no es inherentemente una operación de `class`.

En cierto sentido, la palabra clave `new` secuestra una función y fuerza su comportamiento a un modo diferente al de una invocación normal. Aquí están los 4 pasos especiales que JS realiza cuando una función se invoca con `new`:

1. crea un objeto vacío completamente nuevo, de la nada.

2. enlaza el `[[Prototype]]` de ese nuevo objeto vacío al objeto `.prototype` de la función (ver Capítulo 2).

3. invoca la función con el contexto de `this` establecido en ese nuevo objeto vacío.

4. si la función no retorna explícitamente su propio valor de objeto (con una sentencia `return ..`), asume que la llamada a la función debería en cambio retornar el nuevo objeto (de los pasos 1-3).

| ADVERTENCIA: |
| :--- |
| El paso 4 implica que si invocas con `new` una función que *sí* retorna su propio objeto -- como `return { .. }`, etc -- entonces el nuevo objeto de los pasos 1-3 *no* se retorna. Ese es un gotcha complicado del cual hay que estar al tanto, en el sentido de que efectivamente descarta ese nuevo objeto antes de que el programa tenga la oportunidad de recibir y almacenar una referencia a él. Esencialmente, `new` nunca debería usarse para invocar una función que tiene sentencia(s) `return ..` explícita(s) dentro. |

Para entender estos 4 pasos de `new` de manera más concreta, voy a ilustrarlos en código, como una alternativa a usar la palabra clave `new`:

```js
// alternative to:
//   var anotherPoint = new point.init(3,4)

var anotherPoint;
// this is a bare block to hide local
// `let` declarations
{
    // (Step 1)
    let tmpObj = {};

    // (Step 2)
    Object.setPrototypeOf(
        tmpObj, point.init.prototype
    );
    // or: tmpObj.__proto__ = point.init.prototype

    // (Step 3)
    let res = point.init.call(tmpObj,3,4);

    // (Step 4)
    anotherPoint = (
        typeof res !== "object" ? tmpObj : res
    );
}
```

¡Claramente, la invocación con `new` agiliza ese conjunto de pasos manuales!

| TIP: |
| :--- |
| El `Object.setPrototypeOf(..)` en el paso 2 también podría haberse hecho vía la propiedad `__proto__`, como `tmpObj.__proto__ = point.init.prototype`, o incluso como parte del object literal (paso 1) con `tmpObj = { __proto__: point.init.prototype }`. |

Omitiendo parte de la formalidad de estos pasos, recordemos un fragmento anterior y veamos cómo `new` aproxima un resultado similar:

```js
var point = { /* .. */ };

// this approach:
var anotherPoint = {};
point.init.call(anotherPoint,5,6);

// can instead be approximated as:
var yetAnotherPoint = new point.init(5,6);
```

¡Eso es un poco más lindo! Pero hay una salvedad aquí.

Usar las otras funciones que `point` contiene contra `anotherPoint` / `yetAnotherPoint`, no querremos hacerlo con `new`. ¿Por qué? Porque `new` está creando un *nuevo* objeto, pero eso no es lo que queremos si pretendemos invocar una función contra un objeto existente.

En cambio, probablemente usaremos la asignación de *contexto explícito*:

```js
point.rotate.call( anotherPoint, /*angleRadians=*/Math.PI );

point.toString.call( yetAnotherPoint );
// (5,6)
```

### Review This

Hemos visto cuatro reglas para la asignación de contexto de `this` en las llamadas a funciones. Pongámoslas en orden de precedencia:

1. ¿La función se invoca con `new`, creando y estableciendo un *nuevo* `this`?

2. ¿La función se invoca con `call(..)` o `apply(..)`, estableciendo *explícitamente* `this`?

3. ¿La función se invoca con una referencia de objeto en el call-site (por ejemplo, `point.init(..)`), estableciendo *implícitamente* `this`?

4. Si nada de lo anterior... ¿estamos en non-strict mode? Si es así, pon por *defecto* el `this` en `globalThis`. Pero si estás en strict mode, pon por *defecto* el `this` en `undefined`.

Estas reglas, *en este orden*, son cómo JS determina el `this` para una invocación de función. Si múltiples reglas coinciden con un call-site (por ejemplo, `new point.init.call(..)`), gana la primera regla de la lista que coincida.

Eso es todo, ahora eres maestro de la palabra clave `this`. Bueno, no del todo. Hay un montón más de matices por cubrir. ¡Pero vas bien encaminado!

## An Arrow Points Somewhere

Todo lo que he afirmado hasta ahora sobre `this` en las funciones, y cómo se determina basándose en el call-site, hace una suposición gigante: que estás tratando con una función (o method) *regular*.

Entonces, ¿qué es una función *irregular*?!? Se ve así:

```js
const x = x => x <= x;
```

| NOTA: |
| :--- |
| Sí, estoy siendo un poco sarcástico e injusto al llamar "irregular" a una arrow function y al usar un ejemplo tan artificioso. Es un chiste, ¿okay? |

Aquí hay un ejemplo real de una arrow function `=>`:

```js
const clickHandler = evt =>
    evt.target.matches("button") ?
        this.theFormElem.submit() :
        evt.stopPropagation();
```

A modo de comparación, déjame mostrar también el equivalente sin arrow:

```js
const clickHandler = function(evt) {
    evt.target.matches("button") ?
        this.theFormElem.submit() :
        evt.stopPropagation();
};
```

O si lo hiciéramos un poco a la vieja escuela -- ¡esto es lo mío! -- podríamos probar la forma de function declaration independiente:

```js
function clickHandler(evt) {
    evt.target.matches("button") ?
        this.theFormElem.submit() :
        evt.stopPropagation();
}
```

O si la función apareciera como un method en una definición de `class`, o como un method conciso en un object literal, se vería así:

```js
// ..
clickHandler(evt) {
    evt.target.matches("button") ?
        this.theFormElem.submit() :
        evt.stopPropagation();
}
```

En lo que realmente quiero enfocarme es en cómo cada una de estas formas de la función se comportará con respecto a su referencia `this`, y si la primera forma `=>` difiere de las demás (pista: ¡lo hace!). Pero empecemos con una pequeña prueba para ver si has estado prestando atención.

Para cada una de esas formas de función que acabamos de mostrar, ¿cómo sabemos a qué referenciará cada `this`?

### Where's The Call-site?

Con suerte, respondiste con algo como: "primero, necesitamos ver cómo se llaman las funciones".

Bastante justo.

Digamos que nuestro programa se ve así:

```js
var infoForm = {
    theFormElem: null,
    theSubmitBtn: null,

    init() {
        this.theFormElem =
            document.getElementById("the-info-form");
        this.theSubmitBtn =
            theFormElem.querySelector("button[type=submit]");

        // is *this* the call-site?
        this.theSubmitBtn.addEventListener(
            "click",
            this.clickHandler,
            false
        );
    },

    // ..
}
```

Ah, interesante. La mitad de ustedes, lectores, nunca han visto código real de la DOM API como `getElementById(..)`, `querySelector(..)` y `addEventListener(..)` antes. ¡Escuché las campanas de confusión silbar recién!

| NOTA: |
| :--- |
| Lo siento, estoy delatando mi edad, aquí. He estado haciendo estas cosas el tiempo suficiente como para recordar cuando hacíamos ese tipo de código mucho antes de tener utilidades como jQuery atiborrando el código con `$` por todos lados. Y después de muchos años de evolución del front-end, parece que aterrizamos en algún lugar bastante más "moderno" -- al menos, esa es la presunción predominante. |

Supongo que muchos de ustedes hoy en día están acostumbrados a ver código de frameworks de componentes (React, etc) algo así:

```jsx
// ..

infoForm(props) {
    return (
        <form ref={this.theFormElem}>
            <button type=submit onClick=this.clickHandler>
                Click Me
            </button>
        </form>
    );
}

// ..
```

Por supuesto, hay un montón de otras maneras en que ese código podría tomar forma, dependiendo de si estás usando un framework u otro, etc.

O quizás ya ni siquiera estés usando componentes estilo `class` / `this`, porque has movido todo a hooks y closures. En cualquier caso, para los propósitos de nuestra discusión, *este* capítulo trata todo sobre `this`, así que necesitamos atenernos a un estilo de código como el de arriba, para tener código relacionado con la discusión.

Y ninguno de esos dos fragmentos de código anteriores muestra la función `clickHandler` siendo definida. Pero he dicho repetidamente hasta ahora, que eso no importa; todo lo que importa es ... ¿qué? dilo conmigo... todo lo que importa es *cómo* se invoca la función.

Entonces, ¿cómo se está invocando `clickHandler`? ¿Cuál es el call-site, y qué regla de asignación de contexto coincide?

### Hidden From Sight

Si estás atascado, no te preocupes. Estoy haciendo esto difícil deliberadamente, para señalar algo muy importante.

Cuando ocurren los bindings de event handler `"click"` o `onClick=`, en ambos casos, especificamos `this.clickHandler`, lo que implica que hay un objeto de contexto `this` con una propiedad llamada `clickHandler`, que está conteniendo nuestra definición de función.

Entonces, ¿es `this.clickHandler` el call-site? Si lo fuera, ¿qué regla de asignación aplica? ¿La regla de *contexto implícito* (#3)?

Desafortunadamente, no.

El problema es que, **en realidad no podemos ver el call-site** en este programa. Uh oh.

Si no podemos ver el call-site, ¿cómo sabemos *cómo* se va a llamar realmente la función?

*Ese* es exactamente el punto que estoy planteando.

No importa que hayamos pasado `this.clickHandler`. Eso es meramente una referencia a un valor de objeto función. No es un call-site.

Por detrás, en algún lugar dentro de un framework, librería, o incluso el propio entorno de JS, cuando un usuario hace clic en el botón, se va a invocar una referencia a la función `clickHandler(..)`. Y como hemos insinuado, ese call-site incluso va a pasar el objeto de evento del DOM como el argumento `evt`.

Como no podemos ver el call-site, tenemos que *imaginarlo*. ¿Podría verse como...?

```js
// ..
eventCallback( domEventObj );
// ..
```

Si así fuera, ¿qué regla de `this` aplicaría? ¿La regla de *contexto por defecto* (#4)?

O, ¿qué pasaría si el call-site se viera así...?

```js
// ..
eventCallback.call( domElement, domEventObj );
```

Ahora, ¿qué regla de `this` aplicaría? ¿La regla de *contexto explícito* (#2)?

A menos que abras y veas el código fuente del framework/librería, o leas la documentación/especificación, no *sabrás* qué esperar de ese call-site. Lo que significa que predecir, en última instancia, a qué apunta `this` en la función `clickHandler` que escribes, es... por decirlo suavemente... un poco enrevesado.

### *This* Is Wrong

Para ahorrarte más dolor aquí, iré directo al grano.

Prácticamente todas las implementaciones de un mecanismo de click-handler van a hacer algo como el `.call(..)`, y van a establecer el elemento del DOM (por ejemplo, el botón) al que el event listener está vinculado, como el *contexto explícito* para la invocación.

Hmmm... ¿está bien eso, o va a ser un problema?

Recuerda que nuestra función `clickHandler(..)` es `this`-aware, y que su referencia `this.theFormElem` implica referenciar un objeto con una propiedad `theFormElem`, que a su vez apunta al elemento `<form>` padre. Los botones del DOM no tienen, por defecto, una propiedad `theFormElem`.

En otras palabras, la referencia `this` que nuestro event handler tendrá establecida es casi con certeza incorrecta. Ups.

A menos que queramos reescribir la función `clickHandler`, vamos a necesitar arreglar eso.

### Fixing `this`

Consideremos algunas opciones para abordar la mala asignación. Para mantener las cosas enfocadas, me atendré a este estilo de binding de evento para la discusión:

```js
this.submitBtnaddEventListener(
    "click",
    this.clickHandler,
    false
);
```

Aquí hay una manera de abordarlo:

```js
// store a fixed reference to the current
// `this` context
var context = this;

this.submitBtn.addEventListener(
    "click",
    function handler(evt){
        return context.clickHandler(evt);
    },
    false
);
```

| TIP: |
| :--- |
| La mayoría del código JS más antiguo que usa este enfoque dirá algo como `var self = this` en lugar del nombre `context` que le estoy dando aquí. "Self" es una palabra más corta, y suena más genial. Pero también tiene por completo el significado semántico equivocado. La palabra clave `this` no es una referencia "self" a la función, sino más bien el contexto para esa invocación de función actual. Esas pueden parecer la misma cosa a primera vista, pero son conceptos completamente diferentes, tan diferentes como las manzanas y una canción de los Beatles. Así que... parafraseándolos, "Hey developer, don't make it bad. Take a sad `self` and make it better `context`." |

¿Qué está pasando aquí? Reconocí que el código que lo rodea, donde se va a ejecutar la llamada `addEventListener`, tiene un contexto `this` actual que es correcto, y necesitamos asegurarnos de que ese mismo contexto `this` se aplique cuando `clickHandler(..)` sea invocada.

Definí una función envolvente (`handler(..)`) y luego forcé al call-site a verse como:

```js
context.clickHandler(evt);
```

| TIP: |
| :--- |
| ¿Qué regla de asignación de contexto de `this` se aplica aquí? Correcto, la regla de *contexto implícito* (#3). |

Ahora, no importa cómo se vea el call-site interno de la librería/framework/entorno. Pero, ¿por qué?

Porque ahora estamos *realmente* en control del call-site. No importa cómo se invoque `handler(..)`, o a qué se asigne su `this`. Solo importa que cuando `clickHandler(..)` sea invocada, el contexto `this` se establezca en lo que queríamos.

Logré ese truco no solo definiendo una función envolvente (`handler(..)`) para poder controlar el call-site, sino... y esto es importante, así que no te lo pierdas... ¡definí `handler(..)` como una función NO `this`-aware! No hay palabra clave `this` dentro de `handler(..)`, así que cualquier `this` que establezca (o no) la librería/framework/entorno, es completamente irrelevante.

La línea `var context = this` es crítica para el truco. Define una variable léxica `context`, que no es ninguna palabra clave especial, que contiene una instantánea del valor del `this` externo. Luego dentro de `clickHandler`, simplemente referenciamos una variable léxica (`context`), sin ninguna palabra clave `this` relativa/mágica.

### Lexical This

El nombre de este patrón, por cierto, es "lexical this", que significa un `this` que se comporta como una variable de lexical scope en lugar de como un binding de contexto dinámico.

Pero resulta que JS tiene una manera más fácil de realizar el truco de magia de "lexical this". ¿Estás listo para la revelación del truco?

...

¡La arrow function `=>`! ¡Tadá!

Así es, la función `=>` es, a diferencia de todas las otras formas de función, especial, en el sentido de que no es especial en absoluto. O, más bien, que no define nada especial para el comportamiento de `this`, en lo más mínimo.

En una función `=>`, la palabra clave `this`... **no es una palabra clave**. No es absolutamente nada diferente de cualquier otra variable, como `context` o `happyFace` o `foobarbaz`.

Déjame ilustrar *este* punto más directamente:

```js
function outer() {
    console.log(this.value);

    // define a return an "inner"
    // function
    var inner = () => {
        console.log(this.value);
    };

    return inner;
}

var one = {
    value: 42,
};
var two = {
    value: "sad face",
};

var innerFn = outer.call(one);
// 42

innerFn.call(two);
// 42   <-- not "sad face"
```

El `innerFn.call(two)` habría, para cualquier definición de función *regular*, resultado en `"sad face"` aquí. Pero dado que la función `inner` que definimos y retornamos (y asignamos a `innerFn`) era una arrow function `=>` *irregular*, no tiene ningún comportamiento especial de `this`, sino que tiene comportamiento de "lexical this".

Cuando la función `innerFn(..)` (también conocida como `inner(..)`) se invoca, incluso con una asignación de *contexto explícito* vía `.call(..)`, esa asignación se ignora.

| NOTA: |
| :--- |
| No estoy seguro de por qué las arrow functions `=>` tienen siquiera un `call(..)` / `apply(..)`, ya que son funciones silenciosas no-op. Supongo que es por consistencia con las funciones normales. Pero como veremos más adelante, hay otras inconsistencias entre las funciones *regulares* y las arrow functions `=>` *irregulares*. |

Cuando se encuentra un `this` (`this.value`) dentro de una arrow function `=>`, `this` se trata como una variable léxica normal, no como una palabra clave especial. Y dado que no hay una variable `this` en esa función misma, JS hace lo que siempre hace con las variables léxicas: sube un nivel de lexical scope -- en este caso, a la función `outer(..)` que la rodea, y verifica si hay algún `this` registrado en ese scope.

Por suerte, `outer(..)` es una función *regular*, lo que significa que tiene una palabra clave `this` normal. Y la invocación `outer.call(one)` asignó `one` a su `this`.

Así que, `innerFn.call(two)` está invocando `inner()`, pero cuando `inner()` busca un valor para `this`, obtiene... `one`, no `two`.

#### Back To The... Button

Pensaste que iba a hacer un chiste de juego de palabras y decir "future" ahí, ¿verdad?

Una manera más directa y apropiada de resolver nuestro problema anterior, donde habíamos hecho `var context = this` para obtener una especie de comportamiento falso de "lexical this", es usar la arrow function `=>`, ya que su característica de diseño primaria es... "lexical this".

```js
this.submitBtn.addEventListener(
    "click",
    evt => this.clickHandler(evt),
    false
);
```

¡Boom! ¡Problema resuelto! ¡Mic drop!

Escúchame en *esto*: la arrow function `=>` *no* -- repito, *no* -- se trata de escribir menos caracteres. El punto primario de que la función `=>` fuera agregada a JS era darnos el comportamiento de "lexical this" sin tener que recurrir a hacks estilo `var context = this` (o peor, `var self = this`).

| TIP: |
| :--- |
| Si necesitas "lexical this", prefiere siempre una arrow function `=>`. Si no necesitas "lexical this", bueno... la arrow function `=>` podría no ser la mejor herramienta para el trabajo. |

#### Confession Time

He dicho todo el tiempo en este capítulo, que cómo escribes una función, y dónde escribes la función, no tiene *nada* que ver con cómo se asignará su `this`.

Para las funciones regulares, eso es cierto. Pero cuando consideramos una arrow function `=>` irregular, ya no es del todo preciso.

¿Recuerdas la forma `=>` original de `clickHandler` de antes en el capítulo?

```js
const clickHandler = evt =>
    evt.target.matches("button") ?
        this.theFormElem.submit() :
        evt.stopPropagation();
```

Si usamos esa forma, en el mismo contexto que nuestro binding de evento, podría verse así:

```js
const clickHandler = evt =>
    evt.target.matches("button") ?
        this.theFormElem.submit() :
        evt.stopPropagation();

this.submitBtn.addEventListener("click",clickHandler,false);
```

A muchos desarrolladores les gusta incluso reducirlo aún más, a una arrow function `=>` en línea:

```js
this.submitBtn.addEventListener(
    "click",
    evt => evt.target.matches("button") ?
        this.theFormElem.submit() :
        evt.stopPropagation(),
    false
);
```

Cuando escribimos una arrow function `=>`, sabemos con certeza que su binding de `this` será exactamente el binding de `this` actual de cualquier función que la rodee y que se esté ejecutando, independientemente de cómo se vea el call-site de la arrow function `=>`. Así que en otras palabras, *cómo* escribimos la arrow function `=>`, y *dónde* la escribimos, sí importa.

Eso no responde del todo la pregunta de `this`, eso sí. Solo desplaza la pregunta a *cómo se invocó la función que la contiene*. En realidad, el enfoque en el call-site sigue siendo lo único que importa.

Pero el matiz que confieso haber omitido hasta *este* momento es: importa *qué* call-site consideramos, no solo *cualquier* call-site en el call stack actual. El call-site que importa es la invocación de función más cercana en el call stack actual ***que realmente asigna un contexto `this`***.

Dado que una arrow function `=>` nunca tiene un call-site que asigne `this` (sin importar qué), ese call-site no es relevante para la pregunta. Tenemos que seguir subiendo por el call stack hasta que encontremos una invocación de función que *sí* asigne `this` -- incluso si tal función invocada no es en sí misma `this`-aware.

**ESE** es el único call-site que importa.

#### Find The Right Call-Site

Déjame ilustrar, con un lío enrevesado de un montón de funciones/llamadas anidadas:

```js
globalThis.value = { result: "Sad face" };

function one() {
    function two() {
        var three = {
            value: { result: "Hmmm" },

            fn: () => {
                const four = () => this.value;
                return four.call({
                    value: { result: "OK", },
                });
            },
        };
        return three.fn();
    };
    return two();
}

new one();          // ???
```

¿Puedes recorrer eso (esa pesadilla) en tu cabeza y determinar qué se retornará de la invocación `new one()`?

Podría ser cualquiera de estos:

```js
// from `four.call(..)`:
{ result: "OK" }

// or, from `three` object:
{ result: "Hmmm" }

// or, from the `globalThis.value`:
{ result: "Sad face" }

// or, empty object from the `new` call:
{}
```

El call-stack para esa invocación `new one()` es:

```
four         |
three.fn     |
two          | (this = globalThis)
one          | (this = {})
[ global ]   | (this = globalThis)
```

Dado que `four()` y `fn()` son ambas arrow functions `=>`, los call-sites `three.fn()` y `four.call(..)` no asignan `this`; por lo tanto, son irrelevantes para nuestra consulta. ¿Cuál es la siguiente invocación a considerar en el call-stack? `two()`. Esa es una función regular (puede aceptar asignación de `this`), y el call-site coincide con la regla de asignación de *contexto por defecto* (#4). Dado que no estamos en strict mode, `this` se asigna a `globalThis`.

Cuando `four()` se está ejecutando, `this` es simplemente una variable normal. Entonces mira a la función que la contiene (`three.fn()`), pero nuevamente encuentra una función sin `this`. Así que sube otro nivel, y encuentra una función `two()` *regular* que tiene un `this` definido. Y ese `this` es `globalThis`. Así que la expresión `this.value` se resuelve a `globalThis.value`, que nos retorna... `{ result: "Sad face" }`.

...

Respira hondo. Sé que eso es mucho que procesar mentalmente. Y para ser justos, ese es un ejemplo súper artificioso. Casi nunca verás toda esa complejidad mezclada en un mismo call-stack.

Pero absolutamente encontrarás call-stacks mixtos en programas reales. Necesitas sentirte cómodo con el análisis que acabo de ilustrar, para poder desentrañar el call-stack hasta que encuentres el call-site más reciente que asigne `this`.

Recuerda el adagio que cité antes: "un gran poder conlleva una gran responsabilidad". Elegir código orientado a `this` (incluso `class`es) significa elegir tanto la flexibilidad que nos brinda, como la necesidad de sentirse cómodo navegando el call-stack para entender cómo se comportará.

Esa es la única manera de escribir efectivamente (¡y luego leer!) código `this`-aware.

### This Is Bound To Come Up

Retrocediendo un poco, hay otra opción si no quieres usar el comportamiento de "lexical this" de una arrow function `=>` para abordar la funcionalidad del event handler del botón.

Además de `call(..)` / `apply(..)` -- ¡estas invocan funciones, recuerda! -- las funciones de JS también tienen una tercera utilidad incorporada, llamada `bind(..)` -- que *no* invoca la función, solo para que quede claro.

La utilidad `bind(..)` define una *nueva* versión envuelta/vinculada de una función, donde su `this` está preestablecido y fijo, y no puede sobrescribirse con un `call(..)` o `apply(..)`, ni siquiera con un objeto de *contexto implícito* en el call-site:

```js
this.submitBtn.addEventListener(
    "click",
    this.clickHandler.bind(this),
    false
);
```

Dado que estoy pasando una función vinculada a `this` como el event handler, de manera similar no importa cómo esa utilidad intente establecer un `this`, porque ya he forzado a `this` a ser lo que quería: el valor de `this` del contexto de invocación de la función que lo rodea.

#### Hardly New

Este patrón a menudo se denomina "hard binding", ya que estamos creando una referencia de función que está fuertemente vinculada a un `this` en particular. Muchos escritos de JS han afirmado que la arrow function `=>` es esencialmente solo sintaxis para el hard-binding `bind(this)`. No lo es. Profundicemos.

Si fueras a crear una utilidad `bind(..)`, podría verse algo como *esto*:

```js
function bind(fn,context) {
    return function bound(...args){
        return fn.apply(context,args);
    };
}
```

| NOTA: |
| :--- |
| Así no es como `bind(..)` está implementado en realidad. El comportamiento es más sofisticado y matizado. Solo estoy ilustrando una porción de su comportamiento en este fragmento. |

¿Eso te resulta familiar? Está usando el viejo y querido hack falso de "lexical this". Y por detrás, es una asignación de *contexto explícito*, en este caso vía `apply(..)`.

Entonces, espera... ¿eso no significa que podríamos simplemente hacerlo con una arrow function `=>`?

```js
function bind(fn,context) {
    return (...args) => fn.apply(context,args);
}
```

Eh... no del todo. Como con la mayoría de las cosas en JS, hay un poco de matiz. Déjame ilustrar:

```js
// candidate implementation, for comparison
function fakeBind(fn,context) {
    return (...args) => fn.apply(context,args);
}

// test subject
function thisAwareFn() {
    console.log(`Value: ${this.value}`);
}

// control data
var obj = {
    value: 42,
};

// experiment
var f = thisAwareFn.bind(obj);
var g = fakeBind(thisAwareFn,obj);

f();            // Value: 42
g();            // Value: 42

new f();        // Value: undefined
new g();        // <--- ???
```

Primero, mira la llamada `new f()`. Eso es, admitámoslo, un uso extraño, llamar `new` sobre una función hard-bound. Probablemente sea bastante raro que alguna vez lo hagas. Pero muestra algo medio interesante. Aunque `f()` estaba hard-bound a un contexto `this` de `obj`, el operador `new` fue capaz de secuestrar el `this` de la función hard-bound y re-vincularlo al objeto recién creado y vacío. Ese objeto no tiene propiedad `value`, por eso vemos `"Value: undefined"` impreso.

Si eso se siente extraño, estoy de acuerdo. Es un matiz raro de los rincones del lenguaje. No es algo que probablemente alguna vez explotes. Pero lo señalo no solo por trivia. Vuelve a las cuatro reglas presentadas antes en este capítulo. ¿Recuerdas cómo afirmé su orden de precedencia, y `new` estaba en la cima (#1), por delante de la regla de asignación *explícita* `call(..)` / `apply(..)` (#2)?

Dado que podemos pensar en `bind(..)` como una especie de variación de esa regla, ahora vemos ese orden de precedencia demostrado. `new` tiene más precedencia que, y puede sobrescribir, incluso una función hard-bound. Medio te hace pensar que la función hard-bound quizás no está tan "hard"-bound, ¿eh?

Pero... ¿qué va a pasar con la llamada `new g()`, que está invocando `new` sobre la arrow function `=>` retornada? ¿Predices el mismo resultado que `new f()`?

Lamento decepcionarte.

Esa línea en realidad lanzará una excepción, porque una función `=>` no puede usarse con la palabra clave `new`.

¿Pero por qué? Mi mejor respuesta, no siendo yo mismo una autoridad en TC39, es que conceptual y realmente, una arrow function `=>` no es una función con un `this` hard-bound, es una función que no tiene `this` en absoluto. Como tal, `new` no tiene sentido contra tal función, así que JS simplemente lo prohíbe.

| NOTA: |
| :--- |
| Recuerda antes, cuando señalé que las arrow functions `=>` tienen `call(..)`, `apply(..)`, e incluso un `bind(..)`. Pero hemos visto que tales funciones básicamente ignoran estas utilidades como no-ops. Es un poco extraño, en mi opinión, que las arrow functions `=>` tengan todas esas utilidades como no-ops de paso, pero para la palabra clave `new`, eso no es solo, de nuevo, un no-op de paso, sino más bien prohibido con una excepción. |

Pero el punto principal es: una arrow function `=>` *no* es una forma sintáctica de `bind(this)`.

### Losing This Battle

Volviendo una vez más a nuestro ejemplo de event handler del botón:

```js
this.submitBtnaddEventListener(
    "click",
    this.clickHandler,
    false
);
```

Hay una preocupación más profunda que todavía no hemos abordado.

Hemos visto varios enfoques diferentes para construir una referencia de función callback diferente que pasar ahí, en lugar de `this.clickHandler`.

Pero cualquiera de esas maneras que elijamos, están produciendo literalmente una función diferente, no solo una modificación in situ de nuestra función `clickHandler` existente.

¿Por qué importa eso?

Bueno, en primer lugar, cuantas más funciones creemos (y re-creemos), más tiempo de procesamiento (muy ligero) y más memoria (bastante pequeña, usualmente) estamos consumiendo. Y cuando estamos re-creando una referencia de función, y descartando una vieja, eso también está dejando memoria no reclamada dando vueltas, lo que pone presión sobre el garbage collector (GC) para que, más a menudo, pause el universo de nuestro programa momentáneamente mientras limpia y reclama esa memoria.

Si conectar esta escucha de eventos es una operación de una sola vez, no es gran cosa. Pero si está ocurriendo una y otra vez, los efectos de rendimiento a nivel del sistema *pueden* empezar a acumularse. ¿Alguna vez tuviste una animación que de otra manera era fluida y que se entrecortó? Eso fue probablemente el GC entrando en acción, limpiando un montón de memoria reclamable.

Pero otra preocupación es, para cosas como los event handlers, si vamos a quitar un event listener en algún momento posterior, necesitamos mantener una referencia a la misma función exacta que adjuntamos originalmente. Si estamos usando una librería/framework, a menudo (¡pero no siempre!) ellos se encargan de ese pequeño detalle de trabajo sucio por ti. Pero de lo contrario, depende de nosotros asegurarnos de que cualquier función que planeemos adjuntar, mantengamos una referencia por si la necesitamos después.

Así que el punto que estoy planteando es: preestablecer una asignación de `this`, sin importar cómo lo hagas, para que sea predecible, viene con un costo. Un costo a nivel del sistema y un costo de mantenimiento/complejidad del programa. *Nunca* es gratis.

Una manera de reaccionar ante ese hecho es decidir, OK, simplemente vamos a fabricar todas esas referencias de función con `this` asignado de una vez, por adelantado, al principio. De esa manera, nos aseguramos de reducir tanto la presión del sistema como la presión del código, al mínimo.

Suena razonable, ¿verdad? No tan rápido.

#### Pre-Binding Function Contexts

Si tienes una referencia de función única que necesita estar vinculada a `this`, y usas una arrow `=>` o una llamada `bind(this)`, no veo ningún problema con eso.

Pero si la mayoría o todas las funciones `this`-aware en un segmento de tu código se invocan de maneras donde el `this` no es el contexto predecible que esperas, y por eso decides que necesitas hacer hard-bind a todas ellas... creo que esa es una gran señal de advertencia de que estás encarando las cosas de la manera equivocada.

Por favor recuerda la discusión en la sección "Avoid This" del Capítulo 3, que comenzó con este fragmento de código:

```js
class Point2d {
    x = null
    getDoubleX = () => this.x * 2

    constructor(x,y) {
        this.x = x;
        this.y = y;
    }
    toString() { /* .. */ }
}

var point = new Point2d(3,4);
```

Ahora imagina que hiciéramos esto con ese código:

```js
const getX = point.getDoubleX;

// later, elsewhere

getX();         // 6
```

Como puedes ver, el problema que estábamos tratando de resolver es el mismo con el que hemos estado lidiando aquí en este capítulo. Es que queríamos poder invocar una referencia de función como `getX()`, y que eso *signifique* y *se comporte como* `point.getDoubleX()`. Pero las reglas de `this` en las funciones *regulares* no funcionan de esa manera.

Así que usamos una arrow function `=>`. No es gran cosa, ¿verdad?

Error.

El verdadero problema de raíz es que *queremos* dos cosas conflictivas de nuestro código, y estamos tratando de usar el mismo *martillo* para ambos *clavos*.

Queremos tener un method `this`-aware almacenado en el prototype de la `class`, de modo que haya solo una definición para la función, y todas nuestras subclases e instancias compartan agradablemente esa misma función. Y la manera en que todas comparten es a través del poder del binding dinámico de `this`.

Pero al mismo tiempo, *también* queremos que esas referencias de función se mantengan mágicamente con `this` asignado a nuestra instancia cuando pasemos esas referencias de función por ahí y otro código esté a cargo del call-site.

En otras palabras, a veces queremos que algo como `point.getDoubleX` signifique, "dame una referencia que tenga `this` asignado a `point`", y otras veces queremos que la misma expresión `point.getDoubleX` signifique, dame una referencia de función con `this` dinámicamente asignable para que pueda obtener correctamente el contexto que necesito en este momento.

Quizás JS podría ofrecer un operador diferente además de `.`, como `::` o `->` o algo así, que te permitiera distinguir qué tipo de referencia de función buscas. De hecho, hay una propuesta de larga data para un operador de binding de `this` (`::`), que recibe atención de vez en cuando, y luego parece estancarse. Quién sabe, quizás algún día tal operador finalmente aterrice, y tengamos mejores opciones.

Pero sospecho firmemente que incluso si aterriza algún día, va a entregar una referencia de función completamente nueva, exactamente como los enfoques `=>` o `bind(this)` de los que ya hemos hablado. No vendrá como una solución gratuita y perfecta. Siempre habrá una tensión entre querer que la misma función sea a veces `this`-flexible y a veces `this`-predecible.

Con lo que los autores de JS de código orientado a `class` a menudo se topan, tarde o temprano, es con esta tensión exacta. ¿Y sabes qué hacen?

No consideran los *costos* de simplemente pre-vincular todos los methods `this`-aware de la clase convirtiéndolos en arrow functions `=>` en member properties. No se dan cuenta de que han anulado por completo todo el propósito de la cadena de `[[Prototype]]`. Y no se dan cuenta de que si el contexto fijo es lo que *realmente necesitan*, hay un mecanismo totalmente diferente en JS que está mejor adaptado para ese propósito.

#### Take A More Critical Look

Así que cuando haces este tipo de cosas:

```js
class Point2d {
    x = null
    y = null
    getDoubleX = () => this.x * 2
    toString = () => `(${this.x},${this.y})`

    constructor(x,y) {
        this.x = x;
        this.y = y;
    }
}

var point = new Point2d(3,4);
var anotherPoint = new Point2d(5,6);

var f = point.getDoubleX;
var g = anotherPoint.toString;

f();            // 6
g();            // (5,6)
```

Yo digo, "¡puaj!", a los methods `this`-aware hard-bound `getDoubleX()` y `toString()` ahí. Para mí, eso es un code smell. Pero aquí hay un enfoque aún *peor* que ha sido favorecido por muchos desarrolladores en el pasado:

```js
class Point2d {
    x = null
    y = null

    constructor(x,y) {
        this.x = x;
        this.y = y;
        this.getDoubleX = this.getDoubleX.bind(this);
        this.toString = this.toString.bind(this);
    }
    getDoubleX() { return this.x * 2; }
    toString() { return `(${this.x},${this.y})`; }
}

var point = new Point2d(3,4);
var anotherPoint = new Point2d(5,6);

var f = point.getDoubleX;
var g = anotherPoint.toString;

f();            // 6
g();            // (5,6)
```

Doble puaj.

En ambos casos, estás usando un mecanismo de `this` pero traicionándolo/neutralizándolo por completo, quitándole todo el poderoso dinamismo de `this`.

Realmente deberías al menos estar contemplando este enfoque alternativo, que se salta todo el mecanismo de `this` por completo:

```js
function Point2d(px,py) {
    var x = px;
    var y = py;

    return {
        getDoubleX() { return x * 2; },
        toString() { return `(${x},${y})`; }
    };
}

var point = Point2d(3,4);
var anotherPoint = Point2d(5,6);

var f = point.getDoubleX;
var g = anotherPoint.toString;

f();            // 6
g();            // (5,6)
```

¿Ves? No hay un `this` feo o complejo que ensucie ese código o del cual preocuparse por casos límite. El lexical scope es súper sencillo e intuitivo.

Cuando todo lo que queremos es que la mayoría/todos nuestros comportamientos de función tengan un contexto fijo y predecible, la solución más apropiada, la solución más sencilla e incluso más performante, son las variables léxicas y el scope closure.

Cuando te tomas toda la molestia de salpicar referencias `this` por todo un fragmento de código, y luego cortas todo el mecanismo de raíz con "lexical this" de `=>` o `bind(this)`, elegiste hacer el código más verboso, más complejo, más recargado. Y no obtuviste nada de ello que fuera más beneficioso, excepto seguir la moda de `this` (y de `class`).

...

Respira hondo. Recomponte.

Me estoy hablando a mí mismo, no a ti. ¡Pero si lo que acabo de decir te molesta, te estoy hablando a ti, también!

OK, escucha. Esa es solo mi opinión. Si no estás de acuerdo, está bien. Pero aplica el mismo nivel de rigor al pensar en cómo funcionan estos mecanismos, como yo lo he hecho, cuando decides a qué conclusiones quieres llegar.

## Variations

Antes de cerrar nuestra extensa discusión sobre `this`, hay algunas variaciones irregulares en las llamadas a funciones de las que deberíamos hablar.

### Indirect Function Calls

¿Recuerdas este ejemplo de antes en el capítulo?

```js
var point = {
    x: null,
    y: null,

    init(x,y) {
        this.x = x;
        this.y = y;
    },
    rotate(angleRadians) { /* .. */ },
    toString() { /* .. */ },
};

var init = point.init;
init(3,4);                  // broken!
```

Esto está roto porque el call-site `init(3,4)` no proporciona la señal de asignación de `this` necesaria. Pero hay otras maneras de observar una ruptura similar. Por ejemplo:

```js
(1,point.init)(3,4);        // broken!
```

Esta sintaxis de aspecto extraño primero evalúa una expresión `(1,point.init)`, que es una expresión de serie de comas. El resultado de tal expresión es el valor evaluado final, que en este caso es la referencia de función (contenida por `point.init`).

Así que el resultado pone esa referencia de función en la pila de expresiones, y luego invoca ese valor con `(3,4)`. Esa es una invocación indirecta de la función. ¿Y cuál es el resultado? En realidad coincide con la regla de asignación de *contexto por defecto* (#4) que vimos antes en el capítulo.

Por lo tanto, en non-strict mode, el `this` para la llamada `point.init(..)` será `globalThis`. De haber estado en strict mode, habría sido `undefined`, y la operación `this.x = x` habría entonces lanzado una excepción por acceder inválidamente a la propiedad `x` en el valor `undefined`.

Hay varias maneras diferentes de obtener una invocación de función indirecta. Por ejemplo:

```js
(()=>point.init)()(3,4);    // broken!
```

Y otro ejemplo de invocación de función indirecta es el patrón Immediately Invoked Function Expression (IIFE):

```js
(function(){
    // `this` assigned via "default" rule
})();
```

Como puedes ver, el valor de function expression se pone en la pila de expresiones, y luego se invoca con el `()` al final.

¿Pero qué hay de este código:

```js
(point.init)(3,4);
```

¿Cuál será el resultado de ese código?

Por el mismo razonamiento que hemos visto en los ejemplos anteriores, es lógico pensar que la expresión `point.init` pone el valor de función en la pila de expresiones, y luego se invoca indirectamente con `(3,4)`.

¡No del todo, eso sí! La gramática de JS tiene una regla especial para manejar la forma de invocación `(someIdentifier)(..)` como si hubiera sido `someIdentifier(..)` (sin el `(..)` alrededor del nombre del identificador).

¿Te preguntas por qué alguna vez querrías forzar el *contexto por defecto* para la asignación de `this` vía una invocación de función indirecta?

### Accessing `globalThis`

Antes de responder eso, introduzcamos otra manera de realizar la asignación indirecta de `this` en una función. Hasta ahora, los patrones de invocación de función indirecta mostrados son sensibles al strict mode. Pero, ¿qué pasaría si quisiéramos una asignación indirecta de `this` en una función que no respete el strict mode?

El constructor `Function(..)` toma un string de código y define dinámicamente la función equivalente. Sin embargo, siempre lo hace como si esa función hubiera sido declarada en el scope global. Y más aún, asegura que tal función *no* se ejecute en strict mode, sin importar el estado de strict mode del programa. Ese es el mismo resultado que ejecutar un indirecto

Un uso de nicho de tal asignación indirecta de `this` en función, agnóstica al strict mode, es para obtener una referencia confiable al verdadero objeto global antes de que la especificación de JS realmente definiera el identificador `globalThis` (por ejemplo, en un polyfill para él):

```js
"use strict";

var gt = new Function("return this")();
gt === globalThis;                      // true
```

De hecho, un resultado similar, usando el truco del operador coma (ver sección anterior) y `eval(..)`:

```js
"use strict";

function getGlobalThis() {
    return (1,eval)("this");
}

getGlobalThis() === globalThis;      // true
```

| NOTA: |
| :--- |
| `eval("this")` sería sensible al strict mode, pero `(1,eval)("this")` no lo es, y por lo tanto nos da de manera confiable el `globalThis` en cualquier programa. |

Desafortunadamente, los enfoques `new Function(..)` y `(1,eval)(..)` ambos tienen una limitación importante: ese código será bloqueado en el código JS basado en navegador si la app se sirve con ciertas restricciones de Content-Security-Policy (CSP), que no permiten la evaluación dinámica de código (por razones de seguridad).

¿Podemos sortear esto? Sí, en su mayor parte. [^globalThisPolyfill]

La especificación de JS dice que una función getter definida en el objeto global, o en cualquier objeto que herede de él (como `Object.prototype`), ejecuta la función getter con el contexto de `this` asignado a `globalThis`, independientemente del strict mode del programa.

```js
// Adapted from: https://mathiasbynens.be/notes/globalthis#robust-polyfill
function getGlobalThis() {
    Object.defineProperty(Object.prototype,"__get_globalthis__",{
        get() { return this; },
        configurable: true
    });
    var gt = __get_globalthis__;
    delete Object.prototype.__get_globalthis__;
    return gt;
}

getGlobalThis() === globalThis;      // true
```

Sí, eso es súper retorcido. ¡Pero así es el `this` de JS para ti!

### Template Tag Functions

Hay una variación inusual más de invocación de función que deberíamos cubrir: las tagged template functions.

Los template strings -- lo que prefiero llamar literales interpolados -- pueden "etiquetarse" con una función prefijo, que se invoca con el contenido parseado del template literal:

```js
function tagFn(/* .. */) {
    // ..
}

tagFn`actually a function invocation!`;
```

Como puedes ver, no hay sintaxis de invocación `(..)`, solo la función tag (`tagFn`) apareciendo antes del `` `template literal` ``; se permite el espacio en blanco entre ellos, pero es muy poco común.

A pesar de la apariencia extraña, la función `tagFn(..)` será invocada. Se le pasa la lista de uno o más literales string que fueron parseados del template literal, junto con cualquier valor de expresión interpolada que se haya encontrado.

No vamos a cubrir todos los pormenores de las tagged template functions -- son, en serio, una de las características más poderosas e interesantes jamás agregadas a JS -- pero dado que estamos hablando de la asignación de `this` en las invocaciones de función, por completar, necesitamos hablar de cómo se asignará `this`.

La otra forma de funciones tag que puedes encontrar es:

```js
var someObj = {
    tagFn() { /* .. */ }
};

someObj.tagFn`also a function invocation!`;
```

Aquí está la explicación fácil: `` tagFn`..` `` y `` someObj.tagFn`..` `` tendrán cada una un comportamiento de asignación de `this` correspondiente a los call-sites `tagFn(..)` y `someObj.tagFn(..)`, respectivamente. En otras palabras, `` tagFn`..` `` se comporta según la regla de asignación de *contexto por defecto* (#4), y `` someObj.tagFn`..` `` se comporta según la regla de asignación de *contexto implícito* (#3).

Por suerte para nosotros, no necesitamos preocuparnos por las reglas de asignación de `new` o `call(..)` / `apply(..)`, ya que esas formas no son posibles con las funciones tag.

Cabe señalar que es bastante raro que una función de tagged template literal se defina como `this`-aware, así que es bastante improbable que necesites aplicar estas reglas. Pero por si acaso, ahora estás al *tanto*.

## Stay Aware

Entonces, eso es `this`. Estoy dispuesto a apostar que para muchos de ustedes, fue un poco más... digamos, enrevesado... de lo que podrían haber estado esperando.

La buena noticia, quizás, es que en la práctica no tropiezas a menudo con todas estas complejidades diferentes. Pero cuanto más uses `this`, más requerirá de ti, y de los lectores de tu código, entender cómo funciona realmente.

La lección aquí es que deberías ser intencional y consciente de todos los aspectos de `this` antes de ir salpicándolo por tu código. Asegúrate de estar usándolo de la manera más efectiva y aprovechando al máximo este importante pilar de JS.

[^globalThisPolyfill]: "A horrifying globalThis polyfill in universal JavaScript"; Mathias Bynens; April 18 2019; https://mathiasbynens.be/notes/globalthis#robust-polyfill ; Accessed July 2022
