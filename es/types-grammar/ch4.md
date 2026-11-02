# You Don't Know JS Yet: Types & Grammar - 2nd Edition
# Capítulo 4: Coercionando Valores

| NOTA: |
| :--- |
| Trabajo en progreso |

Hemos cubierto a fondo todos los distintos *tipos* de valores en JS. Y en el camino, más de una vez, mencionamos la noción de convertir -- en realidad, coercionar -- de un tipo de valor a otro.

En este capítulo, nos sumergiremos a fondo en la coerción y develaremos todos sus misterios.

## Coerción: Explícita vs Implícita

Algunos desarrolladores afirman que cuando indicás explícitamente un cambio de tipo en una operación, eso no califica como una *coerción* sino apenas como un type-cast o una conversión de tipos. En otras palabras, la afirmación es que la coerción es solo implícita.

No estoy de acuerdo con esa caracterización. Yo uso *coerción* para etiquetar cualquier conversión de tipos en un lenguaje de tipado dinámico, ya sea que resulte evidente en el código o no. Acá está el porqué: la línea entre *explícito* e *implícito* no es clara ni objetiva, es bastante subjetiva. Si vos pensás que una conversión de tipos es implícita (y por lo tanto *coerción*), pero yo pienso que es explícita (y por lo tanto no es *coerción*), la distinción se vuelve irrelevante.

Tené esa subjetividad en mente mientras exploramos varias formas *explícitas* e *implícitas* de coerción. De hecho, acá va un spoiler: la mayoría de las coerciones podrían argumentarse como una u otra, así que las vamos a mirar con esa perspectiva balanceada.

### Implícita: ¿Mala o ...?

Una opinión extremadamente común entre los desarrolladores de JS es que *la coerción es mala*, específicamente, que *la coerción implícita es mala*; el aumento de popularidad de herramientas conscientes de los tipos como TypeScript habla a las claras de ese sentimiento.

Pero ese sentimiento no es nuevo. Hace más de 14 años, el libro "The Good Parts" de Douglas Crockford también condenó célebremente la *coerción implícita* como una de las *bad parts*. Hasta Brendan Eich, el creador de JS, afirma con regularidad que la *coerción implícita* fue un error[^EichCoercion] en el diseño temprano del lenguaje que ahora lamenta.

Si estuviste en el mundo de JS por más de unos pocos meses, casi con certeza escuchaste estas opiniones expresadas con fuerza y de manera predominante. Y si estuviste en JS por años o más, probablemente ya tengas tu decisión tomada.

De hecho, creo que te costaría nombrar casi cualquier otra fuente reconocida de enseñanza de JS que respalde con fuerza la coerción (en prácticamente todas sus formas); yo lo hago -- ¡y este libro definitivamente lo hace! -- pero me siento mayormente como una voz solitaria gritando en vano en el desierto.

Sin embargo, acá va una observación que hice a lo largo de los años: la mayoría de la gente que condena públicamente la *coerción implícita*, en realidad usa *coerción implícita* en su propio código. Mmmmm...

Douglas Crockford dice que hay que evitar el error de la *coerción implícita*[^CrockfordCoercion], pero su código usa sentencias `if (..)` con valores no booleanos evaluados. [^CrockfordIfs] Muchos descartaron mi señalamiento de eso en el pasado, con la afirmación de que la conversión a booleano no es *realmente* coerción. Ehhh... ¿ok?

Brendan Eich dice que lamenta la *coerción implícita*, pero aun así respalda abiertamente[^BrendanToString] expresiones idiomáticas como `x + ""` (¡y otras!) para coercionar el valor de `x` a un string (lo cubriremos más adelante); y eso es sin dudas una *coerción implícita*.

¿Qué hacemos con esta disonancia? ¿Es apenas una, "hacé lo que digo, no lo que hago", una menor autocontradicción? ¿O hay algo más detrás?

No voy a emitir un juicio final acá todavía, pero quiero que vos, lector, reflexiones profundamente sobre esa pregunta, a medida que avanzás a lo largo de este capítulo y del libro.

## Abstractas

Ahora que te desafié a examinar la coerción con más profundidad de la que quizás te habías permitido antes, miremos primero los fundamentos de cómo ocurre la coerción, según la especificación de JS.

La especificación detalla una cantidad de *operaciones abstractas*[^AbstractOperations] que dictan la conversión interna de un tipo de valor a otro. Es importante conocer estas operaciones, ya que las mecánicas de coerción del lenguaje las combinan y entremezclan de varias maneras.

Estas operaciones *parecen* ser funciones reales que podrían invocarse, como `ToString(..)` o `ToNumber(..)`. Pero por *abstractas*, queremos decir que solo existen conceptualmente bajo estos nombres; no son funciones que podamos invocar *directamente* en nuestros programas. En cambio, las activamos implícita/indirectamente dependiendo de las sentencias/expresiones en nuestros programas.

### ToBoolean

La toma de decisiones (ramificación condicional) siempre requiere un valor booleano `true` o `false`. Pero es extremadamente común querer tomar esas decisiones basándonos en condiciones de valores no booleanos, como si un string está vacío o tiene algo adentro.

Cuando se encuentran valores no booleanos en un contexto que requiere un booleano -- como la cláusula de condición de una sentencia `if` o un loop `for` -- se activa la operación abstracta `ToBoolean(..)`[^ToBoolean] para facilitar la coerción.

Todos los valores en JS están en uno de dos cubos: *truthy* o *falsy*. Los valores truthy se coercionan vía la operación `ToBoolean()` a `true`, mientras que los valores falsy se coercionan a `false`:

```
// ToBoolean() is abstract

ToBoolean(undefined);               // false
ToBoolean(null);                    // false
ToBoolean("");                      // false
ToBoolean(0);                       // false
ToBoolean(-0);                      // false
ToBoolean(0n);                      // false
ToBoolean(NaN);                     // false
```

Regla simple: *cualquier otro valor* que no esté en la lista de arriba es truthy y se coerciona vía `ToBoolean()` a `true`:

```
ToBoolean("hello");                 // true
ToBoolean(42);                      // true
ToBoolean([ 1, 2, 3 ]);             // true
ToBoolean({ a: 1 });                // true
```

Incluso valores como `"   "` (string con solo espacios en blanco), `[]` (array vacío) y `{}` (objeto vacío), que intuitivamente podrían parecer más "false" que "true", sin embargo se coercionan a `true`.

| ADVERTENCIA: |
| :--- |
| *Existen* excepciones estrechas y complicadas a esta regla de truthy. Por ejemplo, la plataforma web deprecó la antigua característica de colección/array `document.all`, aunque no puede eliminarse por completo -- eso rompería demasiados sitios. Incluso donde `document.all` sigue estando definido, se comporta como un "objeto falsy"[^ExoticFalsyObjects] -- `undefined` que luego se coerciona a `false`; esto significa que verificaciones condicionales heredadas como `if (document.all) { .. }` ya no pasan. |

La operación de coerción `ToBoolean()` es básicamente una tabla de búsqueda más que un algoritmo de pasos a usar para coercionar un no booleano a un booleano. Por eso, algunos desarrolladores afirman que esto no es *realmente* coerción de la manera en que lo son otras operaciones abstractas de coerción. Creo que eso es un disparate. `ToBoolean()` convierte de tipos de valores no booleanos a un booleano, y eso es coerción de tipos pura y dura (aunque sea una búsqueda muy simple en lugar de un algoritmo).

Tené en mente: estas reglas de coerción booleana solo aplican cuando `ToBoolean()` está efectivamente activada. Hay construcciones/expresiones idiomáticas en el lenguaje JS que pueden parecer involucrar coerción booleana pero que en realidad no lo hacen. Más sobre esto después.

### ToPrimitive

Cualquier valor que no sea ya un primitive puede reducirse a un primitive usando la operación abstracta `ToPrimitive()` (específicamente, `OrdinaryToPrimitive()`[^OrdinaryToPrimitive]). Generalmente, a `ToPrimitive()` se le da un *hint* para indicarle si se prefiere un `number` o un `string`.

```
// ToPrimitive() is abstract

ToPrimitive({ a: 1 },"string");          // "[object Object]"

ToPrimitive({ a: 1 },"number");          // NaN
```

La operación `ToPrimitive()` buscará en el objeto provisto, ya sea un método `toString()` o un método `valueOf()`; el orden en que los busca está controlado por el *hint*. `"string"` significa verificar en orden `toString()` / `valueOf()`, mientras que `"number"` (o ningún *hint*) significa verificar en orden `valueOf()` / `toString()`.

Si el método devuelve un valor que coincide con el tipo *hinteado*, la operación termina. Pero si el método no devuelve un valor del tipo *hinteado*, `ToPrimitive()` entonces buscará e invocará el otro método (si lo encuentra).

Si los intentos de invocación de métodos fallan en producir un valor del tipo *hinteado*, el valor de retorno final se coerciona forzosamente vía la operación abstracta correspondiente: `ToString()` o `ToNumber()`.

### ToString

Prácticamente cualquier valor que no sea ya un string puede coercionarse a una representación en string, vía `ToString()`. [^ToString] Esto suele ser bastante intuitivo, especialmente con valores primitive:

```
// ToString() is abstract

ToString(42.0);                 // "42"
ToString(-3);                   // "-3"
ToString(Infinity);             // "Infinity"
ToString(NaN);                  // "NaN"
ToString(42n);                  // "42"

ToString(true);                 // "true"
ToString(false);                // "false"

ToString(null);                 // "null"
ToString(undefined);            // "undefined"
```

Hay *algunos* resultados que pueden variar de la intuición común. Como se mencionó en el Capítulo 2, los números muy grandes o muy chicos se representarán usando notación científica:

```
ToString(Number.MAX_VALUE);     // "1.7976931348623157e+308"
ToString(Math.EPSILON);         // "2.220446049250313e-16"
```

Otro resultado contraintuitivo proviene de `-0`:

```
ToString(-0);                   // "0" -- wtf?
```

Esto no es un bug, es solo un comportamiento intencional desde los primeros días de JS, basado en la suposición de que los desarrolladores en general no querrían nunca ver una salida de cero negativo.

Un tipo de valor primitive que *no tiene permitido* coercionarse (implícitamente, al menos) a string es `symbol`:

```
ToString(Symbol("ok"));         // TypeError exception thrown
```

| ADVERTENCIA: |
| :--- |
| Invocar la función concreta `String()`[^StringFunction] (sin el operador `new`) generalmente se piensa como *meramente* invocar la operación abstracta `ToString()`. Si bien eso es mayormente cierto, no lo es del todo. `String(Symbol("ok"))` funciona, mientras que la abstracta `ToString(Symbol(..))` en sí misma lanza una excepción. Más sobre `String(..)` más adelante en este capítulo. |

#### `toString()` por defecto

Cuando `ToString()` se activa con un tipo de valor objeto, delega a la operación `ToPrimitive()` (como se explicó antes), con `"string"` como su tipo *hinteado*:

```
ToString(new String("abc"));        // "abc"
ToString(new Number(42));           // "42"

ToString({ a: 1 });                 // "[object Object]"
ToString([ 1, 2, 3 ]);              // "1,2,3"
```

En virtud de la delegación `ToPrimitive(..,"string")`, todos estos objetos tienen invocado su método `toString()` por defecto (heredado vía `[[Prototype]]`).

### ToNumber

Los valores no numéricos *que se asemejan* a números, como los strings numéricos, generalmente pueden coercionarse a una representación numérica, usando `ToNumber()`: [^ToNumber]

```
// ToNumber() is abstract

ToNumber("42");                     // 42
ToNumber("-3");                     // -3
ToNumber("1.2300");                 // 1.23
ToNumber("   8.0    ");             // 8
```

Si el valor completo no se asemeja *completamente* (más allá de los espacios en blanco) a un número válido, el resultado será `NaN`:

```
ToNumber("123px");                  // NaN
ToNumber("hello");                  // NaN
```

Otros valores primitive tienen ciertos equivalentes numéricos designados:

```
ToNumber(true);                     // 1
ToNumber(false);                    // 0

ToNumber(null);                     // 0
ToNumber(undefined);                // NaN
```

Hay algunas designaciones bastante sorprendentes para `ToNumber()`:

```
ToNumber("");                       // 0
ToNumber("       ");                // 0
```

| NOTA: |
| :--- |
| Las llamo "sorprendentes" porque creo que habría tenido mucho más sentido que se coercionaran a `NaN`, de la manera en que lo hace `undefined`. |

Algunos valores primitive *no tienen permitido* coercionarse a números, y resultan en excepciones en lugar de `NaN`:

```
ToNumber(42n);                      // TypeError exception thrown
ToNumber(Symbol("42"));             // TypeError exception thrown
```

| ADVERTENCIA: |
| :--- |
| Invocar la función concreta `Number()`[^NumberFunction] (sin el operador `new`) generalmente se piensa como *meramente* invocar la operación abstracta `ToNumber()` para coercionar un valor a un número. Si bien eso es mayormente cierto, no lo es del todo. `Number(42n)` funciona, mientras que la abstracta `ToNumber(42n)` en sí misma lanza una excepción. |

#### Otras Conversiones Numéricas Abstractas

Además de `ToNumber()`, la especificación define `ToNumeric()`, que activa `ToPrimitive()` sobre un valor, y luego condicionalmente delega a `ToNumber()` si el valor *no* es ya un tipo de valor `bigint`.

