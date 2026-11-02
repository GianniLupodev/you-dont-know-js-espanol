# You Don't Know JS Yet: Objects & Classes - 2nd Edition
# Capítulo 1: Fundamentos de los objetos

| NOTA: |
| :--- |
| Trabajo en progreso |

> Todo en JS es un objeto.

Este es uno de los "hechos" más difundidos, pero más incorrectos, que circula perpetuamente sobre JS. Que comience el desmentido del mito.

JS definitivamente tiene objetos, pero eso no significa que todos los valores sean objetos. No obstante, los objetos son, posiblemente, el tipo de valor más importante (¡y variado!) del lenguaje, así que dominarlos es fundamental para tu recorrido por JS.

El mecanismo de objetos es sin duda el tipo contenedor más flexible y potente -- algo donde ponés otros valores; cada programa JS que escribas los usará de una manera u otra. Pero no es por eso que los objetos merecen el primer lugar en este libro. Los objetos son la base del segundo de los tres pilares de JS: el prototype.

¿Por qué los prototypes (junto con la palabra clave `this`, que se cubre más adelante en el libro) son tan centrales a JS como para ser uno de sus tres pilares? Entre otras cosas, los prototypes son la forma en que el sistema de objetos de JS puede expresar el patrón de diseño de clases, uno de los patrones de diseño más utilizados en toda la programación.

Así que nuestro recorrido aquí comenzará con los objetos, construirá un entendimiento completo de los prototypes, desmitificará la palabra clave `this`, y explorará el sistema `class`.

## Sobre este libro

¡Bienvenido al libro 3 de la serie *You Don't Know JS Yet*! Si ya terminaste *Get Started* (el primer libro) y *Scope & Closures* (el segundo libro), ¡estás en el lugar correcto! Si no, antes de continuar te animo a leer esos dos como base antes de sumergirte en este libro.

La primera edición de este libro se titula "this & Object Prototypes". En aquel libro, nuestro foco comenzaba con la palabra clave `this`, ya que es posiblemente uno de los temas más confusos de todo JS. Luego el libro dedicaba la mayor parte de su tiempo a exponer el sistema de prototypes y a abogar por la adopción del patrón de "delegación", menos conocido, en lugar de los diseños de clases. En el momento de la escritura de ese libro (2014), a ES6 todavía le faltaban casi 2 años para completarse, así que sentí que los primeros esbozos de la palabra clave `class` solo merecían un breve apéndice de cobertura.

Es quedarse bastante corto decir que mucho ha cambiado en el panorama de JS en los casi 8 años desde ese libro. ES6 ya es una noticia vieja; al momento de la escritura de *este* libro, JS ha visto 7 actualizaciones anuales **después de ES6** (de ES2016 a ES2022).

Ahora bien, todavía necesitamos hablar de cómo funciona `this`, y cómo eso se relaciona con los métodos invocados contra distintos objetos. Y `class` en realidad opera (¡en su mayoría!) a través de la cadena de prototypes, en lo profundo bajo la superficie. Pero los desarrolladores de JS en 2022 casi nunca escriben código para cablear explícitamente la herencia prototipal ya. Y por más que yo personalmente desee lo contrario, los patrones de diseño de clases -- no la "delegación de comportamiento" -- son la forma en que la mayoría de la organización de datos y comportamiento (estructuras de datos) en JS se expresa.

Este libro refleja la realidad actual de JS: de ahí el nuevo subtítulo, la nueva organización y enfoque de los temas, y la reescritura completa del texto de la edición anterior.

## Los objetos como contenedores

Una forma común de reunir múltiples valores en un solo contenedor es con un objeto. Los objetos son colecciones de pares clave/valor. También hay sub-tipos de objeto en JS con comportamientos especializados, como los arrays (indexados numéricamente) e incluso las funciones (invocables); más sobre estos sub-tipos más adelante.

| NOTA: |
| :--- |
| A las claves a menudo se las llama "nombres de propiedad" (property names), y al emparejamiento de un nombre de propiedad y un valor a menudo se lo llama "propiedad" (property). Este libro usará esos términos de manera distintiva de esa forma. |

Los objetos JS regulares típicamente se declaran con sintaxis literal, así:

```js
myObj = {
    // ..
};
```

**Nota:** Hay una forma alternativa de crear un objeto (usando `myObj = new Object()`), pero no es común ni preferida, y casi nunca es la forma apropiada de hacerlo. Quedate con la sintaxis de objeto literal.

Es fácil confundirse sobre qué significan los pares de `{ .. }`, ya que JS sobrecarga las llaves para significar cualquiera de las siguientes cosas, según el contexto en que se usen:

* delimitar valores, como los objetos literales
* definir patrones de desestructuración de objetos (más sobre esto luego)
* delimitar expresiones de string interpoladas, como `` `some ${ getNumber() } thing` ``
* definir bloques, como en `if` y en bucles `for`
* definir cuerpos de función

Aunque a veces puede ser un desafío mientras leés código, fijate si un par de llaves `{ .. }` se usa en el programa donde es válido que aparezca un valor/expresión; si es así, es un objeto literal, de lo contrario es uno de los otros usos sobrecargados.

## Definir propiedades

Dentro de las llaves del objeto literal, definís propiedades (nombre y valor) con pares `propertyName: propertyValue`, así:

```js
myObj = {
    favoriteNumber: 42,
    isDeveloper: true,
    firstName: "Kyle"
};
```

