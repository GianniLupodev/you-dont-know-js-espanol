# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Capítulo 3: La Cadena de Scope

Los Capítulos 1 y 2 establecieron una definición concreta de *lexical scope* (y sus partes) e ilustraron metáforas útiles para su fundamento conceptual. Antes de continuar con este capítulo, buscá a alguien más para explicarle (por escrito o en voz alta), con tus propias palabras, qué es el lexical scope y por qué es útil entenderlo.

Eso parece un paso que podrías saltear, pero descubrí que realmente ayuda tomarse el tiempo de reformular estas ideas como explicaciones para otros. ¡Eso ayuda a nuestro cerebro a digerir lo que estamos aprendiendo!

Ahora es momento de meternos en los detalles finos, así que esperá que las cosas se vuelvan mucho más detalladas de acá en adelante. Seguí adelante, de todos modos, porque estas discusiones realmente dejan en claro cuánto es lo que todavía *no sabemos* sobre el scope. Asegurate de tomarte tu tiempo con el texto y con todos los fragmentos de código proporcionados.

Para refrescar el contexto de nuestro ejemplo recurrente, recordemos la ilustración codificada por colores de las burbujas de scope anidadas, del Capítulo 2, Figura 2:

<figure>
    <img src="images/fig2.png" width="500" alt="Colored Scope Bubbles" align="center">
    <figcaption><em>Fig. 2 (Ch. 2): Colored Scope Bubbles</em></figcaption>
    <br><br>
</figure>

Las conexiones entre los scopes que están anidados dentro de otros scopes se llaman la cadena de scope, que determina el camino a lo largo del cual se puede acceder a las variables. La cadena es dirigida, lo que significa que la búsqueda se mueve solamente hacia arriba/afuera.

## La "Búsqueda" Es (Mayormente) Conceptual

En la Figura 2, fijate en el color de la referencia a la variable `students` en el bucle `for`. ¿Cómo determinamos exactamente que es una canica RED(1)?

En el Capítulo 2, describimos el acceso en tiempo de ejecución a una variable como una "búsqueda", donde el *Engine* tiene que empezar preguntándole al *Scope Manager* del scope actual si conoce un identificador/variable, y proceder hacia arriba/afuera de vuelta a través de la cadena de scopes anidados (hacia el global scope) hasta encontrarla, si es que lo hace. La búsqueda se detiene en cuanto se encuentra la primera declaración con nombre coincidente en un balde de scope.

El proceso de búsqueda determinó así que `students` es una canica RED(1), porque no habíamos encontrado todavía un nombre de variable coincidente mientras recorríamos la cadena de scope, hasta que llegamos al global scope RED(1) final.

De manera similar, se determina que `studentID` en el statement `if` es una canica BLUE(2).

Esta sugerencia de un proceso de búsqueda en tiempo de ejecución funciona bien para la comprensión conceptual, pero no es realmente como funcionan las cosas usualmente en la práctica.

El color del balde de una canica (es decir, la metainformación de qué scope proviene una variable) *generalmente se determina* durante el procesamiento inicial de compilación. Como el lexical scope prácticamente queda finalizado en ese punto, el color de una canica no cambiará en base a nada que pueda suceder después durante el tiempo de ejecución.

Dado que el color de la canica se conoce desde la compilación, y es inmutable, esta información probablemente se almacenaría con (o al menos sería accesible desde) la entrada de cada variable en el AST; esa información luego es usada explícitamente por las instrucciones ejecutables que constituyen el tiempo de ejecución del programa.

En otras palabras, el *Engine* (del Capítulo 2) no necesita buscar a través de un montón de scopes para averiguar de qué balde de scope proviene una variable. ¡Esa información ya se conoce! Evitar la necesidad de una búsqueda en tiempo de ejecución es un beneficio clave de optimización del lexical scope. El tiempo de ejecución opera de manera más eficiente sin gastar tiempo en todas estas búsquedas.

Pero dije "...generalmente se determina..." hace un momento, con respecto a averiguar el color de una canica durante la compilación. Entonces, ¿en qué caso *no* se conocería durante la compilación?

Considerá una referencia a una variable que no está declarada en ninguno de los scopes léxicamente disponibles en el archivo actual—ver *Get Started*, Capítulo 1, que afirma que cada archivo es su propio programa separado desde la perspectiva de la compilación de JS. Si no se encuentra ninguna declaración, eso no es *necesariamente* un error. Otro archivo (programa) en el tiempo de ejecución bien podría declarar esa variable en el global scope compartido.

