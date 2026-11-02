# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Apéndice A: Explorando más a fondo

Ahora exploraremos una serie de matices y casos límite en torno a muchos de los temas tratados en el texto principal de este libro. Este apéndice es material opcional y complementario.

Algunas personas consideran que sumergirse demasiado en los casos límite más sutiles y en las distintas opiniones no genera más que ruido y distracción; según ellas, a los desarrolladores les conviene más ceñirse a los caminos habitualmente transitados. Mi enfoque ha sido criticado por ser poco práctico y contraproducente. Entiendo y valoro esa perspectiva, aunque no necesariamente la comparta.

Creo que es mejor estar empoderado por el conocimiento de cómo funcionan las cosas que simplemente pasar por alto los detalles con suposiciones y falta de curiosidad. Tarde o temprano te encontrarás con situaciones en las que algo surge de una pieza que no habías explorado. En otras palabras, no podrás dedicar todo tu tiempo a recorrer el suave *camino feliz*. ¿No preferirías estar preparado para los inevitables baches del todoterreno?

Estas discusiones también estarán más influenciadas por mis opiniones de lo que lo estuvo el texto principal, así que tenlo en cuenta a medida que consumes y consideras lo que se presenta. Este apéndice es un poco como una colección de mini entradas de blog que amplían varios temas del libro. Es largo y profundiza mucho en los detalles, así que tómate tu tiempo y no te apresures a pasar por todo lo que hay aquí.

## Scopes implícitos

A veces los scopes se crean en lugares no obvios. En la práctica, estos scopes implícitos no suelen afectar el comportamiento de tu programa, pero aun así es útil saber que ocurren. Mantente atento a los siguientes scopes sorprendentes:

* Scope de parámetros
* Scope del nombre de función

### Scope de parámetros

La metáfora de la conversación del Capítulo 2 da a entender que los parámetros de una función son básicamente lo mismo que las variables declaradas localmente en el scope de la función. Pero eso no siempre es cierto.

Considera:

```js
// outer/global scope: RED(1)

function getStudentName(studentID) {
    // function scope: BLUE(2)

    // ..
}
```

Aquí, `studentID` se considera un parámetro "simple", así que sí se comporta como un miembro del scope de función BLUE(2). Pero si lo cambiamos para que sea un parámetro no simple, técnicamente eso ya no es así. Las formas de parámetros consideradas no simples incluyen parámetros con valores por defecto, parámetros rest (usando `...`) y parámetros desestructurados.

Considera:

```js
// outer/global scope: RED(1)

function getStudentName(/*BLUE(2)*/ studentID = 0) {
    // function scope: GREEN(3)

    // ..
}
```

Aquí, la lista de parámetros se convierte esencialmente en su propio scope, y el scope de la función queda entonces anidado dentro de *ese* scope.

¿Por qué? ¿Qué diferencia hace? Las formas de parámetros no simples introducen varios casos límite, así que la lista de parámetros se convierte en su propio scope para manejarlos de forma más efectiva.

Considera:

```js
function getStudentName(studentID = maxID, maxID) {
    // ..
}
```

Suponiendo operaciones de izquierda a derecha, el valor por defecto `= maxID` para el parámetro `studentID` requiere que un `maxID` ya exista (y que haya sido inicializado). Este código produce un error de TDZ (Capítulo 5). La razón es que `maxID` está declarado en el scope de parámetros, pero aún no ha sido inicializado debido al orden de los parámetros. Si se invierte el orden de los parámetros, no ocurre ningún error de TDZ:

```js
function getStudentName(maxID,studentID = maxID) {
    // ..
}
```

La complicación se vuelve aún más *enrevesada* si introducimos una function expression en la posición del parámetro por defecto, la cual puede entonces crear su propia closure (Capítulo 7) sobre los parámetros en este scope de parámetros implícito:

```js
function whatsTheDealHere(id,defaultID = () => id) {
    id = 5;
    console.log( defaultID() );
}

whatsTheDealHere(3);
// 5
```

Ese fragmento probablemente tenga sentido, porque la arrow function `defaultID()` cierra (closure) sobre el parámetro/variable `id`, que luego reasignamos a `5`. Pero ahora introduzcamos una definición que hace shadowing de `id` en el scope de la función:

```js
function whatsTheDealHere(id,defaultID = () => id) {
    var id = 5;
    console.log( defaultID() );
}

whatsTheDealHere(3);
// 3
```

¡Oh oh! El `var id = 5` está haciendo shadowing del parámetro `id`, pero la closure de la función `defaultID()` es sobre el parámetro, no sobre la variable que hace shadowing en el cuerpo de la función. Esto demuestra que hay una burbuja de scope alrededor de la lista de parámetros.

¡Pero se pone aún más loco que eso!

```js
function whatsTheDealHere(id,defaultID = () => id) {
    var id;

    console.log(`local variable 'id': ${ id }`);
    console.log(
        `parameter 'id' (closure): ${ defaultID() }`
    );

    console.log("reassigning 'id' to 5");
    id = 5;

    console.log(`local variable 'id': ${ id }`);
    console.log(
        `parameter 'id' (closure): ${ defaultID() }`
    );
}

whatsTheDealHere(3);
// local variable 'id': 3   <--- Huh!? Weird!
// parameter 'id' (closure): 3
// reassigning 'id' to 5
// local variable 'id': 5
// parameter 'id' (closure): 3
```

La parte extraña aquí es el primer mensaje de la consola. En ese momento, la variable local `id` que hace shadowing acaba de ser declarada con `var id`, la cual —según afirma el Capítulo 5— típicamente se auto-inicializa a `undefined` al comienzo de su scope. ¿Por qué no imprime `undefined`?

En este caso límite específico (por razones de compatibilidad con código heredado), JS no auto-inicializa `id` a `undefined`, sino al valor del parámetro `id` (`3`).

Aunque en ese momento los dos `id` parecen ser una sola variable, en realidad siguen siendo distintos (y en scopes distintos). La asignación `id = 5` hace observable la divergencia, donde el parámetro `id` permanece en `3` y la variable local pasa a ser `5`.

Mi consejo para evitar que estos extraños matices te muerdan:

* Nunca hagas shadowing de parámetros con variables locales

* Evita usar una función de parámetro por defecto que cierre (closure) sobre cualquiera de los parámetros

Al menos ahora estás al tanto y puedes tener cuidado con el hecho de que la lista de parámetros es su propio scope si alguno de los parámetros es no simple.

### Scope del nombre de función

En la sección "Scope del nombre de función" del Capítulo 3, afirmé que el nombre de una function expression se agrega al propio scope de la función. Recuerda:

```js
var askQuestion = function ofTheTeacher(){
    // ..
};
```

Es cierto que `ofTheTeacher` no se agrega al scope envolvente (donde se declara `askQuestion`), pero tampoco se agrega *solamente* al scope de la función, como probablemente estás suponiendo. Es otro extraño caso límite de scope implícito.