Los valores que asignás a las propiedades pueden ser literales, como se muestra, o pueden calcularse mediante una expresión:

```js
function twenty() { return 20; }

myObj = {
    favoriteNumber: (twenty() + 1) * 2,
};
```

La expresión `(twenty() + 1) * 2` se evalúa inmediatamente, con el resultado (`42`) asignado como el valor de la propiedad.

A veces los desarrolladores se preguntan si hay una forma de definir una expresión para el valor de una propiedad donde la expresión sea "perezosa", es decir, que no se calcule en el momento de la asignación, sino que se defina más tarde. JS no tiene expresiones perezosas, así que la única forma de hacerlo es que la expresión esté envuelta en una función:

```js
function twenty() { return 20; }
function myNumber() { return (twenty() + 1) * 2; }

myObj = {
    favoriteNumber: myNumber   // notá, NO `myNumber()` como llamada a función
};
```

En este caso, `favoriteNumber` no está guardando un valor numérico, sino más bien una referencia a una función. Para calcular el resultado, esa referencia a función debe ejecutarse explícitamente.

### ¿Se parece a JSON?

Puede que notes que esta sintaxis de objeto literal que vimos hasta ahora se parece a una sintaxis relacionada, "JSON" (JavaScript Object Notation):

```json
{
    "favoriteNumber": 42,
    "isDeveloper": true,
    "firstName": "Kyle"
}
```

Las mayores diferencias entre los objetos literales de JS y JSON son, para los objetos definidos como JSON:

1. los nombres de propiedad deben ir entre comillas con caracteres de comilla doble `"`

2. los valores de las propiedades deben ser literales (ya sean primitivos, objetos o arrays), no expresiones JS arbitrarias

En los programas JS, un objeto literal no requiere nombres de propiedad entre comillas -- *podés* ponerlos entre comillas (se permite `'` o `"`), pero usualmente es opcional. Sin embargo, hay caracteres que son válidos en un nombre de propiedad, pero que no pueden incluirse sin comillas que los rodeen; por ejemplo, números iniciales o espacios en blanco:

```js
myObj = {
    favoriteNumber: 42,
    isDeveloper: true,
    firstName: "Kyle",
    "2 nicknames": [ "getify", "ydkjs" ]
};
```

Otra diferencia menor es que la sintaxis JSON -- es decir, el texto que será *parseado* como JSON, como el de un archivo `.json` -- es más estricta que JS en general. Por ejemplo, JS permite comentarios (`// ..` y `/* .. */`), y comas `,` finales en expresiones de objetos y arrays; JSON no permite nada de esto. Por suerte, JSON sí permite espacios en blanco arbitrarios.

### Nombres de propiedad

Los nombres de propiedad en los objetos literales casi siempre son tratados/convertidos a valores string. Una excepción a esto es para los "nombres" de propiedad enteros (o que "parecen enteros"):

```js
anotherObj = {
    42:       "<-- this property name will be treated as an integer",
    "41":     "<-- ...and so will this one",

    true:     "<-- this property name will be treated as a string",
    [myObj]:  "<-- ...and so will this one"
};
```

El nombre de propiedad `42` será tratado como un nombre de propiedad entero (también conocido como índice); el valor string `"41"` también será tratado como tal, ya que *parece* un entero. En cambio, el valor `true` se convertirá en el nombre de propiedad string `"true"`, y la referencia al identificador `myObj`, *calculada* mediante los corchetes `[ .. ]` que la rodean, convertirá el valor del objeto a un string (generalmente el `"[object Object]"` por defecto).

| ADVERTENCIA: |
| :--- |
| Si realmente necesitás usar un objeto como clave/nombre de propiedad, nunca confíes en esta conversión implícita a string; su comportamiento es sorprendente y casi con certeza no es lo que se espera, así que es probable que ocurran errores en el programa. En su lugar, usá una estructura de datos más especializada, llamada `Map` (agregada en ES6), donde los objetos usados como "nombres" de propiedad se dejan tal cual en vez de ser convertidos a un valor string. |

Como con `[myObj]` arriba, podés *calcular* cualquier **nombre de propiedad** (distinto de calcular el valor de la propiedad) en el momento de la definición del objeto literal:

```js
anotherObj = {
    ["x" + (21 * 2)]: true
};
```

La expresión `"x" + (21 * 2)`, que debe aparecer dentro de los corchetes `[ .. ]`, se calcula inmediatamente, y el resultado (`"x42"`) se usa como el nombre de propiedad.

### Symbols como nombres de propiedad

ES6 agregó un nuevo tipo de valor primitivo, `Symbol`, que a menudo se usa como un nombre de propiedad especial para almacenar y recuperar valores de propiedades. Se crean mediante la llamada a función `Symbol(..)` (**sin** la palabra clave `new`), que acepta un string de descripción opcional usado solo con fines de depuración más amigable; si se especifica, la descripción es inaccesible para el programa JS y por lo tanto no se usa para ningún otro propósito más que la salida de depuración.

```js
myPropSymbol = Symbol("optional, developer-friendly description");
```

| NOTA: |
| :--- |
| Los symbols son algo así como números o strings, excepto que su valor es *opaco* y globalmente único dentro del programa JS. En otras palabras, podés crear y usar symbols, pero JS no te deja saber nada sobre, ni hacer nada con, el valor subyacente; eso se mantiene como un detalle de implementación oculto por el JS engine. |