También hay una amplia variedad de operaciones abstractas relacionadas con la conversión de valores a subconjuntos muy específicos del tipo general `number`:

* `ToIntegerOrInfinity()`
* `ToInt32()`
* `ToUint32()`
* `ToInt16()`
* `ToUint16()`
* `ToInt8()`
* `ToUint8()`
* `ToUint8Clamp()`

Otras operaciones relacionadas con `bigint`:

* `ToBigInt()`
* `StringToBigInt()`
* `ToBigInt64()`
* `ToBigUint64()`

Probablemente puedas inferir el propósito de estas operaciones a partir de sus nombres, y/o consultando sus algoritmos en la especificación. Para la mayoría de las operaciones de JS, es más probable que se active una operación de más alto nivel como `ToNumber()`, en lugar de estas específicas.

#### `valueOf()` por defecto

Cuando `ToNumber()` se activa sobre un tipo de valor objeto, en cambio delega a la operación `ToPrimitive()` (como se explicó antes), con `"number"` como su tipo *hinteado*:

```
ToNumber(new String("abc"));        // NaN
ToNumber(new Number(42));           // 42

ToNumber({ a: 1 });                 // NaN
ToNumber([ 1, 2, 3 ]);              // NaN
ToNumber([]);                       // 0
```

En virtud de la delegación `ToPrimitive(..,"number")`, todos estos objetos tienen invocado su método `valueOf()` por defecto (heredado vía `[[Prototype]]`).

### Comparación de Igualdad

Cuando JS necesita determinar si dos valores son el *mismo valor*, activa la operación `SameValue()`[^SameValue], que delega a una variedad de sub-operaciones relacionadas.

Esta operación es muy estrecha y estricta, y no realiza ninguna coerción ni ninguna otra excepción de caso especial. Si dos valores son *exactamente* iguales, el resultado es `true`, de lo contrario es `false`:

```
// SameValue() is abstract

SameValue("hello","\x68ello");          // true
SameValue("\u{1F4F1}","📱");  // true
SameValue(42,42);                       // true
SameValue(NaN,NaN);                     // true

SameValue("é","é");     // false
SameValue(0,-0);                        // false
SameValue([1,2,3],[1,2,3]);             // false
```

Una variación de estas operaciones es `SameValueZero()` y sus sub-operaciones asociadas. La diferencia principal es que estas operaciones tratan `0` y `-0` como indistinguibles.

```
// SameValueZero() is abstract

SameValueZero(0,-0);                    // true
```

Si los valores son numéricos (`number` o `bigint`), tanto `SameValue()` como `SameValueZero()` delegan a sub-operaciones de los mismos nombres, especializadas para cada tipo `number` y `bigint`, respectivamente.

De lo contrario, `SameValueNonNumeric()` es la sub-operación a la que se delega si los valores que se comparan son ambos no numéricos:

```
// SameValueNonNumeric() is abstract

SameValueNonNumeric("hello","hello");   // true

SameValueNonNumeric([1,2,3],[1,2,3]);   // false
```

#### Igualdad de Más Alta Abstracción

A diferencia de `SameValue()` y sus variaciones, la especificación también define dos importantes operaciones abstractas de comparación de igualdad de más alta abstracción:

* `IsStrictlyEqual()`[^StrictEquality]
* `IsLooselyEqual()`[^LooseEquality]

La operación `IsStrictlyEqual()` devuelve inmediatamente `false` si los tipos de valor que se comparan son diferentes.

Si los tipos de valor son iguales, `IsStrictlyEqual()` delega a sub-operaciones para comparar valores `number` o `bigint`. [^NumericAbstractOps] Lógicamente podrías esperar que estas sub-operaciones delegadas sean las antes mencionadas operaciones `SameValue()` / `SameValueZero()` especializadas en numéricos. Sin embargo, `IsStrictlyEqual()` en cambio delega a `Number:equal()`[^NumberEqual] o `BigInt:equal()`[^BigIntEqual].

La diferencia entre `Number:SameValue()` y `Number:equal()` es que esta última define casos límite para la comparación de `0` vs `-0`:

```
// all of these are abstract operations

Number:SameValue(0,-0);             // false
Number:SameValueZero(0,-0);         // true
Number:equal(0,-0);                 // true
```

Estas operaciones también difieren en la comparación de `NaN` vs `NaN`:

```
Number:SameValue(NaN,NaN);          // true
Number:equal(NaN,NaN);              // false
```

| ADVERTENCIA: |
| :--- |
| Así que, en otras palabras, a pesar de su nombre, `IsStrictlyEqual()` no es tan "estricta" como `SameValue()`, en el sentido de que *miente* cuando se involucran comparaciones de `-0` o `NaN`. |

La operación `IsLooselyEqual()` también inspecciona los tipos de valor que se comparan; si son iguales, delega inmediatamente a `IsStrictlyEqual()`.

Pero si los tipos de valor que se comparan son diferentes, `IsLooselyEqual()` realiza una variedad de pasos de *igualdad coercitiva*. Es importante notar que este algoritmo siempre está tratando de reducir la comparación hasta donde ambos tipos de valor sean iguales (y tiende a preferir `number` / `bigint`).

Los pasos de la porción de *igualdad coercitiva* del algoritmo pueden resumirse aproximadamente de la siguiente manera:

1. Si alguno de los valores es `null` y el otro es `undefined`, `IsLooselyEqual()` devuelve `true`. En otras palabras, este algoritmo aplica igualdad *nullish*, en el sentido de que `null` y `undefined` son coercitivamente iguales entre sí (y a ningún otro valor).

2. Si alguno de los valores es un `number` y el otro es un `string`, el valor `string` se coerciona a un `number` vía `ToNumber()`.

3. Si alguno de los valores es un `bigint` y el otro es un `string`, el valor `string` se coerciona a un `bigint` vía `StringToBigInt()`.

4. Si alguno de los valores es un `boolean`, se coerciona a un `number`.

5. Si alguno de los valores es un no primitive (objeto, etc), se coerciona a un primitive con `ToPrimitive()`; aunque no se provee explícitamente un *hint*, el comportamiento por defecto será como si `"number"` fuera el hint.

Cada vez que se realiza una coerción en los pasos de arriba, el algoritmo se reactiva *recursivamente* con el/los nuevo(s) valor(es). Ese proceso continúa hasta que los tipos son iguales, y entonces la comparación se delega a la operación `IsStrictlyEqual()`.

¿Qué podemos sacar de este algoritmo? Primero, vemos que hay un sesgo hacia la comparación `number` (o `bigint`); nunca coerciona valores a los tipos de valor `string` o `boolean`.

Es importante destacar que vemos que tanto `IsLooselyEqual()` como `IsStrictlyEqual()` son sensibles al tipo. `IsStrictlyEqual()` abandona inmediatamente si los tipos no coinciden, mientras que `IsLooselyEqual()` realiza el trabajo extra de coercionar los tipos de valor que no coinciden para que sean iguales (de nuevo, idealmente, `number` o `bigint`).

Además, si/una vez que los tipos son iguales, ambas operaciones son idénticas -- `IsLooselyEqual()` delega a `IsStrictlyEqual()`.

### Comparación Relacional

Cuando los valores se comparan relacionalmente -- es decir, ¿es un valor "menor que" otro? -- hay una operación abstracta específica que se activa: `IsLessThan()`. [^LessThan]

```
// IsLessThan() is abstract

IsLessThan(1,2, /*LeftFirst=*/ true );            // true
```

No hay una operación `IsGreaterThan()`; en cambio, los primeros dos argumentos de `IsLessThan()` pueden invertirse para lograr una comparación "mayor que". Para preservar la semántica de evaluación de izquierda a derecha (en el caso de efectos secundarios sutiles), `isLessThan()` también toma un tercer argumento (`LeftFirst`); si es `false`, esto indica que una comparación fue invertida y que el segundo parámetro debe evaluarse antes que el primero.

```
IsLessThan(1,2, /*LeftFirst=*/ true );            // true

// equivalent of a fictional "IsGreaterThan()"
IsLessThan(2,1, /*LeftFirst=*/ false );          // false
```

Similar a `IsLooselyEqual()`, la operación `IsLessThan()` es *coercitiva*, lo que significa que primero se asegura de que los tipos de valor de sus dos valores coincidan, y prefiere las comparaciones numéricas. No hay un `IsStrictLessThan()` para la comparación relacional no coercitiva.

Como ejemplo de comparación relacional coercitiva, si el tipo de un valor es `string` y el tipo del otro es `bigint`, el `string` se coerciona a un `bigint` con la antes mencionada operación `StringToBigInt()`. Una vez que los tipos son iguales, `IsLessThan()` procede como se describe en las siguientes secciones.

#### Comparación de Strings

Cuando ambos valores son de tipo `string`, `IsLessThan()` verifica si el valor de la izquierda es un prefijo (los primeros *n* caracteres[^StringPrefix]) del de la derecha; si es así, se devuelve `true`.

Si ninguno de los strings es prefijo del otro, se compara la primera posición de carácter (dirección inicio-a-fin, no izquierda-a-derecha) que sea diferente entre los dos strings, según sus respectivos valores de code-unit (numéricos); luego se devuelve el resultado.

Generalmente, los code-units siguen un orden lexicográfico intuitivo (también conocido como orden de diccionario):

```
IsLessThan("a","b", /*LeftFirst=*/ true );        // true
```

Incluso los dígitos se tratan como caracteres (no como números):

```
IsLessThan("101","12", /*LeftFirst=*/ true );     // true
```

Hay hasta un poco de *humor* incrustado en el ordenamiento de code-units unicode:

```
IsLessThan("🐔","🥚", /*LeftFirst=*/ true );      // true
```

¡Al menos ahora respondimos la vieja pregunta de *qué viene primero*!

#### Comparación Numérica

Para las comparaciones numéricas, `IsLessThan()` delega ya sea a la operación `Number:lessThan()` o `BigInt:lessThan()`[^NumericAbstractOps], respectivamente:

```
IsLessThan(41,42, /*LeftFirst=*/ true );         // true

IsLessThan(-0,0, /*LeftFirst=*/ true );          // false

IsLessThan(NaN,1 /*LeftFirst=*/ true );          // false

IsLessThan(41n,42n, /*LeftFirst=*/ true );       // true
```

## Coerciones Concretas

Ahora que cubrimos todas las operaciones abstractas que JS define para manejar varias coerciones, es momento de dirigir nuestra atención a las sentencias/expresiones concretas que podemos usar en nuestros programas que activan estas operaciones.

### A Booleano

Para coercionar un valor que no es de tipo `boolean` a ese tipo, necesitamos la operación abstracta `ToBoolean()`, como se describió antes en este capítulo.

Antes de explorar *cómo* activarla, discutamos *por qué* querrías forzar una coerción `ToBoolean()`.

Desde una perspectiva de legibilidad del código, ser *explícito* sobre las coerciones de tipos puede ser preferible (aunque no universalmente). Pero funcionalmente, la razón más común para forzar un `boolean` es cuando estás pasando datos a una fuente externa -- por ejemplo, enviando datos como JSON a un endpoint de una API -- y ese lugar espera `true` / `false` sin necesidad de hacer coerciones.

Hay varias maneras en que `ToBoolean()` puede activarse. Quizás la más *explícita* (obvia) es la función `Boolean(..)`:

```js
Boolean("hello");               // true
Boolean(42);                    // true

Boolean("");                    // false
Boolean(0);                     // false
```

Como se mencionó en el Capítulo 3, tené en mente que `Boolean(..)` se está invocando sin la palabra clave `new`, para activar la operación abstracta `ToBoolean()`.

No es terriblemente común ver a los desarrolladores de JS usar la función `Boolean(..)` para tales coerciones explícitas. Con más frecuencia, los desarrolladores usarán la expresión idiomática del doble-`!`:

```js
!!"hello";                      // true
!!42;                           // true

!!"";                           // false
!!0;                            // false
```

El `!!` no es su propio operador, aunque lo parezca. En realidad son dos usos del operador unario `!`. Este operador primero coerciona cualquier no-`boolean`, luego lo niega. Para deshacer la negación, el segundo `!` lo vuelve a invertir.

Entonces... ¿cuál de los dos, `Boolean(..)` o `!!`, considerás que es más una coerción explícita?

Dado el volteo que hace `!`, que luego debe deshacerse con otro `!`, yo diría que `Boolean(..)` es *más* explícita -- en el trabajo de coercionar un no-`boolean` a un `boolean` -- que `!!`. Pero relevando código JS open-source, el `!!` se usa mucho más seguido.

Si definimos *explícito* como, "realizar una acción de la manera más directa y obvia", `Boolean(..)` le gana por poco a `!!`. Pero si definimos *explícito* como, "realizar una acción de la manera más reconocible", `!!` podría tener la ventaja. ¿Hay una respuesta definitiva acá?

Mientras reflexionás sobre esa pregunta, miremos otro mecanismo de JS que activa `ToBoolean()` por debajo:

```js
specialNumber = 42;

if (specialNumber) {
    // ..
}
```

La sentencia `if` requiere un `boolean` para que el condicional tome su decisión de control de flujo. Si le pasás un no-`boolean`, se realiza una *coerción* `ToBoolean()`.

