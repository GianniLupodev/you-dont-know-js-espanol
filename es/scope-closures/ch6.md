# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Capítulo 6: Limitando la Exposición del Scope

Hasta ahora nuestro foco ha estado en explicar los mecanismos de cómo funcionan los scopes y las variables. Con esa base ya firmemente asentada, nuestra atención se eleva a un nivel de pensamiento más alto: decisiones y patrones que aplicamos a lo largo de todo el programa.

Para empezar, vamos a ver cómo y por qué deberíamos usar diferentes niveles de scope (funciones y bloques) para organizar las variables de nuestro programa, específicamente para reducir la sobreexposición del scope.

## Mínima Exposición

Tiene sentido que las funciones definan sus propios scopes. Pero ¿por qué necesitamos que los bloques creen scopes también?

La ingeniería de software articula una disciplina fundamental, aplicada típicamente a la seguridad del software, llamada "El Principio de Mínimo Privilegio" (POLP). [^POLP] Y una variante de este principio que aplica a nuestra discusión actual se denomina típicamente "Mínima Exposición" (POLE).

POLP expresa una postura defensiva hacia la arquitectura de software: los componentes del sistema deberían diseñarse para funcionar con el mínimo privilegio, el mínimo acceso, la mínima exposición. Si cada pieza está conectada con las capacidades mínimas necesarias, el sistema en conjunto es más fuerte desde el punto de vista de la seguridad, porque un compromiso o fallo de una pieza tiene un impacto minimizado sobre el resto del sistema.

Si POLP se enfoca en el diseño de componentes a nivel de sistema, la variante *Exposición* de POLE se enfoca en un nivel más bajo; la aplicaremos a cómo interactúan los scopes entre sí.

Al seguir POLE, ¿de qué queremos minimizar la exposición? Simplemente: de las variables registradas en cada scope.

Pensalo de esta manera: ¿por qué no deberías simplemente colocar todas las variables de tu programa en el scope global? Eso probablemente se siente de inmediato como una mala idea, pero vale la pena considerar por qué es así. Cuando las variables que usa una parte del programa quedan expuestas a otra parte del programa, a través del scope, surgen tres peligros principales que aparecen con frecuencia:

* **Colisiones de Nombres**: si usás un nombre de variable/función común y útil en dos partes diferentes del programa, pero el identificador proviene de un scope compartido (como el scope global), entonces ocurre una colisión de nombres, y es muy probable que aparezcan bugs cuando una parte usa la variable/función de una manera que la otra parte no espera.

    Por ejemplo, imaginá que todos tus bucles usaran una única variable índice global `i`, y resulta que un bucle de una función se está ejecutando durante una iteración de un bucle de otra función, y ahora la variable compartida `i` obtiene un valor inesperado.

* **Comportamiento Inesperado**: si exponés variables/funciones cuyo uso de otro modo es *privado* a una parte del programa, eso permite que otros desarrolladores las usen de maneras que no pretendías, lo que puede violar el comportamiento esperado y causar bugs.

    Por ejemplo, si tu parte del programa asume que un array contiene solo números, pero el código de otra persona accede y modifica el array para incluir booleanos y strings, tu código puede entonces comportarse mal de maneras inesperadas.

    Peor aún, la exposición de detalles *privados* invita a quienes tienen malas intenciones a intentar sortear las limitaciones que impusiste, para hacer con tu parte del software cosas que no deberían estar permitidas.

* **Dependencia No Intencionada**: si exponés variables/funciones innecesariamente, invitás a otros desarrolladores a usar y depender de esas piezas de otro modo *privadas*. Si bien eso no rompe tu programa hoy, crea un peligro de refactorización en el futuro, porque ahora no podés refactorizar tan fácilmente esa variable o función sin potencialmente romper otras partes del software que no controlás.

    Por ejemplo, si tu código depende de un array de números, y más tarde decidís que es mejor usar alguna otra estructura de datos en lugar de un array, ahora debés asumir la responsabilidad de ajustar otras partes afectadas del software.

POLE, aplicado al scoping de variables/funciones, dice esencialmente: por defecto, exponé el mínimo indispensable, manteniendo todo lo demás lo más privado posible. Declará las variables en scopes lo más pequeños y profundamente anidados posible, en lugar de colocar todo en el scope global (o incluso en el de la función externa).

Si diseñás tu software en consecuencia, tenés muchas más chances de evitar (o al menos minimizar) estos tres peligros.

Considerá:

```js
function diff(x,y) {
    if (x > y) {
        let tmp = x;
        x = y;
        y = tmp;
    }

    return y - x;
}

diff(3,7);      // 4
diff(7,5);      // 2
```

En esta función `diff(..)`, queremos asegurarnos de que `y` sea mayor o igual que `x`, de modo que cuando restemos (`y - x`), el resultado sea `0` o mayor. Si `x` es inicialmente mayor (¡el resultado sería negativo!), intercambiamos `x` e `y` usando una variable `tmp`, para mantener el resultado positivo.