Los nombres de propiedad calculados, como se describió previamente, son la forma de definir un nombre de propiedad de tipo symbol en un objeto literal:

```js
myPropSymbol = Symbol("optional, developer-friendly description");

anotherObj = {
    [myPropSymbol]: "Hello, symbol!"
};
```

El nombre de propiedad calculado que se usa para definir la propiedad en `anotherObj` será el valor primitivo symbol real (sea cual sea), no el string de descripción opcional (`"optional, developer-friendly description"`).

Como los symbols son globalmente únicos en tu programa, **no** hay ninguna posibilidad de colisión accidental en la que una parte del programa pudiera definir accidentalmente un nombre de propiedad igual al que otra parte del programa intentó definir/asignar.

Los symbols también son útiles para engancharse a comportamientos especiales por defecto de los objetos, y cubriremos eso con más detalle en "Extending the MOP" en el próximo capítulo.

### Propiedades concisas

Al definir un objeto literal, es común usar un nombre de propiedad que sea igual a un identificador existente dentro del scope que contiene el valor que querés asignar.

```js
coolFact = "the first person convicted of speeding was going 8 mph";

anotherObj = {
    coolFact: coolFact
};
```

| NOTA: |
| :--- |
| Eso habría sido lo mismo que la definición de nombre de propiedad entre comillas `"coolFact": coolFact`, pero los desarrolladores de JS rara vez ponen comillas en los nombres de propiedad a menos que sea estrictamente necesario. De hecho, es idiomático evitar las comillas a menos que se requieran, así que se desaconseja incluirlas innecesariamente. |

En esta situación, donde el nombre de propiedad y el identificador de la expresión del valor son idénticos, podés omitir la porción del nombre de propiedad de la definición de la propiedad, como una definición de "propiedad concisa":

```js
coolFact = "the first person convicted of speeding was going 8 mph";

anotherObj = {
    coolFact   // <-- concise property short-hand
};
```

El nombre de propiedad es `"coolFact"` (string), y el valor asignado a la propiedad es lo que haya en la variable `coolFact` en ese momento: `"the first person convicted of speeding was going 8 mph"`.

Al principio, esta conveniencia abreviada puede parecer confusa. Pero a medida que te familiarices más con ver esta característica tan común y popular en uso, es probable que la prefieras para escribir (¡y leer!) menos.

### Métodos concisos

Otra abreviación similar es definir funciones/métodos en un objeto literal usando una forma más concisa:

```js
anotherObj = {
    // standard function property
    greet: function() { console.log("Hello!"); },

    // concise function/method property
    greet2() { console.log("Hello, friend!"); }
};
```

Ya que estamos en el tema de las propiedades de método concisas, también podemos definir funciones generadoras (otra característica de ES6):

```js
anotherObj = {
    // instead of:
    //   greet3: function*() { yield "Hello, everyone!"; }

    // concise generator method
    *greet3() { yield "Hello, everyone!"; }
};
```

Y aunque no es particularmente común, los métodos/generadores concisos pueden incluso tener nombres entre comillas o calculados:

```js
anotherObj = {
    "greet-4"() { console.log("Hello, audience!"); },

    // concise computed name
    [ "gr" + "eet 5" ]() { console.log("Hello, audience!"); },

    // concise computed generator name
    *[ "ok, greet 6".toUpperCase() ]() { yield "Hello, audience!"; }
};
```

### Object Spread

Otra forma de definir propiedades en el momento de creación del objeto literal es con una forma de la sintaxis `...` -- técnicamente no es un operador, pero sin duda parece uno -- a menudo llamada "object spread".

El `...` cuando se usa dentro de un objeto literal "esparcirá" el contenido (propiedades, es decir, pares clave/valor) de otro valor de objeto dentro del objeto que se está definiendo:

```js
anotherObj = {
    favoriteNumber: 12,

    ...myObj,   // object spread, shallow copies `myObj`

    greeting: "Hello!"
}
```

El esparcido de las propiedades de `myObj` es superficial, en el sentido de que solo copia las propiedades de nivel superior de `myObj`; cualquier valor que esas propiedades contengan simplemente se asigna. Si alguno de esos valores son referencias a otros objetos, las referencias en sí se asignan (por copia), pero los valores de objeto subyacentes *no* se duplican -- así que terminás con múltiples referencias compartidas al mismo objeto (u objetos).

Podés pensar el esparcido de objetos como un bucle `for` que recorre las propiedades una por una y hace una asignación de estilo `=` desde el objeto fuente (`myObj`) al objeto destino (`anotherObj`).

Además, considerá que estas operaciones de definición de propiedades ocurren "en orden", de arriba hacia abajo del objeto literal. En el fragmento de arriba, como `myObj` tiene una propiedad `favoriteNumber`, el object spread terminará sobrescribiendo la asignación de propiedad `favoriteNumber: 12` de la línea anterior. Además, si `myObj` hubiera contenido una propiedad `greeting` que se copiara, la línea siguiente (`greeting: "Hello!"`) sobrescribiría esa definición de propiedad.

| NOTA: |
| :--- |
| El object spread también solo copia propiedades *propias* (owned) (las que están directamente en el objeto) que sean *enumerables* (que se permite enumerar/listar). No duplica la propiedad -- es decir, no imita las características exactas de la propiedad -- sino que hace una copia de estilo asignación simple. Cubriremos más de estos detalles en la sección "Property Descriptors" del próximo capítulo. |

