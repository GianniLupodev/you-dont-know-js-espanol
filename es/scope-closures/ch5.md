# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Capítulo 5: El (No Tan) Secreto Ciclo de Vida de las Variables

A esta altura ya deberías tener una comprensión decente del anidamiento de scopes, desde el global scope hacia abajo—lo que se denomina la cadena de scopes de un programa.

Pero conocer de qué scope proviene una variable es solo parte de la historia. Si la declaración de una variable aparece después del primer statement de un scope, ¿cómo se comportará cualquier referencia a ese identificador *antes* de la declaración? ¿Qué pasa si intentás declarar la misma variable dos veces en un scope?

El particular sabor de lexical scope de JS está lleno de matices sobre cómo y cuándo las variables cobran existencia y quedan disponibles para el programa.

## ¿Cuándo Puedo Usar una Variable?

¿En qué punto una variable queda disponible para usarse dentro de su scope? Podría parecer que hay una respuesta obvia: *después* de que la variable haya sido declarada/creada. ¿No? No del todo.

Considerá:

```js
greeting();
// Hello!

function greeting() {
    console.log("Hello!");
}
```

Este código funciona perfecto. Quizás viste o incluso escribiste código como este antes. Pero, ¿alguna vez te preguntaste cómo o por qué funciona? Específicamente, ¿por qué podés acceder al identificador `greeting` desde la línea 1 (para recuperar y ejecutar una referencia a función), aun cuando la declaración de la función `greeting()` no ocurre hasta la línea 4?

Recordá que el Capítulo 1 señala que todos los identificadores se registran en sus respectivos scopes durante el compile time. Es más, cada identificador se *crea* al comienzo del scope al que pertenece, **cada vez que se ingresa a ese scope**.

El término usado con mayor frecuencia para referirse a que una variable sea visible desde el comienzo de su scope contenedor, aun cuando su declaración pueda aparecer más abajo en el scope, se denomina **hoisting**.

Pero el hoisting por sí solo no responde del todo la pregunta. Podemos ver un identificador llamado `greeting` desde el comienzo del scope, pero ¿por qué podemos **invocar** la función `greeting()` antes de que haya sido declarada?

En otras palabras, ¿cómo es que la variable `greeting` tiene algún valor (la referencia a la función) asignado, desde el momento en que el scope empieza a ejecutarse? La respuesta es una característica especial de las declaraciones formales con `function`, llamada *function hoisting*. Cuando el identificador del nombre de una declaración `function` se registra en la parte superior de su scope, además se auto-inicializa con la referencia a esa función. ¡Por eso la función puede invocarse a lo largo de todo el scope!

Un detalle clave es que tanto el *function hoisting* como el *variable hoisting* al estilo de `var` adjuntan sus identificadores de nombre al **function scope** contenedor más cercano (o, si no hay ninguno, al global scope), no a un block scope.

| NOTA: |
| :--- |
| Las declaraciones con `let` y `const` igualmente hacen hoisting (ver la discusión sobre la TDZ más adelante en este capítulo). Pero estas dos formas de declaración se adjuntan a su bloque contenedor en vez de simplemente a una función contenedora, como ocurre con las declaraciones `var` y `function`. Ver "Scoping con Bloques" en el Capítulo 6 para más información. |

### Hoisting: Declaración vs. Expresión

El *function hoisting* solo aplica a las declaraciones formales con `function` (específicamente aquellas que aparecen fuera de bloques—ver "FiB" en el Capítulo 6), no a las asignaciones de function expression. Considerá:

```js
greeting();
// TypeError

var greeting = function greeting() {
    console.log("Hello!");
};
```

La línea 1 (`greeting();`) lanza un error. Pero el *tipo* de error que se lanza es muy importante de notar. Un `TypeError` significa que estamos intentando hacer algo con un valor que no está permitido. Dependiendo de tu entorno de JS, el mensaje de error diría algo como "'undefined' is not a function", o de forma más útil, "'greeting' is not a function".

Fijate que el error **no** es un `ReferenceError`. JS no nos está diciendo que no pudo encontrar `greeting` como identificador en el scope. Nos está diciendo que `greeting` fue encontrado pero no contiene una referencia a función en ese momento. Solo las funciones pueden invocarse, así que intentar invocar algún valor que no es una función resulta en un error.

