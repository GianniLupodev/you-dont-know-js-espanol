# You Don't Know JS Yet: Types & Grammar - 2nd Edition
# Capítulo 3: Valores Objeto

| NOTA: |
| :--- |
| Trabajo en progreso |

Ahora que ya nos sentimos cómodos con los tipos primitivos integrados, dirigimos nuestra atención a los tipos `object` en JS.

Podría escribir un libro entero hablando de los objetos en profundidad; de hecho, ¡ya lo hice! El título "Objects & Classes" de esta serie cubre los objetos en profundidad, así que asegurate de haberlo leído antes de continuar con este capítulo.

En lugar de repetir el contenido de ese libro, aquí centraremos nuestra atención en cómo el value-type `object` se comporta e interactúa con otros valores en JS.

## Tipos de Objetos

El value-type `object` comprende varios sub-tipos, cada uno con comportamientos especializados, incluyendo:

* objetos planos (plain objects)
* objetos fundamentales (primitivos "encajados" / boxed primitives)
* objetos integrados (built-in objects)
* arrays
* expresiones regulares
* funciones (es decir, "objetos invocables")

Más allá de los comportamientos especializados, una característica compartida es que todos los objetos pueden actuar como colecciones (de propiedades) que contienen valores (incluyendo funciones/métodos).

## Objetos Planos (Plain Objects)

Al value-type objeto general a veces se lo denomina *plain ol' javascript objects* (POJOs).

Los objetos planos tienen una forma literal:

```js
address = {
    street: "12345 Market St",
    city: "San Francisco",
    state: "CA",
    zip: "94114"
};
```

Este objeto plano (POJO), tal como se define con las llaves `{ .. }`, es una colección de propiedades con nombre (`street`, `city`, `state` y `zip`). Las propiedades pueden contener cualquier valor, primitivos u otros objetos (incluyendo arrays, funciones, etc).

El mismo objeto también podría haberse definido de manera imperativa usando el constructor `new Object()`:

```js
address = new Object();
address.street = "12345 Market St";
address.city = "San Francisco";
address.state = "CA";
address.zip = "94114";
```

Los objetos planos están por defecto `[[Prototype]]`-vinculados a `Object.prototype`, lo que les da acceso delegado a varios métodos generales de objeto, tales como:

* `toString()` / `toLocaleString()`
* `valueOf()`
* `isPrototypeOf(..)`
* `hasOwnProperty(..)` (recientemente obsoleto -- alternativa: la utilidad estática `Object.hasOwn(..)`)
* `propertyIsEnumerable(..)`
* `__proto__` (función getter)

```js
address.isPrototypeOf(Object.prototype);    // true
address.isPrototypeOf({});                  // false
```

## Objetos Fundamentales (Fundamental Objects)

JS define varios tipos de objeto *fundamentales*, que son instancias de varios constructores integrados, incluyendo:

* `new String()`
* `new Number()`
* `new Boolean()`

Notá que estos constructores deben usarse con la palabra clave `new` para construir instancias de los objetos fundamentales. De lo contrario, estas funciones en realidad realizan type coercion (ver el Capítulo 4).

Estos constructores de objetos fundamentales crean value-types objeto en lugar de primitivos:

```js
myName = "Kyle";
typeof myName;                      // "string"

myNickname = new String("getify");
typeof myNickname;                  // "object"
```

En otras palabras, una instancia de un constructor de objeto fundamental puede verse, en realidad, como un envoltorio (wrapper) alrededor del valor primitivo subyacente correspondiente.

| ADVERTENCIA: |
| :--- |
| Se considera, de manera casi universal, una *mala práctica* instanciar directamente estos objetos fundamentales. Las contrapartes primitivas son, en general, más predecibles, más performantes, y ofrecen *auto-boxing* (ver la sección "Objetos Automáticos" más abajo) cada vez que se necesita la forma de envoltorio-objeto subyacente para acceder a una propiedad/método. |