Así que la determinación definitiva de si la variable alguna vez fue declarada apropiadamente en algún balde accesible puede necesitar diferirse al tiempo de ejecución.

Cualquier referencia a una variable que inicialmente está *sin declarar* queda como una canica sin color durante la compilación de ese archivo; este color no puede determinarse hasta que otro(s) archivo(s) relevante(s) hayan sido compilados y comience el tiempo de ejecución de la aplicación. Esa búsqueda diferida eventualmente resolverá el color a cualquiera que sea el scope en el que se encuentra la variable (probablemente el global scope).

Sin embargo, esta búsqueda solo sería necesaria una vez por variable como máximo, ya que nada más durante el tiempo de ejecución podría cambiar después el color de esa canica.

La sección "Fallos de Búsqueda" del Capítulo 2 cubre qué sucede si una canica termina estando todavía sin color en el momento en que su referencia se ejecuta en tiempo de ejecución.

## Shadowing

El "Shadowing" podría sonar misterioso y un poco turbio. Pero no te preocupes, ¡es completamente legítimo!

Nuestro ejemplo recurrente de estos capítulos usa diferentes nombres de variables a lo largo de los límites de scope. Como todos tienen nombres únicos, en cierto modo no importaría si todos ellos estuvieran simplemente almacenados en un solo balde (como RED(1)).

Donde tener diferentes baldes de lexical scope empieza a importar más es cuando tenés dos o más variables, cada una en diferentes scopes, con los mismos nombres léxicos. Un solo scope no puede tener dos o más variables con el mismo nombre; tales referencias múltiples se asumirían como una sola variable.

Así que si necesitás mantener dos o más variables del mismo nombre, tenés que usar scopes separados (a menudo anidados). Y en ese caso, es muy relevante cómo están dispuestos los diferentes baldes de scope.

Considerá:

```js
var studentName = "Suzy";

function printStudent(studentName) {
    studentName = studentName.toUpperCase();
    console.log(studentName);
}

printStudent("Frank");
// FRANK

printStudent(studentName);
// SUZY

console.log(studentName);
// Suzy
```

| TIP: |
| :--- |
| Antes de que sigas, tomate un tiempo para analizar este código usando las diversas técnicas/metáforas que cubrimos en el libro. En particular, asegurate de identificar los colores de las canicas/burbujas en este fragmento. ¡Es buena práctica! |

La variable `studentName` en la línea 1 (el statement `var studentName = ..`) crea una canica RED(1). La variable con el mismo nombre se declara como una canica BLUE(2) en la línea 3, el parámetro en la definición de la función `printStudent(..)`.

¿De qué color de canica será `studentName` en el statement de asignación `studentName = studentName.toUpperCase()` y en el statement `console.log(studentName)`? Las tres referencias a `studentName` serán BLUE(2).

Con la noción conceptual de la "búsqueda", afirmamos que empieza con el scope actual y se abre camino hacia afuera/arriba, deteniéndose en cuanto se encuentra una variable coincidente. El `studentName` BLUE(2) se encuentra enseguida. El `studentName` RED(1) ni siquiera se considera.

Este es un aspecto clave del comportamiento del lexical scope, llamado *shadowing*. La variable `studentName` BLUE(2) (parámetro) hace shadowing sobre el `studentName` RED(1). Así que el parámetro está haciendo shadowing sobre la variable global (sombreada). ¡Repetí esa oración para vos mismo unas cuantas veces para asegurarte de tener la terminología clara!

Por eso la reasignación de `studentName` afecta solamente a la variable interna (parámetro): el `studentName` BLUE(2), no el `studentName` global RED(1).

Cuando elegís hacer shadowing sobre una variable de un scope externo, un impacto directo es que desde ese scope hacia adentro/abajo (a través de cualquier scope anidado) ahora es imposible que cualquier canica se coloree como la variable sombreada—(RED(1), en este caso). En otras palabras, cualquier referencia al identificador `studentName` corresponderá a esa variable de parámetro, nunca a la variable global `studentName`. Es léxicamente imposible referenciar al `studentName` global en cualquier parte dentro de la función `printStudent(..)` (o desde cualquier scope anidado).