Una forma común en que se usa el object spread `...` es para realizar la duplicación *superficial* de objetos:

```js
myObjShallowCopy = { ...myObj };
```

Tené en cuenta que no podés hacer spread `...` dentro de un valor de objeto existente; la sintaxis de object spread `...` solo puede aparecer dentro del objeto literal `{ .. }`, que está creando un nuevo valor de objeto. Para realizar una copia superficial de objeto similar pero con APIs en lugar de sintaxis, consultá la sección "Object Entries" más adelante en este capítulo (con cobertura de `Object.entries(..)` y `Object.fromEntries(..)`).

Pero si en cambio querés copiar propiedades de objeto (superficialmente) dentro de un objeto *existente*, consultá la sección "Assigning Properties" más adelante en este capítulo (con cobertura de `Object.assign(..)`).

### Copia profunda de objetos

Además, como `...` no hace una duplicación de objeto completa y profunda, el object spread generalmente solo es adecuado para duplicar objetos que contienen únicamente valores simples y primitivos, no referencias a otros objetos.

La duplicación profunda de objetos es una operación increíblemente compleja y matizada. Duplicar un valor como `42` es obvio y directo, pero ¿qué significa copiar una función (que es un tipo especial de objeto, también mantenido por referencia), o copiar una referencia a un objeto externo (no enteramente dentro de JS), como un elemento del DOM? ¿Y qué pasa si un objeto tiene referencias circulares (como cuando un objeto descendiente anidado contiene una referencia de vuelta hacia un objeto ancestro externo)? Hay una variedad de opiniones dando vueltas sobre cómo deberían manejarse todos estos casos límite, y por lo tanto no existe un único estándar para la duplicación profunda de objetos.

Para la duplicación profunda de objetos, los enfoques estándar han sido:

1. Usar una utilidad de biblioteca que declara una opinión específica sobre cómo deben manejarse los comportamientos/matices de la duplicación.

2. Usar el truco de ida y vuelta `JSON.parse(JSON.stringify(..))` -- esto solo "funciona" correctamente si no hay referencias circulares, y si no hay valores en el objeto que no puedan serializarse correctamente con JSON (como las funciones).

Recientemente, sin embargo, aterrizó una tercera opción. Esta no es una característica de JS, sino más bien una API complementaria proporcionada a JS por entornos como la plataforma web. Los objetos ahora pueden copiarse en profundidad usando `structuredClone(..)`[^structuredClone].

```js
myObjCopy = structuredClone(myObj);
```

El algoritmo subyacente detrás de esta utilidad incorporada soporta la duplicación de referencias circulares, así como **muchos más** tipos de valores que el truco de ida y vuelta con `JSON`. Sin embargo, este algoritmo todavía tiene sus límites, incluyendo la falta de soporte para clonar funciones o elementos del DOM.

## Acceder a propiedades

El acceso a una propiedad de un objeto existente se hace preferiblemente con el operador `.`:

```js
myObj.favoriteNumber;    // 42
myObj.isDeveloper;       // true
```

Si es posible acceder a una propiedad de esta forma, se sugiere encarecidamente hacerlo.

Si el nombre de propiedad contiene caracteres que no pueden aparecer en identificadores, como números iniciales o espacios en blanco, se pueden usar los corchetes `[ .. ]` en lugar del `.`:

```js
myObj["2 nicknames"];    // [ "getify", "ydkjs" ]
```

```js
anotherObj[42];          // "<-- this property name will..."
anotherObj["41"];        // "<-- this property name will..."
```

Aunque los "nombres" de propiedad numéricos siguen siendo números, el acceso a la propiedad mediante los corchetes `[ .. ]` convertirá una representación de string a número (por ejemplo, `"42"` como el equivalente numérico `42`), y luego accederá a la propiedad numérica asociada de forma acorde.

De manera similar al objeto literal, el nombre de propiedad al que acceder puede calcularse mediante los corchetes `[ .. ]`. La expresión puede ser un identificador simple:

```js
propName = "41";
anotherObj[propName];
```

En realidad, lo que pongas entre los corchetes `[ .. ]` puede ser cualquier expresión JS arbitraria, no solo identificadores o valores literales como `42` o `"isDeveloper"`. JS primero evaluará la expresión, y el valor resultante se usará entonces como el nombre de propiedad a buscar en el objeto:

```js
function howMany(x) {
    return x + 1;
}

myObj[`${ howMany(1) } nicknames`];   // [ "getify", "ydkjs" ]
```

En este fragmento, la expresión es un `` `template string literal` `` delimitado por comillas invertidas con una expresión interpolada de la llamada a función `howMany(1)`. El resultado general de esa expresión es el valor string `"2 nicknames"`, que luego se usa como el nombre de propiedad al que acceder.

### Object Entries

Podés obtener un listado de las propiedades de un objeto, como un array de tuplas (sub-arrays de dos elementos) que contienen el nombre y el valor de la propiedad:

```js
myObj = {
    favoriteNumber: 42,
    isDeveloper: true,
    firstName: "Kyle"
};

Object.entries(myObj);
// [ ["favoriteNumber",42], ["isDeveloper",true], ["firstName","Kyle"] ]
```

Agregado en ES6, `Object.entries(..)` recupera esta lista de entradas -- que contiene solo propiedades propias (owned) y enumerables; ver la sección "Property Descriptors" en el próximo capítulo -- de un objeto fuente.

