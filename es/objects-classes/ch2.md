# You Don't Know JS Yet: Objects & Classes - 2nd Edition
# Capítulo 2: Cómo funcionan los objetos

| NOTA: |
| :--- |
| Trabajo en progreso |

Los objetos no son solo contenedores de múltiples valores, aunque claramente ese es el contexto de la mayoría de las interacciones con los objetos.

Para entender completamente el mecanismo de objetos en JS, y sacarle el máximo provecho al uso de objetos en nuestros programas, necesitamos observar más de cerca una serie de características de los objetos (y sus propiedades) que pueden afectar su comportamiento al interactuar con ellos.

Estas características que definen el comportamiento subyacente de los objetos se denominan colectivamente, en términos formales, "protocolo de metaobjetos" (MOP)[^mop]. El MOP es útil no solo para entender cómo se comportarán los objetos, sino también para sobrescribir los comportamientos predeterminados de los objetos y así doblegar el lenguaje para que se ajuste más plenamente a las necesidades de nuestro programa.

## Descriptores de propiedad

Cada propiedad de un objeto se describe internamente mediante lo que se conoce como un "descriptor de propiedad". Este es, en sí mismo, un objeto (también llamado "metaobjeto") con varias propiedades (también llamadas "atributos"), que dictan cómo se comporta la propiedad de destino.

Podemos recuperar un descriptor de propiedad para cualquier propiedad existente usando `Object.getOwnPropertyDescriptor(..)` (ES5):

```js
myObj = {
    favoriteNumber: 42,
    isDeveloper: true,
    firstName: "Kyle"
};

Object.getOwnPropertyDescriptor(myObj,"favoriteNumber");
// {
//     value: 42,
//     enumerable: true,
//     writable: true,
//     configurable: true
// }
```

Incluso podemos usar un descriptor así para definir una nueva propiedad en un objeto, usando `Object.defineProperty(..)` (ES5):

```js
anotherObj = {};

Object.defineProperty(anotherObj,"fave",{
    value: 42,
    enumerable: true,     // default if omitted
    writable: true,       // default if omitted
    configurable: true    // default if omitted
});

anotherObj.fave;          // 42
```

Si una propiedad existente aún no ha sido marcada como no configurable (con `configurable: false` en su descriptor), siempre puede ser re-definida/sobrescrita usando `Object.defineProperty(..)`.

| ADVERTENCIA: |
| :--- |
| Varias secciones anteriores de este capítulo se refieren a "copiar" o "duplicar" propiedades. Uno podría suponer que tal copia/duplicación se realizaría a nivel del descriptor de propiedad. Sin embargo, ninguna de esas operaciones funciona realmente de esa manera; todas hacen un acceso y asignación simple al estilo `=`, lo cual tiene el efecto de ignorar cualquier matiz en cómo se define el descriptor subyacente de una propiedad. |

Aunque parece mucho menos común en la práctica, incluso podemos definir múltiples propiedades a la vez, cada una con su propio descriptor:

```js
anotherObj = {};

Object.defineProperties(anotherObj,{
    "fave": {
        // a property descriptor
    },
    "superFave": {
        // another property descriptor
    }
});
```

No es muy común ver este uso, porque es más raro que necesites controlar específicamente la definición de múltiples propiedades. Pero puede ser útil en algunos casos.

### Propiedades de acceso (accessor)

Un descriptor de propiedad usualmente define una propiedad `value`, como se mostró arriba. Sin embargo, se puede definir un tipo especial de propiedad, conocida como "propiedad de acceso" (también llamada getter/setter). Para una propiedad de este tipo, su descriptor no define una propiedad `value` fija, sino que se vería algo así:

```js
{
    get() { .. },    // function to invoke when retrieving the value
    set(v) { .. },   // function to invoke when assigning the value
    // .. enumerable, etc
}
```

Un getter se parece a un acceso a propiedad (`obj.prop`), pero por debajo invoca el método `get()` tal como fue definido; es como si hubieras llamado `obj.prop()`. Un setter se parece a una asignación de propiedad (`obj.prop = value`), pero invoca el método `set(..)` tal como fue definido; es como si hubieras llamado `obj.prop(value)`.

Ilustremos una propiedad de acceso getter/setter:

```js
anotherObj = {};

Object.defineProperty(anotherObj,"fave",{
    get() { console.log("Getting 'fave' value!"); return 123; },
    set(v) { console.log(`Ignoring ${v} assignment.`); }
});

anotherObj.fave;
// Getting 'fave' value!
// 123

anotherObj.fave = 42;
// Ignoring 42 assignment.

anotherObj.fave;
// Getting 'fave' value!
// 123
```

### Enumerable, writable, configurable

Además de `value` o `get()` / `set(..)`, los otros 3 atributos de un descriptor de propiedad son (como se mostró arriba):

* `enumerable`
* `writable`
* `configurable`

El atributo `enumerable` controla si la propiedad aparecerá en varias enumeraciones de propiedades de objetos, como `Object.keys(..)`, `Object.entries(..)`, los bucles `for..in`, y la copia que ocurre con el operador de propagación (spread) `...` de objetos y `Object.assign(..)`. La mayoría de las propiedades deberían dejarse como enumerables, pero puedes marcar ciertas propiedades especiales de un objeto como no enumerables si no deberían ser iteradas/copiadas.

El atributo `writable` controla si se permite una asignación de `value` (mediante `=`). Para hacer una propiedad "de solo lectura", defínela con `writable: false`. Sin embargo, mientras la propiedad siga siendo configurable, `Object.defineProperty(..)` todavía puede cambiar el valor estableciendo `value` de manera diferente.

El atributo `configurable` controla si el **descriptor** de una propiedad puede ser re-definido/sobrescrito. Una propiedad que es `configurable: false` queda bloqueada en su definición, y cualquier intento posterior de cambiarla con `Object.defineProperty(..)` fallará. A una propiedad no configurable todavía se le pueden asignar nuevos valores (mediante `=`), siempre que `writable: true` siga estando establecido en el descriptor de la propiedad.

## Subtipos de objetos

Hay una variedad de subtipos especializados de objetos en JS. Pero, por lejos, los dos más comunes con los que interactuarás son los arrays y las `function`s.

| NOTA: |
| :--- |
| Por "subtipo", nos referimos a la noción de un tipo derivado que ha heredado los comportamientos de un tipo padre, pero que luego ha especializado o extendido esos comportamientos. En otras palabras, los valores de estos subtipos son completamente objetos, pero también son *más que solo* objetos. |

### Arrays

Los arrays son objetos que están específicamente pensados para ser **indexados numéricamente**, en lugar de usar ubicaciones de propiedades nombradas con strings. Siguen siendo objetos, así que una propiedad nombrada como `favoriteNumber` es legal. Pero está muy mal visto mezclar propiedades nombradas dentro de arrays indexados numéricamente.

Los arrays se definen preferiblemente con sintaxis literal (similar a los objetos), pero con los corchetes `[ .. ]` en lugar de las llaves `{ .. }`:

```js
myList = [ 23, 42, 109 ];
```

JS permite cualquier mezcla de tipos de valores en los arrays, incluidos objetos, otros arrays, funciones, etc. Como probablemente ya sabes, los arrays están "indexados desde cero", lo que significa que el primer elemento del array está en el índice `0`, no en el `1`:

```js
myList = [ 23, 42, 109 ];

myList[0];      // 23
myList[1];      // 42
```

Recuerda que cualquier nombre de propiedad en forma de string en un objeto que "parezca" un entero -- que pueda ser coaccionado válidamente a un entero numérico -- será tratado en realidad como una propiedad entera (también llamada índice entero). Lo mismo aplica para los arrays. Siempre deberías usar `42` como índice entero (también llamado nombre de propiedad), pero si usas el string `"42"`, JS asumirá que lo querías como un entero y lo hará por ti.

```js
// "2" works as an integer index here, but it's not advised
myList["2"];    // 109
```

Una excepción a la *regla* de "no usar propiedades nombradas en arrays" es que todos los arrays exponen automáticamente una propiedad `length`, que se mantiene actualizada automáticamente con la "longitud" del array.

```js
myList = [ 23, 42, 109 ];

myList.length;   // 3

// "push" another value onto the end of the list
myList.push("Hello");

myList.length;   // 4
```