A diferencia de las expresiones de coerción `ToBoolean()` anteriores, como `Boolean(..)` o `!!`, esta coerción del `if` es efímera, en el sentido de que nuestro programa JS nunca ve el resultado de la coerción; solo lo usa internamente el `if`. Algunos pueden sentir que no es *realmente* coerción si el programa no preserva/usa el valor. Pero estoy fuertemente en desacuerdo, porque la coerción definitivamente afecta el comportamiento del programa.

Muchos otros tipos de sentencias también activan la coerción `ToBoolean()`, incluyendo el condicional ternario `? :`, y los loops `for` / `while`. También tenemos los operadores `&&` (AND lógico) y `||` (OR lógico). Por ejemplo:

```js
isLoggedIn = user.sessionID || req.cookie["Session-ID"];

isAdmin = isLoggedIn && ("admin" in user.permissions);
```

Para ambos operadores, la expresión de la izquierda se evalúa primero; si no es ya un `boolean`, se activa una coerción `ToBoolean()` para producir un valor para la decisión condicional.

| NOTA: |
| :--- |
| Para explicar brevemente estos operadores: para `||`, si el valor de la expresión de la izquierda (post-coerción, si es necesario) es `true`, se devuelve el valor pre-coerción; de lo contrario se evalúa y devuelve la expresión de la derecha (sin coerción). Para `&&`, si el valor de la expresión de la izquierda (post-coerción, si es necesario) es `false`, se devuelve el valor pre-coerción; de lo contrario, se evalúa y devuelve la expresión de la derecha (sin coerción). En otras palabras, tanto `&&` como `||` fuerzan una coerción `ToBoolean()` del operando de la izquierda para tomar la decisión, pero el resultado final de ninguno de los operadores se coerciona realmente a un `boolean`. |

En el fragmento anterior, a pesar de las implicancias del nombre, es improbable que `isLoggedIn` sea realmente un `boolean`; y si es truthy, `isAdmin` tampoco será un `boolean`. Ese tipo de código es bastante común, pero es definitivamente peligroso que los tipos `boolean` resultantes asumidos no estén realmente ahí. Revisaremos este ejemplo, y estos operadores, en el próximo capítulo.

¿Están estos tipos de sentencias/expresiones (p. ej., `if (..)`, `||`, `&&`, etc) ilustrando coerción *explícita* o coerción *implícita* en su toma de decisiones condicionales?

De nuevo, creo que depende de tu perspectiva. La especificación dicta bastante explícitamente que solo toman sus decisiones con valores condicionales `boolean`, requiriendo coerción si se recibe un no-`boolean`. Por otro lado, también puede hacerse un argumento fuerte de que cualquier coerción interna es un efecto secundario (implícito) respecto del trabajo principal de `if` / `&&` / etc.

Además, como se mencionó antes en la discusión de `ToBoolean()`, algunos no consideran que *ninguna* activación de `ToBoolean()` sea una coerción.

Creo que eso es forzar demasiado las cosas, de todos modos. Mi postura: `Boolean(..)` es la forma de coerción *explícita* más preferible. Creo que `!!`, `if`, `for`, `while`, `&&` y `||` están todos coercionando *implícitamente* los no-`boolean`s, pero estoy OK con eso.

Dado que la mayoría de los desarrolladores, incluyendo nombres famosos como Doug Crockford, también usan en la práctica coerciones (`boolean`) implícitas en su código[^CrockfordIfs], creo que podemos decir que al menos *algunas formas* de coerción *implícita* son ampliamente aceptables, sin importar la omnipresente retórica en contra.

### A String

Al igual que con `ToBoolean()`, hay una cantidad de maneras de activar la coerción `ToString()` (como se discutió antes en el capítulo). La decisión de cuál enfoque es igualmente subjetiva.

Como la función `Boolean(..)`, la función `String(..)` (sin la palabra clave `new`) es una manera principal de activar la coerción *explícita* `ToString()`:

```js
String(true);                   // "true"
String(42);                     // "42"
String(-0);                     // "0"
String(Infinity);               // "Infinity"

String(null);                   // "null"
String(undefined);              // "undefined"
```

Sin embargo, `String(..)` es más que *solo* una activación de `ToString()`. Por ejemplo:

```js
String(Symbol("ok"));           // "Symbol(ok)"
```

Esto funciona, porque la coerción *explícita* de valores `symbol` está permitida. Pero en casos donde un symbol se coerciona *implícitamente* a un string (p. ej., `Symbol("ok") + ""`), la operación subyacente `ToString()` lanza una excepción. Eso prueba que `String(..)` es más que solo una activación de `ToString()`. Más sobre la coerción *implícita* de symbols a string en un ratito.

Si invocás `String(..)` con un valor objeto (p. ej., array, etc), activa la operación `ToPrimitive()` (vía la operación `ToString()`), que luego busca e invoca el método `toString()` de ese valor:

```js
String([1,2,3]);                // "1,2,3"

String(x => x + 1);             // "x => x + 1"
```

Aparte de `String(..)`, cualquier valor primitive, no nullish (ni `null` ni `undefined`) puede ser auto-boxeado (ver Capítulo 3) en su respectivo wrapper de objeto, proveyendo un método `toString()` invocable.

```js
true.toString();                // "true"
42..toString();                 // "42"
-0..toString();                 // "0"
Infinity.toString();            // "Infinity"
Symbol("ok").toString();        // "Symbol(ok)"
```

| NOTA: |
| :--- |
| Tené en mente que estos métodos `toString()` *no* necesariamente activan la operación `ToString()`, solo definen sus propias reglas de cómo representar el valor como un string. |

Como se mostró con `String(..)` hace un momento, los distintos sub-tipos de objeto -- como arrays, funciones, expresiones regulares, instancias de `Date` y `Error`, etc -- todos definen sus propios métodos `toString()` específicos, que pueden invocarse directamente:

```js
[1,2,3].toString();             // "1,2,3"

(x => x + 1).toString();        // "x => x + 1"
```

Además, cualquier objeto plano que (por defecto) esté enlazado vía `[[Prototype]]` a `Object.prototype` tiene disponible un método `toString()` por defecto:

```js
({ a : 1 }).toString();         // "[object Object]"
```

¿Es el enfoque `toString()` de coerción *explícito* o *implícito*? De nuevo, depende. Es ciertamente un mecanismo autodescriptivo, lo que se inclina hacia *explícito*. Pero a menudo depende del auto-boxing, que es en sí mismo una coerción bastante *implícita*.

Miremos otra expresión idiomática común -- ¡y famosamente respaldada! -- para coercionar un valor a un string. Recordá de "Concatenación de Strings" en el Capítulo 2 que el operador `+` está sobrecargado para preferir la concatenación de strings si alguno de los operandos ya es un string, y por lo tanto coerciona el operando no string a un string si es necesario.

Considerá:

```js
true + "";                      // "true"
42 + "";                        // "42"
null + "";                      // "null"
undefined + "";                 // "undefined"
```

La expresión idiomática `+ ""` para coerción a string aprovecha la sobrecarga de `+`, sin alterar el valor string coercionado final. Por cierto, todas estas funcionan igual con los operandos invertidos (es decir, `"" + ..`).

| ADVERTENCIA: |
| :--- |
| Un concepto erróneo extremadamente común es que `String(x)` y `x + ""` son básicamente coerciones equivalentes, respectivamente solo *explícita* vs *implícita* en forma. ¡Pero eso no es del todo cierto! Revisaremos esto en la sección "A Primitive" más adelante en este capítulo. |

Algunos sienten que esta es una coerción *explícita*, pero creo que es claramente más *implícita*, en el sentido de que aprovecha la sobrecarga de `+`; además, el `""` se usa indirectamente para activar la coerción sin modificarla. Es más, considerá qué pasa cuando esta expresión idiomática se aplica con un valor symbol:

```js
Symbol("ok") + "";              // TypeError exception thrown
```

| ADVERTENCIA: |
| :--- |
| Permitir la coerción *explícita* de symbols (`String(Symbol("ok"))`), pero prohibir la coerción *implícita* (`Symbol("ok") + ""`), es bastante intencional por parte de TC39. [^SymbolString] Se sintió que los symbols, como primitives que suelen usarse en lugares donde de otro modo se usan strings, podían confundirse demasiado fácilmente con strings. Por eso, quisieron asegurarse de que los desarrolladores expresaran la intención de coercionar un symbol a un string, con la esperanza de evitar muchas de esas confusiones anticipadas. Este es uno de los *casos extremadamente raros* donde el diseño del lenguaje afirma una opinión, y de hecho discrimina, entre coerciones *explícitas* vs. *implícitas*. |

¿Por qué la excepción? JS trata `+ ""` como una coerción *implícita*, por lo que cuando se activa con un symbol, se lanza una excepción. Creo que esa es una prueba bastante irrefutable.

No obstante, como mencioné al comienzo de este capítulo, Brendan Eich respalda `+ ""`[^BrendanToString] como la *mejor* manera de coercionar valores a strings. Creo que eso tiene mucho peso, en términos de que él apoya al menos un subconjunto de prácticas de coerción *implícita*. Sus puntos de vista sobre la coerción *implícita* deben ser un poco más matizados que, "todo es malo".

### A Número

Las coerciones numéricas son un poco más complicadas que las coerciones a string, ya que podemos estar hablando ya sea de `number` o `bigint` como el tipo objetivo. También hay un conjunto mucho más chico de valores que pueden representarse numéricamente de manera válida (todo lo demás se convierte en `NaN`).

Empecemos con las funciones `Number(..)` y `BigInt(..)` (sin palabras clave `new`):

```js
Number("42");                   // 42
Number("-3.141596");            // -3.141596
Number("-0");                   // -0

BigInt("42");                   // 42n
BigInt("-0");                   // 0n
```

La coerción `Number` que falla (no reconocida) resulta en `NaN` (ver "Número Inválido" en el Capítulo 1), mientras que `BigInt` lanza una excepción:

```js
Number("123px");                // NaN

BigInt("123px");
// SyntaxError: Cannot convert 123px to a BigInt
```

Es más, aunque `42n` es sintaxis válida como un `bigint` literal, el string `"42n"` nunca es una representación en string reconocida de un `bigint`, por ninguna de las formas de función coercitiva:

```js
Number("42n");                  // NaN

BigInt("42n");
// SyntaxError: Cannot convert 42n to a BigInt
```

Sin embargo, *sí podemos* coercionar strings numéricos con otras representaciones de los números distintas a los típicos decimales en base-10 (ver Capítulo 1 para más información):

```js
Number("0b101010");             // 42

BigInt("0b101010");             // 42n
```

Típicamente, `Number(..)` y `BigInt(..)` reciben valores string, pero eso en realidad no es requerido. Por ejemplo, `true` y `false` se coercionan a sus típicos equivalentes numéricos:

```js
Number(true);                   // 1
Number(false);                  // 0

BigInt(true);                   // 1n
BigInt(false);                  // 0n
```

También podés en general coercionar entre los tipos `number` y `bigint`:

```js
Number(42n);                    // 42
Number(42n ** 1000n);           // Infinity

BigInt(42);                     // 42n
```

También podemos usar el operador unario `+`, que comúnmente se asume que coerciona igual que la función `Number(..)`:

```js
+"42";                          // 42
+"0b101010";                    // 42
```

Ojo, eso sí. Si las coerciones son inseguras/inválidas de ciertas maneras, se lanzan excepciones:

```js
BigInt(3.141596);
// RangeError: The number 3.141596 cannot be converted to a BigInt

+42n;
// TypeError: Cannot convert a BigInt value to a number
```

Claramente, `3.141596` no se coerciona de manera segura a un entero, mucho menos a un `bigint`.

Pero `+42n` lanzando una excepción es un caso interesante. En contraste, `Number(42n)` funciona bien, así que es un poco sorprendente que `+42n` falle.

| ADVERTENCIA: |
| :--- |
| Esa sorpresa es especialmente palpable ya que anteponer un `+` delante de un número típicamente se asume que significa solo un "número positivo", de la misma manera en que `-` delante de un número se asume que significa un "número negativo". Como se explicó en el Capítulo 1, sin embargo, la sintaxis numérica de JS (`number` y `bigint`) no reconoce ninguna sintaxis para "valores negativos". Todos los literales numéricos se parsean como "positivos" por defecto. Si se antepone un `+` o un `-`, esos se tratan como operadores unarios aplicados contra el número (positivo) parseado. |

OK, entonces `+42n` se parsea como `+(42n)`. Pero aun así... ¿por qué `+` lanza una excepción acá?

¿Te acordás antes cuando mostramos que JS permite la coerción *explícita* a string de valores symbol, pero prohíbe las coerciones *implícitas* a string? Lo mismo está pasando acá. El diseño del lenguaje JS interpreta el `+` unario delante de un valor `bigint` como una coerción `ToNumber()` *implícita* (¡por lo tanto prohibida!), pero `Number(..)` se interpreta como una coerción `ToNumber()` *explícita* (¡por lo tanto permitida!).

En otras palabras, contrario a la suposición/afirmación popular, `Number(..)` y `+` no son intercambiables. Creo que `Number(..)` es la forma más segura/confiable.

#### Operaciones Matemáticas

Los operadores matemáticos (p. ej., `+`, `-`, `*`, `/`, `%` y `**`) esperan que sus operandos sean numéricos. Si usás un no-`number` con ellos, ese valor será coercionado a un `number` para los fines del cálculo matemático.

Similar a cómo `x + ""` es una expresión idiomática para coercionar `x` a un string, una expresión como `x - 0` coerciona de manera segura `x` a un número.