Las funciones `Symbol(..)` y `BigInt(..)` son referidas en la especificación como "constructores", aunque no se usan con la palabra clave `new`, y los valores que producen en un programa JS son efectivamente primitivos.

Sin embargo, existen *objetos fundamentales* internos para estos dos tipos, usados para la delegación de prototipos y el *auto-boxing*.

En contraste, para los valores primitivos `null` y `undefined`, no existen "constructores" `Null()` o `Undefined()`, ni objetos fundamentales o prototipos correspondientes.

### Prototipos

Las instancias de los constructores de objetos fundamentales están `[[Prototype]]`-vinculadas a los objetos `prototype` de sus constructores:

* `String.prototype`: define la propiedad `length`, así como métodos específicos de string, como `toUpperCase()`, etc.

* `Number.prototype`: define métodos específicos de number, como `toPrecision(..)`, `toFixed(..)`, etc.

* `Boolean.prototype`: define los métodos por defecto `toString()` y `valueOf()`.

* `Symbol.prototype`: define `description` (getter), así como los métodos por defecto `toString()` y `valueOf()`.

* `BigInt.prototype`: define los métodos por defecto `toString()`, `toLocaleString()` y `valueOf()`.

Cualquier instancia directa de los constructores integrados tiene acceso `[[Prototype]]`-delegado a las propiedades/métodos de su respectivo `prototype`. Más aún, los valores primitivos correspondientes también tienen ese acceso delegado, por medio del *auto-boxing*.

### Objetos Automáticos

He mencionado el *auto-boxing* varias veces (incluyendo los Capítulos 1 y 2, y unas cuantas veces hasta ahora en este capítulo). Finalmente llegó el momento de explicar ese concepto.

Acceder a una propiedad o método en un valor requiere que el valor sea un objeto. Como ya vimos en el Capítulo 1, los primitivos *no son* objetos, así que JS necesita entonces convertir/envolver temporalmente ese primitivo a su contraparte de objeto fundamental[^AutoBoxing] para realizar ese acceso.

Por ejemplo:

```js
myName = "Kyle";

myName.length;              // 4

myName.toUpperCase();       // "KYLE"
```

Acceder a la propiedad `length` o al método `toUpperCase()` solo está permitido sobre un valor string primitivo porque JS hace *auto-boxing* del primitivo `string` convirtiéndolo en un objeto fundamental envoltorio, una instancia de `new String(..)`. De lo contrario, todos esos accesos tendrían que fallar, ya que los primitivos no tienen ninguna propiedad.

Más importante aún, cuando el valor primitivo es sometido a *auto-boxing* hacia su contraparte de objeto fundamental, esos objetos creados internamente tienen acceso a propiedades/métodos predefinidos (como `length` y `toUpperCase()`) por medio de un vínculo `[[Prototype]]` al prototipo de su respectivo objeto fundamental.

Así, un `string` *auto-boxed* es una instancia de `new String()`, y por lo tanto está vinculado a `String.prototype`. Además, lo mismo es cierto para `number` (envuelto como una instancia de `new Number()`) y `boolean` (envuelto como una instancia de `new Boolean()`).

Aunque los "constructores" `Symbol(..)` y `BigInt(..)` (usados sin `new`) producen valores primitivos, estos valores primitivos también pueden ser sometidos a *auto-boxing* hacia sus formas de envoltorio de objeto fundamental internas, a los efectos del acceso delegado a propiedades/métodos.

| NOTA: |
| :--- |
| Ver el libro "Objects & Classes" de esta serie para más sobre los vínculos `[[Prototype]]` y el acceso delegado/heredado a los objetos prototype de los constructores de objetos fundamentales. |

Dado que `null` y `undefined` no tienen objetos fundamentales correspondientes, no hay *auto-boxing* de estos valores.