Pero, ¿qué contiene `greeting`, si no la referencia a la función?

Además de hacer hoisting, las variables declaradas con `var` también se inicializan automáticamente a `undefined` al comienzo de su scope—de nuevo, la función contenedora más cercana, o el global. Una vez inicializadas, quedan disponibles para usarse (asignarles, recuperar de ellas, etc.) a lo largo de todo el scope.

Así que en esa primera línea, `greeting` existe, pero solo contiene el valor por defecto `undefined`. Recién en la línea 4 `greeting` recibe la asignación de la referencia a la función.

Prestá mucha atención a la distinción acá. Una declaración `function` hace hoisting **y se inicializa con su valor de función** (de nuevo, lo que se llama *function hoisting*). Una variable `var` también hace hoisting, y luego se auto-inicializa a `undefined`. Cualquier asignación posterior de function expression a esa variable no ocurre hasta que esa asignación se procesa durante la ejecución en runtime.

En ambos casos, el nombre del identificador hace hoisting. Pero la asociación con la referencia a la función no se maneja en el momento de la inicialización (comienzo del scope) a menos que el identificador haya sido creado en una declaración formal con `function`.

### Variable Hoisting

Veamos otro ejemplo de *variable hoisting*:

```js
greeting = "Hello!";
console.log(greeting);
// Hello!

var greeting = "Howdy!";
```

Aunque `greeting` no se declara hasta la línea 5, está disponible para asignarle tan temprano como en la línea 1. ¿Por qué?

Hay dos partes necesarias en la explicación:

* el identificador hace hoisting,
* **y** se inicializa automáticamente con el valor `undefined` desde la parte superior del scope.

| NOTA: |
| :--- |
| Usar *variable hoisting* de este tipo probablemente se sienta poco natural, y muchos lectores podrían querer, con razón, evitar depender de esto en sus programas. Pero, ¿debería evitarse todo hoisting (incluido el *function hoisting*)? Exploraremos estas distintas perspectivas sobre el hoisting en más detalle en el Apéndice A. |

## Hoisting: Otra Metáfora Más

El Capítulo 2 estuvo repleto de metáforas (para ilustrar el scope), pero acá nos enfrentamos a otra más: el hoisting mismo. En lugar de que el hoisting sea un paso concreto de ejecución que el engine de JS realiza, es más útil pensar el hoisting como una visualización de varias acciones que JS toma al armar el programa **antes de la ejecución**.

La afirmación típica de lo que significa hoisting: *elevar*—como elevar un peso pesado hacia arriba—cualquier identificador hasta la parte superior de un scope. La explicación que suele afirmarse es que el engine de JS en realidad *reescribirá* ese programa antes de la ejecución, de modo que se vea más así:

```js
var greeting;           // hoisted declaration
greeting = "Hello!";    // the original line 1
console.log(greeting);  // Hello!
greeting = "Howdy!";    // `var` is gone!
```

El hoisting (metáfora) propone que JS pre-procesa el programa original y lo re-ordena un poco, de modo que todas las declaraciones hayan sido movidas a la parte superior de sus respectivos scopes, antes de la ejecución. Es más, la metáfora del hoisting afirma que las declaraciones `function` son, en su totalidad, elevadas a la parte superior de cada scope. Considerá:

```js
studentName = "Suzy";
greeting();
// Hello Suzy!

function greeting() {
    console.log(`Hello ${ studentName }!`);
}
var studentName;
```

La "regla" de la metáfora del hoisting es que las declaraciones de función se elevan primero, y luego las variables se elevan inmediatamente después de todas las funciones. Así, la historia del hoisting sugiere que ese programa es *re-ordenado* por el engine de JS para verse así:

```js
function greeting() {
    console.log(`Hello ${ studentName }!`);
}
var studentName;

studentName = "Suzy";
greeting();
// Hello Suzy!
```