En este ejemplo simple, no parece importar si `tmp` está dentro del bloque `if` o si pertenece al nivel de la función—¡ciertamente no debería ser una variable global! Sin embargo, siguiendo el principio POLE, `tmp` debería estar lo más oculta en el scope posible. Así que ponemos `tmp` en block scope (usando `let`) dentro del bloque `if`.

## Ocultando a la Vista (del Scope de Función)

Ahora debería estar claro por qué es importante ocultar nuestras declaraciones de variables y funciones en los scopes más bajos (más profundamente anidados) posibles. Pero ¿cómo lo hacemos?

Ya vimos las palabras clave `let` y `const`, que son declaradores de block scope; volveremos a ellas en más detalle en breve. Pero primero, ¿qué pasa con ocultar declaraciones `var` o `function` en scopes? Eso puede hacerse fácilmente envolviendo un scope de `function` alrededor de una declaración.

Consideremos un ejemplo donde el scoping de `function` puede ser útil.

La operación matemática "factorial" (notada como "6!") es la multiplicación de un entero dado contra todos los enteros sucesivamente menores hasta `1`—en realidad, podés detenerte en `2` ya que multiplicar por `1` no hace nada. En otras palabras, "6!" es lo mismo que "6 * 5!", que es lo mismo que "6 * 5 * 4!", y así sucesivamente. Debido a la naturaleza de la matemática involucrada, una vez que se ha calculado el factorial de cualquier entero dado (como "4!"), no deberíamos necesitar hacer ese trabajo de nuevo, ya que siempre será la misma respuesta.

Así que si calculás ingenuamente el factorial de `6`, y luego querés calcular el factorial de `7`, podrías recalcular innecesariamente los factoriales de todos los enteros desde 2 hasta 6. Si estás dispuesto a intercambiar memoria por velocidad, podés resolver ese cómputo desperdiciado cacheando el factorial de cada entero a medida que se calcula:

```js
var cache = {};

function factorial(x) {
    if (x < 2) return 1;
    if (!(x in cache)) {
        cache[x] = x * factorial(x - 1);
    }
    return cache[x];
}

factorial(6);
// 720

cache;
// {
//     "2": 2,
//     "3": 6,
//     "4": 24,
//     "5": 120,
//     "6": 720
// }

factorial(7);
// 5040
```

Estamos almacenando todos los factoriales computados en `cache` para que, a través de múltiples llamadas a `factorial(..)`, los cálculos previos permanezcan. Pero la variable `cache` es bastante obviamente un detalle *privado* de cómo funciona `factorial(..)`, no algo que debería exponerse en un scope externo—especialmente no el scope global.

| NOTA: |
| :--- |
| `factorial(..)` aquí es recursiva—se hace una llamada a sí misma desde dentro—pero eso es solo por brevedad del código; una implementación no recursiva daría el mismo análisis de scoping con respecto a `cache`. |

Sin embargo, arreglar este problema de sobreexposición no es tan simple como ocultar la variable `cache` dentro de `factorial(..)`, como podría parecer. Dado que necesitamos que `cache` sobreviva a múltiples llamadas, debe ubicarse en un scope fuera de esa función. Entonces ¿qué podemos hacer?

Definir otro scope intermedio (entre el scope externo/global y el interior de `factorial(..)`) para que `cache` se ubique allí:

```js
// scope externo/global

function hideTheCache() {
    // "scope intermedio", donde ocultamos `cache`
    var cache = {};

    return factorial;

    // **********************

    function factorial(x) {
        // scope interno
        if (x < 2) return 1;
        if (!(x in cache)) {
            cache[x] = x * factorial(x - 1);
        }
        return cache[x];
    }
}

var factorial = hideTheCache();

factorial(6);
// 720

factorial(7);
// 5040
```

La función `hideTheCache()` no tiene otro propósito que crear un scope para que `cache` persista a través de múltiples llamadas a `factorial(..)`. Pero para que `factorial(..)` tenga acceso a `cache`, tenemos que definir `factorial(..)` dentro de ese mismo scope. Luego retornamos la referencia de la función, como un valor de `hideTheCache()`, y la almacenamos en una variable de scope externo, también llamada `factorial`. Ahora, al llamar a `factorial(..)` (¡múltiples veces!), ¡su `cache` persistente permanece oculta pero accesible solo para `factorial(..)`!

OK, pero... va a ser tedioso definir (¡y nombrar!) un scope de función `hideTheCache(..)` cada vez que surja tal necesidad de ocultar variables/funciones, especialmente porque probablemente querremos evitar colisiones de nombres con esta función dándole a cada ocurrencia un nombre único. Uf.