| ADVERTENCIA: |
| :--- |
| `x + 0` no es tan seguro, ya que el operador `+` está sobrecargado para realizar concatenación de strings si alguno de los operandos ya es un string. El operador menos `-` no está sobrecargado de esa manera, así que la única coerción será a `number`. Por supuesto, `x * 1`, `x / 1`, e incluso `x ** 1` también serían en general equivalentes matemáticamente, pero esos son mucho menos comunes, y probablemente deberían evitarse por ser potencialmente confusos para los lectores de tu código. Incluso `x % 1` parece que debería ser seguro, pero puede introducir sesgo de punto flotante (ver "Imprecisión de Punto Flotante" en el Capítulo 2). |

Sin importar qué operador matemático se use, si la coerción falla, un `NaN` es el resultado, y todos estos operadores propagarán el `NaN` hacia afuera como su resultado.

#### Operaciones a Nivel de Bits

Los operadores a nivel de bits (p. ej., `|`, `&`, `^`, `>>`, `<<` y `<<<`) todos esperan operandos number, pero específicamente limitan estos valores a enteros de 32 bits.

Si estás seguro de que los números con los que estás tratando están de manera segura dentro del rango de enteros de 32 bits, `x | 0` es otra expresión idiomática común que tiene el efecto de coercionar `x` a un `number` si es necesario.

Es más, ya que los engines de JS saben que estos valores serán enteros, hay potencial para que optimicen hacia matemática de solo enteros si ven `x | 0`. Esta es una de varias "anotaciones de tipo" recomendadas por los esfuerzos de ASM.js[^ASMjs] de hace años.

#### Acceso a Propiedades

El acceso a propiedades de objetos (y el acceso por índice de arrays) es otro lugar donde puede ocurrir coerción implícita.

Considerá:

```js
myObj = {};

myObj[3] = "hello";
myObj["3"] = "world";

console.log( myObj );
```

¿Qué esperás del contenido de este objeto? ¿Esperás dos propiedades diferentes, numérica `3` (conteniendo `"hello"`) y string `"3"` (conteniendo `"world"`)? ¿O pensás que ambas propiedades están en la misma ubicación?

Si probás ese código, verás que efectivamente obtenemos un objeto con una sola propiedad, y contiene el valor `"world"`. Eso significa que JS está coercionando internamente ya sea el `3` a `"3"`, o viceversa, cuando se hacen esos accesos a propiedades.

Curiosamente, la consola de desarrollador muy probablemente represente el objeto más o menos así:

```js
console.log( myObj );
// {3: 'world'}
```

¿Ese `3` de ahí indica que la propiedad es un `3` numérico? No del todo. Probá agregar otra propiedad a `myObj`:

```js
myObj.something = 42;

console.log( myObj )
// {3: 'world', something: 42}
```

Podemos ver que esta consola de desarrollador no pone comillas en las claves de propiedad string, así que no podemos inferir nada de `3` versus si la consola hubiera usado `"3"` para el nombre de la clave.

En cambio, probemos consultar la especificación para el valor objeto[^ObjectValue], donde encontramos:

> Una clave de propiedad es o bien un valor String de ECMAScript o bien un valor Symbol. Todos los valores String y Symbol, incluyendo el String vacío, son válidos como claves de propiedad. Un nombre de propiedad es una clave de propiedad que es un valor String.

¡OK! Entonces, en JS, los objetos solo contienen propiedades string (o symbol). Eso debe significar que el `3` numérico se coerciona a un string `"3"`, ¿no?

En la misma sección de la especificación, leemos además:

> Un índice entero es una clave de propiedad con valor String que es un String numérico canónico (ver 7.1.21) y cuyo valor numérico es o bien +0𝔽 o bien un Number entero positivo ≤ 𝔽(253 - 1). Un índice de array es un índice entero cuyo valor numérico i está en el rango +0𝔽 ≤ i < 𝔽(232 - 1).

Si una clave de propiedad (como `"3"`) *parece* un número, se trata como un índice entero. Mmmm... eso casi parece sugerir lo opuesto de lo que acabamos de postular, ¿no?

No obstante, sabemos de la cita anterior que las claves de propiedad son *solo* strings (o symbols). Entonces debe ser que "índice entero" acá no describe la ubicación real, sino más bien el uso intencional de `3` en el código JS, como un "índice entero" expresado por el desarrollador; JS entonces aún debe en realidad almacenarlo en la ubicación del "String numérico canónico".

Considerá intentos de usar otros tipos de valor, como `true`, `null`, `undefined`, o incluso no primitives (otros objetos):

```js
myObj[true] = 100;
myObj[null] = 200;
myObj[undefined] = 300;
myObj[ {a:1} ] = 400;

console.log(myObj);
// {3: 'world', something: 42, true: 100, null: 200,
// undefined: 300, [object Object]: 400}
```

Como podés ver, todos esos otros tipos de valor fueron coercionados a strings para los fines de los nombres de propiedad del objeto.

Pero antes de convencernos de esta interpretación de que todo (hasta los números) se coerciona a strings, miremos un ejemplo con array:

```js
myArr = [];

myArr[3] = "hello";
myArr["3"] = "world";

console.log( myArr );
// [empty × 3, 'world']
```

La consola de desarrollador probablemente represente un array de manera un poco diferente a un objeto plano. No obstante, aún vemos que este array solo tiene el único valor `"world"` adentro, en la posición de índice numérico correspondiente a `3`.

Ese tipo de salida más o menos implica lo opuesto de nuestra interpretación anterior: que los valores de un array se están almacenando solo en posiciones numéricas. Si agregamos otro nombre de propiedad string a `myArr`:

```js
myArr.something = 42;
console.log( myArr );
// [empty × 3, 'world', something: 42]
```

Ahora vemos que esta consola de desarrollador representa las posiciones indexadas numéricamente en el array *sin* los nombres de propiedad (ubicaciones), pero la propiedad `something` sí aparece nombrada en la salida.

También es cierto que los engines de JS como v8 tienden a, por razones de optimización de rendimiento, tratar como caso especial las propiedades de objeto que son strings de aspecto numérico como si realmente se almacenaran en posiciones numéricas como si fueran arrays. Así que incluso si el programa JS actúa como si el nombre de propiedad fuera `"3"`, de hecho por debajo, v8 podría estar tratándolo como si fuera coercionado a `3`.

¿Qué podemos sacar de todo esto?

La especificación nos dice claramente que el comportamiento de las propiedades de objeto es que se traten como strings (o symbols). Eso significa que podemos asumir que usar `3` para acceder a una ubicación en un objeto tendrá el efecto interno de coercionar ese nombre de propiedad a `"3"`.

Pero con los arrays, observamos una especie de semántica opuesta: usar `"3"` como un nombre de propiedad tiene el efecto de acceder a la posición `3` indexada numéricamente, como si el string se coercionara al número. Pero eso es mayormente solo una consecuencia del hecho de que los arrays siempre tienden a comportarse como indexados numéricamente, y/o quizás un reflejo de detalles de implementación/optimización subyacentes en el engine de JS.

La parte importante es que necesitamos reconocer que los objetos no pueden simplemente usar cualquier valor como un nombre de propiedad. Si es algo distinto a un string o un número, podemos esperar que *habrá* una coerción de ese valor.

¡Necesitamos esperar y planear para eso en lugar de permitir que nos sorprenda con bugs más adelante!

### A Primitive

La mayoría de los operadores en JS, incluyendo los que hemos visto con coerciones a `string` y `number`, están diseñados para ejecutarse contra valores primitive. Cuando cualquiera de estos operadores se usa en cambio contra un valor objeto, se activa el algoritmo abstracto `ToPrimitive` (como se describió antes) para coercionar el objeto a un primitive.

Armemos un objeto que podamos usar para inspeccionar cómo se comportan las diferentes operaciones:

```js
spyObject = {
    toString() {
        console.log("toString() invoked!");
        return "10";
    },
    valueOf() {
        console.log("valueOf() invoked!");
        return 42;
    },
};
```

Este objeto define tanto el método `toString()` como el `valueOf()`, y cada uno devuelve un tipo de valor diferente (`string` vs `number`).

Probemos algunas de las operaciones de coerción que ya vimos:

```js
String(spyObject);
// toString() invoked!
// "10"

spyObject + "";
// valueOf() invoked!
// "42"
```

¡Guau! Apuesto a que eso sorprendió a varios de ustedes, lectores; a mí sin dudas me sorprendió. Es tan común que la gente afirme que `String(..)` y `+ ""` son formas equivalentes de activar la operación `ToString()`. ¡Pero claramente no lo son!

La diferencia se reduce al *hint* que cada operación provee a `ToPrimitive()`. `String(..)` claramente provee `"string"` como el *hint*, mientras que la expresión idiomática `+ ""` no provee ningún *hint* (similar a *hintear* `"number"`). Pero no te pierdas este detalle: aunque `+ ""` invoca `valueOf()`, cuando este devuelve un valor primitive `number` de `42`, ese valor luego se coerciona a un string (vía `ToString()`), así que obtenemos `"42"` en lugar de `42`.

Sigamos:

```js
Number(spyObject);
// valueOf() invoked!
// 42

+spyObject;
// valueOf() invoked!
// 42
```

Este ejemplo implica que `Number(..)` y el operador unario `+` ambos realizan la misma coerción `ToPrimitive()` (con *hint* de `"number"`), que en nuestro caso devuelve `42`. Como eso ya es un `number` como se pidió, el valor sale sin más vueltas.

¿Pero qué pasa si un `valueOf()` devuelve un `bigint`?

```js
spyObject2 = {
    valueOf() {
        console.log("valueOf() invoked!");
        return 42n;  // bigint!
    }
};

Number(spyObject2);
// valueOf() invoked!
// 42     <--- look, not a bigint!

+spyObject2;
// valueOf() invoked!
// TypeError: Cannot convert a BigInt value to a number
```

Vimos esta diferencia antes en la sección "A Número". JS permite una coerción *explícita* del valor bigint `42n` al valor number `42`, pero prohíbe lo que considera una forma de coerción *implícita*.

¿Qué hay de la función de coerción `BigInt(..)` (sin palabra clave `new`)?

```js
BigInt(spyObject);
// valueOf() invoked!
// 42n    <--- look, a bigint!

BigInt(spyObject2);
// valueOf() invoked!
// 42n

// *******************************

spyObject3 = {
    valueOf() {
        console.log("valueOf() invoked!");
        return 42.3;
    }
};

BigInt(spyObject3);
// valueOf() invoked!
// RangeError: The number 42.3 cannot be converted to a BigInt
```

De nuevo, como vimos en la sección "A Número", `42` puede coercionarse de manera segura a `42n`. Por otro lado, `42.3` no puede coercionarse de manera segura a un `bigint`.

Hemos visto que `toString()` y `valueOf()` se invocan, de maneras variadas, a medida que se realizan ciertas coerciones `string` y `number` / `bigint`.

#### ¿No Se Encontró Primitive?

Si `ToPrimitive()` falla en producir un valor primitive, se lanzará una excepción:

```js
spyObject4 = {
    toString() {
        console.log("toString() invoked!");
        return [];
    },
    valueOf() {
        console.log("valueOf() invoked!");
        return {};
    }
};

String(spyObject4);
// toString() invoked!
// valueOf() invoked!
// TypeError: Cannot convert object to primitive value

Number(spyObject4);
// valueOf() invoked!
// toString() invoked!
// TypeError: Cannot convert object to primitive value
```

Si vas a definir coerciones a-primitive personalizadas vía `toString()` / `valueOf()`, ¡asegurate de devolver un primitive desde al menos uno de ellos!

#### Objeto A Booleano

¿Qué hay de las coerciones a `boolean` de objetos?

```js
Boolean(spyObject);
// true

!spyObject;
// false

if (spyObject) {
    console.log("if!");
}
// if!

result = spyObject ? "ternary!" : "nope";
// "ternary!"

while (spyObject) {
    console.log("while!");
    break;
}
// while!
```

Cada uno de estos está activando `ToBoolean()`. Pero si recordás de antes, *ese* algoritmo nunca delega a `ToPrimitive()`; por lo tanto, no vemos "valueOf() invoked!" siendo logueado.

#### Unboxing: Wrapper A Primitive

Una forma especial de objetos que a menudo se coercionan vía `ToPrimitive()`: primitives boxeados/wrappeados (como se vio en el Capítulo 3). Esta coerción particular de objeto-a-primitive a menudo se denomina *unboxing*.

Considerá:

```js
hello = new String("hello");
String(hello);                  // "hello"
hello + "";                     // "hello"

fortyOne = new Number(41);
Number(fortyOne);               // 41
fortyOne + 1;                   // 42
```

Los wrappers de objeto `hello` y `fortyOne` de arriba tienen métodos `toString()` y `valueOf()` configurados sobre ellos, para comportarse de manera similar a los objetos `spyObject` / etc de nuestros ejemplos anteriores.

Un caso especial con el que hay que tener cuidado con los primitives wrappeados en objeto es con `Boolean()`:

```js
nope = new Boolean(false);
Boolean(nope);                  // true   <--- oops!
!!nope;                         // true   <--- oops!
```

Recordá, esto es porque `ToBoolean()` *no* reduce un objeto a su forma primitive con `ToPrimitive`; simplemente busca el valor en su tabla interna, y como los objetos normales (no exóticos[^ExoticFalsyObjects]) son siempre truthy, sale `true`.