El identificador del nombre de una function expression está en su propio scope implícito, anidado entre el scope envolvente exterior y el scope principal interno de la función.

Si `ofTheTeacher` estuviera en el scope de la función, esperaríamos un error aquí:

```js
var askQuestion = function ofTheTeacher(){
    // why is this not a duplicate declaration error?
    let ofTheTeacher = "Confused, yet?";
};
```

La forma de declaración `let` no permite la re-declaración (ver Capítulo 5). Pero esto es shadowing perfectamente legal, no re-declaración, porque los dos identificadores `ofTheTeacher` están en scopes distintos.

Rara vez te encontrarás con un caso donde el scope del identificador del nombre de una función importe. Pero, de nuevo, es bueno saber cómo funcionan realmente estos mecanismos. Para evitar que te muerdan, nunca hagas shadowing de identificadores de nombres de función.

## Funciones anónimas vs. con nombre

Como se discutió en el Capítulo 3, las funciones pueden expresarse ya sea en forma con nombre o anónima. Es muchísimo más común usar la forma anónima, pero ¿es una buena idea?

Mientras contemplas nombrar tus funciones, considera:

* La inferencia de nombres es incompleta
* Los nombres léxicos permiten la auto-referencia
* Los nombres son descripciones útiles
* Las arrow functions no tienen nombres léxicos
* Las IIFE también necesitan nombres

### ¿Nombres explícitos o inferidos?

Toda función en tu programa tiene un propósito. Si no tiene un propósito, quítala, porque solo estás desperdiciando espacio. Si *sí* tiene un propósito, *hay* un nombre para ese propósito.

Hasta aquí, probablemente muchos lectores estén de acuerdo conmigo. Pero ¿eso significa que siempre deberíamos poner ese nombre en el código? Aquí es donde levantaré más de una ceja. Digo, sin lugar a dudas, ¡que sí!

En primer lugar, que aparezca "anonymous" en los rastros de pila (stack traces) simplemente no es demasiado útil para la depuración:

```js
btn.addEventListener("click",function(){
    setTimeout(function(){
        ["a",42].map(function(v){
            console.log(v.toUpperCase());
        });
    },100);
});
// Uncaught TypeError: v.toUpperCase is not a function
//     at myProgram.js:4
//     at Array.map (<anonymous>)
//     at myProgram.js:3
```

Uf. Compáralo con lo que se reporta si les doy nombres a las funciones:

```js
btn.addEventListener("click",function onClick(){
    setTimeout(function waitAMoment(){
        ["a",42].map(function allUpper(v){
            console.log(v.toUpperCase());
        });
    },100);
});
// Uncaught TypeError: v.toUpperCase is not a function
//     at allUpper (myProgram.js:4)
//     at Array.map (<anonymous>)
//     at waitAMoment (myProgram.js:3)
```

¿Ves cómo aparecen los nombres `waitAMoment` y `allUpper` y le dan al stack trace información/contexto más útil para la depuración? El programa es más depurable si usamos nombres razonables para todas nuestras funciones.

| NOTA: |
| :--- |
| El desafortunado "&lt;anonymous>" que aún aparece se refiere al hecho de que la implementación de `Array.map(..)` no está presente en nuestro programa, sino que está incorporada en el engine de JS. No proviene de ninguna confusión que nuestro programa introduzca con atajos de legibilidad. |

Por cierto, asegurémonos de estar en la misma página sobre qué es una función con nombre:

```js
function thisIsNamed() {
    // ..
}

ajax("some.url",function thisIsAlsoNamed(){
   // ..
});

var notNamed = function(){
    // ..
};

makeRequest({
    data: 42,
    cb /* also not a name */: function(){
        // ..
    }
});

var stillNotNamed = function butThisIs(){
    // ..
};
```

"¡Pero espera!", dices. Algunas de esas *sí* tienen nombre, ¿verdad?

```js
var notNamed = function(){
    // ..
};

var config = {
    cb: function(){
        // ..
    }
};

notNamed.name;
// notNamed

config.cb.name;
// cb
```

Estos se conocen como nombres *inferidos*. Los nombres inferidos están bien, pero realmente no abordan la totalidad de la preocupación que estoy discutiendo.

### ¿Nombres faltantes?

Sí, estos nombres inferidos podrían aparecer en los stack traces, lo cual es definitivamente mejor que que aparezca "anonymous". Pero...

```js
function ajax(url,cb) {
    console.log(cb.name);
}

ajax("some.url",function(){
    // ..
});
// ""
```

Ups. Las function expressions anónimas pasadas como callbacks son incapaces de recibir un nombre inferido, así que `cb.name` contiene solo la cadena vacía `""`. La gran mayoría de todas las function expressions, especialmente las anónimas, se usan como argumentos de callback; ninguna de estas obtiene un nombre. Así que confiar en la inferencia de nombres es, en el mejor de los casos, incompleto.

Y no son solo los callbacks los que se quedan cortos con la inferencia:

```js
var config = {};

config.cb = function(){
    // ..
};

config.cb.name;
// ""

var [ noName ] = [ function(){} ];
noName.name
// ""
```

Cualquier asignación de una function expression que no sea una *asignación simple* también fallará en la inferencia de nombres. Así que, en otras palabras, a menos que seas cuidadoso e intencional al respecto, esencialmente casi todas las function expressions anónimas en tu programa de hecho no tendrán nombre alguno.

La inferencia de nombres simplemente... no es suficiente.

E incluso si una function expression *sí* obtiene un nombre inferido, eso todavía no cuenta como ser una función con nombre completa.

### ¿Quién soy?

Sin un identificador de nombre léxico, la función no tiene forma interna de referirse a sí misma. La auto-referencia es importante para cosas como la recursión y el manejo de eventos:

```js
// broken
runOperation(function(num){
    if (num <= 1) return 1;
    return num * oopsNoNameToCall(num - 1);
});

// also broken
btn.addEventListener("click",function(){
   console.log("should only respond to one click!");
   btn.removeEventListener("click",oopsNoNameHere);
});
```

Dejar fuera el nombre léxico de tu callback hace más difícil auto-referenciar la función de forma confiable. *Podrías* declarar una variable en un scope envolvente que referencie la función, pero esa variable está *controlada* por ese scope envolvente —podría ser reasignada, etc.—, así que no es tan confiable como que la función tenga su propia auto-referencia interna.

### Los nombres son descriptores

Por último, y creo que lo más importante de todo, dejar fuera el nombre de una función hace más difícil para el lector distinguir cuál es el propósito de la función de un vistazo rápido. Tiene que leer más código, incluyendo el código dentro de la función y el código circundante fuera de la función, para descifrarlo.

Considera:

```js
[ 1, 2, 3, 4, 5 ].filter(function(v){
    return v % 2 == 1;
});
// [ 1, 3, 5 ]

[ 1, 2, 3, 4, 5 ].filter(function keepOnlyOdds(v){
    return v % 2 == 1;
});
// [ 1, 3, 5 ]
```