Dicha lista puede recorrerse/iterarse, posiblemente asignando propiedades a otro objeto existente. Sin embargo, también es posible crear un nuevo objeto a partir de una lista de entradas, usando `Object.fromEntries(..)` (agregado en ES2019):

```js
myObjShallowCopy = Object.fromEntries( Object.entries(myObj) );

// alternate approach to the earlier discussed:
// myObjShallowCopy = { ...myObj };
```

### Desestructuración

Otro enfoque para acceder a propiedades es a través de la desestructuración de objetos (agregada en ES6). Pensá la desestructuración como la definición de un "patrón" que describe cómo se supone que un valor de objeto "se ve" (estructuralmente), y luego pedirle a JS que siga ese "patrón" para acceder sistemáticamente al contenido de un valor de objeto.

El resultado final de la desestructuración de objetos no es otro objeto, sino más bien una o más asignaciones a otros destinos (variables, etc.) de los valores del objeto fuente.

Imaginá este tipo de código pre-ES6:

```js
myObj = {
    favoriteNumber: 42,
    isDeveloper: true,
    firstName: "Kyle"
};

const favoriteNumber = (
    myObj.favoriteNumber !== undefined ? myObj.favoriteNumber : 42
);
const isDev = myObj.isDeveloper;
const firstName = myObj.firstName;
const lname = (
    myObj.lastName !== undefined ? myObj.lastName : "--missing--"
);
```

Esos accesos a los valores de las propiedades, y asignaciones a otros identificadores, en general se llaman "desestructuración manual". Para usar la sintaxis declarativa de desestructuración de objetos, podría verse así:

```js
myObj = {
    favoriteNumber: 42,
    isDeveloper: true,
    firstName: "Kyle"
};

const { favoriteNumber = 12 } = myObj;
const {
    isDeveloper: isDev,
    firstName: firstName,
    lastName: lname = "--missing--"
} = myObj;

favoriteNumber;   // 42
isDev;            // true
firstName;        // "Kyle"
lname;            // "--missing--"
```

Como se muestra, la desestructuración de objetos `{ .. }` se parece a la definición de un valor de objeto literal, pero aparece del lado izquierdo del operador `=` en lugar del lado derecho donde aparecería una expresión de valor de objeto. Eso hace que el `{ .. }` del lado izquierdo sea un patrón de desestructuración en lugar de otra definición de objeto.

La desestructuración `{ favoriteNumber } = myObj` le dice a JS que encuentre una propiedad llamada `favoriteNumber` en el objeto, y que asigne su valor a un identificador del mismo nombre. La instancia única del identificador `favoriteNumber` en el patrón es similar a las "propiedades concisas" como se discutió antes en este capítulo: si la fuente (nombre de propiedad) y el destino (identificador) son iguales, podés omitir uno de ellos y listarlo solo una vez.

La parte `= 12` le dice a JS que provea `12` como valor por defecto para la asignación a `favoriteNumber`, si el objeto fuente o bien no tiene una propiedad `favoriteNumber`, o si la propiedad contiene un valor `undefined`.

En el segundo patrón de desestructuración, el patrón `isDeveloper: isDev` le indica a JS que encuentre una propiedad llamada `isDeveloper` en el objeto fuente, y asigne su valor a un identificador llamado `isDev`. Es una especie de "renombrado" de la fuente al destino. En cambio, `firstName: firstName` provee la fuente y el destino para una asignación, pero es redundante ya que son idénticos; un solo `firstName` habría bastado aquí, y en general es más preferido.

El `lastName: lname = "--missing--"` combina tanto el renombrado fuente-destino como un valor por defecto (si la propiedad fuente `lastName` falta o es `undefined`).

El fragmento de arriba combina la desestructuración de objetos con declaraciones de variables -- en este ejemplo, se usa `const`, pero `var` y `let` funcionan también -- pero no es inherentemente un mecanismo de declaración. La desestructuración se trata de acceso y asignación (fuente a destino), así que puede operar contra destinos existentes en lugar de declarar nuevos:

```js
let fave;

// surrounding ( ) are required syntax here,
// when a declarator is not used
({ favoriteNumber: fave } = myObj);

fave;  // 42
```

La sintaxis de desestructuración de objetos se prefiere en general por su estilo declarativo y más legible, por sobre los equivalentes pre-ES6 fuertemente imperativos. Pero no te pases de la raya con la desestructuración. ¡A veces hacer simplemente `x = someObj.x` está perfectamente bien!

### Acceso condicional a propiedades

Recientemente (en ES2020), se agregó a JS una característica conocida como "optional chaining" (encadenamiento opcional), que amplía las capacidades de acceso a propiedades (especialmente el acceso a propiedades anidadas). La forma principal es el operador compuesto de dos caracteres `?.`, como `A?.B`.

Este operador verificará la referencia del lado izquierdo (`A`) para ver si es null'ish (`null` o `undefined`). Si es así, el resto de la expresión de acceso a la propiedad se corta en circuito (se omite), y se devuelve `undefined` como resultado (¡incluso si fue `null` lo que realmente se encontró!). De lo contrario, `?.` accederá a la propiedad tal como lo haría un operador `.` normal.

Por ejemplo:

```js
myObj?.favoriteNumber
```