| NOTA: |
| :--- |
| La técnica ilustrada—cachear la salida computada de una función para optimizar el rendimiento cuando se esperan llamadas repetidas con las mismas entradas—es bastante común en el mundo de la Programación Funcional (FP), referida canónicamente como "memoización"; este cacheo se basa en closure (ver el Capítulo 7). Además, hay preocupaciones sobre el uso de memoria (abordadas en "Una Palabra Sobre la Memoria" en el Apéndice B). Las bibliotecas de FP usualmente proveen una utilidad optimizada y verificada para la memoización de funciones, que tomaría el lugar de `hideTheCache(..)` aquí. La memoización está más allá del *scope* (¡juego de palabras!) de nuestra discusión, pero mirá mi libro *Functional-Light JavaScript* para más información. |

En lugar de definir una función nueva y nombrada de manera única cada vez que ocurre una de esas situaciones de scope-solo-con-el-propósito-de-ocultar-una-variable, una solución quizás mejor es usar una expresión de función:

```js
var factorial = (function hideTheCache() {
    var cache = {};

    function factorial(x) {
        if (x < 2) return 1;
        if (!(x in cache)) {
            cache[x] = x * factorial(x - 1);
        }
        return cache[x];
    }

    return factorial;
})();

factorial(6);
// 720

factorial(7);
// 5040
```

¡Esperá! Esto todavía usa una función para crear el scope que oculta `cache`, y en este caso, la función todavía se llama `hideTheCache`, así que ¿cómo resuelve eso algo?

Recordá de "Scope del Nombre de Función" (en el Capítulo 3), qué le ocurre al identificador de nombre de una expresión de `function`. Dado que `hideTheCache(..)` se define como una expresión de `function` en lugar de una declaración de `function`, su nombre está en su propio scope—esencialmente el mismo scope que `cache`—en lugar de en el scope externo/global.

Eso significa que podemos nombrar cada una de las ocurrencias de tal expresión de función con exactamente el mismo nombre, y nunca tener ninguna colisión. Más apropiadamente, podemos nombrar cada ocurrencia semánticamente según lo que sea que estemos intentando ocultar, y no preocuparnos de que el nombre que elijamos vaya a colisionar con cualquier otro scope de expresión de `function` en el programa.

De hecho, *podríamos* simplemente omitir el nombre por completo—definiendo así una "expresión de `function` anónima" en su lugar. Pero el Apéndice A discutirá la importancia de los nombres incluso para tales funciones de solo-scope.

### Invocando Expresiones de Función de Inmediato

Hay otra parte importante en el programa recursivo factorial anterior que es fácil pasar por alto: la línea al final de la expresión de `function` que contiene `})();`.

Notá que rodeamos la expresión de `function` entera en un conjunto de `( .. )`, y luego al final, agregamos ese segundo conjunto de paréntesis `()`; eso en realidad está llamando a la expresión de `function` que acabamos de definir. Además, en este caso, el primer conjunto de `( .. )` que rodea la expresión de función no es estrictamente necesario (más sobre eso en un momento), pero los usamos de todos modos por legibilidad.

Así que, en otras palabras, estamos definiendo una expresión de `function` que luego es invocada de inmediato. Este patrón común tiene un nombre (¡muy creativo!): Expresión de Función Invocada de Inmediato (IIFE, por sus siglas en inglés).

Una IIFE es útil cuando queremos crear un scope para ocultar variables/funciones. Dado que es una expresión, puede usarse en **cualquier** lugar de un programa JS donde se permita una expresión. Una IIFE puede tener nombre, como con `hideTheCache()`, o (¡mucho más comúnmente!) sin nombre/anónima. Y puede ser independiente o, como antes, parte de otra sentencia—`hideTheCache()` retorna la referencia a la función `factorial()`, que luego se asigna con `=` a la variable `factorial`.

A modo de comparación, aquí hay un ejemplo de una IIFE independiente:

```js
// scope externo

(function(){
    // scope interno oculto
})();

// más scope externo
```

A diferencia de antes con `hideTheCache()`, donde los `(..)` externos que la rodeaban se señalaban como una elección estilística opcional, para una IIFE independiente son **obligatorios**; distinguen a la `function` como una expresión, no como una sentencia. Por consistencia, sin embargo, siempre rodeá una `function` de una IIFE con `( .. )`.

| NOTA: |
| :--- |
| Técnicamente, los `( .. )` que la rodean no son la única manera sintáctica de asegurar que la `function` en una IIFE sea tratada por el parser de JS como una expresión de función. Veremos algunas otras opciones en el Apéndice A. |

#### Fronteras de Función

Tené cuidado de que usar una IIFE para definir un scope puede tener algunas consecuencias no intencionadas, dependiendo del código a su alrededor. Debido a que una IIFE es una función completa, la frontera de la función altera el comportamiento de ciertas sentencias/constructos.

Por ejemplo, una sentencia `return` en alguna porción de código cambiaría su significado si se envuelve una IIFE a su alrededor, porque ahora el `return` se referiría a la función de la IIFE. Las IIFE con funciones no-flecha también cambian el binding de la palabra clave `this`—más sobre eso en el libro *Objects & Classes*. Y sentencias como `break` y `continue` no operarán a través de la frontera de función de una IIFE para controlar un bucle o bloque externo.