Simplemente no hay ningún argumento razonable que pueda hacerse de que **omitir** el nombre `keepOnlyOdds` del primer callback comunica más efectivamente al lector el propósito de este callback. Ahorraste 13 caracteres, pero perdiste información importante de legibilidad. El nombre `keepOnlyOdds` le dice muy claramente al lector, de un vistazo rápido, qué está sucediendo.

Al engine de JS no le importa el nombre. Pero a los lectores humanos de tu código absolutamente sí.

¿Puede el lector mirar `v % 2 == 1` y descifrar qué está haciendo? Claro. Pero tiene que inferir el propósito (y el nombre) ejecutando mentalmente el código. Incluso una breve pausa para hacerlo ralentiza la lectura del código. Un buen nombre descriptivo hace que este proceso sea casi sin esfuerzo e instantáneo.

Piénsalo de esta manera: ¿cuántas veces necesita el autor de este código descifrar el propósito de una función antes de agregar el nombre al código? Alrededor de una vez. Quizás dos o tres veces si necesita ajustar el nombre. Pero ¿cuántas veces tendrán que descifrar el nombre/propósito los lectores de este código? Cada vez que se lea esta línea. ¿Cientos de veces? ¿Miles? ¿Más?

No importa la longitud ni la complejidad de la función, mi afirmación es que el autor debería descifrar un buen nombre descriptivo y agregarlo al código. Incluso las funciones de una sola línea en sentencias `map(..)` y `then(..)` deberían tener nombre:

```js
lookupTheRecords(someData)
.then(function extractSalesRecords(resp){
   return resp.allSales;
})
.then(storeRecords);
```

El nombre `extractSalesRecords` le dice al lector el propósito de este manejador de `then(..)` *mejor* que simplemente inferir ese propósito ejecutando mentalmente `return resp.allSales`.

La única excusa para no incluir un nombre en una función es ya sea la pereza (no querer teclear unos pocos caracteres extra) o la falta de creatividad (no poder pensar en un buen nombre). Si no puedes descifrar un buen nombre, probablemente todavía no entiendes la función y su propósito. La función tal vez esté mal diseñada, o hace demasiadas cosas, y debería ser reelaborada. Una vez que tengas una función bien diseñada y de propósito único, su nombre apropiado debería volverse evidente.

Aquí tienes un truco que uso: mientras escribo por primera vez una función, si no entiendo del todo su propósito y no se me ocurre un buen nombre para usar, simplemente uso `TODO` como nombre. De esa manera, más tarde, cuando revise mi código, es probable que encuentre esos marcadores de nombre, y estoy más inclinado (¡y más preparado!) a volver y descifrar un mejor nombre, en lugar de simplemente dejarlo como `TODO`.

Todas las funciones necesitan nombres. Cada una de ellas. Sin excepciones. Cualquier nombre que omitas hace que el programa sea más difícil de leer, más difícil de depurar, más difícil de extender y mantener más adelante.

### Arrow functions

Las arrow functions son **siempre** anónimas, incluso si (rara vez) se usan de una manera que les da un nombre inferido. Acabo de pasar varias páginas explicando por qué las funciones anónimas son una mala idea, así que probablemente puedas adivinar lo que pienso sobre las arrow functions.

No las uses como un reemplazo general de las funciones regulares. Son más concisas, sí, pero esa brevedad tiene el costo de omitir delimitadores visuales clave que ayudan a nuestros cerebros a parsear rápidamente lo que estamos leyendo. Y, al punto de esta discusión, son anónimas, lo que las hace peores para la legibilidad desde ese ángulo también.

Las arrow functions tienen un propósito, pero ese propósito no es ahorrar pulsaciones de teclas. Las arrow functions tienen comportamiento de *this léxico*, lo cual está un poco más allá de los límites de nuestra discusión en este libro.

Brevemente: las arrow functions no definen en absoluto una palabra clave identificadora `this`. Si usas un `this` dentro de una arrow function, se comporta exactamente como cualquier otra referencia a variable, lo cual es que se consulta la cadena de scopes para encontrar un scope de función (función no arrow) donde *sí* esté definido, y usar ese.

En otras palabras, las arrow functions tratan a `this` como cualquier otra variable léxica.

Si estás acostumbrado a hacks como `var self = this`, o si prefieres llamar a `.bind(this)` sobre function expressions internas, solo para forzarlas a heredar un `this` de una función externa como si fuera una variable léxica, entonces las arrow functions `=>` son absolutamente la mejor opción. Están diseñadas específicamente para arreglar ese problema.

Así que, en los raros casos en que necesites *this léxico*, usa una arrow function. Es la mejor herramienta para ese trabajo. Pero ten en cuenta que, al hacerlo, estás aceptando las desventajas de una función anónima. Deberías dedicar un esfuerzo adicional a mitigar el *costo* de legibilidad, como nombres de variables más descriptivos y comentarios en el código.

### Variaciones de IIFE

Todas las funciones deberían tener nombres. Lo dije unas cuantas veces, ¿verdad? Eso incluye a las IIFE.

```js
(function(){
    // don't do this!
})();

(function doThisInstead(){
    // ..
})();
```

¿Cómo se nos ocurre un nombre para una IIFE? Identifica para qué está ahí la IIFE. ¿Por qué necesitas un scope en ese lugar? ¿Estás ocultando una variable de caché para registros de estudiantes?

```js
var getStudents = (function StoreStudentRecords(){
    var studentRecords = [];

    return function getStudents() {
        // ..
    }
})();
```

Nombré a la IIFE `StoreStudentRecords` porque eso es lo que está haciendo: almacenar registros de estudiantes. Toda IIFE debería tener un nombre. Sin excepciones.

Las IIFE se definen típicamente colocando `( .. )` alrededor de la function expression, como se muestra en esos fragmentos anteriores. Pero esa no es la única forma de definir una IIFE. Técnicamente, la única razón por la que usamos ese primer conjunto de `( .. )` que las rodea es para que la palabra clave `function` no quede en una posición que la califique como una function declaration para el parser de JS. Pero hay otras formas sintácticas de evitar ser parseada como una declaración:

```js
!function thisIsAnIIFE(){
    // ..
}();

+function soIsThisOne(){
    // ..
}();

~function andThisOneToo(){
    // ..
}();
```

El `!`, el `+`, el `~` y varios otros operadores unarios (operadores con un solo operando) pueden colocarse todos delante de `function` para convertirla en una expresión. Luego la llamada final `()` es válida, lo que la convierte en una IIFE.

De hecho, me gusta bastante usar el operador unario `void` cuando defino una IIFE independiente:

```js
void function yepItsAnIIFE() {
    // ..
}();
```

El beneficio de `void` es que comunica claramente, al comienzo de la función, que esta IIFE no retornará ningún valor.

Sea cual sea la forma en que definas tus IIFE, muéstrales algo de cariño dándoles nombres.

## Hoisting: funciones y variables