Aquí, la verificación null'ish se realiza contra `myObj`, lo que significa que el acceso a la propiedad `favoriteNumber` solo se realiza si el valor en `myObj` es no-null'ish. Notá que no verifica que `myObj` esté realmente conteniendo un objeto real, solo que sea no-null'ish. Sin embargo, a todos los valores no-null'ish se puede "acceder" (sin excepción de JS) de forma "segura" mediante el operador `.`, incluso si no hay una propiedad coincidente para recuperar.

Es fácil confundirse y pensar que la verificación null'ish es contra la propiedad `favoriteNumber`. Pero una forma de tenerlo claro es recordar que el `?` está del lado donde se realiza la verificación de seguridad, mientras que el `.` está del lado que solo se evalúa condicionalmente si la verificación no-null'ish pasa.

Típicamente, el operador `?.` se usa en accesos a propiedades anidadas que pueden tener 3 o más niveles de profundidad, como:

```js
myObj?.address?.city
```

La operación equivalente con el operador `?.` se vería así:

```js
(myObj != null && myObj.address != null) ? myObj.address.city : undefined
```

De nuevo, recordá que aquí no se ha realizado ninguna verificación contra la propiedad más a la derecha (`city`).

Además, el `?.` no debería usarse universalmente en lugar de cada operador `.` individual en tus programas. Deberías esforzarte por saber si un acceso a propiedad con `.` tendrá éxito o no antes de hacer el acceso, siempre que sea posible. Usá `?.` solo cuando la naturaleza de los valores a los que se accede esté sujeta a condiciones que no se pueden predecir/controlar.

Por ejemplo, en el fragmento anterior, el uso de `myObj?.` probablemente esté mal orientado, porque realmente no debería ser el caso que inicies una cadena de accesos a propiedades contra una variable que quizás ni siquiera contenga un objeto de nivel superior (más allá de que su contenido pueda carecer de ciertas propiedades en ciertas condiciones).

En su lugar, yo recomendaría un uso más parecido a esto:

```js
myObj.address?.city
```

Y esa expresión solo debería usarse en una parte de tu programa donde estés seguro de que `myObj` al menos esté conteniendo un objeto válido (tenga o no una propiedad `address` con un sub-objeto adentro).

Otra forma del operador de "optional chaining" es `?.[`, que se usa cuando el acceso a la propiedad que querés hacer condicional/seguro requiere un corchete `[ .. ]`.

```js
myObj["2 nicknames"]?.[0];   // "getify"
```

Todo lo afirmado sobre cómo se comporta `?.` vale igual para `?.[`.

| ADVERTENCIA: |
| :--- |
| Hay una tercera forma de esta característica, llamada "optional call" (llamada opcional), que usa `?.(` como operador. Se usa para realizar una verificación no-null'ish sobre una propiedad antes de ejecutar el valor de función en la propiedad. Por ejemplo, en lugar de `myObj.someFunc(42)`, podés hacer `myObj.someFunc?.(42)`. El `?.(` verifica que `myObj.someFunc` sea no-null'ish antes de invocarla (con la parte `(42)`). Aunque eso pueda sonar como una característica útil, creo que es lo suficientemente peligrosa como para justificar la evitación completa de esta forma/construcción.<br><br>Mi preocupación es que `?.(` hace parecer como si estuviéramos asegurándonos de que la función sea "invocable" antes de llamarla, cuando en realidad solo estamos verificando si es no-null'ish. A diferencia de `?.` que puede permitir un acceso `.` "seguro" contra un valor no-null'ish que tampoco es un objeto, la verificación no-null'ish de `?.(` no es igual de "segura". Si la propiedad en cuestión tiene cualquier valor no-null'ish y no-función, como `true` o `"Hello"`, la parte de llamada `(42)` se invocará y aun así lanzará una excepción JS. Así que, en otras palabras, esta forma lamentablemente se disfraza de más "segura" de lo que realmente es, y por lo tanto debería evitarse en esencialmente todas las circunstancias. Si un valor de propiedad puede alguna vez *no ser* una función, hacé una verificación más completa de su "función-idad" antes de intentar invocarla. No pretendas que `?.(` esté haciendo eso por vos, o los futuros lectores/mantenedores de tu código (¡incluido tu yo futuro!) probablemente lo lamenten. |

### Acceder a propiedades en no-objetos

Esto puede sonar contraintuitivo, pero en general podés acceder a propiedades/métodos desde valores que no son objetos en sí mismos:

```js
fave = 42;

fave;              // 42
fave.toString();   // "42"
```

Aquí, `fave` contiene un valor numérico primitivo `42`. Entonces, ¿cómo podemos hacer `.toString` para acceder a una propiedad desde él, y luego `()` para invocar la función contenida en esa propiedad?

Este es un tema tremendamente más a fondo de lo que abordaremos en este libro; ver el libro 4, "Types & Grammar", de esta serie para más. Sin embargo, como un vistazo rápido: si realizás un acceso a propiedad (`.` o `[ .. ]`) contra un valor no-objeto y no-null'ish, JS por defecto (¡temporalmente!) convertirá el valor en una representación envuelta en objeto, permitiendo el acceso a la propiedad contra ese objeto instanciado implícitamente.

Este proceso típicamente se llama "boxing", como poner un valor dentro de una "caja" (contenedor de objeto).

Así que en el fragmento de arriba, solo por el momento en que se accede a `.toString` sobre el valor `42`, JS hará el boxing de este valor en un objeto `Number`, y luego realizará el acceso a la propiedad.