Esta metáfora del hoisting es conveniente. Su beneficio es permitirnos pasar por alto el mágico pre-procesamiento de mirar hacia adelante que es necesario para encontrar todas estas declaraciones enterradas en lo profundo de los scopes y de algún modo moverlas (elevarlas) a la parte superior; podemos simplemente pensar en el programa como si fuera ejecutado por el engine de JS en una **única pasada**, de arriba hacia abajo.

Una única pasada definitivamente parece más directo que la afirmación del Capítulo 1 de un procesamiento en dos fases.

El hoisting como mecanismo para re-ordenar código puede ser una simplificación atractiva, pero no es precisa. El engine de JS en realidad no re-ordena el código. No puede mirar hacia adelante mágicamente y encontrar las declaraciones; la única manera de encontrarlas con precisión, así como todos los límites de scope en el programa, sería parsear completamente el código.

¿Adiviná qué es el parsing? ¡La primera fase del procesamiento en dos fases! No hay gimnasia mental mágica que esquive ese hecho.

Entonces, si la metáfora del hoisting es (en el mejor de los casos) imprecisa, ¿qué deberíamos hacer con el término? Creo que todavía es útil—es más, ¡incluso miembros de TC39 lo usan regularmente!—pero no creo que debamos afirmar que es un re-ordenamiento real del código fuente.

| ADVERTENCIA: |
| :--- |
| Los modelos mentales incorrectos o incompletos muchas veces igual parecen suficientes porque de vez en cuando pueden llevar a respuestas correctas por accidente. Pero a la larga es más difícil analizar y predecir resultados con precisión si tu forma de pensar no está particularmente alineada con cómo funciona el engine de JS. |

Yo sostengo que el hoisting *debería* usarse para referirse a la **operación en compile-time** de generar instrucciones de runtime para el registro automático de una variable al comienzo de su scope, cada vez que se ingresa a ese scope.

Ese es un cambio sutil pero importante, desde el hoisting como un comportamiento de runtime hacia su lugar apropiado entre las tareas de compile-time.

## ¿Re-declaración?

¿Qué pensás que pasa cuando una variable se declara más de una vez en el mismo scope? Considerá:

```js
var studentName = "Frank";
console.log(studentName);
// Frank

var studentName;
console.log(studentName);   // ???
```

¿Qué esperás que se imprima en ese segundo mensaje? Muchos creen que el segundo `var studentName` ha re-declarado la variable (y por lo tanto la "reseteó"), así que esperan que se imprima `undefined`.

Pero, ¿existe tal cosa como una variable siendo "re-declarada" en el mismo scope? No.

Si considerás este programa desde la perspectiva de la metáfora del hoisting, el código sería re-ordenado así para propósitos de ejecución:

```js
var studentName;
var studentName;    // clearly a pointless no-op!

studentName = "Frank";
console.log(studentName);
// Frank

console.log(studentName);
// Frank
```

Dado que el hoisting en realidad se trata de registrar una variable al comienzo de un scope, no hay nada que hacer en medio del scope donde el programa original realmente tenía el segundo statement `var studentName`. Es simplemente un no-op(eración), un statement sin sentido.

| TIP: |
| :--- |
| Al estilo de la narrativa de conversación del Capítulo 2, el *Compilador* encontraría el segundo statement de declaración `var` y le preguntaría al *Administrador de Scope* si ya había visto un identificador `studentName`; como sí lo había visto, no habría nada más que hacer. |

También es importante señalar que `var studentName;` no significa `var studentName = undefined;`, como la mayoría asume. Probemos que son diferentes considerando esta variación del programa:

```js
var studentName = "Frank";
console.log(studentName);   // Frank

var studentName;
console.log(studentName);   // Frank <--- still!

// let's add the initialization explicitly
var studentName = undefined;
console.log(studentName);   // undefined <--- see!?
```

¿Ves cómo la inicialización explícita `= undefined` produce un resultado diferente que asumir que ocurre implícitamente cuando se omite? En la próxima sección, revisitaremos este tema de la inicialización de variables a partir de sus declaraciones.

Una declaración `var` repetida del mismo nombre de identificador en un scope es, en efecto, una operación que no hace nada. Acá hay otra ilustración, esta vez a lo largo de una función del mismo nombre:

```js
var greeting;

function greeting() {
    console.log("Hello!");
}

// basically, a no-op
var greeting;

typeof greeting;        // "function"

var greeting = "Hello!";

typeof greeting;        // "string"
```

La primera declaración `greeting` registra el identificador en el scope, y como es un `var` la auto-inicialización será `undefined`. La declaración `function` no necesita re-registrar el identificador, pero debido al *function hoisting* sobrescribe la auto-inicialización para usar la referencia a la función. El segundo `var greeting` por sí solo no hace nada, ya que `greeting` ya es un identificador y el *function hoisting* ya tuvo precedencia para la auto-inicialización.

Realmente asignar `"Hello!"` a `greeting` cambia su valor de la función inicial `greeting()` al string; `var` en sí mismo no tiene ningún efecto.

¿Y qué pasa con repetir una declaración dentro de un scope usando `let` o `const`?

```js
let studentName = "Frank";

console.log(studentName);

let studentName = "Suzy";
```

Este programa no va a ejecutarse, sino que lanzará de inmediato un `SyntaxError`. Dependiendo de tu entorno de JS, el mensaje de error indicará algo como: "studentName has already been declared". En otras palabras, ¡este es un caso en el que el intento de "re-declaración" no está permitido explícitamente!

No es solo que dos declaraciones que involucran `let` lanzarán este error. Si cualquiera de las declaraciones usa `let`, la otra puede ser `let` o `var`, y el error igualmente ocurrirá, como se ilustra con estas dos variaciones:

```js
var studentName = "Frank";

let studentName = "Suzy";
```

y:

```js
let studentName = "Frank";

var studentName = "Suzy";
```

En ambos casos, se lanza un `SyntaxError` en la *segunda* declaración. En otras palabras, la única manera de "re-declarar" una variable es usar `var` para todas (dos o más) sus declaraciones.

Pero, ¿por qué no permitirlo? La razón del error no es técnica per se, ya que la "re-declaración" con `var` siempre ha estado permitida; claramente, la misma concesión podría haberse hecho para `let`.

En realidad es más una cuestión de "ingeniería social". La "re-declaración" de variables es vista por algunos, incluidos muchos del cuerpo de TC39, como un mal hábito que puede llevar a bugs en el programa. Así que cuando ES6 introdujo `let`, decidieron prevenir la "re-declaración" con un error.

| NOTA: |
| :--- |
| Esta es, por supuesto, una opinión estilística, no realmente un argumento técnico. Muchos desarrolladores están de acuerdo con la postura, y eso probablemente sea en parte por qué TC39 incluyó el error (además de que `let` se ajusta a `const`). Pero se podría haber hecho un caso razonable de que mantenerse consistente con el precedente de `var` era más prudente, y que tal imposición de opiniones estaba mejor dejada a herramientas de opt-in como los linters. En el Apéndice A, exploraremos si `var` (y su comportamiento asociado, como la "re-declaración") todavía puede ser útil en el JS moderno. |

Cuando el *Compilador* le pregunta al *Administrador de Scope* sobre una declaración, si ese identificador ya ha sido declarado, y si una o ambas declaraciones se hicieron con `let`, se lanza un error. La señal buscada para el desarrollador es "¡Dejá de depender de la re-declaración descuidada!".

### ¿Constantes?

La palabra clave `const` es más restringida que `let`. Al igual que `let`, `const` no puede repetirse con el mismo identificador en el mismo scope. Pero en realidad hay una razón técnica superior por la cual ese tipo de "re-declaración" está prohibida, a diferencia de `let`, que prohíbe la "re-declaración" principalmente por razones estilísticas.

La palabra clave `const` requiere que una variable sea inicializada, así que omitir una asignación en la declaración resulta en un `SyntaxError`:

```js
const empty;   // SyntaxError
```

Las declaraciones `const` crean variables que no pueden ser re-asignadas:

```js
const studentName = "Frank";
console.log(studentName);
// Frank

studentName = "Suzy";   // TypeError
```

La variable `studentName` no puede ser re-asignada porque está declarada con un `const`.