| NOTA: |
| :--- |
| Es un pequeño y feo gotcha. Ciertamente podría argumentarse que `new Boolean(false)` debería configurarse internamente como un "objeto falsy" exótico. [^ExoticFalsyObjects] Desafortunadamente, ese cambio ahora, 25 años después del inicio de la historia de JS, podría fácilmente crear roturas en los programas. Por eso, JS dejó este gotcha intacto. |

#### Sobrescribiendo el `toString()` por defecto

Como hemos visto, siempre podés definir un `toString()` en un objeto para que *él* sea invocado por la coerción `ToPrimitive()` apropiada. Pero otra opción es sobrescribir el `Symbol.toStringTag`:

```js
spyObject5a = {};
String(spyObject5a);
// "[object Object]"
spyObject5a.toString();
// "[object Object]"

spyObject5b = {
    [Symbol.toStringTag]: "my-spy-object"
};
String(spyObject5b);
// "[object my-spy-object]"
spyObject5b.toString();
// "[object my-spy-object]"

spyObject5c = {
    get [Symbol.toStringTag]() {
        return `myValue:${this.myValue}`;
    },
    myValue: 42
};
String(spyObject5c);
// "[object myValue:42]"
spyObject5c.toString();
// "[object myValue:42]"
```

`Symbol.toStringTag` está pensado para definir un valor string personalizado para describir el objeto cada vez que su operación `toString()` por defecto se invoca directamente, o implícitamente vía coerción; en su ausencia, el valor usado es `"Object"` en la común salida `"[object Object]"`.

La sintaxis `get ..` en `spyObject5c` está definiendo un *getter*. Eso significa que cuando JS intenta acceder a este `Symbol.toStringTag` como una propiedad (como es normal), este código getter en cambio causa que la función que especificamos sea invocada para computar el resultado. Podemos ejecutar cualquier lógica arbitraria dentro de este getter para determinar dinámicamente un *tag* string para uso del método `toString()` por defecto.

#### Sobrescribiendo `ToPrimitive`

Alternativamente, podés sobrescribir toda la operación `ToPrimitive()` por defecto para cualquier objeto, seteando la propiedad symbol especial `Symbol.toPrimitive` para que contenga una función:

```js
spyObject6 = {
    [Symbol.toPrimitive](hint) {
        console.log(`toPrimitive(${hint}) invoked!`);
        return 25;
    },
    toString() {
        console.log("toString() invoked!");
        return "10";
    },
    valueOf() {
        console.log("valueOf() invoked!");
        return 42;
    },
};

String(spyObject6);
// toPrimitive(string) invoked!
// "25"   <--- not "10"

spyObject6 + "";
// toPrimitive(default) invoked!
// "25"   <--- not "42"

Number(spyObject6);
// toPrimitive(number) invoked!
// 25     <--- not 42 or "25"

+spyObject6;
// toPrimitive(number) invoked!
// 25
```

Como podés ver, si definís esta función en un objeto, se usa enteramente en reemplazo de la operación abstracta `ToPrimitive()` por defecto. Ya que `hint` todavía se provee a esta función invocada (`[Symbol.toPrimitive](..)`), podrías en teoría implementar tu propia versión del algoritmo, invocando un `toString()`, `valueOf()`, o cualquier otro método del objeto (referencia de contexto `this`).

O simplemente podés definir manualmente un valor de retorno como se muestra arriba. Sin importar cuál, JS *no* invocará automáticamente ni el método `toString()` ni el `valueOf()`.

| ADVERTENCIA: |
| :--- |
| Como se discutió antes en "¿No Se Encontró Primitive?", si la función `Symbol.toPrimitive` definida no devuelve en realidad un valor que sea un primitive, se lanzará una excepción sobre no poder "...convertir objeto a valor primitive". ¡Asegurate de devolver siempre un valor primitive real desde tal función! |

### Igualdad

Hasta ahora, las coerciones que hemos visto se enfocaron en valores individuales. Dirigimos nuestra atención ahora a las comparaciones de igualdad, que inherentemente involucran dos valores, cualquiera o ambos de los cuales pueden estar sujetos a coerción.

Antes en este capítulo, hablamos de varias operaciones abstractas para la comparación de igualdad de valores.

Por ejemplo, la operación `SameValue()`[^SameValue] es la más estricta de las comparaciones de igualdad, sin absolutamente ninguna coerción. La operación de JS más obvia que depende de `SameValue()` es:

```js
Object.is(42,42);                   // true
Object.is(-0,-0);                   // true
Object.is(NaN,NaN);                 // true

Object.is(0,-0);                    // false
```

La operación `SameValueZero()` -- recordá, solo difiere de `SameValue()` en tratar `-0` y `0` como indistinguibles -- se usa en bastantes más lugares, incluyendo:

```js
[ 1, 2, NaN ].includes(NaN);        // true
```

Podemos ver el malentendido de `0` / `-0` de `SameValueZero()` acá:

```js
[ 1, 2, -0 ].includes(0);           // true  <--- oops!

(new Set([ 1, 2, 0 ])).has(-0);     // true  <--- ugh

(new Map([[ 0, "ok" ]])).has(-0);   // true  <--- :(
```

En estos casos, hay una *coerción* (¡de cierta clase!) que trata `-0` y `0` como indistinguibles. No, técnicamente eso no es una "coerción" en el sentido de que el tipo no está cambiando, pero estoy medio forzando la definición para *incluir* este caso en nuestra discusión más amplia de coerción acá.

Contrastá los métodos `includes()` / `has()` acá, que activan `SameValueZero()`, con el viejo y querido utilitario de array `indexOf(..)`, que en cambio activa `IsStrictlyEqual()`. Este algoritmo es un poco más "coercitivo" que `SameValueZero()`, en el sentido de que previene que los valores `NaN` sean tratados como iguales entre sí:

```js
[ 1, 2, NaN ].indexOf(NaN);         // -1  <--- not found
```

Si estas peculiaridades matizadas de `includes(..)` e `indexOf(..)` te molestan, cuando buscás -- buscando una coincidencia de igualdad dentro de -- un valor en un array, podés evitar cualquier peculiaridad "coercitiva" y *forzar* la coincidencia de igualdad más estricta de `SameValue()`, vía `Object.is(..)`:

```js
vals = [ 0, 1, 2, -0, NaN ];

vals.find(v => Object.is(v,-0));            // -0
vals.find(v => Object.is(v,NaN));           // NaN

vals.findIndex(v => Object.is(v,-0));       // 3
vals.findIndex(v => Object.is(v,NaN));      // 4
```

#### Operadores de Igualdad: `==` vs `===`

El lugar más obvio donde se involucra *coerción* en las verificaciones de igualdad es con el operador `==`. A pesar de cualquier noción preconcebida que puedas tener sobre `==`, se comporta de manera extremadamente predecible, asegurando que ambos operandos coincidan en tipos antes de realizar su verificación de igualdad.

Para decir algo que puede o no ser súper obvio: los operadores `==` (y `===`) siempre devuelven un `boolean` (`true` o `false`), indicando el resultado de la verificación de igualdad; nunca devuelven ninguna otra cosa, sin importar qué coerción pueda ocurrir.

Ahora, recordá y repasá los pasos discutidos antes en el capítulo para la operación `IsLooselyEqual()`. [^LooseEquality] Su comportamiento, y por lo tanto cómo actúa `==`, puede intuirse pragmáticamente teniendo en mente solo estos dos hechos:

1. Si los tipos de ambos operandos son iguales, `==` tiene exactamente el mismo comportamiento que `===` -- `IsLooselyEqual()` delega inmediatamente a `IsStrictlyEqual()`. [^StrictEquality]

    Por ejemplo, cuando ambos operandos son referencias a objetos:

    ```js
    myObj = { a: 1 };
    anotherObj = myObj;

    myObj == anotherObj;                // true
    myObj === anotherObj;               // true
    ```

    Acá, `==` y `===` determinan que ambos de sus respectivos operandos son del tipo referencia `object`, así que ambas verificaciones de igualdad se comportan idénticamente; comparan las referencias a los objetos para igualdad.

2. Pero si los tipos de los operandos difieren, `==` permite coerción hasta que coincidan, y prefiere la comparación numérica; intenta coercionar ambos operandos a números, si es posible:

    ```js
    42 == "42";                         // true
    ```

    Acá, el string `"42"` se coerciona a un number `42` (no viceversa), y por lo tanto la comparación es entonces `42 == 42`, y debe claramente devolver `true`.


Armados con este conocimiento, ahora disiparemos el mito común de que solo `===` verifica el tipo y el valor, mientras que `==` verifica solo el valor. ¡No es cierto!

De hecho, `==` y `===` son ambos sensibles al tipo, cada uno verificando los tipos de sus operandos. El operador `==` permite coerción de tipos que no coinciden, mientras que `===` prohíbe cualquier coerción.

Es una opinión sostenida casi universalmente que `==` debería evitarse a favor de `===`. Puede que yo sea uno de los únicos desarrolladores que públicamente defiende con la cara seria el caso opuesto. Creo que la razón principal por la que la gente en cambio prefiere `===`, más allá de simplemente conformarse con el status quo, es una falta de tomarse el tiempo para entender realmente `==`.

Voy a revisitar este tema para presentar el caso de preferir `==` sobre `===`, más adelante en este capítulo, en "Igualdad Consciente del Tipo". Todo lo que pido es, no importa cuán fuertemente estés en desacuerdo conmigo ahora, tratá de mantener una mente abierta.

#### Coerción Nullish

Ya hemos visto una cantidad de operaciones de JS que son nullish -- tratando `null` y `undefined` como coercitivamente iguales entre sí, incluyendo el operador de encadenamiento opcional `?.` y el operador de coalescencia nullish `??` (ver "Null'ish" en el Capítulo 1).

Pero `==` es el lugar más obvio donde JS expone la igualdad coercitiva nullish:

```js
null == undefined;              // true
```

Ni `null` ni `undefined` serán jamás coercitivamente iguales a ningún otro valor en el lenguaje, más allá de entre sí. Eso significa que `==` hace ergonómico tratar estos dos valores como indistinguibles.

Podrías aprovechar esta capacidad así:

```js
if (someData == null) {
    // `someData` is "unset" (either null or undefined),
    // so set it to some default value
}

// OR:

if (someData != null) {
    // `someData` is set (neither null nor undefined),
    // so use it somehow
}
```

Recordá que `!=` es la negación de `==`, mientras que `!==` es la negación de `===`. ¡No hagas coincidir la cantidad de `=`s a menos que quieras confundirte!

Compará estos dos enfoques:

```js
if (someData == null) {
    // ..
}

// vs:

if (someData === null || someData === undefined) {
    // ..
}
```

Ambas sentencias `if` se comportarán exactamente idénticamente. ¿Cuál preferirías escribir, y cuál preferirías leer más adelante?

Para ser justos, algunos de ustedes prefieren el equivalente más verboso con `===`. Y eso está OK. Estoy en desacuerdo, creo que la versión con `==` de esta verificación es *mucho* mejor. Y también sostengo que la versión con `==` es más consistente en espíritu estilístico con cómo actúan los otros operadores nullish como `?.` y `??`.

Pero otro hecho menor que podrías considerar: en benchmarks de rendimiento que corrí muchas veces, los engines de JS pueden realizar la única verificación `== null` como se muestra *ligeramente más rápido* que la combinación de dos verificaciones `===`. En otras palabras, hay un diminuto pero medible beneficio en dejar que el `==` de JS realice la coerción nullish *implícita* que en tratar de listar *explícitamente* ambas verificaciones vos mismo.

Observaría que hasta muchos fans acérrimos de `===` tienden a conceder que `== null` es al menos uno de esos casos donde `==` es preferible.

#### Gotcha de Booleanos con `==`

Aparte de algunos casos límite coercitivos que abordaremos en la próxima sección, probablemente el gotcha más grande a tener en cuenta con `==` tiene que ver con los booleanos.

Prestá mucha atención acá, ya que es una de las mayores razones por las que la gente se quema con, y luego llega a despreciar, `==`. ¡Si seguís mi simple consejo (al final de esta sección), nunca serás una víctima!

Considerá el siguiente fragmento, y asumamos por un minuto que `isLoggedIn` *no* está conteniendo un valor `boolean` (`true` o `false`):

```js
if (isLoggedIn) {
    // ..
}

// vs:

if (isLoggedIn == true) {
    // ..
}
```

Ya cubrimos la primera forma de sentencia `if`. Sabemos que `if` espera un `boolean`, así que en este caso `isLoggedIn` será coercionado a un `boolean` usando la tabla de búsqueda en la operación abstracta `ToBoolean()`. Bastante directo de predecir, ¿no?

Pero mirá la expresión `isLoggedIn == true`. ¿Pensás que se va a comportar de la misma manera?

Si tu instinto fue *sí*, acabás de caer en una trampita engañosa. Recordá al principio de este capítulo cuando advertí que las reglas de la coerción `ToBoolean()` solo aplican si la operación de JS está efectivamente activando ese algoritmo. Acá, parece que JS debe estar haciéndolo, porque `== true` parece tan claramente un tipo de comparación "relacionada con booleanos".

Pero nop. Andá y releé el algoritmo `IsLooselyEqual()` (para `==`) antes en el capítulo. Dale, te espero. Si no te gusta mi resumen, andá y leé el algoritmo de la especificación[^LooseEquality] en sí.