Notá que `null` y `undefined` pueden ser objetivados, llamando a `Object(null)` / `Object(undefined)`. Sin embargo, JS no hace el boxing automático de estos valores null'ish, así que el acceso a propiedades contra ellos fallará (como se discutió antes en la sección "Acceso condicional a propiedades").

| NOTA: |
| :--- |
| El boxing tiene una contraparte: el unboxing. Por ejemplo, el JS engine tomará un envoltorio de objeto -- como un objeto `Number` envuelto alrededor de `42` -- creado con `Number(42)` o `Object(42)` -- y lo desenvolverá para recuperar el primitivo `42` subyacente, cada vez que una operación matemática (como `*` o `-`) encuentre dicho objeto. El comportamiento de unboxing está muy fuera del alcance de nuestra discusión, pero está cubierto completamente en el mencionado título "Types & Grammar". |

## Asignar propiedades

Ya sea que una propiedad se defina en el momento de la definición del objeto literal, o se agregue más tarde, la asignación del valor de una propiedad se hace con el operador `=`, como se haría con cualquier otra asignación normal:

```js
myObj.favoriteNumber = 123;
```

Si la propiedad `favoriteNumber` todavía no existe, esa sentencia creará una nueva propiedad de ese nombre y asignará su valor. Pero si ya existe, esa sentencia reasignará su valor.

| ADVERTENCIA: |
| :--- |
| Una asignación `=` a una propiedad puede fallar (silenciosamente o lanzando una excepción), o puede no asignar directamente el valor sino invocar una función *setter* que realiza alguna(s) operación(es). Más detalles sobre estos comportamientos en el próximo capítulo. |

También es posible asignar una o más propiedades a la vez -- asumiendo que las propiedades fuente (pares de nombre y valor) están en otro objeto -- usando el método `Object.assign(..)` (agregado en ES6):

```js
// shallow copy all (owned and enumerable) properties
// from `myObj` into `anotherObj`
Object.assign(anotherObj,myObj);

Object.assign(
    /*target=*/anotherObj,
    /*source1=*/{
        someProp: "some value",
        anotherProp: 1001,
    },
    /*source2=*/{
        yetAnotherProp: false
    }
);
```

`Object.assign(..)` toma el primer objeto como destino, y el segundo (y opcionalmente los subsiguientes) objeto(s) como fuente(s). La copia se hace de la misma manera que se describió antes en la sección "Object Spread".

## Eliminar propiedades

Una vez que una propiedad está definida en un objeto, la única forma de quitarla es con el operador `delete`:

```js
anotherObj = {
    counter: 123
};

anotherObj.counter;   // 123

delete anotherObj.counter;

anotherObj.counter;   // undefined
```

Contrario a la creencia errónea común, el operador `delete` de JS **no** realiza directamente ninguna desasignación/liberación de memoria, a través del recolector de basura (GC). Lo único que hace es quitar una propiedad de un objeto. Si el valor en la propiedad era una referencia (a otro objeto/etc.), y no hay otras referencias sobrevivientes a ese valor una vez que se quita la propiedad, ese valor probablemente sería entonces elegible para su eliminación en un futuro barrido del GC.

Llamar a `delete` sobre cualquier cosa que no sea una propiedad de objeto es un mal uso del operador `delete`, y o bien fallará silenciosamente (en modo no estricto) o lanzará una excepción (en strict mode).

Eliminar una propiedad de un objeto es distinto de asignarle un valor como `undefined` o `null`. Una propiedad a la que se le asigna `undefined`, ya sea inicialmente o más tarde, sigue estando presente en el objeto, y aún podría revelarse al enumerar el contenido

## Determinar el contenido del contenedor

Podés determinar el contenido de un objeto de varias maneras. Para preguntarle a un objeto si tiene una propiedad específica:

```js
myObj = {
    favoriteNumber: 42,
    coolFact: "the first person convicted of speeding was going 8 mph",
    beardLength: undefined,
    nicknames: [ "getify", "ydkjs" ]
};

"favoriteNumber" in myObj;            // true

myObj.hasOwnProperty("coolFact");     // true
myObj.hasOwnProperty("beardLength");  // true

myObj.nicknames = undefined;
myObj.hasOwnProperty("nicknames");    // true

delete myObj.nicknames;
myObj.hasOwnProperty("nicknames");    // false
```

*Sí* hay una diferencia importante entre cómo se comportan el operador `in` y el método `hasOwnProperty(..)`. El operador `in` verificará no solo el objeto destino especificado, sino que, si no lo encuentra ahí, también consultará la cadena `[[Prototype]]` del objeto (cubierta en el próximo capítulo). En cambio, `hasOwnProperty(..)` solo consulta el objeto destino.

Si estás prestando mucha atención, puede que hayas notado que `myObj` parece tener una propiedad de método llamada `hasOwnProperty(..)`, aunque no definimos tal cosa. Eso es porque `hasOwnProperty(..)` está definido como un incorporado en `Object.prototype`, que por defecto es "heredado por" todos los objetos normales. Sin embargo, hay un riesgo inherente al acceder a un método "heredado" de ese tipo. De nuevo, más sobre prototypes en el próximo capítulo.

### Mejor verificación de existencia