| ADVERTENCIA: |
| :--- |
| El error que se lanza al re-asignar `studentName` es un `TypeError`, no un `SyntaxError`. La distinción sutil acá es en realidad bastante importante, pero lamentablemente demasiado fácil de pasar por alto. Los errores de sintaxis representan fallas en el programa que lo detienen antes de siquiera empezar a ejecutarse. Los errores de tipo representan fallas que surgen durante la ejecución del programa. En el fragmento anterior, `"Frank"` se imprime antes de que procesemos la re-asignación de `studentName`, que luego lanza el error. |

Así que si las declaraciones `const` no pueden ser re-asignadas, y las declaraciones `const` siempre requieren asignaciones, entonces tenemos una razón técnica clara por la cual `const` debe prohibir cualquier "re-declaración": ¡cualquier "re-declaración" de `const` también sería necesariamente una re-asignación de `const`, lo cual no puede permitirse!

```js
const studentName = "Frank";

// obviously this must be an error
const studentName = "Suzy";
```

Dado que la "re-declaración" de `const` debe estar prohibida (por esos fundamentos técnicos), TC39 esencialmente sintió que la "re-declaración" de `let` debería estar prohibida también, por consistencia. Es debatible si esta fue la mejor elección, pero al menos tenemos el razonamiento detrás de la decisión.

### Loops

Entonces queda claro de nuestra discusión anterior que JS realmente no quiere que "re-declaremos" nuestras variables dentro del mismo scope. Eso probablemente parezca una advertencia directa, hasta que considerás qué significa para la ejecución repetida de statements de declaración en loops. Considerá:

```js
var keepGoing = true;
while (keepGoing) {
    let value = Math.random();
    if (value > 0.5) {
        keepGoing = false;
    }
}
```

¿Se está "re-declarando" `value` repetidamente en este programa? ¿Vamos a obtener errores? No.

Todas las reglas de scope (incluida la "re-declaración" de variables creadas con `let`) se aplican *por instancia de scope*. En otras palabras, cada vez que se ingresa a un scope durante la ejecución, todo se resetea.

Cada iteración del loop es su propia nueva instancia de scope, y dentro de cada instancia de scope, `value` solo se declara una vez. Así que no hay intento de "re-declaración", y por lo tanto no hay error. Antes de considerar otras formas de loop, ¿qué pasaría si la declaración de `value` en el fragmento anterior se cambiara a un `var`?

```js
var keepGoing = true;
while (keepGoing) {
    var value = Math.random();
    if (value > 0.5) {
        keepGoing = false;
    }
}
```

¿Se está "re-declarando" `value` acá, especialmente dado que sabemos que `var` lo permite? No. Como `var` no se trata como una declaración de block-scoping (ver Capítulo 6), se adjunta al global scope. Así que hay un solo `value`, en el mismo scope que `keepGoing` (global scope, en este caso). ¡Tampoco hay "re-declaración" acá!

Una manera de mantener todo esto en claro es recordar que las palabras clave `var`, `let` y `const` son, en efecto, *removidas* del código para cuando empieza a ejecutarse. Las maneja enteramente el compilador.

Si borrás mentalmente las palabras clave declaradoras y luego intentás procesar el código, debería ayudarte a decidir si y cuándo podrían ocurrir (re-)declaraciones.

¿Qué pasa con la "re-declaración" en otras formas de loop, como los loops `for`?

```js
for (let i = 0; i < 3; i++) {
    let value = i * 10;
    console.log(`${ i }: ${ value }`);
}
// 0: 0
// 1: 10
// 2: 20
```

Debería quedar claro que hay un solo `value` declarado por instancia de scope. Pero, ¿qué pasa con `i`? ¿Se está "re-declarando"?

Para responder eso, considerá en qué scope está `i`. Podría parecer que estaría en el scope externo (en este caso, el global), pero no es así. Está en el scope del cuerpo del loop `for`, igual que `value`. De hecho, podrías pensar en ese loop en esta forma equivalente más detallada:

```js
{
    // a fictional variable for illustration
    let $$i = 0;

    for ( /* nothing */; $$i < 3; $$i++) {
        // here's our actual loop `i`!
        let i = $$i;

        let value = i * 10;
        console.log(`${ i }: ${ value }`);
    }
    // 0: 0
    // 1: 10
    // 2: 20
}
```