El Capítulo 5 articuló tanto el *hoisting de funciones* como el *hoisting de variables*. Dado que el hoisting a menudo se cita como un error en el diseño de JS, quería explorar brevemente por qué ambas formas de hoisting *pueden* ser beneficiosas y aún deberían ser consideradas.

Dale al hoisting un nivel más profundo de consideración analizando los méritos de:

* Código ejecutable primero, function declarations al final
* Ubicación semántica de las declaraciones de variables

### Hoisting de funciones

A modo de repaso, este programa funciona gracias al *hoisting de funciones*:

```js
getStudents();

// ..

function getStudents() {
    // ..
}
```

La function declaration se somete a hoisting durante la compilación, lo que significa que `getStudents` es un identificador declarado para todo el scope. Adicionalmente, el identificador `getStudents` se auto-inicializa con la referencia a la función, nuevamente al comienzo del scope.

¿Por qué es esto útil? La razón por la que prefiero aprovechar el *hoisting de funciones* es que coloca el código *ejecutable* de cualquier scope arriba, y cualquier otra declaración (funciones) debajo. Esto significa que es más fácil encontrar el código que se ejecutará en cualquier área dada, en lugar de tener que desplazarse y desplazarse, esperando encontrar una `}` final que marque el fin de un scope/función en algún lugar.

Aprovecho este posicionamiento inverso en todos los niveles de scope:

```js
getStudents();

// *************

function getStudents() {
    var whatever = doSomething();

    // other stuff

    return whatever;

    // *************

    function doSomething() {
        // ..
    }
}
```

Cuando abro por primera vez un archivo como ese, la primerísima línea es código ejecutable que pone en marcha su comportamiento. ¡Eso es muy fácil de detectar! Luego, si alguna vez necesito ir a buscar e inspeccionar `getStudents()`, me gusta que su primera línea también sea código ejecutable. Solo si necesito ver los detalles de `doSomething()` voy a buscar su definición más abajo.

En otras palabras, creo que el *hoisting de funciones* hace que el código sea más legible mediante un orden de lectura fluido y progresivo, de arriba hacia abajo.

### Hoisting de variables

¿Qué hay del *hoisting de variables*?

Aunque `let` y `const` se someten a hoisting, no puedes usar esas variables en su TDZ (ver Capítulo 5). Así que la siguiente discusión solo aplica a las declaraciones `var`. Antes de continuar, lo admitiré: en casi todos los casos, estoy completamente de acuerdo en que el *hoisting de variables* es una mala idea:

```js
pleaseDontDoThis = "bad idea";

// much later
var pleaseDontDoThis;
```

Si bien ese tipo de ordenamiento invertido era útil para el *hoisting de funciones*, aquí creo que normalmente hace que el código sea más difícil de razonar.

Pero hay una excepción que he encontrado, de forma algo poco frecuente, en mi propia programación. Tiene que ver con dónde coloco mis declaraciones `var` dentro de la definición de un módulo CommonJS.

Así es como típicamente estructuro mis definiciones de módulo en Node:

```js
// dependencies
var aModuleINeed = require("very-helpful");
var anotherModule = require("kinda-helpful");

// public API
var publicAPI = Object.assign(module.exports,{
    getStudents,
    addStudents,
    // ..
});

// ********************************
// private implementation

var cache = { };
var otherData = [ ];

function getStudents() {
    // ..
}

function addStudents() {
    // ..
}
```

¿Notas cómo las variables `cache` y `otherData` están en la sección "privada" del diseño del módulo? Eso es porque no planeo exponerlas públicamente. Así que organizo el módulo de modo que queden ubicadas junto a los otros detalles de implementación ocultos del módulo.

Pero he tenido algunos casos poco frecuentes donde necesitaba que las asignaciones de esos valores ocurrieran *arriba*, antes de declarar la API pública exportada del módulo. Por ejemplo:

```js
// public API
var publicAPI = Object.assign(module.exports,{
    getStudents,
    addStudents,
    refreshData: refreshData.bind(null,cache)
});
```

Necesito que a la variable `cache` ya se le haya asignado un valor, porque ese valor se usa en la inicialización de la API pública (la aplicación parcial de `.bind(..)`).

¿Debería simplemente mover el `var cache = { .. }` arriba del todo, por encima de esta inicialización de la API pública? Bueno, tal vez. Pero ahora es menos obvio que `var cache` es un detalle de implementación *privado*. Aquí está el compromiso que he usado (de forma algo poco frecuente):

```js
cache = {};   // used here, but declared below

// public API
var publicAPI = Object.assign(module.exports,{
    getStudents,
    addStudents,
    refreshData: refreshData.bind(null,cache)
});

// ********************************
// private implementation

var cache /* = {}*/;
```

¿Ves el *hoisting de variables*? He declarado `cache` abajo, donde lógicamente pertenece, pero en este raro caso lo he usado antes, arriba, en el área donde se necesita su inicialización. Incluso dejé una pista del valor que se asigna a `cache` en un comentario del código.

Ese es literalmente el único caso que he encontrado para aprovechar el *hoisting de variables* para asignar una variable más arriba en un scope que su declaración. Pero creo que es una excepción razonable para emplear con precaución.

## El caso a favor de `var`

Hablando de *hoisting de variables*, hablemos un poco en serio sobre `var`, un villano favorito al que a los desarrolladores les encanta culpar por muchos de los males del desarrollo en JS. En el Capítulo 5, exploramos `let`/`const` y prometimos que revisaríamos dónde encaja `var` en toda la mezcla.

Mientras expongo el caso, no te pierdas:

* `var` nunca estuvo roto
* `let` es tu amigo
* `const` tiene utilidad limitada
* Lo mejor de ambos mundos: `var` *y* `let`

### No deseches `var`

`var` está bien, y funciona perfectamente. Ha existido durante 25 años, y existirá y será útil y funcional durante otros 25 años o más. Las afirmaciones de que `var` está roto, deprecado, obsoleto, peligroso o mal diseñado son tonterías de seguir la corriente.

¿Significa eso que `var` es el declarador correcto para cada una de las declaraciones en tu programa? Ciertamente no. Pero aun así tiene su lugar en tus programas. Negarte a usarlo porque alguien del equipo eligió una opinión agresiva de linter que se atraganta con `var` es cortarte la nariz para fastidiar tu cara.

OK, ahora que te tengo realmente alterado, déjame intentar explicar mi posición.

Para que conste, soy fan de `let`, para declaraciones con scope de bloque. Realmente me disgusta la TDZ y creo que fue un error. Pero `let` en sí es genial. Lo uso a menudo. De hecho, probablemente lo uso tanto o más de lo que uso `var`.

### Constante-mente confundido

`const`, por otro lado, no lo uso tan a menudo. No voy a profundizar en todas las razones del porqué, pero se reduce a que `const` no *carga con su propio peso*. Es decir, si bien hay un pequeñísimo beneficio de `const` en algunos casos, ese beneficio queda superado por la larga historia de problemas en torno a la confusión con `const` en una variedad de lenguajes, mucho antes de que apareciera en JS.