### Truco para Deshacer el Shadowing Global

Por favor, tené cuidado: aprovechar la técnica que estoy por describir no es muy buena práctica, ya que es limitada en utilidad, confusa para los lectores de tu código, y propensa a invitar bugs a tu programa. La cubro solo porque podrías encontrarte con este comportamiento en programas existentes, y entender lo que está pasando es crítico para no tropezarte.

*Sí* es posible acceder a una variable global desde un scope donde esa variable ha sido sombreada, pero no a través de una referencia típica de identificador léxico.

En el global scope (RED(1)), las declaraciones `var` y las declaraciones `function` también se exponen a sí mismas como propiedades (del mismo nombre que el identificador) en el *objeto global*—esencialmente una representación en objeto del global scope. Si has escrito JS para un entorno de navegador, probablemente reconozcas el objeto global como `window`. Eso no es *enteramente* preciso, pero es suficientemente bueno para nuestra discusión. En el próximo capítulo, exploraremos más el tema del global scope/objeto.

Considerá este programa, ejecutado específicamente como un archivo .js independiente en un entorno de navegador:

```js
var studentName = "Suzy";

function printStudent(studentName) {
    console.log(studentName);
    console.log(window.studentName);
}

printStudent("Frank");
// "Frank"
// "Suzy"
```

¿Notás la referencia `window.studentName`? Esta expression está accediendo a la variable global `studentName` como una propiedad en `window` (que por ahora estamos fingiendo que es sinónimo del objeto global). Esa es la única manera de acceder a una variable sombreada desde dentro de un scope donde la variable que hace shadowing está presente.

El `window.studentName` es un espejo de la variable global `studentName`, no una copia instantánea separada. Los cambios a una siguen viéndose desde la otra, en cualquier dirección. Podés pensar en `window.studentName` como un getter/setter que accede a la variable `studentName` real. De hecho, incluso podés *agregar* una variable al global scope creando/estableciendo una propiedad en el objeto global.

| WARNING: |
| :--- |
| Recordá: que *puedas* no significa que *debas*. No hagas shadowing sobre una variable global a la que necesitás acceder, y a la inversa, evitá usar este truco para acceder a una variable global que hayas sombreado. ¡Y definitivamente no confundas a los lectores de tu código creando variables globales como propiedades de `window` en lugar de con declaraciones formales! |

Este pequeño "truco" solo funciona para acceder a una variable del global scope (no a una variable sombreada de un scope anidado), e incluso en ese caso, solo a una que fue declarada con `var` o `function`.

Otras formas de declaraciones del global scope no crean propiedades espejadas en el objeto global:

```js
var one = 1;
let notOne = 2;
const notTwo = 3;
class notThree {}

console.log(window.one);       // 1
console.log(window.notOne);    // undefined
console.log(window.notTwo);    // undefined
console.log(window.notThree);  // undefined
```

Las variables (¡sin importar cómo se declaren!) que existen en cualquier otro scope que no sea el global scope son completamente inaccesibles desde un scope donde han sido sombreadas:

```js
var special = 42;

function lookingFor(special) {
    // The identifier `special` (parameter) in this
    // scope is shadowed inside keepLooking(), and
    // is thus inaccessible from that scope.

    function keepLooking() {
        var special = 3.141592;
        console.log(special);
        console.log(window.special);
    }

    keepLooking();
}

lookingFor(112358132134);
// 3.141592
// 42
```

El `special` global RED(1) está sombreado por el `special` BLUE(2) (parámetro), y el `special` BLUE(2) a su vez está sombreado por el `special` GREEN(3) dentro de `keepLooking()`. Todavía podemos acceder al `special` RED(1) usando la referencia indirecta `window.special`. Pero no hay manera de que `keepLooking()` acceda al `special` BLUE(2) que contiene el número `112358132134`.

### Copiar No Es Acceder

Me han hecho la siguiente pregunta de "¿Pero qué pasa con...?" docenas de veces. Considerá:

```js
var special = 42;

function lookingFor(special) {
    var another = {
        special: special
    };

    function keepLooking() {
        var special = 3.141592;
        console.log(special);
        console.log(another.special);  // Ooo, tricky!
        console.log(window.special);
    }

    keepLooking();
}

lookingFor(112358132134);
// 3.141592
// 112358132134
// 42
```