Ahora debería quedar claro: las variables `i` y `value` ambas se declaran exactamente una vez **por instancia de scope**. Acá no hay "re-declaración".

¿Qué pasa con otras formas de loop `for`?

```js
for (let index in students) {
    // this is fine
}

for (let student of students) {
    // so is this
}
```

Lo mismo con los loops `for..in` y `for..of`: la variable declarada se trata como *dentro* del cuerpo del loop, y por lo tanto se maneja por iteración (o sea, por instancia de scope). Nada de "re-declaración".

OK, ya sé que estás pensando que a esta altura sueno como un disco rayado. Pero exploremos cómo `const` impacta estas construcciones de loop. Considerá:

```js
var keepGoing = true;
while (keepGoing) {
    // ooo, a shiny constant!
    const value = Math.random();
    if (value > 0.5) {
        keepGoing = false;
    }
}
```

Al igual que la variante con `let` de este programa que vimos antes, `const` se está ejecutando exactamente una vez dentro de cada iteración del loop, así que está a salvo de problemas de "re-declaración". Pero las cosas se complican más cuando hablamos de loops `for`.

`for..in` y `for..of` están bien para usar con `const`:

```js
for (const index in students) {
    // this is fine
}

for (const student of students) {
    // this is also fine
}
```

Pero no el loop `for` general:

```js
for (const i = 0; i < 3; i++) {
    // oops, this is going to fail with
    // a Type Error after the first iteration
}
```

¿Qué está mal acá? Podríamos usar `let` perfectamente en esta construcción, y afirmamos que crea un nuevo `i` para cada scope de iteración del loop, así que ni siquiera parece ser una "re-declaración".

Vamos a "expandir" mentalmente ese loop como hicimos antes:

```js
{
    // a fictional variable for illustration
    const $$i = 0;

    for ( ; $$i < 3; $$i++) {
        // here's our actual loop `i`!
        const i = $$i;
        // ..
    }
}
```

¿Detectás el problema? Nuestro `i` efectivamente se crea una sola vez dentro del loop. Ese no es el problema. El problema es el `$$i` conceptual que debe incrementarse cada vez con la expresión `$$i++`. Eso es **re-asignación** (no "re-declaración"), que no está permitida para las constantes.

Recordá, esta forma "expandida" es solo un modelo conceptual para ayudarte a intuir el origen del problema. Quizás te preguntes si JS podría haber convertido en efecto el `const $$i = 0` en `let $ii = 0`, lo que luego permitiría que `const` funcionara con nuestro clásico loop `for`. Es posible, pero entonces podría haber introducido excepciones potencialmente sorprendentes a la semántica del loop `for`.

Por ejemplo, habría sido una excepción matizada bastante arbitraria (y probablemente confusa) permitir que `i++` en el encabezado del loop `for` eludiera la estrictez de la asignación de `const`, pero no permitir otras re-asignaciones de `i` dentro de la iteración del loop, como a veces es útil.

La respuesta directa es: `const` no puede usarse con la forma clásica del loop `for` debido a la re-asignación requerida.

Curiosamente, si no hacés re-asignación, entonces es válido:

```js
var keepGoing = true;

for (const i = 0; keepGoing; /* nothing here */ ) {
    keepGoing = (Math.random() > 0.5);
    // ..
}
```

Eso funciona, pero no tiene sentido. No hay razón para declarar `i` en esa posición con un `const`, ya que todo el punto de una variable en esa posición es **usarse para contar iteraciones**. ¡Simplemente usá una forma de loop diferente, como un loop `while`, o usá un `let`!

## Variables No Inicializadas (o sea, la TDZ)

Con las declaraciones `var`, la variable hace "hoisting" a la parte superior de su scope. Pero también se inicializa automáticamente con el valor `undefined`, de modo que la variable pueda usarse a lo largo de todo el scope.

Sin embargo, las declaraciones `let` y `const` no son exactamente iguales en este aspecto.

Considerá:

```js
console.log(studentName);
// ReferenceError

let studentName = "Suzy";
```