`const` pretende crear valores que no pueden ser mutados —un concepto erróneo que es extremadamente común en las comunidades de desarrolladores de muchos lenguajes—, mientras que lo que realmente hace es prevenir la reasignación.

```js
const studentIDs = [ 14, 73, 112 ];

// later

studentIDs.push(6);   // whoa, wait... what!?
```

Usar un `const` con un valor mutable (como un array o un objeto) es pedir que un futuro desarrollador (o lector de tu código) caiga en la trampa que tendiste, que era que o bien no sabían, o más o menos olvidaron, que la *inmutabilidad de valor* no es en absoluto lo mismo que la *inmutabilidad de asignación*.

Simplemente no creo que debamos tender esas trampas. La única vez que alguna vez uso `const` es cuando estoy asignando un valor ya inmutable (como `42` o `"Hello, friends!"`), y cuando es claramente una "constante" en el sentido de ser un marcador de posición con nombre para un valor literal, con fines semánticos. Para eso es para lo que mejor se usa `const`. Sin embargo, eso es bastante raro en mi código.

Si la reasignación de variables fuera un gran problema, entonces `const` sería más útil. Pero la reasignación de variables simplemente no es un problema tan grande en términos de causar bugs. Hay una larga lista de cosas que llevan a bugs en los programas, pero la "reasignación accidental" está muy, muy abajo en esa lista.

Combina eso con el hecho de que `const` (y `let`) se supone que deben usarse en bloques, y que los bloques se supone que deben ser cortos, y tienes un área realmente pequeña de tu código donde una declaración `const` siquiera es aplicable. Un `const` en la línea 1 de tu bloque de diez líneas solo te dice algo sobre las siguientes nueve líneas. Y lo que te dice ya es obvio con solo echar un vistazo a esas nueve líneas: la variable nunca está del lado izquierdo de un `=`; no se reasigna.

Eso es todo, eso es todo lo que realmente hace `const`. Aparte de eso, no es muy útil. Puesto frente a la significativa confusión entre inmutabilidad de valor y de asignación, `const` pierde gran parte de su brillo.

Un `let` (¡o `var`!) que nunca se reasigna ya es, en comportamiento, una "constante", aunque no tenga la garantía del compilador. Eso es suficientemente bueno en la mayoría de los casos.

### `var` *y* `let`

En mi opinión, `const` es bastante raramente útil, así que esto es solo una carrera de dos caballos entre `let` y `var`. Pero en realidad tampoco es una carrera, porque no tiene que haber un solo ganador. Ambos pueden ganar... carreras diferentes.

El hecho es que deberías estar usando tanto `var` como `let` en tus programas. No son intercambiables: no deberías usar `var` donde se requiere un `let`, pero tampoco deberías usar `let` donde `var` es lo más apropiado.

Entonces, ¿dónde deberíamos seguir usando `var`? ¿En qué circunstancias es una mejor elección que `let`?

Por un lado, siempre uso `var` en el scope de nivel superior de cualquier función, independientemente de si eso está al principio, en el medio o al final de la función. También uso `var` en el scope global, aunque trato de minimizar el uso del scope global.

¿Por qué usar `var` para scoping de función? Porque eso es exactamente lo que hace `var`. Literalmente no hay mejor herramienta para el trabajo de aplicar scope de función a una declaración que un declarador que, durante 25 años, ha hecho exactamente eso.

*Podrías* usar `let` en este scope de nivel superior, pero no es la mejor herramienta para ese trabajo. También encuentro que si usas `let` en todas partes, entonces es menos obvio cuáles declaraciones están diseñadas para ser localizadas y cuáles están destinadas a usarse a lo largo de toda la función.

En contraste, rara vez uso un `var` dentro de un bloque. Para eso está `let`. Usa la mejor herramienta para el trabajo. Si ves un `let`, te dice que estás lidiando con una declaración localizada. Si ves `var`, te dice que estás lidiando con una declaración de ámbito de función completa. Así de simple.

```js
function getStudents(data) {
    var studentRecords = [];

    for (let record of data.records) {
        let id = `student-${ record.id }`;
        studentRecords.push({
            id,
            record.name
        });
    }

    return studentRecords;
}
```

La variable `studentRecords` está destinada a usarse a lo largo de toda la función. `var` es el mejor declarador para decirle eso al lector. En contraste, `record` e `id` están destinados a usarse solo en el scope más estrecho de la iteración del bucle, así que `let` es la mejor herramienta para ese trabajo.

Además de este argumento semántico de *la mejor herramienta*, `var` tiene algunas otras características que, en ciertas circunstancias limitadas, lo hacen más poderoso.

Un ejemplo es cuando un bucle está usando exclusivamente una variable, pero su cláusula condicional no puede ver las declaraciones con scope de bloque dentro de la iteración:

```js
function commitAction() {
    do {
        let result = commit();
        var done = result && result.code == 1;
    } while (!done);
}
```

Aquí, `result` claramente solo se usa dentro del bloque, así que usamos `let`. Pero `done` es un poco diferente. Solo es útil para el bucle, pero la cláusula `while` no puede ver las declaraciones `let` que aparecen dentro del bucle. Así que nos comprometemos y usamos `var`, de modo que `done` se somete a hoisting hacia el scope externo donde puede ser vista.

La alternativa —declarar `done` fuera del bucle— lo separa de donde se usa por primera vez, y o bien hace necesario elegir un valor por defecto para asignar, o peor, dejarlo sin asignar y por lo tanto luciendo ambiguo para el lector. Creo que `var` dentro del bucle es preferible aquí.

Otra característica útil de `var` se ve con declaraciones dentro de bloques no intencionados. Los bloques no intencionados son bloques que se crean porque la sintaxis requiere un bloque, pero donde la intención del desarrollador no es realmente crear un scope localizado. La mejor ilustración de un scope no intencionado es la sentencia `try..catch`:

```js
function getStudents() {
    try {
        // not really a block scope
        var records = fromCache("students");
    }
    catch (err) {
        // oops, fall back to a default
        var records = [];
    }
    // ..
}
```

Hay otras formas de estructurar este código, sí. Pero creo que esta es la *mejor* forma, dadas varias concesiones.

No quiero declarar `records` (con `var` o `let`) fuera del bloque `try`, y luego asignarle en uno o ambos bloques. Prefiero que las declaraciones iniciales estén siempre lo más cerca posible (idealmente, en la misma línea) del primer uso de la variable. En este ejemplo simple, eso sería solo un par de líneas de distancia, pero en código real puede crecer a muchas más líneas. Cuanto más grande es la brecha, más difícil es descifrar a qué variable de qué scope le estás asignando. `var` usado en la asignación real lo hace menos ambiguo.

Nota también que usé `var` tanto en el bloque `try` como en el `catch`. Eso es porque quiero señalizar al lector que no importa qué camino se tome, `records` siempre se declara. Técnicamente, eso funciona porque `var` se somete a hoisting una vez hacia el scope de la función. Pero aun así es una buena señal semántica para recordarle al lector lo que cualquiera de los dos `var` asegura. Si `var` solo se usara en uno de los bloques, y solo estuvieras leyendo el otro bloque, no descubrirías tan fácilmente de dónde provenía `records`.