ES2022 (casi oficial al momento de escribir) ya ha fijado una nueva característica, `Object.hasOwn(..)`. Hace esencialmente lo mismo que `hasOwnProperty(..)`, pero se invoca como un helper estático externo al valor del objeto en lugar de mediante el `[[Prototype]]` del objeto, haciéndolo más seguro y consistente en su uso:

```js
// instead of:
myObj.hasOwnProperty("favoriteNumber")

// we should now prefer:
Object.hasOwn(myObj,"favoriteNumber")
```

Aunque (al momento de escribir) esta característica recién está emergiendo en JS, hay polyfills que hacen que esta API esté disponible en tus programas incluso cuando se ejecutan en un entorno JS previo que todavía no tiene la característica definida. Por ejemplo, un esbozo rápido de polyfill de reemplazo:

```js
// simple polyfill sketch for `Object.hasOwn(..)`
if (!Object.hasOwn) {
    Object.hasOwn = function hasOwn(obj,propName) {
        return Object.prototype.hasOwnProperty.call(obj,propName);
    };
}
```

Incluir un parche de polyfill como ese en tu programa significa que podés empezar a usar `Object.hasOwn(..)` de forma segura para las verificaciones de existencia de propiedades sin importar si un entorno JS ya tiene `Object.hasOwn(..)` incorporado o no.

### Listar todo el contenido del contenedor

Ya discutimos la API `Object.entries(..)` antes, que nos dice qué propiedades tiene un objeto (siempre que sean enumerables -- más en el próximo capítulo).

También hay disponible una variedad de otros mecanismos. `Object.keys(..)` nos da la lista de los nombres de propiedad enumerables (es decir, las claves) de un objeto -- solo nombres, sin valores; `Object.values(..)` en cambio nos da la lista de todos los valores contenidos en propiedades enumerables.

¿Pero qué pasa si quisiéramos obtener *todas* las claves de un objeto (enumerables o no)? `Object.getOwnPropertyNames(..)` parece hacer lo que queremos, en el sentido de que es como `Object.keys(..)` pero también devuelve los nombres de propiedades no enumerables. Sin embargo, esta lista **no** incluirá ningún nombre de propiedad Symbol, ya que esos se tratan como ubicaciones especiales en el objeto. `Object.getOwnPropertySymbols(..)` devuelve todas las propiedades Symbol de un objeto. Así que si concatenás ambas listas juntas, tendrías todo el contenido directo (*propio*) de un objeto.

Sin embargo, como ya hemos insinuado varias veces, y cubriremos en detalle completo en el próximo capítulo, un objeto también puede "heredar" contenido de su cadena `[[Prototype]]`. Estos no se consideran contenido *propio* (owned), así que no aparecerán en ninguna de estas listas.

Recordá que el operador `in` potencialmente recorrerá toda la cadena buscando la existencia de una propiedad. De manera similar, un bucle `for..in` recorrerá la cadena y listará cualquier propiedad enumerable (propia o heredada). Pero no hay ninguna API incorporada que recorra toda la cadena y devuelva una lista del conjunto combinado tanto del contenido *propio* como del *heredado*.

## Contenedores temporales

Usar un contenedor para almacenar múltiples valores a veces es solo un mecanismo de transporte temporal, como cuando querés pasar múltiples valores a una función mediante un único argumento, o cuando querés que una función devuelva múltiples valores:

```js
function formatValues({ one, two, three }) {
    // the actual object passed in as an
    // argument is not accessible, since
    // we destructured it into three
    // separate variables

    one = one.toUpperCase();
    two = `--${two}--`;
    three = three.substring(0,5);

    // this object is only to transport
    // all three values in a single
    // return statement
    return { one, two, three };
}

// destructuring the return value from
// the function, because that returned
// object is just a temporary container
// to transport us multiple values
const { one, two, three } =

    // this object argument is a temporary
    // transport for multiple input values
    formatValues({
       one: "Kyle",
       two: "Simpson",
       three: "getify"
    });

one;     // "KYLE"
two;     // "--Simpson--"
three;   // "getif"
```

El objeto literal pasado a `formatValues(..)` se desestructura inmediatamente como parámetro, así que dentro de la función solo lidiamos con tres variables separadas (`one`, `two` y `three`). El objeto literal que la función `return`a también se desestructura inmediatamente, así que de nuevo solo lidiamos con tres variables separadas (`one`, `two`, `three`).

Este fragmento ilustra el idiom/patrón de que un objeto a veces es solo un contenedor de transporte temporal en lugar de un valor significativo en sí mismo.

## Los contenedores son colecciones de propiedades

El uso más común de los objetos es como contenedores de múltiples valores. Creamos y gestionamos objetos contenedores de propiedades mediante:

* definir propiedades (ubicaciones con nombre), ya sea en el momento de creación del objeto o más tarde
* asignar valores, ya sea en el momento de creación del objeto o más tarde
* acceder a valores más tarde, usando los nombres de las ubicaciones (nombres de propiedad)
* eliminar propiedades mediante `delete`
* determinar el contenido del contenedor con `in`, `hasOwnProperty(..)` / `hasOwn(..)`, `Object.entries(..)` / `Object.keys(..)`, etc.

Pero hay mucho más en los objetos que solo colecciones estáticas de nombres de propiedad y valores. En el próximo capítulo, nos meteremos bajo el capó para ver cómo funcionan realmente.

[^structuredClone]: "Structured Clone Algorithm", HTML Specification; https://html.spec.whatwg.org/multipage/structured-data.html#structured-cloning ; Consultado en julio de 2022