Una pregunta subjetiva para considerar: ¿es el *auto-boxing* una forma de coercion? Yo digo que sí, aunque algunos no están de acuerdo. Internamente, un primitivo se convierte en un objeto, lo que significa que ocurrió un cambio en el value-type. Sí, es temporal, pero muchísimas coercions son temporales. Más aún, la conversión es más bien *implícita* (implicada por el acceso a la propiedad/método, pero que solo ocurre internamente). Revisaremos la naturaleza de la coercion en el Capítulo 4.

## Otros Objetos Integrados

Además de los constructores de objetos fundamentales, JS define una cantidad de otros constructores integrados que crean sub-tipos de objeto aún más especializados:

* `new Date(..)`
* `new Error(..)`
* `new Map(..)`, `new Set(..)`, `new WeakMap(..)`, `new WeakSet(..)` -- colecciones con clave
* `new Int8Array(..)`, `new Uint32Array(..)`, etc -- colecciones indexadas, de typed-array
* `new ArrayBuffer(..)`, `new SharedArrayBuffer(..)`, etc -- colecciones de datos estructurados

## Arrays

Los arrays son objetos especializados para comportarse como colecciones de valores indexadas numéricamente, a diferencia de contener valores en propiedades con nombre como lo hacen los objetos planos.

Los arrays tienen una forma literal:

```js
favoriteNumbers = [ 3, 12, 42 ];

favoriteNumbers[2];                 // 42
```

El mismo array también podría haberse definido de manera imperativa usando el constructor `new Array()`:

```js
favoriteNumbers = new Array();
favoriteNumbers[0] = 3;
favoriteNumbers[1] = 12;
favoriteNumbers[2] = 42;
```

Los arrays están `[[Prototype]]`-vinculados a `Array.prototype`, lo que les da acceso delegado a una variedad de métodos orientados a arrays, tales como `map(..)`, `includes(..)`, etc:

```js
favoriteNumbers.map(v => v * 2);
// [ 6, 24, 84 ]

favoriteNumbers.includes(42);       // true
```

Algunos de los métodos definidos en `Array.prototype` -- por ejemplo, `push(..)`, `pop(..)`, `sort(..)`, etc -- se comportan modificando el valor del array en el lugar (in place). Otros métodos -- por ejemplo, `concat(..)`, `map(..)`, `slice(..)` -- se comportan creando un nuevo array para retornar, dejando el array original intacto. Una tercera categoría de funciones de array -- por ejemplo, `indexOf(..)`, `includes(..)`, etc -- simplemente computa y retorna un resultado (que no es un array).

## Expresiones Regulares

// TODO

## Funciones

## Propuesta: Records/Tuples

Al momento de escribir esto, existe una propuesta (en stage-2)[^RecordsTuplesProposal] para agregar un nuevo conjunto de características a JS, que se corresponden estrechamente con los objetos planos y los arrays, pero con algunas diferencias notables.

Los Records son similares a los objetos planos, pero son inmutables (sellados, de solo lectura), y (a diferencia de los objetos) son tratados como valores primitivos, a los efectos de la asignación de valor y la comparación de igualdad. La diferencia de sintaxis es un `#` antes del delimitador `{ }`. Los Records solo pueden contener valores primitivos (incluyendo records y tuples).

Los Tuples tienen exactamente la misma relación, pero con los arrays, incluyendo el `#` antes de los delimitadores `[ ]`.

Es importante notar que, si bien lucen y parecen objetos/arrays, son efectivamente valores primitivos (no-objeto).

[^FundamentalObjects]: "20 Fundamental Objects", EcamScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-fundamental-objects ; Consultado en Agosto de 2022

[^AutoBoxing]: "6.2.4.6 PutValue(V,W)", Step 5.a, ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-putvalue ; Consultado en Agosto de 2022

[^RecordsTuplesProposal]: "JavaScript Records & Tuples Proposal"; Robin Ricard, Rick Button, Nicolò Ribaudo;
https://github.com/tc39/proposal-record-tuple ; Consultado en Agosto de 2022