| ADVERTENCIA: |
| :--- |
| Muchos desarrolladores de JS creen incorrectamente que el `length` de un array es básicamente un *getter* (ver "Propiedades de acceso (accessor)" anteriormente en este capítulo), pero no lo es. La consecuencia es que estos desarrolladores sienten que es "costoso" acceder a esta propiedad -- como si JS tuviera que recalcular la longitud sobre la marcha -- y por lo tanto harán cosas como capturar/almacenar la longitud de un array antes de hacer un bucle que no la mute. Esto solía ser "buena práctica" desde una perspectiva de rendimiento. Pero desde hace al menos 10 años, eso ha sido en realidad un antipatrón, porque el motor (engine) de JS es más eficiente gestionando la propiedad `length` de lo que lo es nuestro código JS tratando de "ser más listo" que el engine para evitar invocar algo que creemos que es un *getter*. Es más eficiente dejar que el engine de JS haga su trabajo, y simplemente acceder a la propiedad cuando y cuantas veces sea necesario. |

#### Slots vacíos

Los arrays de JS también tienen una "falla" realmente desafortunada en su diseño, denominada "slots vacíos" (empty slots). Si asignas un índice de un array más de una posición más allá del final actual del array, JS dejará los slots intermedios "vacíos" en lugar de asignarlos automáticamente a `undefined`, como podrías esperar:

```js
myList = [ 23, 42, 109 ];
myList.length;              // 3

myList[14] = "Hello";
myList.length;              // 15

myList;                     // [ 23, 42, 109, empty x 11, "Hello" ]

// looks like a real slot with a
// real `undefined` value in it,
// but beware, it's a trick!
myList[9];                  // undefined
```

Quizás te preguntes por qué los slots vacíos son tan malos. Una razón: hay APIs en JS, como el `map(..)` de los arrays, ¡donde los slots vacíos son sorprendentemente omitidos! Nunca, jamás crees intencionalmente slots vacíos en tus arrays. Esta es, sin lugar a dudas, una de las "partes malas" de JS.

### Funciones

No tengo mucho que decir específicamente sobre las funciones aquí, más allá de señalar que también son subtipos de objetos. Esto significa que, además de ser ejecutables, también pueden tener propiedades nombradas agregadas o accedidas desde ellas.

Las funciones tienen dos propiedades predefinidas con las que puede que te encuentres interactuando, específicamente con fines de metaprogramación:

```js
function help(opt1,opt2,...remainingOpts) {
    // ..
}

help.name;          // "help"
help.length;        // 2
```

El `length` de una función es la cantidad de sus parámetros definidos explícitamente, hasta pero sin incluir un parámetro que tenga un valor por defecto definido (p. ej., `param = 42`) o un "parámetro rest" (p. ej., `...remainingOpts`).

#### Evita establecer propiedades en objetos-función

Deberías evitar asignar propiedades en objetos-función. Si lo que buscas es almacenar información extra asociada a una función, usa un `Map(..)` (o `WeakMap(..)`) separado, con el objeto-función como la clave y la información extra como el valor.

```js
extraInfo = new Map();

extraInfo.set(help,"this is some important information");

// later:
extraInfo.get(help);   // "this is some important information"
```

## Características de los objetos

Además de definir comportamientos para propiedades específicas, ciertos comportamientos son configurables a nivel de todo el objeto:

* extensible
* sealed (sellado)
* frozen (congelado)

### Extensible

La extensibilidad se refiere a si un objeto puede tener nuevas propiedades definidas/agregadas. Por defecto, todos los objetos son extensibles, pero puedes cambiar y desactivar la extensibilidad de un objeto:

```js
myObj = {
    favoriteNumber: 42
};

myObj.firstName = "Kyle";                  // works fine

Object.preventExtensions(myObj);

myObj.nicknames = [ "getify", "ydkjs" ];   // fails
myObj.favoriteNumber = 123;                // works fine
```

En modo no estricto (non-strict-mode), una asignación que crea una nueva propiedad fallará silenciosamente, mientras que en strict mode se lanzará una excepción.

### Sealed (sellado)

// TODO

### Frozen (congelado)

// TODO

## Extendiendo el MOP

Como se mencionó al comienzo de este capítulo, los objetos en JS se comportan según un conjunto de reglas denominado protocolo de metaobjetos (MOP)[^mop]. Ahora que entendemos más plenamente cómo funcionan los objetos por defecto, queremos dirigir nuestra atención a cómo podemos engancharnos a algunos de estos comportamientos predeterminados y sobrescribirlos/personalizarlos.