¡Ah! Entonces, ¿esta técnica del objeto `another` desmiente mi afirmación de que el parámetro `special` es "completamente inaccesible" desde dentro de `keepLooking()`? No, la afirmación sigue siendo correcta.

`special: special` está copiando el valor de la variable de parámetro `special` dentro de otro contenedor (una propiedad del mismo nombre). Por supuesto, si ponés un valor en otro contenedor, el shadowing ya no se aplica (¡a menos que `another` también estuviera sombreado!). Pero eso no significa que estemos accediendo al parámetro `special`; significa que estamos accediendo a la copia del valor que tenía en ese momento, por medio de *otro* contenedor (propiedad de objeto). No podemos reasignar el parámetro `special` BLUE(2) a un valor diferente desde dentro de `keepLooking()`.

Otro "¡Pero...!?" que quizás estés por plantear: ¿qué pasa si hubiera usado objetos o arrays como los valores en lugar de los números (`112358132134`, etc.)? ¿El que tengamos referencias a objetos en lugar de copias de valores primitivos "arreglaría" la inaccesibilidad?

No. Mutar el contenido del valor de objeto a través de una copia de referencia **no** es lo mismo que acceder léxicamente a la variable en sí. Todavía no podemos reasignar el parámetro `special` BLUE(2).

### Shadowing Ilegal

No todas las combinaciones de shadowing de declaraciones están permitidas. `let` puede hacer shadowing sobre `var`, pero `var` no puede hacer shadowing sobre `let`:

```js
function something() {
    var special = "JavaScript";

    {
        let special = 42;   // totally fine shadowing

        // ..
    }
}

function another() {
    // ..

    {
        let special = "JavaScript";

        {
            var special = "JavaScript";
            // ^^^ Syntax Error

            // ..
        }
    }
}
```

Fijate que en la función `another()`, la declaración interna `var special` está intentando declarar un `special` de alcance de función, lo cual en sí mismo está bien (como se muestra en la función `something()`).

La descripción del error de sintaxis en este caso indica que `special` ya ha sido definido, pero ese mensaje de error es un poco engañoso—de nuevo, ningún error de este tipo ocurre en `something()`, ya que el shadowing en general está permitido sin problemas.

La verdadera razón por la que se genera como un `SyntaxError` es porque el `var` básicamente está intentando "cruzar el límite" de (o saltar por encima de) la declaración `let` del mismo nombre, lo cual no está permitido.

Esa prohibición de cruzar límites se detiene efectivamente en cada límite de función, así que esta variante no genera ninguna excepción:

```js
function another() {
    // ..

    {
        let special = "JavaScript";

        ajax("https://some.url",function callback(){
            // totally fine shadowing
            var special = "JavaScript";

            // ..
        });
    }
}
```

Resumen: `let` (en un scope interno) siempre puede hacer shadowing sobre un `var` de un scope externo. `var` (en un scope interno) solo puede hacer shadowing sobre un `let` de un scope externo si hay un límite de función en el medio.

## Scope del Nombre de Función

Como ya has visto, una declaración `function` se ve así:

```js
function askQuestion() {
    // ..
}
```

Y como se discutió en los Capítulos 1 y 2, tal declaración `function` creará un identificador en el scope circundante (en este caso, el global scope) llamado `askQuestion`.

¿Qué pasa con este programa?

```js
var askQuestion = function(){
    // ..
};
```

Lo mismo es cierto para la variable `askQuestion` que se crea. Pero como es una function expression—una definición de función usada como valor en lugar de una declaración independiente—la función en sí no hará "hoisting" (ver Capítulo 5).

Una diferencia importante entre las declaraciones `function` y las function expressions es qué le sucede al identificador de nombre de la función. Considerá una named function expression:

```js
var askQuestion = function ofTheTeacher(){
    // ..
};
```

Sabemos que `askQuestion` termina en el scope externo. Pero, ¿qué pasa con el identificador `ofTheTeacher`? Para las declaraciones `function` formales, el identificador de nombre termina en el scope externo/circundante, así que podría ser razonable asumir que ese es el caso acá. Pero `ofTheTeacher` se declara como un identificador **dentro de la función misma**:

```js
var askQuestion = function ofTheTeacher() {
    console.log(ofTheTeacher);
};

askQuestion();
// function ofTheTeacher()...

console.log(ofTheTeacher);
// ReferenceError: ofTheTeacher is not defined
```

| NOTA: |
| :--- |
| En realidad, `ofTheTeacher` no está exactamente *en el scope de la función*. El Apéndice A, "Scopes Implícitos" lo explicará con más detalle. |

No solo `ofTheTeacher` se declara dentro de la función en lugar de afuera, sino que también se define como de solo lectura:

```js
var askQuestion = function ofTheTeacher() {
    "use strict";
    ofTheTeacher = 42;   // TypeError

    //..
};

askQuestion();
// TypeError
```

Como usamos strict mode, el fallo de asignación se reporta como un `TypeError`; en modo no estricto, tal asignación falla silenciosamente sin excepción.

¿Qué pasa cuando una function expression no tiene un identificador de nombre?

```js
var askQuestion = function(){
   // ..
};
```

Una function expression con un identificador de nombre se denomina "named function expression", pero una sin un identificador de nombre se denomina "anonymous function expression". Las anonymous function expressions claramente no tienen ningún identificador de nombre que afecte a ningún scope.

| NOTA: |
| :--- |
| Discutiremos las function expressions con nombre vs. anónimas con mucho más detalle, incluyendo qué factores afectan la decisión de usar una u otra, en el Apéndice A. |

## Arrow Functions

ES6 agregó una forma adicional de function expression al lenguaje, llamada "arrow functions":

```js
var askQuestion = () => {
    // ..
};
```

La arrow function `=>` no requiere la palabra `function` para definirla. Además, los `( .. )` alrededor de la lista de parámetros son opcionales en algunos casos simples. Del mismo modo, las `{ .. }` alrededor del cuerpo de la función son opcionales en algunos casos. Y cuando se omiten las `{ .. }`, se devuelve un valor de retorno sin usar una palabra clave `return`.

| NOTA: |
| :--- |
| El atractivo de las arrow functions `=>` a menudo se vende como "sintaxis más corta", y se afirma que eso equivale a un código objetivamente más legible. Esta afirmación es dudosa en el mejor de los casos, y creo que directamente equivocada. Profundizaremos en la "legibilidad" de las diversas formas de función en el Apéndice A. |

Las arrow functions son léxicamente anónimas, lo que significa que no tienen ningún identificador directamente relacionado que haga referencia a la función. La asignación a `askQuestion` crea un nombre inferido de "askQuestion", pero eso **no es lo mismo que no ser anónima**:

```js
var askQuestion = () => {
    // ..
};

askQuestion.name;   // askQuestion
```

Las arrow functions logran su brevedad sintáctica a expensas de tener que hacer malabares mentales con un montón de variaciones para diferentes formas/condiciones. Solo algunas, por ejemplo:

```js
() => 42;

id => id.toUpperCase();

(id,name) => ({ id, name });

(...args) => {
    return args[args.length - 1];
};
```

La verdadera razón por la que traigo a colación las arrow functions es por la afirmación común pero incorrecta de que las arrow functions de algún modo se comportan diferente con respecto al lexical scope que las funciones `function` estándar.

Esto es incorrecto.

Más allá de ser anónimas (y de no tener forma declarativa), las arrow functions `=>` tienen las mismas reglas de lexical scope que tienen las funciones `function`. Una arrow function, con o sin `{ .. }` alrededor de su cuerpo, igual crea un balde de scope separado, interno y anidado. Las declaraciones de variables dentro de este balde de scope anidado se comportan igual que en un scope de `function`.

## Retrocediendo

Cuando se define una función (declaración o expression), se crea un nuevo scope. El posicionamiento de los scopes anidados unos dentro de otros crea una jerarquía natural de scope a lo largo del programa, llamada la cadena de scope. La cadena de scope controla el acceso a las variables, orientada direccionalmente hacia arriba y hacia afuera.

Cada nuevo scope ofrece una hoja en blanco, un espacio para contener su propio conjunto de variables. Cuando un nombre de variable se repite en diferentes niveles de la cadena de scope, ocurre el shadowing, que impide el acceso a la variable externa desde ese punto hacia adentro.

A medida que damos un paso atrás de estos detalles más finos, el próximo capítulo cambia el foco hacia el scope primario que todos los programas de JS incluyen: el global scope.