El resultado de este programa es que se lanza un `ReferenceError` en la primera línea. Dependiendo de tu entorno de JS, el mensaje de error puede decir algo como: "Cannot access studentName before initialization".

| NOTA: |
| :--- |
| El mensaje de error como se ve acá solía ser mucho más vago o engañoso. Afortunadamente, varios de nosotros en la comunidad logramos hacer lobby con éxito para que los engines de JS mejoraran este mensaje de error, ¡de modo que te diga de forma más precisa qué está mal! |

Ese mensaje de error es bastante indicativo de qué está mal: `studentName` existe en la línea 1, pero no ha sido inicializado, así que todavía no puede usarse. Probemos esto:

```js
studentName = "Suzy";   // let's try to initialize it!
// ReferenceError

console.log(studentName);

let studentName;
```

Uy. Seguimos obteniendo el `ReferenceError`, pero ahora en la primera línea donde estamos intentando asignarle a (¡o sea, inicializar!) esta llamada variable "no inicializada" `studentName`. ¡¿Qué onda?!

La verdadera pregunta es, ¿cómo inicializamos una variable no inicializada? Para `let`/`const`, la **única manera** de hacerlo es con una asignación adjunta a un statement de declaración. ¡Una asignación por sí sola es insuficiente! Considerá:

```js
let studentName = "Suzy";
console.log(studentName);   // Suzy
```

Acá, estamos inicializando `studentName` (en este caso, a `"Suzy"` en lugar de `undefined`) mediante la forma del statement de declaración `let` que viene acoplada con una asignación.

Alternativamente:

```js
// ..

let studentName;
// or:
// let studentName = undefined;

// ..

studentName = "Suzy";

console.log(studentName);
// Suzy
```

| NOTA: |
| :--- |
| ¡Eso es interesante! Recordá que antes dijimos que `var studentName;` *no* es lo mismo que `var studentName = undefined;`, pero acá con `let`, se comportan igual. La diferencia se reduce al hecho de que `var studentName` se inicializa automáticamente en la parte superior del scope, mientras que `let studentName` no lo hace. |

Recordá que hemos afirmado algunas veces hasta ahora que el *Compilador* termina removiendo cualquier declarador `var`/`let`/`const`, reemplazándolos con las instrucciones en la parte superior de cada scope para registrar los identificadores apropiados.

Así que si analizamos qué está pasando acá, vemos que un matiz adicional es que el *Compilador* también está agregando una instrucción en medio del programa, en el punto donde se declaró la variable `studentName`, para manejar la auto-inicialización de esa declaración. No podemos usar la variable en ningún punto previo a que ocurra esa inicialización. Lo mismo vale para `const` que para `let`.

El término acuñado por TC39 para referirse a este *período de tiempo* desde el ingreso a un scope hasta donde ocurre la auto-inicialización de la variable es: Temporal Dead Zone (TDZ).

La TDZ es la ventana de tiempo en la que una variable existe pero todavía no está inicializada, y por lo tanto no puede accederse de ninguna manera. Solo la ejecución de las instrucciones dejadas por el *Compilador* en el punto de la declaración original puede hacer esa inicialización. Después de ese momento, la TDZ termina, y la variable queda libre para usarse durante el resto del scope.

Un `var` también técnicamente tiene una TDZ, ¡pero es de longitud cero y por lo tanto no observable para nuestros programas! Solo `let` y `const` tienen una TDZ observable.

Por cierto, "temporal" en TDZ sí se refiere al *tiempo*, no a la *posición en el código*. Considerá:

```js
askQuestion();
// ReferenceError

let studentName = "Suzy";

function askQuestion() {
    console.log(`${ studentName }, do you know?`);
}
```

Aunque posicionalmente el `console.log(..)` que referencia a `studentName` viene *después* de la declaración `let studentName`, en términos de tiempo la función `askQuestion()` se invoca *antes* de que se encuentre el statement `let`, ¡mientras `studentName` todavía está en su TDZ! De ahí el error.

Hay una idea errónea común de que la TDZ significa que `let` y `const` no hacen hoisting. Esta es una afirmación imprecisa, o al menos ligeramente engañosa. Definitivamente hacen hoisting.