Esto es, en mi opinión, un pequeño superpoder de `var`. No solo puede escapar de los bloques `try..catch` no intencionados, sino que se le permite aparecer múltiples veces en el scope de una función. No puedes hacer eso con `let`. No es malo, en realidad es una pequeña característica útil. Piensa en `var` más como una anotación declarativa que te recuerda, en cada uso, de dónde proviene la variable. "Ajá, claro, pertenece a toda la función."

Este superpoder de anotación repetida es útil en otros casos:

```js
function getStudents() {
    var data = [];

    // do something with data
    // .. 50 more lines of code ..

    // purely an annotation to remind us
    var data;

    // use data again
    // ..
}
```

El segundo `var data` no está re-declarando `data`, solo está anotando, en beneficio de los lectores, que `data` es una declaración de ámbito de función completa. De esa manera, el lector no necesita desplazarse 50+ líneas de código hacia arriba para encontrar la declaración inicial.

Estoy perfectamente bien con reutilizar variables para múltiples propósitos a lo largo del scope de una función. También estoy perfectamente bien con que dos usos de una variable estén separados por bastantes líneas de código. En ambos casos, la capacidad de "re-declarar" (anotar) de forma segura con `var` ayuda a asegurar que pueda distinguir de dónde proviene mi `data`, sin importar dónde esté en la función.

De nuevo, lamentablemente, `let` no puede hacer esto.

Hay otros matices y escenarios en los que `var` resulta ofrecer algo de ayuda, pero no voy a insistir más en el punto. La conclusión es que `var` puede ser útil en nuestros programas junto con `let` (y el ocasional `const`). ¿Estás dispuesto a usar creativamente las herramientas que el lenguaje JS provee para contar una historia más rica a tus lectores?

No descartes sin más una herramienta útil como `var` porque alguien te avergonzó haciéndote pensar que ya no era cool. No evites `var` porque te confundiste una vez hace años. Aprende estas herramientas y usa cada una para aquello en lo que es mejor.

## ¿Qué onda con la TDZ?

La TDZ (zona muerta temporal, *temporal dead zone*) fue explicada en el Capítulo 5. Ilustramos cómo ocurre, pero pasamos por alto cualquier explicación de *por qué* fue necesario introducirla en primer lugar. Veamos brevemente las motivaciones de la TDZ.

Algunas migajas de pan en la historia del origen de la TDZ:

* Las `const` nunca deberían cambiar
* Todo tiene que ver con el tiempo
* ¿Debería `let` comportarse más como `const` o como `var`?

### Donde todo empezó

La TDZ proviene de `const`, en realidad.

Durante el trabajo de desarrollo temprano de ES6, TC39 tuvo que decidir si `const` (y `let`) se iban a someter a hoisting hacia el inicio de sus bloques. Decidieron que estas declaraciones se someterían a hoisting, de forma similar a como lo hace `var`. De no haber sido así, creo que parte del temor era la confusión con el shadowing a mitad de scope, como:

```js
let greeting = "Hi!";

{
    // what should print here?
    console.log(greeting);

    // .. a bunch of lines of code ..

    // now shadowing the `greeting` variable
    let greeting = "Hello, friends!";

    // ..
}
```

¿Qué deberíamos hacer con esa sentencia `console.log(..)`? ¿Tendría algún sentido para los desarrolladores de JS que imprimiera "Hi!"? Parece que eso podría ser un gotcha: que el shadowing entre en acción solo para la segunda mitad del bloque, pero no para la primera mitad. Ese no es un comportamiento muy intuitivo ni propio de JS. Así que `let` y `const` tienen que someterse a hoisting hacia el inicio del bloque, visibles en todo él.

Pero si `let` y `const` se someten a hoisting hacia el inicio del bloque (como `var` se somete a hoisting hacia el inicio de una función), ¿por qué `let` y `const` no se auto-inicializan (a `undefined`) de la forma en que lo hace `var`? Aquí estaba la principal preocupación:

```js
{
    // what should print here?
    console.log(studentName);

    // later

    const studentName = "Frank";

    // ..
}
```

Imaginemos que `studentName` no solo se sometiera a hoisting hacia el inicio de este bloque, sino que también se auto-inicializara a `undefined`. Durante la primera mitad del bloque, se podría observar que `studentName` tiene el valor `undefined`, por ejemplo con nuestra sentencia `console.log(..)`. Una vez que se alcanza la sentencia `const studentName = ..`, ahora a `studentName` se le asigna `"Frank"`. A partir de ese punto en adelante, `studentName` nunca puede ser reasignada.

Pero ¿es extraño o sorprendente que una constante tenga observablemente dos valores diferentes, primero `undefined` y luego `"Frank"`? Eso sí parece ir en contra de lo que pensamos que significa una `const`ante; solo debería poder observarse con un único valor.

Así que... ahora tenemos un problema. No podemos auto-inicializar `studentName` a `undefined` (ni a ningún otro valor, para el caso). Pero la variable tiene que existir a lo largo de todo el scope. ¿Qué hacemos con el período de tiempo entre cuando existe por primera vez (inicio del scope) y cuando se le asigna su valor?

Llamamos a este período de tiempo la "zona muerta", como en la "zona muerta temporal" (TDZ). Para prevenir confusiones, se determinó que cualquier tipo de acceso a una variable mientras está en su TDZ es ilegal y debe resultar en el error de TDZ.

OK, esa línea de razonamiento sí tiene algo de sentido, debo admitirlo.

### ¿Quién dejó salir la TDZ?

Pero eso es solo `const`. ¿Qué hay de `let`?

Bueno, TC39 tomó la decisión: ya que necesitamos una TDZ para `const`, bien podríamos tener una TDZ para `let` también. *De hecho, si hacemos que `let` tenga una TDZ, entonces desalentamos todo ese feo hoisting de variables que la gente hace.* Así que había una perspectiva de consistencia y, quizás, un poco de ingeniería social para cambiar el comportamiento de los desarrolladores.

Mi contraargumento sería: si estás favoreciendo la consistencia, sé consistente con `var` en lugar de con `const`; `let` es definitivamente más parecido a `var` que a `const`. Eso es especialmente cierto dado que ya habían elegido la consistencia con `var` para todo el asunto del hoisting-hacia-el-inicio-del-scope. Deja que `const` sea su propio asunto único con una TDZ, y deja que la respuesta a la TDZ sea puramente: simplemente evita la TDZ declarando siempre tus constantes al inicio del scope. Creo que esto habría sido más razonable.

Pero, por desgracia, no fue así como quedó. `let` tiene una TDZ porque `const` necesita una TDZ, porque `let` y `const` imitan a `var` en su hoisting hacia el inicio del scope (de bloque). Ahí lo tienes. ¿Demasiado circular? Léelo de nuevo unas cuantas veces.