OK, ¿ves ahí algo que mencione invocar `ToBoolean()` bajo alguna circunstancia?

¡Nop!

Recordá: cuando los tipos de los dos operandos de `==` no son iguales, prefiere coercionar ambos a números.

¿Qué podría haber en `isLoggedIn`, si no es un `boolean`? Bueno, podría ser un valor string como `"yes"`, por ejemplo. En esa forma, `if ("yes") { .. }` claramente pasaría la verificación condicional y ejecutaría el bloque.

¿Pero qué va a pasar con la forma `==` del condicional del `if`? Va a actuar así:

```js
// (1)
"yes" == true

// (2)
"yes" == 1

// (3)
NaN == 1

// (4)
NaN === 1           // false
```

Así que en otras palabras, si `isLoggedIn` contiene un valor como `"yes"`, el bloque `if (isLoggedIn) { .. }` pasará la verificación condicional, pero la verificación `if (isLoggedIn == true)` no lo hará. ¡Uf!

¿Qué pasaría si `isLoggedIn` contuviera el string `"true"`?

```js
// (1)
"true" == true

// (2)
"true" == 1

// (3)
NaN == 1

// (4)
NaN === 1           // false
```

Facepalm.

Acá va una pregunta sorpresa: ¿qué valor necesitaría contener `isLoggedIn` para que ambas formas del condicional de la sentencia `if` pasaran?

...

...

...

...

¿Qué pasaría si `isLoggedIn` estuviera conteniendo el número `1`? `1` es truthy, así que la forma `if (isLoggedIn)` pasa. Y la otra forma `==` que involucra coerción:

```js
// (1)
1 == true

// (2)
1 == 1

// (3)
1 === 1             // true
```

¿Pero si `isLoggedIn` estuviera en cambio conteniendo el string `"1"`? De nuevo, `"1"` es truthy, pero ¿qué hay de la coerción `==`?

```js
// (1)
"1" == true

// (2)
"1" == 1

// (3)
1 == 1

// (4)
1 === 1             // true
```

OK, entonces `1` y `"1"` son dos valores que `isLoggedIn` puede contener que son seguros de coercionar junto con `true` en una verificación de igualdad `==`. Pero básicamente casi ningún otro valor es seguro para que `isLoggedIn` contenga.

Tenemos un gotcha similar si la verificación es `== false`. ¿Qué valores son seguros en tal comparación? `""` y `0` funcionan. Pero:

```js
if ([] == false) {
    // this will run!
}
```

`[]` es un valor truthy, ¿pero también es coercitivamente igual a `false`?! Ay.

¿Qué hacemos con estos gotchas con las verificaciones `== true` y `== false`? Tengo una respuesta llana y simple.

Nunca, jamás, bajo ninguna circunstancia, realices una verificación `==` si cualquier lado de la comparación es un valor `true` o `false`. Parece que se va a comportar como una linda coerción `ToBoolean()`, pero astutamente no lo hará, y en cambio quedará atrapada en una variedad de casos límite de coerción (abordados en la próxima sección). Y evitá también las formas `===`.

Cuando estés tratando con booleanos, quedate con las formas implícitamente coercitivas que genuinamente activan `ToBoolean()`, como `if (isLoggedIn)`, y mantenete lejos de las formas `==` / `===`.

## Casos Límite de Coerción

He sido claro al expresar mi opinión pro-coerción hasta ahora. Y *es* solo una opinión, aunque está basada en interpretar hechos recopilados de estudiar la especificación del lenguaje y los comportamientos observables de JS.

Eso no quiere decir que la coerción sea perfecta. Hay varios casos límite frustrantes de los que necesitamos estar conscientes, para evitar tropezar en esos pozos. En caso de que no esté claro, mis siguientes caracterizaciones de estos casos límite son solo más opiniones mías. Tu experiencia puede variar.

### Strings

Ya vimos que la coerción a string de un array se ve así:

```js
String([ 1, 2, 3 ]);                // "1,2,3"
```

Personalmente encuentro eso súper molesto, que no incluya los `[ ]` que lo rodean. En particular, eso lleva a esta absurdidad:

```js
String([]);                         // ""
```

¿Así que no podemos decir que siquiera es un array, porque todo lo que obtenemos es un string vacío? Genial, JS. Eso es simplemente estúpido. Perdón, pero lo es. Y se pone peor:

```js
String([ null, undefined ]);        // ","
```

¡¿WAT?! Sabemos que `null` se coerciona al string `"null"`, y `undefined` se coerciona al string `"undefined"`. Pero si esos valores están en un array, mágicamente simplemente *desaparecen* como strings vacíos en la coerción array-a-string. ¡Solo queda el `","` para siquiera darnos una pista de que había algo en el array! Eso es pura tierra de tontos, ahí mismo.

¿Qué hay de los objetos? Casi igual de exasperante, aunque en la dirección opuesta:

```js
String({});                         // "[object Object]"

String({ a: 1 });                   // "[object Object]"
```

Ehm... OK. Claro, gracias JS por ninguna ayuda en entender cuál es el valor del objeto.

### Números

Estoy por revelar lo que creo que es *la* peor raíz de todos los males de los casos límite de coerción. ¿Están listos?

```js
Number("");                         // 0
Number("       ");                  // 0
```

Todavía estoy sacudiendo mi cabeza por este, y lo conozco desde hace casi 20 años. Todavía no entiendo en qué estaba pensando Brendan con este.

El string vacío está desprovisto de cualquier contenido; no tiene nada adentro con lo cual determinar una representación numérica. `0` absolutamente ***NO*** es el equivalente numérico de un valor numérico faltante/inválido. ¿Sabés qué valor number tenemos que está bien adaptado para comunicar eso? `NaN`. Ni me hagas arrancar sobre cómo se despojan los espacios en blanco de los strings al coercionar a un número, así que el para-nada-vacío string `"       "` todavía se trata igual que `""` para los fines de la coerción numérica.

Peor aún, ¿recordás cómo `[]` se coerciona al string `""`? Por extensión:

```js
Number([]);                         // 0
```

¡Doh! Si `""` no se coercionara a `0` -- recordá, ¡esta es la raíz de todo el mal de coerción! --, entonces `[]` tampoco se coercionaría a `0`.

Esto es simplemente territorio absurdo de universo patas para arriba.

Mucho más moderado, pero aún levemente molesto:

```js
Number("NaN");                      // NaN  <--- accidental!

Number("Infinity");                 // Infinity
Number("infinity");                 // NaN  <--- oops, watch case!
```

El string `"NaN"` no se parsea como un valor numérico reconocible, así que la coerción falla, produciendo (¡accidentalmente!) el valor `NaN`. `"Infinity"` es explícitamente parseable para la coerción, pero cualquier otra capitalización, incluyendo `"infinity"`, fallará, produciendo de nuevo `NaN`.

Este próximo ejemplo, puede que no pienses que es para nada un caso límite:

```js
Number(false);                      // 0
Number(true);                       // 1
```

Es meramente una convención de programadores, legado de lenguajes que originalmente no tenían valores booleanos `true` y `false`, que tratemos `0` como `false`, y `1` como `true`. ¿Pero *realmente* tiene sentido ir en la otra dirección?

Pensalo de esta manera:

```js
false + true + false + false + true;        // 2
```

¿En serio? No creo que haya ningún caso donde tratar un `boolean` como su equivalente `number` tenga algún sentido racional en un programa. Puedo entender el revés, por razones históricas: `Boolean(0)` y `Boolean(1)`.

Pero genuinamente siento que `Number(false)` y `Number(true)` (así como cualquier forma de coerción implícita) deberían producir `NaN`, no `0` / `1`.

### Absurdidad de la Coerción

Para probar mi punto, llevemos la absurdidad hasta el nivel 11:

```js
[] == ![];                          // true
```

¡¿Cómo?! Eso parece más allá de lo creíble, ¡¿que un valor pueda ser coercitivamente igual a su negación, no?!

Pero seguí por la madriguera del conejo de la coerción:

1. `[] == ![]`
2. `[] == false`
3. `"" == false`
4. `0 == false`
5. `0 == 0`
6. `0 === 0`  ->  `true`

Tenemos tres absurdidades diferentes conspirando contra nosotros: `String([])`, `Number("")` y `Number(false)`; si cualquiera de estas no fuera cierta, este resultado disparatado de caso límite no ocurriría.

Dejame dejar algo absolutamente claro, eso sí: nada de esto es culpa de `==`. Se lleva la culpa acá, por supuesto. Pero los verdaderos culpables son los casos límite subyacentes de `string` y `number`.

## Conciencia de Tipos

Ahora hemos cortado y rebanado y examinado la coerción desde cada ángulo concebible, empezando desde las internas abstractas de la especificación, luego moviéndonos a las expresiones y sentencias concretas que efectivamente disparan las coerciones.

¿Pero cuál es el punto de todo esto? ¿El detalle de este capítulo, y de hecho de todo este libro hasta este punto, es mayormente solo trivia? Eh, no lo creo.

Volvamos a las observaciones/preguntas que planteé allá al comienzo de este largo capítulo.

No hay escasez de opiniones (especialmente negativas) sobre la coerción. La posición sostenida casi universalmente es que la coerción es mayormente/enteramente una *parte mala* del diseño del lenguaje JS. Pero a pesar de esa realidad, casi todo desarrollador, en casi todo programa JS jamás escrito, enfrenta la realidad de que la coerción no puede evitarse.

En otras palabras, no importa lo que hagas, no vas a poder escapar de la necesidad de estar consciente de, entender, y manejar los tipos de valor de JS y las conversiones entre ellos. Contrario a las suposiciones comunes, abrazar un lenguaje de tipado dinámico (o incluso de tipado débil), *no* significa ser descuidado o inconsciente de los tipos.

La programación consciente de los tipos es siempre, siempre mejor que la programación ignorante/agnóstica de los tipos.

### Ehh... ¿TypeScript?

Seguramente estás pensando en este momento: "¿Por qué no puedo simplemente usar TypeScript y declarar todos mis tipos estáticamente, evitando toda la confusión del tipado dinámico y la coerción?"

| NOTA: |
| :--- |
| Tengo muchos más pensamientos detallados sobre TypeScript y el rol más grande que juega en nuestro ecosistema; guardaré esas opiniones para el apéndice ("Pensamientos sobre TypeScript"). |

Empecemos por abordar de frente las maneras en que TypeScript ayuda, y no ayuda, en la programación consciente de los tipos, como estoy defendiendo.

TypeScript es tanto **de tipado estático** (lo que significa que los tipos se declaran en tiempo de autoría y se verifican en tiempo de compilación) como **de tipado fuerte** (lo que significa que las variables/contenedores están tipados, y estas asociaciones se hacen cumplir; los sistemas de tipado fuerte también prohíben la coerción *implícita*). La mayor fortaleza de TypeScript es que típicamente obliga tanto al autor del código, como al lector del código, a confrontar los tipos que componen la mayor parte (¡idealmente, toda!) de un programa. Eso es definitivamente algo bueno.

En contraste, JS es **de tipado dinámico** (lo que significa que los tipos se descubren y manejan puramente en tiempo de ejecución) y **de tipado débil** (lo que significa que las variables/contenedores no están tipados, así que no hay asociaciones que hacer cumplir, y las variables pueden por lo tanto contener cualquier tipo de valor; los sistemas de tipado débil permiten cualquier forma de coerción).

| NOTA: |
| :--- |
| Estoy haciendo gestos a un nivel bastante alto acá, e intencionalmente no sumergiéndome profundamente en un montón de matices sobre los espectros de tipado estático/dinámico y fuerte/débil. Si sentís la urgencia de "Bueno, en realidad..." corregirme en este momento, por favor solo aguantá un poco y dejame exponer mis argumentos. |

### Conciencia de Tipos *Sin* TypeScript

¿Un sistema de tipado dinámico automáticamente significa que estás programando con menos conciencia de tipos? Muchos argumentarían eso, pero yo estoy en desacuerdo.

No creo para nada que declarar tipos estáticos (anotaciones, como en TypeScript) sea la única manera de lograr una conciencia de tipos efectiva. Claramente, sin embargo, los proponentes del tipado estático creen que esa es la *mejor* manera.

Dejame ilustrar la conciencia de tipos sin el tipado estático de TypeScript. Considerá esta declaración de variable:

```js
let API_BASE_URL = "https://some.tld/api/2";
```

¿Es esa sentencia de alguna manera *consciente del tipo*? Claro, no hay anotación `: string` después de `API_BASE_URL`. ¡Pero definitivamente creo que *sí* es consciente del tipo! Vemos claramente el tipo de valor (`string`) del valor que se asigna a `API_BASE_URL`.

| ADVERTENCIA: |
| :--- |
| No te distraigas con que la declaración `let` es re-asignable (en contraposición a un `const`). El `const` de JS *no* es una característica de primera clase de su sistema de tipos. En realidad no ganamos conciencia de tipos adicional simplemente porque sabemos que el engine de JS prohíbe la reasignación de una variable `const`. Si el código está bien estructurado -- ejem, estructurado con la conciencia de tipos como prioridad -- podemos simplemente leer el código y ver claramente que `API_BASE_URL` *no* se reasigna y por lo tanto sigue siendo el tipo de valor que se le asignó previamente. Desde una perspectiva de conciencia de tipos, eso es efectivamente lo mismo que si *no pudiera* reasignarse. |

Si más adelante quiero hacer algo como:

```js
// are we using the secure API URL?
isSecureAPI = /^https/.test(API_BASE_URL);
```

Sé que el método `test(..)` de la expresión regular espera un string, y como sé que `API_BASE_URL` está conteniendo un string, sé que esa operación es segura en cuanto a tipos.

Similarmente, como conozco las simples reglas de la coerción `ToBoolean()` tal como se relaciona con los valores string, sé que este tipo de sentencia también es segura en cuanto a tipos:

```js
// do we have an API URL determined yet?
if (API_BASE_URL) {
    // ..
}
```

Pero si más adelante, empiezo a tipear algo como esto:

```js
APIVersion = Number(API_BASE_URL);
```

Una sirena de advertencia se dispara en mi cabeza. Como sé que hay reglas muy específicas sobre cómo los valores string se coercionan a números, reconozco que esta operación **no** es segura en cuanto a tipos. Así que en cambio la encaro de manera diferente:

```js
// pull out the version number from API URL
versionDigit = API_BASE_URL.match(/\/api\/(\d+)$/)[1];

// make sure the version is actually a number
APIVersion = Number(versionDigit);
```

Sé que `API_BASE_URL` es un string, y además sé que el formato de su contenido incluye `".../api/{digits}"` al final. Eso me permite saber que la coincidencia de la expresión regular tendrá éxito, así que el acceso al array `[1]` es seguro en cuanto a tipos.

También sé que `versionDigit` contendrá un string, porque eso es lo que devuelven las coincidencias de expresiones regulares. Ahora, sé que es seguro coercionar ese string de dígito-numérico a un número con `Number(..)`.

Según mi definición, ese tipo de pensamiento, y ese estilo de codificar, es consciente de los tipos. La conciencia de tipos al codificar significa pensar cuidadosamente sobre si tales cosas serán o no *claras* y *obvias* para el lector del código.

### Conciencia de Tipos *Con* TypeScript

Los fans de TypeScript señalarán que TypeScript puede, vía inferencia de tipos, hacer tipado estático (hacerlo cumplir) sin necesitar jamás una sola anotación de tipo en el programa. Así que todos los ejemplos de código que compartí en la sección anterior, TypeScript también puede manejarlos, y proveer su variante de hacer cumplir el tipado estático en tiempo de compilación.

En otras palabras, TypeScript nos dará el mismo tipo de beneficio en verificación de tipos, cualquiera de estos dos que escribamos:

```ts
let API_BASE_URL: string = "https://some.tld/api/2";

// vs:

let API_BASE_URL = "https://some.tld/api/2";
```

Pero no hay almuerzo gratis. Tenemos algunos problemas que necesitamos confrontar. Antes que nada, TypeScript *no* dispara un error acá:

```js
API_BASE_URL = "https://some.tld/api/2";

APIVersion = Number(API_BASE_URL);
// NaN
```

Intuitivamente, *yo* quiero que un sistema consciente de los tipos entienda por qué eso es inseguro. Pero quizás eso es simplemente pedir demasiado. O tal vez si efectivamente definimos un tipo más estrecho/específico para esa variable `API_BASE_URL`, que simplemente `string`, ¿podría ayudar? Podemos usar un truco de TypeScript llamado "Template Literal Types": [^TSLiteralTypes]

```ts
type VersionedURL = `https://some.tld/api/${number}`;

API_BASE_URL: VersionedURL = "https://some.tld/api/2";

APIVersion = Number(API_BASE_URL);
// NaN
```

Nop, TypeScript todavía no ve ningún problema con eso. Sí, sé que hay una explicación para el porqué (cómo está tipado el `Number(..)` en sí).

| NOTA: |
| :--- |
| Me imagino que la gente realmente inteligente que *sabe* TypeScript bien tiene ideas creativas de cómo podemos contorsionarnos para levantar un error ahí. Quizás hasta hay una docena de maneras diferentes de forzar a TypeScript a dispararse en ese código. Pero ese no es realmente el punto. |

Mi punto es que no podemos confiar completamente en los tipos de TypeScript para resolver todos nuestros problemas, dejándonos desentender y permanecer felizmente inconscientes de los matices de los tipos y, en este caso, los comportamientos de coerción.

¡Pero! Seguramente estás objetando esta línea de argumento, desesperado por afirmar que aunque TypeScript no pueda entender alguna situación específica, ¡seguramente usar TypeScript no la hace *peor*! ¡¿No?!

Veamos qué tiene que decir TypeScript[^TSExample1] sobre esta línea:

```ts
type VersionedURL = `https://some.tld/api/${number}`;

let API_BASE_URL: VersionedURL = "https://some.tld/api/2";