Así que, si el código alrededor del cual necesitás envolver un scope tiene `return`, `this`, `break` o `continue`, una IIFE probablemente no sea el mejor enfoque. En ese caso, podrías considerar crear el scope con un bloque en lugar de una función.

## Scoping con Bloques

A esta altura deberías sentirte bastante cómodo con los méritos de crear scopes para limitar la exposición de identificadores.

Hasta ahora, vimos cómo hacer esto a través del scope de `function` (es decir, IIFE). Pero consideremos ahora usar declaraciones `let` con bloques anidados. En general, cualquier par de llaves `{ .. }` que sea una sentencia actuará como un bloque, pero **no necesariamente** como un scope.

Un bloque solo se convierte en scope si es necesario, para contener sus declaraciones de block scope (es decir, `let` o `const`). Considerá:

```js
{
    // no necesariamente un scope (todavía)

    // ..

    // ahora sabemos que el bloque necesita ser un scope
    let thisIsNowAScope = true;

    for (let i = 0; i < 5; i++) {
        // esto también es un scope, activado en cada
        // iteración
        if (i % 2 == 0) {
            // esto es solo un bloque, no un scope
            console.log(i);
        }
    }
}
// 0 2 4
```

No todos los pares de llaves `{ .. }` crean bloques (y por lo tanto son elegibles para convertirse en scopes):

* Los literales de objeto usan pares de llaves `{ .. }` para delimitar sus listas de clave-valor, pero tales valores de objeto **no** son scopes.

* `class` usa llaves `{ .. }` alrededor de la definición de su cuerpo, pero esto no es un bloque ni un scope.

* Una `function` usa `{ .. }` alrededor de su cuerpo, pero esto no es técnicamente un bloque—es una sola sentencia para el cuerpo de la función. Sin embargo, *sí es* un scope (de función).

* El par de llaves `{ .. }` de una sentencia `switch` (alrededor del conjunto de cláusulas `case`) no define un bloque/scope.

Fuera de tales ejemplos de no-bloque, un par de llaves `{ .. }` puede definir un bloque adjunto a una sentencia (como un `if` o `for`), o estar por sí mismo de manera independiente—mirá el par de llaves `{ .. }` más externo en el fragmento anterior. Un bloque explícito de este tipo—si no tiene declaraciones, en realidad no es un scope—no cumple ningún propósito operativo, aunque todavía puede ser útil como señal semántica.

Los bloques `{ .. }` independientes explícitos siempre han sido sintaxis JS válida, pero dado que no podían ser un scope antes de `let`/`const` de ES6, son bastante raros. Sin embargo, después de ES6, están empezando a popularizarse un poco.

En la mayoría de los lenguajes que soportan block scoping, un block scope explícito es un patrón extremadamente común para crear una porción estrecha de scope para una o unas pocas variables. Así que siguiendo el principio POLE, deberíamos adoptar este patrón de manera más generalizada también en JS; usá block scoping (explícito) para reducir la exposición de identificadores al mínimo práctico.

Un block scope explícito puede ser útil incluso dentro de otro bloque (sea que el bloque externo sea un scope o no).

Por ejemplo:

```js
if (somethingHappened) {
    // esto es un bloque, pero no un scope

    {
        // esto es tanto un bloque como un
        // scope explícito
        let msg = somethingHappened.message();
        notifyOthers(msg);
    }

    // ..

    recoverFromSomething();
}
```

Aquí, el par de llaves `{ .. }` **dentro** de la sentencia `if` es un block scope explícito interno aún más pequeño para `msg`, dado que esa variable no se necesita para todo el bloque `if`. La mayoría de los desarrolladores simplemente pondrían `msg` en block scope del bloque `if` y seguirían adelante. Y para ser justos, cuando hay solo unas pocas líneas a considerar, es una decisión de criterio discutible. Pero a medida que el código crece, estos problemas de sobreexposición se vuelven más pronunciados.

¿Entonces importa lo suficiente como para agregar el par `{ .. }` extra y el nivel de indentación? Creo que deberías seguir POLE y siempre (¡dentro de lo razonable!) definir el bloque más pequeño para cada variable. Así que recomiendo usar el block scope explícito extra como se muestra.

Recordá la discusión de los errores de TDZ de "Variables No Inicializadas (TDZ)" (Capítulo 5). Mi sugerencia allí fue: para minimizar el riesgo de errores de TDZ con declaraciones `let`/`const`, siempre colocá esas declaraciones al tope de su scope.

Si te encontrás colocando una declaración `let` en el medio de un scope, primero pensá: "¡Oh, no! ¡Alerta de TDZ!" Si esta declaración `let` no se necesita en la primera mitad de ese bloque, ¡deberías usar un block scope explícito interno para reducir aún más su exposición!

Otro ejemplo con un block scope explícito:

```js
function getNextMonthStart(dateStr) {
    var nextMonth, year;

    {
        let curMonth;
        [ , year, curMonth ] = dateStr.match(
                /(\d{4})-(\d{2})-\d{2}/
            ) || [];
        nextMonth = (Number(curMonth) % 12) + 1;
    }

    if (nextMonth == 1) {
        year++;
    }

    return `${ year }-${
            String(nextMonth).padStart(2,"0")
        }-01`;
}
getNextMonthStart("2019-12-25");   // 2020-01-01
```

Primero identifiquemos los scopes y sus identificadores:

1. El scope externo/global tiene un identificador, la función `getNextMonthStart(..)`.

2. El scope de función de `getNextMonthStart(..)` tiene tres: `dateStr` (parámetro), `nextMonth` y `year`.

3. El par de llaves `{ .. }` define un block scope interno que incluye una variable: `curMonth`.

¿Entonces por qué poner `curMonth` en un block scope explícito en lugar de simplemente junto a `nextMonth` y `year` en el scope de función de nivel superior? Porque `curMonth` solo se necesita para esas dos primeras sentencias; a nivel del scope de función está sobreexpuesta.

Este ejemplo es pequeño, así que los peligros de sobreexponer `curMonth` son bastante limitados. Pero los beneficios del principio POLE se logran mejor cuando adoptás la mentalidad de minimizar la exposición del scope por defecto, como un hábito. Si seguís el principio consistentemente incluso en los casos pequeños, te servirá más a medida que tus programas crezcan.

Veamos ahora un ejemplo aún más sustancial:

```js
function sortNamesByLength(names) {
    var buckets = [];

    for (let firstName of names) {
        if (buckets[firstName.length] == null) {
            buckets[firstName.length] = [];
        }
        buckets[firstName.length].push(firstName);
    }

    // un bloque para estrechar el scope
    {
        let sortedNames = [];

        for (let bucket of buckets) {
            if (bucket) {
                // ordena cada bucket alfanuméricamente
                bucket.sort();

                // anexa los nombres ordenados a nuestra
                // lista acumulada
                sortedNames = [
                    ...sortedNames,
                    ...bucket
                ];
            }
        }

        return sortedNames;
    }
}

sortNamesByLength([
    "Sally",
    "Suzy",
    "Frank",
    "John",
    "Jennifer",
    "Scott"
]);
// [ "John", "Suzy", "Frank", "Sally",
//   "Scott", "Jennifer" ]
```

Hay seis identificadores declarados a lo largo de cinco scopes diferentes. ¿Podrían haber existido todas estas variables en el único scope externo/global? Técnicamente, sí, dado que todas tienen nombres únicos y por lo tanto no tienen colisiones de nombres. Pero esto sería una organización de código realmente pobre, y probablemente llevaría tanto a confusión como a bugs futuros.

Las separamos en cada scope anidado interno según corresponda. Cada variable se define en el scope más interno posible para que el programa opere como se desea.

`sortedNames` podría haberse definido en el scope de función de nivel superior, pero solo se necesita para la segunda mitad de esta función. Para evitar sobreexponer esa variable en un scope de nivel más alto, seguimos nuevamente POLE y la ponemos en block scope dentro del block scope explícito interno.

### `var` *y* `let`

A continuación, hablemos de la declaración `var buckets`. Esa variable se usa a lo largo de toda la función (excepto la sentencia `return` final). Cualquier variable que se necesite a lo largo de toda (o incluso la mayor parte de) una función debería declararse de modo que tal uso sea obvio.

| NOTA: |
| :--- |
| El parámetro `names` no se usa a lo largo de toda la función, pero no hay forma de limitar el scope de un parámetro, así que se comporta como una declaración de alcance de función de todos modos. |

¿Entonces por qué usamos `var` en lugar de `let` para declarar la variable `buckets`? Hay razones tanto semánticas como técnicas para elegir `var` aquí.

Estilísticamente, `var` siempre, desde los primeros días de JS, ha señalado "variable que pertenece a toda una función". Como afirmamos en "Scope Léxico" (Capítulo 1), `var` se adjunta al scope de función envolvente más cercano, sin importar dónde aparezca. Eso es cierto incluso si `var` aparece dentro de un bloque:

```js
function diff(x,y) {
    if (x > y) {
        var tmp = x;    // `tmp` tiene scope de función
        x = y;
        y = tmp;
    }

    return y - x;
}
```

Aunque `var` está dentro de un bloque, su declaración tiene scope de función (de `diff(..)`), no block scope.

Si bien podés declarar `var` dentro de un bloque (y que aún tenga scope de función), yo recomendaría evitar este enfoque excepto en unos pocos casos específicos (discutidos en el Apéndice A). De otro modo, `var` debería reservarse para su uso en el scope de nivel superior de una función.

¿Por qué no simplemente usar `let` en esa misma ubicación? Porque `var` es visualmente distinto de `let` y por lo tanto señala claramente: "esta variable tiene scope de función". Usar `let` en el scope de nivel superior, especialmente si no está en las primeras líneas de una función, y cuando todas las demás declaraciones en bloques usan `let`, no atrae visualmente la atención a la diferencia con la declaración de scope de función.