// TODO

## La cadena `[[Prototype]]`

Una de las características más importantes, pero menos obvias, de un objeto (parte del MOP) se denomina su "cadena de prototipos" (prototype chain); la notación oficial de la especificación de JS es `[[Prototype]]`. Asegúrate de no confundir este `[[Prototype]]` con una propiedad pública llamada `prototype`. A pesar del nombre, estos son conceptos distintos.

El `[[Prototype]]` es un enlace interno que un objeto obtiene por defecto cuando se crea, apuntando a otro objeto. Este enlace es una característica oculta, a menudo sutil, de un objeto, pero tiene impactos profundos en cómo se desarrollarán las interacciones con el objeto. Se denomina "cadena" porque un objeto enlaza a otro, que a su vez enlaza a otro, ... y así sucesivamente. Hay un *final* o *tope* de esta cadena, donde el enlace se detiene y no hay a dónde ir más allá. Más sobre eso en breve.

Ya vimos varias implicaciones del enlace `[[Prototype]]` en el Capítulo 1. Por ejemplo, por defecto, todos los objetos están enlazados mediante `[[Prototype]]` al objeto integrado llamado `Object.prototype`.

| ADVERTENCIA: |
| :--- |
| Ese nombre `Object.prototype` en sí mismo puede ser confuso, ya que usa una propiedad llamada `prototype`. ¡¿Cómo se relacionan `[[Prototype]]` y `prototype`?! Pon esas preguntas/confusiones en pausa por un momento, ya que volveremos a explicar las diferencias entre `[[Prototype]]` y `prototype` más adelante en este capítulo. Por ahora, simplemente asume la presencia de este importante pero extrañamente nombrado objeto integrado, `Object.prototype`. |

Consideremos algo de código:

```js
myObj = {
    favoriteNumber: 42
};
```

Eso debería resultarte familiar del Capítulo 1. Pero lo que *no ves* en este código es que el objeto de allí fue enlazado automáticamente (a través de su `[[Prototype]]` interno) a ese objeto integrado automáticamente, pero extrañamente nombrado, `Object.prototype`.

Cuando hacemos cosas como:

```js
myObj.toString();                             // "[object Object]"

myObj.hasOwnProperty("favoriteNumber");   // true
```

Estamos aprovechando este enlace interno `[[Prototype]]`, sin darnos cuenta realmente. Dado que `myObj` no tiene propiedades `toString` ni `hasOwnProperty` definidas en él, esos accesos a propiedades terminan en realidad **DELEGANDO** el acceso para continuar su búsqueda a lo largo de la cadena `[[Prototype]]`.

Dado que `myObj` está enlazado mediante `[[Prototype]]` al objeto llamado `Object.prototype`, la búsqueda de las propiedades `toString` y `hasOwnProperty` continúa en ese objeto; y, en efecto, ¡estos métodos se encuentran allí!

La capacidad de `myObj.toString` para acceder a la propiedad `toString` aunque en realidad no la tenga, se denomina comúnmente "herencia", o más específicamente, "herencia prototípica". Se dice que las propiedades `toString` y `hasOwnProperty`, junto con muchas otras, son "propiedades heredadas" en `myObj`.