let versionDigit = API_BASE_URL.match(/\/api\/(\d+)$/)[1];
// Object is possibly 'null'.
```

El error indica que el acceso `[1]` no es seguro en cuanto a tipos, porque si la expresión regular falla en encontrar cualquier coincidencia en el string, `match(..)` devuelve `null`.

Verás, aunque *yo* pueda razonar sobre el contenido del string comparado con cómo está escrita la expresión regular, e incluso si *yo* me tomé el trabajo de dejarle súper claro a TypeScript exactamente cuál es ese contenido específico del string, no es lo suficientemente inteligente como para alinear esas dos cosas y ver que en realidad es totalmente seguro en cuanto a tipos asumir que la coincidencia ocurre.

| TIP: |
| :--- |
| ¿Es realmente el trabajo de, y el mejor uso de, una herramienta consciente de los tipos el contorsionarse para expresar cada único matiz posible de la seguridad de tipos? No necesitamos herramientas perfectas y universales para derivar inmensas cantidades de beneficio de las cosas que *sí* pueden hacer. |

Es más, comparando el estilo de código en la sección anterior con el código en esta sección (con o sin las anotaciones), ¿TypeScript realmente está haciendo nuestra codificación más consciente de los tipos?

Tipo, ¿ese asunto de `type VersionedURL = ..` y `API_BASE_URL: VersionedURL` *realmente* hace nuestro código más claramente consciente de los tipos? No necesariamente lo creo.

### Inteligencia de TypeScript

Sí, te escucho gritándome a través de la pantalla de la computadora. Sí, sé que TypeScript provee la información de tipos que descubre (o infiere) a tu editor de código, que llega en la forma de autocompletados inteligentes, marcadores de advertencia inline útiles, etc.

Pero estoy argumentando que incluso *esos* no, en sí mismos, te hacen más consciente de los tipos como desarrollador

¿Por qué? Porque la conciencia de tipos *no* es solo sobre la experiencia de autoría. También es sobre la experiencia de lectura, quizás incluso más. Y no todos los lugares/mecanismos donde se lee código, tienen acceso para beneficiarse de toda la inteligencia extra.

Mirá, la magia de un servidor de lenguaje bombeando inteligencia a tu editor de código es incuestionablemente asombrosa. Es copada y súper útil.

Y no le reprocho a TypeScript como herramienta inferir cosas sobre mi **código JS** y darme pistas y sugerencias a través de deliciosas integraciones con el editor de código. Simplemente no necesariamente quiero *tener* que anotar la información de tipos de alguna manera extremadamente específica solo para silenciar las quejas de la herramienta.

### La Vara Por Encima de TypeScript

Pero incluso si hiciera/tuviera todo eso, aún no es ***suficiente*** para que yo sea plenamente consciente de los tipos, tanto como autor de código como lector de código.

Estas herramientas no atrapan cada error de tipo que puede ocurrir, no importa cuánto queramos decirnos a nosotros mismos que pueden, y no importa cuántos aros y contorsiones soportemos para desear que así fuera. Todos los esfuerzos para engatusar y *coercionar* a una herramienta a atrapar esos errores matizados, a través de una complejidad interminablemente creciente de trucos de sintaxis de tipos, es... en el mejor de los casos, esfuerzo mal empleado.

Es más, ninguna herramienta así es inmune a los falsos positivos, quejándose de cosas que no son en realidad errores; estas herramientas nunca serán tan inteligentes como lo somos nosotros como humanos. Realmente estás desperdiciando tu tiempo persiguiendo algún truco de sintaxis peculiar para callar las quejas de la herramienta.

Simplemente no hay sustituto, si querés ser verdaderamente un autor de código y lector de código consciente de los tipos, para aprender cómo funcionan los sistemas de tipos incorporados del lenguaje. Y sí, eso significa que cada único desarrollador en tu equipo necesita invertir los esfuerzos para aprenderlo. No podés aguar estas cosas solo para que sean más alcanzables para los desarrolladores con menos experiencia en el proyecto/equipo.

Incluso si concediéramos que podrías evitar el 100% de todas las coerciones *implícitas* -- no podés -- vas a enfrentar absolutamente la necesidad de coerciones *explícitas* -- ¡todos los programas lo hacen!

Y si tu respuesta a ese hecho es sugerir que simplemente vas a descargar la carga mental de entenderlas a una herramienta como TypeScript... entonces lamento decírtelo, pero estás llana y dolorosamente quedándote corto de la vara de *conciencia de tipos* que estoy desafiando a todos los desarrolladores a esforzarse por alcanzar.

No estoy abogando, acá, por que descartes TypeScript. Si te gusta, bien. Pero sí te estoy desafiando muy explícita y apasionadamente: dejá de usar TypeScript como una muleta. Dejá de prosternarte para apaciguar a los señores del engine de TypeScript. Dejá de perseguir tontamente cada conejo de tipo por cada madriguera sintáctica.

Desde mi observación, hay una trágica relación inversa entre el uso de herramientas conscientes de los tipos (como TypeScript) y el deseo/esfuerzo de perseguir la conciencia de tipos real como autor de código y lector de código. Cuanto más dependés de TypeScript, más parece que te tientan y alientan a desviar tu atención del sistema de tipos de JS (y especialmente, de la coerción) hacia el sistema de tipos alternativo de TypeScript.

Desafortunadamente, TypeScript nunca puede escapar completamente del sistema de tipos de JS, porque los tipos de TypeScript son *borrados* por el compilador, y lo que queda es solo JS con lo que el engine de JS tiene que lidiar.

| TIP: |
| :--- |
| Imaginá si alguien te diera un vaso de agua filtrada para tomar. Y justo antes de que tomaras un sorbo, dijeran, "Extrajimos esa agua del suelo cerca de un basurero. Pero no te preocupes, usamos un filtro perfectamente bueno, ¡y esa agua es totalmente segura!" ¿Cuánto confiás en ese filtro? Más a mi punto general, ¿no te sentirías más cómodo tomando esa agua si entendieras todo sobre la fuente del agua, todos los procesos de filtración, y todo lo que estaba *en* el agua del vaso en tu mano? ¿O es confiar en ese filtro suficientemente bueno? |

### Igualdad Consciente del Tipo

Cerraré este largo y sinuoso capítulo con una ilustración final, modelando cómo creo que los desarrolladores deberían -- armados con más pensamiento crítico que conformismo de manada -- encarar la codificación consciente de los tipos, uses o no una herramienta como TypeScript.

Volveremos una vez más a las comparaciones de igualdad (`==` vs `===`), desde la perspectiva de la conciencia de tipos. Antes en este capítulo, prometí que presentaría el caso de `==` sobre `===`, así que acá va.

Reafirmemos/resumamos lo que sabemos sobre `==` y `===` hasta ahora:

1. Si los tipos de los operandos para `==` coinciden, se comporta *exactamente igual* que `===`.

2. Si los tipos de los operandos para `===` no coinciden, siempre devolverá `false`.

3. Si los tipos de los operandos para `==` no coinciden, permitirá coerción de cualquiera de los operandos (generalmente prefiriendo los tipos de valor numéricos), hasta que los tipos finalmente coincidan; una vez que coinciden, ver (1).

OK, entonces tomemos esos hechos y analicemos cómo podrían interactuar en nuestro programa.

Si estás haciendo una comparación de igualdad de `x` e `y` así:

```js
if ( /* are x and y equal */ ) {
    // ..
}
```

¿Cuáles son las posibles condiciones en las que podemos estar, con respecto a los tipos de `x` e `y`?

1. Podríamos saber exactamente qué tipo(s) podrían ser `x` e `y`, porque sabemos cómo se están asignando esas variables.

2. O podríamos no ser capaces de decir cuáles podrían ser esos tipos. Podría ser que `x` o `y` pudieran ser cualquier tipo, o al menos cualquiera de varios tipos diferentes, de modo que las combinaciones posibles de tipos en la comparación sean demasiado complejas para entender/predecir.

¿Podemos coincidir en que (1) es muy preferible a (2)? ¿Podemos coincidir además en que (1) representa haber escrito nuestro código de una manera consciente de los tipos, mientras que (2) representa código que es decididamente *inconsciente* de los tipos?

Si estás usando TypeScript, es muy probable que estés consciente de los tipos de `x` e `y`, ¿no? Incluso si no estás usando TypeScript, ya mostramos que podés tomar pasos intencionales para escribir tu código de tal manera que los tipos de `x` e `y` sean conocidos y obvios.

#### (2) Tipos Desconocidos

Si estás en el escenario (2), voy a afirmar que tu código está en un estado problemático. Tu código es menos-que-ideal. Tu código necesita ser refactorizado. Lo mejor que podés hacer, si encontrás código en este estado, es... ¡arreglarlo!

Cambiá el código para que sea consciente de los tipos. Si eso significa usar TypeScript, e incluso insertar algunas anotaciones de tipo, hacelo. O si sentís que podés llegar al estado consciente de los tipos con *solo JS*, hacé eso. De cualquier manera, hacé lo que puedas para llegar al escenario (1).

Si no podés asegurar que el código que hace esta comparación de igualdad entre `x` e `y` sea consciente de los tipos, y no tenés otras opciones, entonces absolutamente *debés* usar el operador de igualdad estricta `===`. No hacerlo sería supremamente irresponsable.

```js
if (x === y) {
    // ..
}
```

Si no sabés nada sobre los tipos, ¿cómo podrías vos (o cualquier otro futuro lector de tu código) tener alguna idea de cómo se van a comportar los pasos coercitivos en `==`? No podés.

Lo único responsable que se puede hacer es, evitar la coerción y usar `===`.

Pero no pierdas de vista este hecho: solo estás eligiendo `===` como último recurso, cuando tu código es tan inconsciente de los tipos -- ejem, ¡roto en los tipos! -- como para no tener otra opción.

#### (1) Tipos Conocidos

OK, asumamos en cambio que estás en el escenario (1). Conocés los tipos de `x` e `y`. Está muy claro en el código cuál es ese conjunto estrecho de tipos que participan en la verificación de igualdad.

¡Genial!

Pero aún hay dos posibles sub-condiciones en las que podés estar:

* (1a): `x` e `y` podrían ser ya del mismo tipo, ya sea que ambos sean `string`s, `number`s, etc.

* (1b): `x` e `y` podrían ser de tipos diferentes.

Consideremos cada uno de estos casos individualmente.

##### (1a) Tipos Conocidos que Coinciden

Si los tipos en la comparación de igualdad coinciden (sean los que sean), ya sabemos con certeza que `==` y `===` hacen exactamente lo mismo. No hay absolutamente ninguna diferencia.

Salvo que `==` *es* más corto por un carácter. La mayoría de los desarrolladores sienten instintivamente que la versión más escueta pero equivalente de algo es a menudo la más preferible. Eso no es universal, por supuesto, pero es al menos una preferencia general.

```js
// this is best
if (x == y) {
    // ..
}
```

En este caso particular, un `=` extra no haría nada por nosotros para hacer el código más claro. De hecho, ¡en realidad haría la comparación peor!

```js
// this is strictly worse here!
if (x === y) {
    // ..
}
```

¿Por qué es peor?

Porque en el escenario (2), ya establecimos que `===` se usa para el último recurso cuando no sabemos lo suficiente/nada sobre los tipos como para poder predecir el resultado. Usamos `===` cuando queremos asegurarnos de evitar la coerción cuando sabemos que la coerción podría ocurrir.

¡Pero eso no aplica acá! Ya sabemos que no ocurriría ninguna coerción. No hay razón para confundir al lector con un `===` acá. Si usás `===` en un lugar donde ya *sabés* los tipos -- y además, ¡coinciden! -- eso en realidad podría enviar una señal mixta al lector. ¡Podrían haber asumido que sabían lo que pasaría en la verificación de igualdad, pero luego ven el `===` y dudan de sí mismos!

De nuevo, para decirlo llanamente, si conocés los tipos de una comparación de igualdad, y sabés que coinciden, solo hay una elección correcta: `==`.

```js
// stick to this option
if (x == y) {
    // ..
}
```

##### (1b) Tipos Conocidos que No Coinciden

OK, estamos en nuestro escenario final. Necesitamos comparar `x` e `y`, y conocemos sus tipos, pero también sabemos que sus tipos **NO** son iguales.

¿Qué operador deberíamos usar acá?

Si elegís `===`, cometiste un error enorme. ¡¿Por qué?! Porque `===` usado con tipos conocidos que no coinciden nunca, jamás, jamás devolverá `true`. Siempre fallará.

```js
// `x` and `y` have different types?
if (x === y) {
    // congratulations, this code in here will NEVER run
}
```

OK. Entonces, `===` queda descartado cuando los tipos son conocidos y no coinciden. ¿Cuál es nuestra única otra opción?

Bueno, en realidad, de nuevo tenemos dos opciones. *Podríamos* decidir:

* (1b-1): Cambiemos el código para que no estemos tratando de hacer una verificación de igualdad con tipos conocidos que no coinciden; eso podría involucrar coercionar explícitamente uno o ambos valores para que sus tipos ahora coincidan, en cuyo caso volvamos de un salto al escenario (1a).

* (1b-2): Si vamos a comparar tipos conocidos que no coinciden para igualdad, y queremos alguna esperanza de que esa verificación alguna vez pase, *debemos* usar `==`, porque es el único de los operadores de igualdad que puede coercionar uno o ambos operandos hasta que los tipos coincidan.

```js
// `x` and `y` have different types,
// so let's allow JS to coerce them
// for equality comparison
if (x == y) {
    // .. (so, you're saying there's a chance?)
}
```

Eso es todo. Terminamos. Miramos cada posible condición de comparación de igualdad sensible al tipo (entre `x` e `y`).

#### Resumiendo la Comparación de Igualdad Sensible al Tipo

El caso de preferir siempre `==` sobre `===` es el siguiente:

1. Uses TypeScript o no -- pero especialmente si *sí* usás TypeScript -- la meta debería ser que cada única parte del código, incluyendo todas las comparaciones de igualdad, sea *consciente de los tipos*.

2. Si conocés los tipos, siempre deberías preferir `==`.

    - En el caso donde los tipos coinciden, `==` es tanto más corto como más apropiado para la verificación.

    - En el caso donde los tipos no coinciden, `==` es el único operador que puede coercionar operando(s) hasta que los tipos coincidan, así que es la única manera en que tal verificación podría esperar siquiera pasar

3. Finalmente, solo si *no podés* conocer/predecir los tipos, por alguna razón frustrante, y no tenés otra opción, recurrí a usar `===` como último recurso. Y probablemente agregá ahí un comentario de código admitiendo por qué se está usando `===`, y quizás incitando a algún futuro desarrollador a más adelante cambiar el código para arreglar esa deficiencia y remover la muleta de `===`.

#### El Problema de Inconsistencia de TypeScript

Dejame ser súper claro: si estás usando TypeScript correctamente, y conocés los tipos de una comparación de igualdad, usar `===` para esa comparación está simplemente *mal*. Punto.

El problema es que TypeScript extraña y frustrantemente todavía te requiere usar `===`, a menos que ya sepa que los tipos coinciden.

Eso es porque TypeScript o bien no entiende completamente la conciencia de tipos y la coerción, o -- ¡y esto es aún más enfurecedor! -- la entiende completamente pero aun así desprecia tanto el sistema de tipos de JS como para rehuir hasta el más básico razonamiento consciente de los tipos.

¿No me creés? ¿Pensás que estoy siendo demasiado duro? Probá esto en TypeScript: [^TSExample2]

```js
let result = (42 == "42");
// This condition will always return 'false' since
// the types 'number' and 'string' have no overlap.
```

No encuentro palabras para describir lo exasperante que eso me resulta. Si prestaste atención a este largo y pesado capítulo, sabés que TypeScript básicamente está diciendo una mentira acá. Por supuesto que `42 == "42"` producirá `true` en JS.

Bueno, no es una mentira, pero está exponiendo una verdad fundamental que tantos todavía no aprecian plenamente: TypeScript tira completamente por la borda las reglas normales del sistema de tipos de JS, porque la posición de TypeScript es que el sistema de tipos de JS -- y especialmente, la coerción implícita -- son malos, y necesitan ser reemplazados.

En el mundo de TypeScript, `42` y `"42"` nunca pueden ser iguales entre sí. De ahí el mensaje de error. Pero en tierra de JS, `42` y `"42"` son absolutamente coercitivamente iguales entre sí. Y creo que he presentado un caso fuerte acá de que *deberían* asumirse como coercitivamente equivalentes de manera segura.

Lo que me molesta aún más es que TypeScript tiene una variedad de inconsistencias en este aspecto. TypeScript está perfectamente bien con la coerción *implícita* en este código:

```js
irony = `The value '42' and ${42} are coercively equal.`;
```

El `42` se coerciona implícitamente a un string al interpolarlo en la oración. ¿Por qué TypeScript está ok con esta coerción implícita, pero no con la coerción implícita de `42 == "42"`?

TypeScript tampoco tiene quejas sobre este código:

```js
API_BASE_URL = "https://some.tld/api/2";
if (API_BASE_URL) {
    // ..
}
```

¿Por qué `ToBoolean()` es una coerción implícita OK, pero `ToNumber()` en el algoritmo de `==` no lo es?

Te dejaré reflexionar sobre esto: ¿realmente pensás que es una buena idea escribir código que finalmente va a correr en un engine de JS, pero usar una herramienta y un estilo de código que intencionalmente ha expulsado la mayor parte de un pilar entero del lenguaje JS? Es más, ¿está bien que también haya titubeado con una variedad de excepciones inconsistentes, simplemente para complacer los viejos hábitos de los desarrolladores de JS?

## ¿Qué Queda?

Espero que a esta altura te sientas mucho más informado sobre cómo funciona el sistema de tipos de JS, desde los tipos de valor primitive hasta los tipos objeto, hasta cómo el engine realiza las coerciones de tipos.

Más importante aún, ahora también tenés una imagen mucho más completa de los pros/contras de las elecciones que hacemos usando el sistema de tipos de JS, como elegir coerciones *implícitas* o *explícitas* en distintos puntos.

Pero no hemos cubierto completamente el contexto en el que opera el sistema de tipos. Para el resto de este libro, dirigiremos nuestra atención a las reglas de sintaxis/gramática de JS que gobiernan cómo se comportan los operadores y las sentencias.

[^EichCoercion]: "The State of JavaScript - Brendan Eich", comment thread, Hacker News; Oct 9 2012; https://news.ycombinator.com/item?id=4632704 ; Accessed August 2022

[^CrockfordCoercion]: "JavaScript: The World's Most Misunderstood Programming Language"; 2001; https://www.crockford.com/javascript/javascript.html ; Accessed August 2022

[^CrockfordIfs]: "json2.js", Github; Apr 21 2018; https://github.com/douglascrockford/JSON-js/blob/8e8b0407e475e35942f7e9461dab81929fcc7321/json2.js#L336 ; Accessed August 2022

[^BrendanToString]: ESDiscuss mailing list; Aug 26 2014; https://esdiscuss.org/topic/string-symbol#content-15 ; Accessed August 2022

[^AbstractOperations]: "7.1 Type Conversion", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-type-conversion ; Accessed August 2022

[^ToBoolean]: "7.1.2 ToBoolean(argument)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-toboolean ; Accessed August 2022

[^ExoticFalsyObjects]: "B.3.6 The [[IsHTMLDDA]] Internal Slot", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-IsHTMLDDA-internal-slot ; Accessed August 2022

[^OrdinaryToPrimitive]: "7.1.1.1 OrdinaryToPrimitive(O,hint)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-ordinarytoprimitive ; Accessed August 2022

[^ToString]: "7.1.17 ToString(argument)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-tostring ; Accessed August 2022

[^StringConstructor]: "22.1.1 The String Constructor", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-string-constructor ; Accessed August 2022

[^StringFunction]: "22.1.1.1 String(value)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-string-constructor-string-value ; Accessed August 2022

[^ToNumber]: "7.1.4 ToNumber(argument)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-tonumber ; Accessed August 2022

[^ToNumeric]: "7.1.3 ToNumeric(argument)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-tonumeric ; Accessed August 2022

[^NumberConstructor]: "21.1.1 The Number Constructor", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-number-constructor ; Accessed August 2022

[^NumberFunction]: "21.1.1.1 Number(value)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-number-constructor-number-value ; Accessed August 2022

[^SameValue]: "7.2.11 SameValue(x,y)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-samevalue ; Accessed August 2022

[^StrictEquality]: "7.2.16 IsStrictlyEqual(x,y)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-isstrictlyequal ; Accessed August 2022

[^LooseEquality]: "7.2.15 IsLooselyEqual(x,y)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-islooselyequal ; Accessed August 2022

[^NumericAbstractOps]: "6.1.6 Numeric Types", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-numeric-types ; Accessed August 2022

[^NumberEqual]: "6.1.6.1.13 Number:equal(x,y)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-numeric-types-number-equal ; Accessed August 2022

[^BigIntEqual]: "6.1.6.2.13 BigInt:equal(x,y)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-numeric-types-bigint-equal ; Accessed August 2022

[^LessThan]: "7.2.14 IsLessThan(x,y,LeftFirst)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-islessthan ; Accessed August 2022

[^StringPrefix]: "7.2.9 IsStringPrefix(p,q)", ECMAScript 2022 Language Specification; https://262.ecma-international.org/13.0/#sec-isstringprefix ; Accessed August 2022

[^SymbolString]: "String(symbol)", ESDiscuss mailing list; Aug 12 2014; https://esdiscuss.org/topic/string-symbol ; Accessed August 2022

[^ASMjs]: "ASM.js - Working Draft"; Aug 18 2014; http://asmjs.org/spec/latest/ ; Accessed August 2022

[^TSExample1]: "TypeScript Playground"; https://tinyurl.com/ydkjs-ts-example-1 ; Accessed August 2022

[^TSExample2]: "TypeScript Playground"; https://tinyurl.com/ydkjs-ts-example-2 ; Accessed August 2022

[^TSLiteralTypes]: "TypeScript 4.1, Template Literal Types"; https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-1.html#template-literal-types ; Accessed August 2022