En otras palabras, siento que `var` comunica mejor el scope de función que `let`, y `let` tanto comunica (¡como logra!) el block scope donde `var` es insuficiente. Mientras tus programas vayan a necesitar tanto variables con scope de función como con block scope, el enfoque más sensato y legible es usar tanto `var` *como* `let` juntos, cada uno para su mejor propósito.

Hay otras razones semánticas y operativas para elegir `var` o `let` en diferentes escenarios. Exploraremos el caso de `var` *y* `let` en más detalle en el Apéndice A.

| ADVERTENCIA: |
| :--- |
| Mi recomendación de usar tanto `var` *como* `let` es claramente controvertida y contradice a la mayoría. Es mucho más común escuchar afirmaciones como "var está roto, let lo arregla" y "nunca uses var, let es el reemplazo". Esas opiniones son válidas, pero son meramente opiniones, igual que la mía. `var` no está fácticamente roto ni deprecado; ha funcionado desde los primeros JS y seguirá funcionando mientras JS exista. |

### ¿Dónde Usar `let`?

Mi consejo de reservar `var` para (mayormente) solo un scope de función de nivel superior significa que la mayoría de las demás declaraciones deberían usar `let`. Pero quizás todavía te estés preguntando cómo decidir dónde pertenece cada declaración en tu programa.

POLE ya te guía en esas decisiones, pero asegurémonos de enunciarlo explícitamente. La forma de decidir no se basa en qué palabra clave querés usar. La forma de decidir es preguntar: "¿Cuál es la exposición de scope más mínima que sea suficiente para esta variable?"

Una vez que eso esté respondido, sabrás si una variable pertenece a un block scope o al scope de función. Si decidís inicialmente que una variable debería tener block scope, y más tarde te das cuenta de que necesita elevarse a scope de función, entonces eso dicta un cambio no solo en la ubicación de la declaración de esa variable, sino también en la palabra clave declaradora utilizada. El proceso de toma de decisiones realmente debería proceder así.

Si una declaración pertenece a un block scope, usá `let`. Si pertenece al scope de función, usá `var` (de nuevo, solo mi opinión).

Pero otra forma de visualizar esta toma de decisiones es considerar la versión pre-ES6 de un programa. Por ejemplo, recordemos `diff(..)` de antes:

```js
function diff(x,y) {
    var tmp;

    if (x > y) {
        tmp = x;
        x = y;
        y = tmp;
    }

    return y - x;
}
```

En esta versión de `diff(..)`, `tmp` está claramente declarada en el scope de función. ¿Es eso apropiado para `tmp`? Yo argumentaría que no. `tmp` solo se necesita para esas pocas sentencias. No se necesita para la sentencia `return`. Por lo tanto debería tener block scope.

Antes de ES6, no teníamos `let` así que no podíamos *realmente* darle block scope. Pero podíamos hacer lo siguiente mejor para señalar nuestra intención:

```js
function diff(x,y) {
    if (x > y) {
        // `tmp` todavía tiene scope de función, pero
        // la colocación aquí señala semánticamente
        // block scope
        var tmp = x;
        x = y;
        y = tmp;
    }

    return y - x;
}
```

Colocar la declaración `var` para `tmp` dentro de la sentencia `if` le señala al lector del código que `tmp` pertenece a ese bloque. Aunque JS no fuerza ese scoping, la señal semántica todavía tiene beneficio para el lector de tu código.

Siguiendo esta perspectiva, podés encontrar cualquier `var` que esté dentro de un bloque de este tipo y cambiarlo a `let` para forzar la señal semántica que ya se está enviando. Ese es el uso adecuado de `let` en mi opinión.

Otro ejemplo que históricamente se basaba en `var` pero que ahora debería prácticamente siempre usar `let` es el bucle `for`:

```js
for (var i = 0; i < 5; i++) {
    // haz algo
}
```

Sin importar dónde se defina tal bucle, la `i` básicamente siempre debería usarse solo dentro del bucle, en cuyo caso POLE dicta que debería declararse con `let` en lugar de `var`:

```js
for (let i = 0; i < 5; i++) {
    // haz algo
}
```

Casi el único caso en el que cambiar un `var` a un `let` de esta manera "rompería" tu código es si estuvieras dependiendo de acceder al iterador del bucle (`i`) fuera/después del bucle, como:

```js
for (var i = 0; i < 5; i++) {
    if (checkValue(i)) {
        break;
    }
}

if (i < 5) {
    console.log("The loop stopped early!");
}
```

Este patrón de uso no es terriblemente poco común, pero la mayoría siente que huele a una mala estructura de código. Un enfoque preferible es usar otra variable de scope externo para ese propósito:

```js
var lastI;

for (let i = 0; i < 5; i++) {
    lastI = i;
    if (checkValue(i)) {
        break;
    }
}

if (lastI < 5) {
    console.log("The loop stopped early!");
}
```