La diferencia real es que las declaraciones `let`/`const` no se inicializan automáticamente al comienzo del scope, de la manera en que lo hace `var`. El *debate* entonces es si la auto-inicialización es *parte del* hoisting, o no. Yo creo que el auto-registro de una variable en la parte superior del scope (es decir, lo que yo llamo "hoisting") y la auto-inicialización en la parte superior del scope (a `undefined`) son operaciones distintas y no deberían agruparse bajo el único término "hoisting".

Ya hemos visto que `let` y `const` no se auto-inicializan en la parte superior del scope. Pero probemos que `let` y `const` *sí* hacen hoisting (auto-registro en la parte superior del scope), cortesía de nuestro amigo el shadowing (ver "Shadowing" en el Capítulo 3):

```js
var studentName = "Kyle";

{
    console.log(studentName);
    // ???

    // ..

    let studentName = "Suzy";

    console.log(studentName);
    // Suzy
}
```

¿Qué va a pasar con el primer statement `console.log(..)`? Si `let studentName` no hiciera hoisting a la parte superior del scope, entonces el primer `console.log(..)` *debería* imprimir `"Kyle"`, ¿no? En ese momento, parecería, solo existe el `studentName` externo, así que esa es la variable que `console.log(..)` debería acceder e imprimir.

Pero en cambio, el primer `console.log(..)` lanza un error de TDZ, porque de hecho, el `studentName` del scope interno **sí** hizo hoisting (auto-registro en la parte superior del scope). Lo que **no** ocurrió (¡todavía!) fue la auto-inicialización de ese `studentName` interno; todavía está no inicializado en ese momento, ¡de ahí la violación de la TDZ!

Así que para resumir, los errores de TDZ ocurren porque las declaraciones `let`/`const` *sí* hacen hoisting de sus declaraciones a la parte superior de sus scopes, pero a diferencia de `var`, difieren la auto-inicialización de sus variables hasta el momento en la secuencia del código donde apareció la declaración original. Esta ventana de tiempo (pista: temporal), cualquiera sea su longitud, es la TDZ.

¿Cómo podés evitar los errores de TDZ?

Mi consejo: siempre poné tus declaraciones `let` y `const` en la parte superior de cualquier scope. Achicá la ventana de la TDZ a longitud cero (o casi cero), y entonces será un punto discutible.

Pero, ¿por qué la TDZ existe siquiera? ¿Por qué TC39 no dictó que `let`/`const` se auto-inicialicen de la manera en que lo hace `var`? Tené paciencia, volveremos a explorar el *porqué* de la TDZ en el Apéndice A.

## Finalmente Inicializada

Trabajar con variables tiene mucho más matiz del que parece a primera vista. El *Hoisting*, la *(re)declaración* y la *TDZ* son fuentes comunes de confusión para los desarrolladores, especialmente aquellos que han trabajado en otros lenguajes antes de llegar a JS. Antes de seguir adelante, asegurate de que tu modelo mental esté totalmente afianzado en estos aspectos del scope y las variables de JS.

El hoisting generalmente se cita como un mecanismo explícito del engine de JS, pero en realidad es más una metáfora para describir las diversas maneras en que JS maneja las declaraciones de variables durante la compilación. Pero incluso como metáfora, el hoisting ofrece una estructura útil para pensar en el ciclo de vida de una variable—cuándo se crea, cuándo queda disponible para usarse, cuándo desaparece.

La declaración y re-declaración de variables tienden a causar confusión cuando se piensan como operaciones de runtime. Pero si cambiás a un pensamiento de compile-time para estas operaciones, las rarezas y las *sombras* disminuyen.

El error de la TDZ (temporal dead zone) es extraño y frustrante cuando se lo encuentra. Afortunadamente, la TDZ es relativamente directa de evitar si siempre tenés el cuidado de ubicar las declaraciones `let`/`const` en la parte superior de cualquier scope.

A medida que navegues con éxito estos vericuetos del scope de variables, el próximo capítulo expondrá los factores que guían nuestras decisiones de ubicar nuestras declaraciones en varios scopes, especialmente bloques anidados.