| NOTA: |
| :--- |
| Tengo muchas frustraciones con el uso de la palabra "herencia" aquí -- ¡debería llamarse "delegación"! -- pero así es como la mayoría de la gente se refiere a ella, así que a regañadientes cumpliremos y usaremos esa misma terminología por ahora (aunque bajo protesta, entre " comillas). Guardaré mis objeciones para un apéndice de este libro. |

`Object.prototype` tiene varias propiedades y métodos integrados, todos los cuales son "heredados" por cualquier objeto que esté enlazado mediante `[[Prototype]]`, ya sea directamente o indirectamente a través del enlace de otro objeto, a `Object.prototype`.

Algunas propiedades "heredadas" comunes de `Object.prototype` incluyen:

* `constructor`
* `__proto__`
* `toString()`
* `valueOf()`
* `hasOwnProperty(..)`
* `isPrototypeOf(..)`

Recuerda `hasOwnProperty(..)`, que vimos anteriormente, que nos da una comprobación booleana de si cierta propiedad (por su nombre de string) es propiedad de un objeto:

```js
myObj = {
    favoriteNumber: 42
};

myObj.hasOwnProperty("favoriteNumber");   // true
```

Siempre se ha considerado algo desafortunado (organización semántica, conflictos de nombres, etc.) que una utilidad tan importante como `hasOwnProperty(..)` fuera incluida en la cadena `[[Prototype]]` de Object como un método de instancia, en lugar de ser definida como una utilidad estática.

A partir de ES2022, JS finalmente ha agregado la versión estática de esta utilidad: `Object.hasOwn(..)`.

```js
myObj = {
    favoriteNumber: 42
};

Object.hasOwn(myObj,"favoriteNumber");   // true
```

Esta forma ahora se considera la opción más preferible y robusta, y la forma del método de instancia (`hasOwnProperty(..)`) ahora debería evitarse generalmente.

De manera algo desafortunada e inconsistente, no hay (todavía, al momento de escribir esto) utilidades estáticas correspondientes, como `Object.isPrototype(..)` (en lugar del método de instancia `isPrototypeOf(..)`). Pero al menos existe `Object.hasOwn(..)`, así que eso es un progreso.

### Crear un objeto con un `[[Prototype]]` diferente

Por defecto, cualquier objeto que crees en tus programas estará enlazado mediante `[[Prototype]]` a ese objeto `Object.prototype`. Sin embargo, puedes crear un objeto con un enlace diferente de esta manera:

```js
myObj = Object.create(differentObj);
```

El método `Object.create(..)` toma su primer argumento como el valor que se establecerá para el `[[Prototype]]` del objeto recién creado.

Una desventaja de este enfoque es que no estás usando la sintaxis literal `{ .. }`, así que inicialmente no defines ningún contenido para `myObj`. Normalmente tienes que definir las propiedades una por una, usando `=`.

| NOTA: |
| :--- |
| El segundo argumento, opcional, de `Object.create(..)` es -- al igual que el segundo argumento de `Object.defineProperties(..)` discutido anteriormente -- un objeto con propiedades que contienen descriptores para definir inicialmente el nuevo objeto. En la práctica, esta forma rara vez se usa, probablemente porque es más incómodo especificar descriptores completos en lugar de solo pares nombre/valor. Pero puede resultar útil en algunos casos limitados. |

Alternativamente, aunque de forma menos preferible, puedes usar la sintaxis literal `{ .. }` junto con una propiedad especial (¡y de aspecto extraño!):

```js
myObj = {
    __proto__: differentObj,

    // .. the rest of the object definition
};
```

| ADVERTENCIA: |
| :--- |
| La propiedad de aspecto extraño `__proto__` ha estado en algunos engines de JS durante más de 20 años, pero solo fue estandarizada en JS a partir de ES6 (en 2015). Aun así, fue agregada en el Apéndice B de la especificación[^specApB], que lista características que TC39 incluye a regañadientes porque existen popularmente en varios engines de JS basados en navegadores y, por lo tanto, son una realidad de facto incluso si no se originaron con TC39. Esta característica está, por ende, "garantizada" por la especificación para existir en todos los engines de JS conformes basados en navegadores, pero no está necesariamente garantizada para funcionar en otros engines de JS independientes. Node.js usa el engine de JS (v8) del navegador Chrome, por lo que Node.js obtiene `__proto__` por defecto/accidente. Ten cuidado al usar `__proto__` de estar al tanto de todos los entornos de engine de JS en los que se ejecutará tu código. |

Ya sea que uses `Object.create(..)` o `__proto__`, el objeto creado en cuestión estará usualmente enlazado mediante `[[Prototype]]` a un objeto diferente del `Object.prototype` por defecto.

#### Enlace `[[Prototype]]` vacío

Mencionamos arriba que la cadena `[[Prototype]]` tiene que detenerse en algún lugar, para que las búsquedas no continúen por siempre. `Object.prototype` es típicamente el tope/final de toda cadena `[[Prototype]]`, ya que su propio `[[Prototype]]` es `null`, y por lo tanto no hay ningún otro lugar donde seguir buscando.

Sin embargo, también puedes definir objetos con su propio valor `null` para `[[Prototype]]`, como por ejemplo:

```js
emptyObj = Object.create(null);
// or: emptyObj = { __proto__: null }

emptyObj.toString;   // undefined
```

Puede ser bastante útil crear un objeto sin enlace `[[Prototype]]` a `Object.prototype`. Por ejemplo, como se mencionó en el Capítulo 1, las construcciones `in` y `for..in` consultarán la cadena `[[Prototype]]` en busca de propiedades heredadas. Pero esto puede ser indeseable, ya que quizás no quieras que algo como `"toString" in myObj` se resuelva exitosamente.

Además, un objeto con un `[[Prototype]]` vacío está a salvo de cualquier colisión accidental de "herencia" entre sus propios nombres de propiedad y los que "hereda" de otros lugares. Estos tipos de objetos (¡útiles!) a veces se denominan en el habla popular "objetos diccionario" (dictionary objects).

### `[[Prototype]]` vs `prototype`

¿Notas ese nombre de propiedad pública `prototype` en el nombre/ubicación de este objeto especial, `Object.prototype`? ¿De qué se trata todo eso?

`Object` es la función `Object(..)`; por defecto, todas las funciones (¡que son en sí mismas objetos!) tienen una propiedad `prototype` como esa, apuntando a un objeto.

Y aquí es donde el conflicto de nombres entre `[[Prototype]]` y `prototype` realmente nos muerde. La propiedad `prototype` de una función no define ningún enlace que la función misma experimente. De hecho, las funciones (como objetos) tienen su propio enlace interno `[[Prototype]]` en otro lugar -- más sobre eso en un segundo.

Más bien, la propiedad `prototype` de una función se refiere a un objeto que debería ser *enlazado POR* cualquier otro objeto que se cree al llamar a esa función con la palabra clave `new`:

```js
myObj = {};

// is basically the same as:
myObj = new Object();
```

Dado que la sintaxis de objeto literal `{ .. }` es esencialmente la misma que una llamada `new Object()`, el objeto integrado nombrado/ubicado en `Object.prototype` se usa como el valor interno `[[Prototype]]` del nuevo objeto que creamos y nombramos `myObj`.

¡Uf! ¡Hablando de un tema que se vuelve significativamente más confuso simplemente por la superposición de nombres entre `[[Prototype]]` y `prototype`!

----

Pero, ¿a dónde enlazan las funciones en sí mismas (¡como objetos!), en términos de `[[Prototype]]`? Enlazan a `Function.prototype`, otro objeto integrado más, ubicado en la propiedad `prototype` de la función `Function(..)`.

En otras palabras, puedes pensar en las funciones mismas como si hubieran sido "creadas" por una llamada `new Function(..)`, y luego enlazadas mediante `[[Prototype]]` al objeto `Function.prototype`. Este objeto contiene propiedades/métodos que todas las funciones "heredan" por defecto, como `toString()` (para serializar como string el código fuente de una función) y `call(..)` / `apply(..)` / `bind(..)` (los explicaremos más adelante en este libro).

## Comportamiento de los objetos

Las propiedades de los objetos se definen y controlan internamente mediante un metaobjeto "descriptor", que incluye atributos como `value` (el valor presente de la propiedad) y `enumerable` (un booleano que controla si la propiedad se incluye en los listados de propiedades/nombres de propiedades que solo muestran las enumerables).

La manera en que funcionan los objetos y sus propiedades en JS se denomina "protocolo de metaobjetos" (MOP)[^mop]. Podemos controlar el comportamiento preciso de las propiedades mediante `Object.defineProperty(..)`, así como los comportamientos a nivel de todo el objeto con `Object.freeze(..)`. Pero, de manera aún más poderosa, podemos engancharnos y sobrescribir ciertos comportamientos predeterminados en los objetos usando Symbols especiales predefinidos.

Los prototipos (prototypes) son enlaces internos entre objetos que permiten que el acceso a una propiedad o método contra un objeto -- si la propiedad/método solicitado está ausente -- sea manejado "delegando" esa búsqueda de acceso a otro objeto. Cuando la delegación involucra un método, el contexto en el que se ejecuta el método se comparte desde el objeto inicial al objeto de destino a través de la palabra clave `this`.

[^mop]: "Metaobject", Wikipedia; https://en.wikipedia.org/wiki/Metaobject ; Consultado en julio de 2022.

[^specApB]: "Appendix B: Additional ECMAScript Features for Web Browsers", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-additional-ecmascript-features-for-web-browsers ; Consultado en julio de 2022