`lastI` se necesita a lo largo de todo este scope, así que se declara con `var`. `i` solo se necesita en (cada) iteración del bucle, así que se declara con `let`.

### ¿Cuál es el Truco?

Hasta ahora hemos afirmado que `var` y los parámetros tienen scope de función, y que `let`/`const` señalan declaraciones de block scope. Hay una pequeña excepción para destacar: la cláusula `catch`.

Desde la introducción de `try..catch` allá por ES3 (en 1999), la cláusula `catch` ha usado una capacidad adicional (poco conocida) de declaración con block scope:

```js
try {
    doesntExist();
}
catch (err) {
    console.log(err);
    // ReferenceError: 'doesntExist' is not defined
    // ^^^^ mensaje impreso de la excepción capturada

    let onlyHere = true;
    var outerVariable = true;
}

console.log(outerVariable);     // true

console.log(err);
// ReferenceError: 'err' is not defined
// ^^^^ esta es otra excepción lanzada (no capturada)
```

La variable `err` declarada por la cláusula `catch` tiene block scope de ese bloque. Este bloque de la cláusula `catch` puede contener otras declaraciones de block scope mediante `let`. Pero una declaración `var` dentro de este bloque todavía se adjunta al scope externo de función/global.

ES2019 (recientemente, al momento de escribir) cambió las cláusulas `catch` para que su declaración sea opcional; si la declaración se omite, el bloque `catch` ya no es (por defecto) un scope; ¡igual sigue siendo un bloque!

Así que si necesitás reaccionar a la condición *de que ocurrió una excepción* (para poder recuperarte con gracia), pero no te importa el valor del error en sí, podés omitir la declaración del `catch`:

```js
try {
    doOptionOne();
}
catch {   // declaración de catch omitida
    doOptionTwoInstead();
}
```

Esta es una simplificación pequeña pero encantadora de la sintaxis para un caso de uso bastante común, ¡y también puede ser ligeramente más performante al eliminar un scope innecesario!

## Declaraciones de Función en Bloques (FiB)

Ya hemos visto que las declaraciones que usan `let` o `const` tienen block scope, y que las declaraciones `var` tienen scope de función. ¿Entonces qué pasa con las declaraciones de `function` que aparecen directamente dentro de bloques? Como característica, esto se llama "FiB".

Típicamente pensamos en las declaraciones de `function` como si fueran el equivalente de una declaración `var`. ¿Entonces tienen scope de función como lo tiene `var`?

No y sí. Lo sé... eso es confuso. Profundicemos:

```js
if (false) {
    function ask() {
        console.log("Does this run?");
    }
}
ask();
```

¿Qué esperás que haga este programa? Tres resultados razonables:

1. La llamada `ask()` podría fallar con una excepción `ReferenceError`, porque el identificador `ask` tiene block scope del scope del bloque `if` y por lo tanto no está disponible en el scope externo/global.

2. La llamada `ask()` podría fallar con una excepción `TypeError`, porque el identificador `ask` existe, pero es `undefined` (dado que la sentencia `if` no se ejecuta) y por lo tanto no es una función invocable.

3. La llamada `ask()` podría ejecutarse correctamente, imprimiendo el mensaje "Does it run?".

Aquí está la parte confusa: ¡dependiendo del entorno JS en el que pruebes ese fragmento de código, podés obtener resultados diferentes! Esta es una de esas pocas áreas locas donde el comportamiento heredado existente traiciona un resultado predecible.

La especificación de JS dice que las declaraciones de `function` dentro de bloques tienen block scope, así que la respuesta debería ser la (1). Sin embargo, la mayoría de los engines de JS basados en navegador (incluyendo v8, que viene de Chrome pero también se usa en Node) se comportarán como la (2), lo que significa que el identificador tiene scope fuera del bloque `if` pero el valor de la función no se inicializa automáticamente, así que permanece `undefined`.

¿Por qué se les permite a los engines de JS de navegador comportarse de manera contraria a la especificación? Porque estos engines ya tenían ciertos comportamientos en torno a FiB antes de que ES6 introdujera el block scoping, y había preocupación de que cambiar para adherir a la especificación pudiera romper algún código JS existente de sitios web. Como tal, se hizo una excepción en el Apéndice B de la especificación de JS, que permite ciertas desviaciones para los engines de JS de navegador (¡solo!).

| NOTA: |
| :--- |
| Típicamente no categorizarías a Node como un entorno JS de navegador, dado que usualmente corre en un servidor. Pero el engine v8 de Node es compartido con los navegadores Chrome (y Edge). Dado que v8 es primero un engine de JS de navegador, adopta esta excepción del Apéndice B, lo que entonces significa que las excepciones de navegador se extienden a Node. |

Uno de los casos de uso más comunes para colocar una declaración de `function` en un bloque es definir condicionalmente una función de una manera u otra (como con una sentencia `if..else`) dependiendo de algún estado del entorno. Por ejemplo:

```js
if (typeof Array.isArray != "undefined") {
    function isArray(a) {
        return Array.isArray(a);
    }
}
else {
    function isArray(a) {
        return Object.prototype.toString.call(a)
            == "[object Array]";
    }
}
```

Es tentador estructurar el código de esta manera por razones de rendimiento, dado que la verificación `typeof Array.isArray` solo se realiza una vez, en contraposición a definir una sola `isArray(..)` y poner la sentencia `if` dentro de ella—la verificación entonces se ejecutaría innecesariamente en cada llamada.

| ADVERTENCIA: |
| :--- |
| Además de los riesgos de las desviaciones de FiB, otro problema con la definición condicional de funciones es que es más difícil depurar tal programa. Si terminás con un bug en la función `isArray(..)`, primero tenés que averiguar *cuál* implementación de `isArray(..)` está realmente corriendo. ¡A veces, el bug es que se aplicó la equivocada porque la verificación condicional era incorrecta! Si definís múltiples versiones de una función, ese programa siempre es más difícil de razonar y mantener. |

Además de los fragmentos anteriores, varios otros casos límite de FiB están al acecho; tales comportamientos en varios navegadores y entornos JS que no son de navegador (engines de JS que no están basados en navegador) probablemente varíen. Por ejemplo:

```js
if (true) {
    function ask() {
        console.log("Am I called?");
    }
}

if (true) {
    function ask() {
        console.log("Or what about me?");
    }
}

for (let i = 0; i < 5; i++) {
    function ask() {
        console.log("Or is it one of these?");
    }
}

ask();

function ask() {
    console.log("Wait, maybe, it's this one?");
}
```

Recordá que el hoisting de funciones, como se describió en "¿Cuándo Puedo Usar una Variable?" (en el Capítulo 5), podría sugerir que la última `ask()` de este fragmento, con "Wait, maybe..." como su mensaje, se elevaría (hoist) por encima de la llamada a `ask()`. Dado que es la última declaración de función con ese nombre, debería "ganar", ¿no? Lamentablemente, no.

No es mi intención documentar todos estos casos límite raros, ni intentar explicar por qué cada uno de ellos se comporta de cierta manera. Esa información es, en mi opinión, trivia heredada y arcana.

Mi verdadera preocupación con FiB es: ¿qué consejo puedo dar para asegurar que tu código se comporte de manera predecible en todas las circunstancias?

En lo que a mí respecta, la única respuesta práctica para evitar las veleidades de FiB es simplemente evitar FiB por completo. En otras palabras, nunca coloques una declaración de `function` directamente dentro de ningún bloque. Siempre colocá las declaraciones de `function` en cualquier lugar del scope de nivel superior de una función (o en el scope global).

Así que para el ejemplo anterior de `if..else`, mi sugerencia es evitar definir funciones condicionalmente si es posible. Sí, puede ser ligeramente menos performante, pero este es el mejor enfoque en general:

```js
function isArray(a) {
    if (typeof Array.isArray != "undefined") {
        return Array.isArray(a);
    }
    else {
        return Object.prototype.toString.call(a)
            == "[object Array]";
    }
}
```

Si ese impacto en el rendimiento se vuelve un problema de ruta crítica para tu aplicación, te sugiero que consideres este enfoque:

```js
var isArray = function isArray(a) {
    return Array.isArray(a);
};

// anula la definición, si debés
if (typeof Array.isArray == "undefined") {
    isArray = function isArray(a) {
        return Object.prototype.toString.call(a)
            == "[object Array]";
    };
}
```

Es importante notar que aquí estoy colocando una **expresión** de `function`, no una declaración, dentro de la sentencia `if`. Eso está perfectamente bien y es válido, que las expresiones de `function` aparezcan dentro de bloques. Nuestra discusión sobre FiB trata de evitar las **declaraciones** de `function` en bloques.

Incluso si probás tu programa y funciona correctamente, el pequeño beneficio que podrías derivar de usar el estilo FiB en tu código es ampliamente superado por los riesgos potenciales en el futuro de confusión por parte de otros desarrolladores, o variaciones en cómo corre tu código en otros entornos JS.

FiB no vale la pena, y debería evitarse.

## Bloqueado y Superado

El punto de las reglas de scoping léxico en un lenguaje de programación es para que podamos organizar apropiadamente las variables de nuestro programa, tanto para propósitos operativos como de comunicación semántica del código.

Y una de las técnicas organizativas más importantes es asegurar que ninguna variable quede sobreexpuesta a scopes innecesarios (POLE). Con suerte ahora apreciás el block scoping mucho más profundamente que antes.

Con suerte, a esta altura sentís que estás parado sobre un terreno mucho más sólido en cuanto a la comprensión del scope léxico. Desde esa base, el próximo capítulo salta al pesado tema del closure.

[^POLP]: *Principle of Least Privilege*, https://en.wikipedia.org/wiki/Principle_of_least_privilege, 3 de marzo de 2020.