## ¿Siguen siendo closures los callbacks síncronos?

El Capítulo 7 presentó dos modelos diferentes para abordar la closure:

* La closure es una instancia de función que recuerda sus variables externas incluso cuando esa función es pasada de un lado a otro e **invocada en** otros scopes.

* La closure es una instancia de función y su entorno de scope que se preservan en su lugar mientras cualquier referencia a ella es pasada de un lado a otro e **invocada desde** otros scopes.

Estos modelos no son enormemente divergentes, pero sí abordan desde una perspectiva diferente. Y esa perspectiva diferente cambia lo que identificamos como una closure.

No te pierdas siguiendo este rastro de conejo a través de las closures y los callbacks:

* ¿Llamar de vuelta a qué (o a dónde)?
* Quizás "callback síncrono" no sea la mejor etiqueta
* Las funciones ***IIF*** no se mueven de un lado a otro, ¿por qué necesitarían una closure?
* Diferir en el tiempo es clave para la closure

### ¿Qué es un callback?

Antes de revisar la closure, permíteme dedicar un breve momento a abordar la palabra "callback". Es una norma generalmente aceptada que decir "callback" es sinónimo tanto de *callbacks asíncronos* como de *callbacks síncronos*. No creo estar de acuerdo con que esto sea una buena idea, así que quiero explicar por qué y proponer que nos alejemos de eso hacia otro término.

Consideremos primero un *callback asíncrono*, una referencia a función que será invocada en algún punto *posterior* futuro. ¿Qué significa "callback" en este caso?

Significa que el código actual ha terminado o se ha pausado, se ha suspendido a sí mismo, y que cuando la función en cuestión sea invocada más tarde, la ejecución entrará de vuelta en el programa suspendido, reanudándolo. Específicamente, el punto de reingreso es el código que fue envuelto en la referencia a función:

```js
setTimeout(function waitForASecond(){
    // this is where JS should call back into
    // the program when the timer has elapsed
},1000);

// this is where the current program finishes
// or suspends
```

En este contexto, "llamar de vuelta" (calling back) tiene mucho sentido. El engine de JS está reanudando nuestro programa suspendido al *llamar de vuelta* en una ubicación específica. OK, así que un callback es asíncrono.

### ¿Callback síncrono?

¿Pero qué hay de los *callbacks síncronos*? Considera:

```js
function getLabels(studentIDs) {
    return studentIDs.map(
        function formatIDLabel(id){
            return `Student ID: ${
               String(id).padStart(6)
            }`;
        }
    );
}

getLabels([ 14, 73, 112, 6 ]);
// [
//    "Student ID: 000014",
//    "Student ID: 000073",
//    "Student ID: 000112",
//    "Student ID: 000006"
// ]
```

¿Deberíamos referirnos a `formatIDLabel(..)` como un callback? ¿Está la utilidad `map(..)` realmente *llamando de vuelta* a nuestro programa al invocar la función que proporcionamos?

No hay nada a lo que *llamar de vuelta* en sí, porque el programa no se ha pausado ni ha salido. Estamos pasando una función (referencia) de una parte del programa a otra parte del programa, y luego es invocada inmediatamente.

Hay otros términos establecidos que podrían coincidir con lo que estamos haciendo: pasar una función (referencia) para que otra parte del programa pueda invocarla en nuestro nombre. Podrías pensar en esto como *Inyección de dependencias* (DI, *Dependency Injection*) o *Inversión de control* (IoC, *Inversion of Control*).

La DI puede resumirse como pasar la(s) parte(s) necesaria(s) de funcionalidad a otra parte del programa de modo que esta pueda invocarlas para completar su trabajo. Esa es una descripción decente para la llamada a `map(..)` de arriba, ¿no? La utilidad `map(..)` sabe iterar sobre los valores de la lista, pero no sabe qué *hacer* con esos valores. Por eso le pasamos la función `formatIDLabel(..)`. Le pasamos la dependencia.

La IoC es un concepto bastante similar y relacionado. Inversión de control significa que, en lugar de que el área actual de tu programa controle lo que está sucediendo, cedes el control a otra parte del programa. Envolvimos la lógica para calcular una cadena de etiqueta en la función `formatIDLabel(..)`, y luego cedimos el control de la invocación a la utilidad `map(..)`.

Cabe destacar que Martin Fowler cita la IoC como la diferencia entre un framework y una librería: con una librería, tú llamas a sus funciones; con un framework, él llama a tus funciones. [^fowlerIOC]

En el contexto de nuestra discusión, tanto DI como IoC podrían funcionar como una etiqueta alternativa para un *callback síncrono*.

Pero tengo una sugerencia diferente. Refirámonos a (las funciones antes conocidas como) *callbacks síncronos*, como *funciones inter-invocadas* (IIFs, *inter-invoked functions*). Sí, exactamente, estoy jugando con el término IIFE. Estos tipos de funciones son *inter-invocadas*, lo que significa: otra entidad las invoca, a diferencia de las IIFE, que se invocan a sí mismas inmediatamente.

¿Cuál es la relación entre un *callback asíncrono* y una IIF? Un *callback asíncrono* es una IIF que es invocada de forma asíncrona en lugar de síncrona.

### ¿Closure síncrona?

Ahora que hemos re-etiquetado los *callbacks síncronos* como IIFs, podemos volver a nuestra pregunta principal: ¿son las IIFs un ejemplo de closure? Obviamente, la IIF tendría que referenciar variable(s) de un scope externo para tener alguna posibilidad de ser una closure. La IIF `formatIDLabel(..)` de antes no referencia ninguna variable fuera de su propio scope, así que definitivamente no es una closure.

¿Qué hay de una IIF que sí tiene referencias externas? ¿Eso es closure?

```js
function printLabels(labels) {
    var list = document.getElementById("labelsList");

    labels.forEach(
        function renderLabel(label){
            var li = document.createElement("li");
            li.innerText = label;
            list.appendChild(li);
        }
    );
}
```

La IIF interna `renderLabel(..)` referencia a `list` del scope envolvente, así que es una IIF que *podría* tener closure. Pero aquí es donde importa la definición/modelo que elijamos para la closure:

* Si `renderLabel(..)` es una **función que es pasada a algún otro lugar**, y esa función es luego invocada, entonces sí, `renderLabel(..)` está ejerciendo una closure, porque la closure es lo que preservó su acceso a su cadena de scopes original.

* Pero si, como en el modelo conceptual alternativo del Capítulo 7, `renderLabel(..)` permanece en su lugar, y solo una referencia a ella es pasada a `forEach(..)`, ¿hay alguna necesidad de que una closure preserve la cadena de scopes de `renderLabel(..)`, mientras se ejecuta de forma síncrona justo dentro de su propio scope?

No. Eso es solo scope léxico normal.

Para entender por qué, considera esta forma alternativa de `printLabels(..)`:

```js
function printLabels(labels) {
    var list = document.getElementById("labelsList");

    for (let label of labels) {
        // just a normal function call in its own
        // scope, right? That's not really closure!
        renderLabel(label);
    }

    // **************

    function renderLabel(label) {
        var li = document.createElement("li");
        li.innerText = label;
        list.appendChild(li);
    }
}
```

Estas dos versiones de `printLabels(..)` son esencialmente lo mismo.

La última definitivamente no es un ejemplo de closure, al menos no en ningún sentido útil u observable. Es solo scope léxico. La primera versión, con `forEach(..)` llamando a nuestra referencia a función, es esencialmente lo mismo. Tampoco es closure, sino simplemente una llamada a función de scope léxico de toda la vida.

### Diferir a la closure

Por cierto, el Capítulo 7 mencionó brevemente la aplicación parcial y el currying (los cuales *sí* dependen de la closure). Este es un escenario interesante donde se puede usar el currying manual:

```js
function printLabels(labels) {
    var list = document.getElementById("labelsList");
    var renderLabel = renderTo(list);

    // definitely closure this time!
    labels.forEach( renderLabel );

    // **************

    function renderTo(list) {
        return function createLabel(label){
            var li = document.createElement("li");
            li.innerText = label;
            list.appendChild(li);
        };
    }
}
```

La función interna `createLabel(..)`, que asignamos a `renderLabel`, está cerrada (closed over) sobre `list`, así que definitivamente se está utilizando una closure.

La closure nos permite recordar `list` para más tarde, mientras diferimos la ejecución de la lógica real de creación de etiquetas desde la llamada a `renderTo(..)` hacia las subsiguientes invocaciones de `forEach(..)` de la IIF `createLabel(..)`. Eso puede ser solo un breve momento aquí, pero podría pasar cualquier cantidad de tiempo, ya que la closure tiende un puente de llamada a llamada.

## Variaciones del módulo clásico

El Capítulo 8 explicó el patrón de módulo clásico, que puede verse así:

```js
var StudentList = (function defineModule(Student){
    var elems = [];

    var publicAPI = {
        renderList() {
            // ..
        }
    };

    return publicAPI;

})(Student);
```

Nota que estamos pasando `Student` (otra instancia de módulo) como una dependencia. Pero hay muchas variaciones útiles de esta forma de módulo con las que te puedes encontrar. Algunas pistas para reconocer estas variaciones:

* ¿Conoce el módulo su propia API?
* Aunque usemos un cargador de módulos sofisticado, sigue siendo solo un módulo clásico
* Algunos módulos necesitan funcionar universalmente

### ¿Dónde está mi API?

Primero, la mayoría de los módulos clásicos no definen ni usan un `publicAPI` de la forma que he mostrado en este código. En cambio, típicamente se ven así:

```js
var StudentList = (function defineModule(Student){
    var elems = [];

    return {
        renderList() {
            // ..
        }
    };

})(Student);
```

La única diferencia aquí es retornar directamente el objeto que sirve como la API pública del módulo, en lugar de guardarlo primero en una variable interna `publicAPI`. Esta es de lejos la forma en que se definen la mayoría de los módulos clásicos.

Pero yo prefiero firmemente, y siempre uso, la forma `publicAPI` anterior. Dos razones:

* `publicAPI` es un descriptor semántico que ayuda a la legibilidad al hacer más obvio cuál es el propósito del objeto.

* Almacenar una variable interna `publicAPI` que referencia el mismo objeto de API pública externo que se retorna puede ser útil si necesitas acceder o modificar la API durante el tiempo de vida del módulo.

    Por ejemplo, podrías querer llamar a una de las funciones expuestas públicamente desde dentro del módulo. O podrías querer agregar o quitar métodos dependiendo de ciertas condiciones, o actualizar el valor de una propiedad expuesta.

    Sea cual sea el caso, simplemente me parece bastante tonto que *no* mantuviéramos una referencia para acceder a nuestra propia API. ¿Verdad?

### Definición de módulo asíncrona (AMD)

Otra variación de la forma de módulo clásico son los módulos estilo AMD (populares hace varios años), como los soportados por la utilidad RequireJS:

```js
define([ "./Student" ],function StudentList(Student){
    var elems = [];

    return {
        renderList() {
            // ..
        }
    };
});
```

Si miras de cerca `StudentList(..)`, es una función fábrica de módulo clásico. Dentro de la maquinaria de `define(..)` (provista por RequireJS), la función `StudentList(..)` se ejecuta, pasándole cualquier otra instancia de módulo declarada como dependencia. El valor de retorno es un objeto que representa la API pública del módulo.

Esto se basa exactamente en los mismos principios (incluyendo cómo funciona la closure) que exploramos con los módulos clásicos.

### Módulos universales (UMD)

La variación final que veremos es UMD, que es menos un formato específico y exacto, y más una colección de formatos muy similares. Fue diseñado para crear mejor interoperabilidad (sin ninguna conversión mediante herramienta de build) para módulos que pueden cargarse en navegadores, mediante cargadores estilo AMD, o en Node. Personalmente, todavía publico muchas de mis librerías de utilidades usando una forma de UMD.

Aquí está la estructura típica de un UMD:

```js
(function UMD(name,context,definition){
    // loaded by an AMD-style loader?
    if (
        typeof define === "function" &&
        define.amd
    ) {
        define(definition);
    }
    // in Node?
    else if (
        typeof module !== "undefined" &&
        module.exports
    ) {
        module.exports = definition(name,context);
    }
    // assume standalone browser script
    else {
        context[name] = definition(name,context);
    }
})("StudentList",this,function DEF(name,context){

    var elems = [];

    return {
        renderList() {
            // ..
        }
    };

});
```

Aunque pueda verse un poco inusual, UMD es en realidad solo una IIFE.

Lo diferente es que la parte principal de la function expression (en la parte superior) de la IIFE contiene una serie de sentencias `if..else if` para detectar en cuál de los tres entornos soportados está siendo cargado el módulo.

El `()` final que normalmente invoca a una IIFE está recibiendo tres argumentos: `"StudentsList"`, `this` y otra function expression. Si haces coincidir esos argumentos con sus parámetros, verás que son: `name`, `context` y `definition`, respectivamente. `"StudentList"` (`name`) es la etiqueta de nombre para el módulo, principalmente por si se define como una variable global. `this` (`context`) es generalmente el `window` (también conocido como objeto global; ver Capítulo 4) para definir el módulo por su nombre.

`definition(..)` es invocada para realmente recuperar la definición del módulo, y notarás que, efectivamente, ¡eso es solo una forma de módulo clásico!

No hay duda de que, al momento de escribir esto, los ESM (ES Modules) se están volviendo populares y de uso generalizado rápidamente. Pero con millones y millones de módulos escritos a lo largo de los últimos 20 años, todos usando alguna variación pre-ESM de los módulos clásicos, siguen siendo muy importantes de poder leer y entender cuando te encuentres con ellos.

[^fowlerIOC]: *Inversion of Control*, Martin Fowler, https://martinfowler.com/bliki/InversionOfControl.html, 26 June 2005.
