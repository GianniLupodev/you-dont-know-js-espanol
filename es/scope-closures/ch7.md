# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Capítulo 7: Usando Closures

Hasta este punto, nos hemos enfocado en los pormenores del lexical scope, y en cómo eso afecta la organización y el uso de las variables en nuestros programas.

Nuestra atención se desplaza de nuevo hacia un nivel más amplio de abstracción, hacia el tema históricamente algo intimidante de closure. ¡No te preocupes! No necesitás un título avanzado en ciencias de la computación para entenderlo. Nuestro objetivo general en este libro no es simplemente entender el scope, sino usarlo de manera más efectiva en la estructura de nuestros programas; closure es central para ese esfuerzo.

Recordá la conclusión principal del Capítulo 6: el principio de *mínima exposición* (POLE) nos anima a usar scope de bloque (y de función) para limitar la exposición del scope de las variables. Esto ayuda a mantener el código comprensible y mantenible, y ayuda a evitar muchas trampas del scope (es decir, colisión de nombres, etc.).

Closure se construye sobre este enfoque: para las variables que necesitamos usar a lo largo del tiempo, en lugar de colocarlas en scopes externos más grandes, podemos encapsularlas (darles un scope más acotado) pero aun así preservar el acceso desde dentro de las funciones, para un uso más amplio. Las funciones *recuerdan* estas variables con scope referenciadas mediante closure.

Ya vimos un ejemplo de este tipo de closure en el capítulo anterior (`factorial(..)` en el Capítulo 6), y casi con seguridad ya lo usaste en tus propios programas. Si alguna vez escribiste un callback que accede a variables fuera de su propio scope... ¡¿adiviná qué?! Eso es closure.

Closure es una de las características de lenguaje más importantes jamás inventadas en programación—subyace a paradigmas de programación mayores, incluyendo la Programación Funcional (FP), los módulos, e incluso un poco del diseño orientado a clases. Sentirse cómodo con closure es requisito para dominar JS y aprovechar efectivamente muchos patrones de diseño importantes a lo largo de tu código.

Abordar todos los aspectos de closure requiere una intimidante montaña de discusión y código a lo largo de este capítulo. Asegurate de tomarte tu tiempo y de sentirte cómodo con cada parte antes de pasar a la siguiente.

## Ver el Closure

Closure es originalmente un concepto matemático, del cálculo lambda. Pero no voy a enumerar fórmulas matemáticas ni a usar un montón de notación y jerga para definirlo.

En cambio, me voy a enfocar en una perspectiva práctica. Empezaremos definiendo closure en términos de lo que podemos observar en el comportamiento diferente de nuestros programas, en contraste con cómo sería si closure no estuviera presente en JS. Sin embargo, más adelante en este capítulo, vamos a dar vuelta closure para mirarlo desde una *perspectiva alternativa*.

Closure es un comportamiento de las funciones y solo de las funciones. Si no estás tratando con una función, closure no aplica. Un objeto no puede tener closure, ni una clase tiene closure (aunque sus funciones/métodos podrían tenerlo). Solo las funciones tienen closure.

Para que closure sea observado, una función debe ser invocada, y específicamente debe ser invocada en una rama diferente de la scope chain respecto de donde fue definida originalmente. Una función que se ejecuta en el mismo scope donde fue definida no exhibiría ningún comportamiento observablemente diferente con o sin la posibilidad de closure; según la perspectiva y la definición observacional, eso no es closure.

Veamos algo de código, anotado con los colores de burbuja de scope relevantes (ver Capítulo 2):

```js
// outer/global scope: RED(1)

function lookupStudent(studentID) {
    // function scope: BLUE(2)

    var students = [
        { id: 14, name: "Kyle" },
        { id: 73, name: "Suzy" },
        { id: 112, name: "Frank" },
        { id: 6, name: "Sarah" }
    ];

    return function greetStudent(greeting){
        // function scope: GREEN(3)

        var student = students.find(
            student => student.id == studentID
        );

        return `${ greeting }, ${ student.name }!`;
    };
}

var chosenStudents = [
    lookupStudent(6),
    lookupStudent(112)
];

// accessing the function's name:
chosenStudents[0].name;
// greetStudent

chosenStudents[0]("Hello");
// Hello, Sarah!

chosenStudents[1]("Howdy");
// Howdy, Frank!
```

Lo primero que hay que notar sobre este código es que la función externa `lookupStudent(..)` crea y devuelve una función interna llamada `greetStudent(..)`. `lookupStudent(..)` es llamada dos veces, produciendo dos instancias separadas de su función interna `greetStudent(..)`, ambas guardadas en el array `chosenStudents`.

Verificamos que ese es el caso revisando la propiedad `.name` de la función devuelta y guardada en `chosenStudents[0]`, y efectivamente es una instancia de la función interna `greetStudent(..)`.

Después de que cada llamada a `lookupStudent(..)` termina, parecería que todas sus variables internas serían descartadas y recolectadas por el GC (garbage collection). La función interna es lo único que parece ser devuelto y preservado. Pero aquí es donde el comportamiento difiere de maneras que podemos empezar a observar.

Si bien `greetStudent(..)` sí recibe un único argumento como el parámetro llamado `greeting`, también hace referencia tanto a `students` como a `studentID`, identificadores que provienen del scope envolvente de `lookupStudent(..)`. Cada una de esas referencias desde la función interna hacia la variable en un scope externo se llama *closure*. En términos académicos, cada instancia de `greetStudent(..)` *cierra sobre* (*closes over*) las variables externas `students` y `studentID`.

Entonces, ¿qué hacen esos closures aquí, en un sentido concreto y observable?

Closure le permite a `greetStudent(..)` seguir accediendo a esas variables externas incluso después de que el scope externo haya terminado (cuando cada llamada a `lookupStudent(..)` se completa). En lugar de que las instancias de `students` y `studentID` sean recolectadas por el GC, permanecen en memoria. En un momento posterior, cuando cualquiera de las instancias de la función `greetStudent(..)` es invocada, esas variables siguen ahí, conservando sus valores actuales.

Si las funciones de JS no tuvieran closure, la finalización de cada llamada a `lookupStudent(..)` desarmaría inmediatamente su scope y recolectaría con el GC las variables `students` y `studentID`. Cuando más tarde llamáramos a una de las funciones `greetStudent(..)`, ¿qué pasaría entonces?

Si `greetStudent(..)` intentara acceder a lo que creía que era una bolilla BLUE(2), pero esa bolilla en realidad no existiera (ya), la suposición razonable es que deberíamos obtener un `ReferenceError`, ¿cierto?

Pero no obtenemos un error. El hecho de que la ejecución de `chosenStudents[0]("Hello")` funcione y nos devuelva el mensaje "Hello, Sarah!", significa que todavía fue capaz de acceder a las variables `students` y `studentID`. ¡Esta es una observación directa de closure!

### Closure Señalado

En realidad, pasamos por alto un pequeño detalle en la discusión anterior que supongo que muchos lectores no notaron!

Debido a lo escueta que es la sintaxis para las arrow functions `=>`, es fácil olvidar que de todos modos crean un scope (como se afirmó en "Arrow Functions" en el Capítulo 3). La arrow function `student => student.id == studentID` está creando otra burbuja de scope dentro del function scope de `greetStudent(..)`.

Construyendo sobre la metáfora de baldes y burbujas de colores del Capítulo 2, si estuviéramos creando un diagrama coloreado para este código, hay un cuarto scope en este nivel de anidamiento más interno, así que necesitaríamos un cuarto color; quizás elegiríamos ORANGE(4) para ese scope:

```js
var student = students.find(
    student =>
        // function scope: ORANGE(4)
        student.id == studentID
);
```

La referencia BLUE(2) `studentID` está en realidad dentro del scope ORANGE(4) en lugar del scope GREEN(3) de `greetStudent(..)`; además, el parámetro `student` de la arrow function es ORANGE(4), haciéndole shadowing al `student` GREEN(3).

La consecuencia aquí es que esta arrow function pasada como callback al método `find(..)` del array tiene que mantener el closure sobre `studentID`, en lugar de que `greetStudent(..)` mantenga ese closure. No es gran cosa, ya que todo sigue funcionando como se espera. Simplemente es importante no pasar por alto el hecho de que incluso las arrow functions más chiquitas pueden sumarse a la fiesta del closure.

### Sumando Closures

Examinemos uno de los ejemplos canónicos citados a menudo para closure:

```js
function adder(num1) {
    return function addTo(num2){
        return num1 + num2;
    };
}

var add10To = adder(10);
var add42To = adder(42);

add10To(15);    // 25
add42To(9);     // 51
```

Cada instancia de la función interna `addTo(..)` está cerrando sobre su propia variable `num1` (con valores `10` y `42`, respectivamente), así que esos `num1` no desaparecen solo porque `adder(..)` termine. Cuando más tarde invocamos una de esas instancias internas de `addTo(..)`, como la llamada `add10To(15)`, su variable `num1` cerrada todavía existe y aún conserva el valor original `10`. La operación es por lo tanto capaz de realizar `10 + 15` y devolver la respuesta `25`.

Un detalle importante podría haber sido demasiado fácil de pasar por alto en ese párrafo anterior, así que reforcémoslo: closure está asociado con una instancia de una función, en lugar de con su única definición léxica. En el fragmento precedente, hay solo una función interna `addTo(..)` definida dentro de `adder(..)`, así que podría parecer que eso implicaría un solo closure.

Pero en realidad, cada vez que la función externa `adder(..)` se ejecuta, se crea una *nueva* instancia de la función interna `addTo(..)`, y para cada nueva instancia, un nuevo closure. Así que cada instancia de función interna (etiquetadas `add10To(..)` y `add42To(..)` en nuestro programa) tiene su propio closure sobre su propia instancia del entorno de scope de esa ejecución de `adder(..)`.

Aunque closure se basa en el lexical scope, que se maneja en tiempo de compilación, closure se observa como una característica en tiempo de ejecución de las instancias de función.

### Enlace Vivo, No una Instantánea

En ambos ejemplos de las secciones anteriores, **leímos el valor de una variable** que estaba retenida en un closure. Eso hace que se sienta como si closure pudiera ser una instantánea de un valor en un momento dado. De hecho, esa es una idea equivocada común.

Closure es en realidad un enlace vivo, que preserva el acceso a la variable completa en sí. No estamos limitados a simplemente leer un valor; ¡la variable cerrada también puede ser actualizada (reasignada)! Al cerrar sobre una variable en una función, podemos seguir usando esa variable (leer y escribir) mientras esa referencia de función exista en el programa, y desde cualquier lugar donde queramos invocar esa función. ¡Por eso closure es una técnica tan poderosa, usada ampliamente en tantas áreas de la programación!

La Figura 4 ilustra las instancias de función y los enlaces de scope:

<figure>
    <img src="images/fig4.png" width="400" alt="Function instances linked to scopes via closure" align="center">
    <figcaption><em>Fig. 4: Visualizando Closures</em></figcaption>
    <br><br>
</figure>

Como se muestra en la Figura 4, cada llamada a `adder(..)` crea un nuevo scope BLUE(2) que contiene una variable `num1`, así como una nueva instancia de la función `addTo(..)` como un scope GREEN(3). Notá que las instancias de función (`addTo10(..)` y `addTo42(..)`) están presentes en el scope RED(1) y son invocadas desde él.

Ahora examinemos un ejemplo donde la variable cerrada es actualizada:

```js
function makeCounter() {
    var count = 0;

    return function getCurrent() {
        count = count + 1;
        return count;
    };
}

var hits = makeCounter();

// later

hits();     // 1

// later

hits();     // 2
hits();     // 3
```

La variable `count` es cerrada por la función interna `getCurrent()`, que la mantiene presente en lugar de que sea sometida al GC. La función `hits()` accede *y* actualiza esta variable, devolviendo un conteo incremental cada vez.

Aunque el scope envolvente de un closure típicamente proviene de una función, eso en realidad no es un requisito; solo necesita haber una función interna presente dentro de un scope externo:

```js
var hits;
{   // an outer scope (but not a function)
    let count = 0;
    hits = function getCurrent(){
        count = count + 1;
        return count;
    };
}
hits();     // 1
hits();     // 2
hits();     // 3
```

| NOTA: |
| :--- |
| Definí deliberadamente `getCurrent()` como una `function` expression en lugar de una `function` declaration. Esto no tiene que ver con closure, sino con las peligrosas rarezas de FiB (Capítulo 6). |

Debido a que es tan común confundir closure como orientado a valores en lugar de orientado a variables, los desarrolladores a veces se traban tratando de usar closure para preservar una instantánea de un valor de algún momento en el tiempo. Considerá:

```js
var studentName = "Frank";

var greeting = function hello() {
    // we are closing over `studentName`,
    // not "Frank"
    console.log(
        `Hello, ${ studentName }!`
    );
}

// later

studentName = "Suzy";

// later

greeting();
// Hello, Suzy!
```

Al definir `greeting()` (es decir, `hello()`) cuando `studentName` tiene el valor `"Frank"` (antes de la reasignación a `"Suzy"`), la suposición equivocada suele ser que el closure va a capturar `"Frank"`. Pero `greeting()` cierra sobre la variable `studentName`, no sobre su valor. Cada vez que `greeting()` es invocada, se refleja el valor actual de la variable (`"Suzy"`, en este caso).

La ilustración clásica de este error es definir funciones dentro de un loop:

```js
var keeps = [];

for (var i = 0; i < 3; i++) {
    keeps[i] = function keepI(){
        // closure over `i`
        return i;
    };
}

keeps[0]();   // 3 -- WHY!?
keeps[1]();   // 3
keeps[2]();   // 3
```

| NOTA: |
| :--- |
| Este tipo de ilustración de closure típicamente usa un `setTimeout(..)` u otro callback como un manejador de eventos, dentro del loop. Simplifiqué el ejemplo almacenando referencias de función en un array, para que no necesitemos considerar el timing asíncrono en nuestro análisis. El principio de closure es el mismo, independientemente de eso. |

Podrías haber esperado que la invocación `keeps[0]()` devolviera `0`, ya que esa función fue creada durante la primera iteración del loop cuando `i` era `0`. Pero de nuevo, esa suposición nace de pensar en closure como orientado a valores en lugar de orientado a variables.

Algo acerca de la estructura de un loop `for` puede engañarnos para que pensemos que cada iteración obtiene su propia variable `i` nueva; de hecho, este programa solo tiene una `i`, ya que fue declarada con `var`.

Cada función guardada devuelve `3`, porque al final del loop, la única variable `i` del programa quedó asignada con `3`. Cada una de las tres funciones en el array `keeps` sí tiene closures individuales, pero todas cierran sobre esa misma variable `i` compartida.

Por supuesto, una única variable solo puede sostener un valor en cualquier momento dado. Así que si querés preservar múltiples valores, necesitás una variable diferente para cada uno.

¿Cómo podríamos hacer eso en el fragmento del loop? Creemos una nueva variable para cada iteración:

```js
var keeps = [];

for (var i = 0; i < 3; i++) {
    // new `j` created each iteration, which gets
    // a copy of the value of `i` at this moment
    let j = i;

    // the `i` here isn't being closed over, so
    // it's fine to immediately use its current
    // value in each loop iteration
    keeps[i] = function keepEachJ(){
        // close over `j`, not `i`!
        return j;
    };
}
keeps[0]();   // 0
keeps[1]();   // 1
keeps[2]();   // 2
```

Cada función ahora cierra sobre una variable separada (nueva) de cada iteración, aunque todas se llamen `j`. Y cada `j` obtiene una copia del valor de `i` en ese punto de la iteración del loop; esa `j` nunca se reasigna. ¡Así que las tres funciones ahora devuelven sus valores esperados: `0`, `1` y `2`!

Recordá de nuevo, incluso si estuviéramos usando asincronía en este programa, como pasar cada función interna `keepEachJ()` a `setTimeout(..)` o a alguna suscripción de manejador de eventos, el mismo tipo de comportamiento de closure seguiría observándose.

Recordá la sección "Loops" del Capítulo 5, que ilustra cómo una declaración `let` en un loop `for` en realidad crea no solo una variable para el loop, sino que de hecho crea una nueva variable para *cada iteración* del loop. Ese truco/rareza es exactamente lo que necesitamos para nuestros closures de loop:

```js
var keeps = [];

for (let i = 0; i < 3; i++) {
    // the `let i` gives us a new `i` for
    // each iteration, automatically!
    keeps[i] = function keepEachI(){
        return i;
    };
}
keeps[0]();   // 0
keeps[1]();   // 1
keeps[2]();   // 2
```

Como estamos usando `let`, se crean tres `i`, una para cada loop, así que cada uno de los tres closures *simplemente funciona* como se espera.

### Closures Comunes: Ajax y Eventos

Closure se encuentra más comúnmente con callbacks:

```js
function lookupStudentRecord(studentID) {
    ajax(
        `https://some.api/student/${ studentID }`,
        function onRecord(record) {
            console.log(
                `${ record.name } (${ studentID })`
            );
        }
    );
}

lookupStudentRecord(114);
// Frank (114)
```

El callback `onRecord(..)` va a ser invocado en algún punto en el futuro, después de que vuelva la respuesta de la llamada Ajax. Esta invocación va a ocurrir desde las entrañas de la utilidad `ajax(..)`, de donde sea que provenga. Además, cuando eso suceda, la llamada `lookupStudentRecord(..)` ya hará mucho que se habrá completado.

¿Por qué entonces `studentID` sigue presente y accesible para el callback? Closure.

Los manejadores de eventos son otro uso común de closure:

```js
function listenForClicks(btn,label) {
    btn.addEventListener("click",function onClick(){
        console.log(
            `The ${ label } button was clicked!`
        );
    });
}

var submitBtn = document.getElementById("submit-btn");

listenForClicks(submitBtn,"Checkout");
```

El parámetro `label` es cerrado por el callback manejador de eventos `onClick(..)`. Cuando el botón es clickeado, `label` todavía existe para ser usado. Esto es closure.

### ¿Qué Pasa Si No Puedo Verlo?

Probablemente hayas escuchado este dicho común:

> Si un árbol cae en el bosque pero no hay nadie cerca para oírlo, ¿hace sonido?

Es una tontería de gimnasia filosófica. Por supuesto que desde una perspectiva científica, se crean ondas sonoras. Pero el verdadero punto: *¿importa* que el sonido ocurra?

Recordá, el énfasis en nuestra definición de closure es la observabilidad. Si un closure existe (en un sentido técnico, de implementación o académico) pero no puede ser observado en nuestros programas, *¿importa?* No.

Para reforzar este punto, veamos algunos ejemplos que *no* se basan observablemente en closure.

Por ejemplo, invocar una función que hace uso de la búsqueda de lexical scope:

```js
function say(myName) {
    var greeting = "Hello";
    output();

    function output() {
        console.log(
            `${ greeting }, ${ myName }!`
        );
    }
}

say("Kyle");
// Hello, Kyle!
```

La función interna `output()` accede a las variables `greeting` y `myName` desde su scope envolvente. Pero la invocación de `output()` ocurre en ese mismo scope, donde por supuesto `greeting` y `myName` siguen disponibles; eso es simplemente lexical scope, no closure.

Cualquier lenguaje con lexical scope cuyas funciones no soportaran closure se comportaría igual de esta misma manera.

De hecho, las variables de scope global esencialmente no pueden ser (observablemente) cerradas, porque siempre son accesibles desde todas partes. Ninguna función puede ser jamás invocada en ninguna parte de la scope chain que no sea descendiente del scope global.

Considerá:

```js
var students = [
    { id: 14, name: "Kyle" },
    { id: 73, name: "Suzy" },
    { id: 112, name: "Frank" },
    { id: 6, name: "Sarah" }
];

function getFirstStudent() {
    return function firstStudent(){
        return students[0].name;
    };
}

var student = getFirstStudent();

student();
// Kyle
```

La función interna `firstStudent()` sí referencia a `students`, que es una variable fuera de su propio scope. Pero como `students` resulta ser del scope global, no importa dónde esa función sea invocada en el programa, su capacidad de acceder a `students` no es nada más especial que el lexical scope normal.

Todas las invocaciones de función pueden acceder a las variables globales, sin importar si closure es soportado por el lenguaje o no. Las variables globales no necesitan ser cerradas.

Las variables que simplemente están presentes pero nunca son accedidas no resultan en closure:

```js
function lookupStudent(studentID) {
    return function nobody(){
        var msg = "Nobody's here yet.";
        console.log(msg);
    };
}

var student = lookupStudent(112);

student();
// Nobody's here yet.
```

La función interna `nobody()` no cierra sobre ninguna variable externa—solo usa su propia variable `msg`. Aunque `studentID` esté presente en el scope envolvente, `studentID` no es referenciada por `nobody()`. ¡El motor de JS no necesita mantener `studentID` presente después de que `lookupStudent(..)` haya terminado de ejecutarse, así que el GC quiere limpiar esa memoria!

Ya sea que las funciones de JS soporten closure o no, este programa se comportaría igual. Por lo tanto, no hay closure observado aquí.

Si no hay invocación de función, closure no puede ser observado:

```js
function greetStudent(studentName) {
    return function greeting(){
        console.log(
            `Hello, ${ studentName }!`
        );
    };
}

greetStudent("Kyle");

// nothing else happens
```

Este es engañoso, porque la función externa definitivamente sí es invocada. Pero la función interna es la que *podría* haber tenido closure, y sin embargo nunca es invocada; la función devuelta aquí simplemente se descarta. Así que incluso si técnicamente el motor de JS creó closure por un breve momento, no fue observado de ninguna manera significativa en este programa.

Un árbol puede haber caído... pero no lo escuchamos, así que no nos importa.

### Definición Observable

Ahora estamos listos para definir closure:

> Closure se observa cuando una función usa variable(s) de scope(s) externo(s) incluso mientras se ejecuta en un scope donde esa(s) variable(s) no serían accesibles.

Las partes clave de esta definición son:

* Debe haber una función involucrada

* Debe referenciar al menos una variable de un scope externo

* Debe ser invocada en una rama diferente de la scope chain respecto de la(s) variable(s)

Esta definición orientada a la observación significa que no deberíamos descartar closure como alguna trivialidad indirecta y académica. En cambio, deberíamos buscar y planificar los efectos directos y concretos que closure tiene sobre el comportamiento de nuestro programa.

## El Ciclo de Vida del Closure y la Recolección de Basura (GC)

Dado que closure está inherentemente ligado a una instancia de función, su closure sobre una variable dura tanto como siga habiendo una referencia a esa función.

Si diez funciones cierran todas sobre la misma variable, y con el tiempo nueve de estas referencias de función se descartan, la única referencia de función restante todavía preserva esa variable. Una vez que esa referencia de función final se descarta, el último closure sobre esa variable desaparece, y la variable en sí es recolectada por el GC.

Esto tiene un impacto importante en la construcción de programas eficientes y de buen rendimiento. Closure puede inesperadamente impedir el GC de una variable con la que de otro modo ya terminaste, lo que lleva a un uso descontrolado de memoria con el tiempo. Por eso es importante descartar las referencias de función (y por lo tanto sus closures) cuando ya no se necesitan más.

Considerá:

```js
function manageBtnClickEvents(btn) {
    var clickHandlers = [];

    return function listener(cb){
        if (cb) {
            let clickHandler =
                function onClick(evt){
                    console.log("clicked!");
                    cb(evt);
                };
            clickHandlers.push(clickHandler);
            btn.addEventListener(
                "click",
                clickHandler
            );
        }
        else {
            // passing no callback unsubscribes
            // all click handlers
            for (let handler of clickHandlers) {
                btn.removeEventListener(
                    "click",
                    handler
                );
            }

            clickHandlers = [];
        }
    };
}

// var mySubmitBtn = ..
var onSubmit = manageBtnClickEvents(mySubmitBtn);

onSubmit(function checkout(evt){
    // handle checkout
});

onSubmit(function trackAction(evt){
    // log action to analytics
});

// later, unsubscribe all handlers:
onSubmit();
```

En este programa, la función interna `onClick(..)` mantiene un closure sobre el `cb` pasado (el callback de evento provisto). Eso significa que las referencias a las function expressions `checkout()` y `trackAction()` se mantienen mediante closure (y no pueden ser recolectadas por el GC) mientras estos manejadores de eventos estén suscritos.

Cuando llamamos a `onSubmit()` sin entrada en la última línea, todos los manejadores de eventos se desuscriben, y el array `clickHandlers` se vacía. Una vez que todas las referencias de función de los manejadores de click se descartan, los closures de las referencias `cb` a `checkout()` y `trackAction()` se descartan.

Al considerar la salud y eficiencia general del programa, ¡desuscribir un manejador de eventos cuando ya no se necesita puede ser incluso más importante que la suscripción inicial!

### ¿Por Variable o por Scope?

Otra pregunta que necesitamos abordar: ¿deberíamos pensar en closure como aplicado solo a la(s) variable(s) externa(s) referenciada(s), o closure preserva la scope chain entera con todas sus variables?

En otras palabras, en el fragmento anterior de suscripción de eventos, ¿la función interna `onClick(..)` cierra solo sobre `cb`, o también cierra sobre `clickHandler`, `clickHandlers` y `btn`?

Conceptualmente, closure es **por variable** en lugar de *por scope*. Los callbacks de Ajax, los manejadores de eventos, y todas las demás formas de closures de función típicamente se asume que cierran solo sobre lo que explícitamente referencian.

Pero la realidad es más complicada que eso.

Otro programa a considerar:

```js
function manageStudentGrades(studentRecords) {
    var grades = studentRecords.map(getGrade);

    return addGrade;

    // ************************

    function getGrade(record){
        return record.grade;
    }

    function sortAndTrimGradesList() {
        // sort by grades, descending
        grades.sort(function desc(g1,g2){
            return g2 - g1;
        });

        // only keep the top 10 grades
        grades = grades.slice(0,10);
    }

    function addGrade(newGrade) {
        grades.push(newGrade);
        sortAndTrimGradesList();
        return grades;
    }
}

var addNextGrade = manageStudentGrades([
    { id: 14, name: "Kyle", grade: 86 },
    { id: 73, name: "Suzy", grade: 87 },
    { id: 112, name: "Frank", grade: 75 },
    // ..many more records..
    { id: 6, name: "Sarah", grade: 91 }
]);

// later

addNextGrade(81);
addNextGrade(68);
// [ .., .., ... ]
```

La función externa `manageStudentGrades(..)` toma una lista de registros de estudiantes, y devuelve una referencia a la función `addGrade(..)`, que externamente etiquetamos como `addNextGrade(..)`. Cada vez que llamamos a `addNextGrade(..)` con una nueva calificación, obtenemos de vuelta una lista actual de las 10 mejores calificaciones, ordenadas numéricamente de forma descendente (ver `sortAndTrimGradesList()`).

Desde el final de la llamada original a `manageStudentGrades(..)`, y entre las múltiples llamadas a `addNextGrade(..)`, la variable `grades` se preserva dentro de `addGrade(..)` mediante closure; así es como se mantiene la lista corriente de mejores calificaciones. Recordá, es un closure sobre la variable `grades` en sí, no sobre el array que ella contiene.

Sin embargo, ese no es el único closure involucrado. ¿Podés detectar otras variables que se están cerrando?

¿Detectaste que `addGrade(..)` referencia a `sortAndTrimGradesList`? Eso significa que también cierra sobre ese identificador, que resulta sostener una referencia a la función `sortAndTrimGradesList()`. Esa segunda función interna tiene que permanecer presente para que `addGrade(..)` pueda seguir llamándola, lo que también significa que cualquier variable que *ella* cierre permanece—aunque, en este caso, nada extra se cierra ahí.

¿Qué más se cierra?

Considerá la variable `getGrade` (y su función); ¿se cierra? Es referenciada en el scope externo de `manageStudentGrades(..)` en la llamada `.map(getGrade)`. Pero no es referenciada en `addGrade(..)` ni en `sortAndTrimGradesList()`.

¿Qué pasa con la lista (potencialmente) grande de registros de estudiantes que pasamos como `studentRecords`? ¿Se cierra esa variable? Si lo hace, el array de registros de estudiantes nunca es recolectado por el GC, lo que lleva a que este programa retenga una cantidad de memoria mayor de la que podríamos suponer. Pero si miramos de cerca de nuevo, ninguna de las funciones internas referencia a `studentRecords`.

Según la definición *por variable* de closure, dado que `getGrade` y `studentRecords` *no* son referenciadas por las funciones internas, no se cierran. Deberían estar libremente disponibles para el GC justo después de que la llamada a `manageStudentGrades(..)` se complete.

De hecho, probá debuggear este código en un motor de JS reciente, como v8 en Chrome, colocando un breakpoint dentro de la función `addGrade(..)`. Puede que notes que el inspector **no** lista la variable `studentRecords`. Eso es prueba, al menos en términos de debugging, de que el motor no mantiene `studentRecords` mediante closure. ¡Uf!

Pero, ¿qué tan confiable es esta observación como prueba? Considerá este programa (¡bastante artificial!):

```js
function storeStudentInfo(id,name,grade) {
    return function getInfo(whichValue){
        // warning:
        //   using `eval(..)` is a bad idea!
        var val = eval(whichValue);
        return val;
    };
}

var info = storeStudentInfo(73,"Suzy",87);

info("name");
// Suzy

info("grade");
// 87
```

Notá que la función interna `getInfo(..)` no cierra explícitamente sobre ninguna de las variables `id`, `name` o `grade`. Y sin embargo, las llamadas a `info(..)` parecen seguir siendo capaces de acceder a las variables, si bien mediante el uso de la trampa de lexical scope de `eval(..)` (ver Capítulo 1).

Así que todas las variables fueron definitivamente preservadas mediante closure, a pesar de no ser explícitamente referenciadas por la función interna. ¿Entonces eso refuta la afirmación *por variable* en favor de *por scope*? Depende.

Muchos motores de JS modernos sí aplican una *optimización* que elimina de un scope de closure cualquier variable que no sea explícitamente referenciada. Sin embargo, como vemos con `eval(..)`, hay situaciones donde tal optimización no puede aplicarse, y el scope de closure sigue conteniendo todas sus variables originales. En otras palabras, closure debe ser *por scope*, a nivel de implementación, y luego una optimización opcional recorta el scope para dejar solo lo que fue cerrado (un resultado similar al del closure *por variable*).

Incluso tan recientemente como hace unos años, muchos motores de JS no aplicaban esta optimización; es posible que tus sitios web todavía se ejecuten en esos navegadores, especialmente en dispositivos más viejos o de gama baja. Eso significa que es posible que closures de larga duración, como los manejadores de eventos, estén reteniendo memoria mucho más tiempo del que habríamos supuesto.

Y el hecho de que sea una optimización opcional en primer lugar, en lugar de un requisito de la especificación, significa que no deberíamos asumir casualmente en exceso su aplicabilidad.

En los casos en que una variable sostiene un valor grande (como un objeto o un array) y esa variable está presente en un scope de closure, si ya no necesitás ese valor y no querés que esa memoria quede retenida, es más seguro (en términos de uso de memoria) descartar manualmente el valor en lugar de confiar en la optimización/GC del closure.

Apliquemos un *arreglo* al ejemplo anterior de `manageStudentGrades(..)` para asegurar que el array potencialmente grande retenido en `studentRecords` no quede atrapado en un scope de closure innecesariamente:

```js
function manageStudentGrades(studentRecords) {
    var grades = studentRecords.map(getGrade);

    // unset `studentRecords` to prevent unwanted
    // memory retention in the closure
    studentRecords = null;

    return addGrade;
    // ..
}
```

No estamos eliminando `studentRecords` del scope de closure; eso no lo podemos controlar. Estamos asegurándonos de que, incluso si `studentRecords` permanece en el scope de closure, esa variable ya no esté referenciando el array de datos potencialmente grande; el array puede ser recolectado por el GC.

De nuevo, en muchos casos JS podría optimizar automáticamente el programa con el mismo efecto. Pero sigue siendo un buen hábito ser cuidadosos y asegurarnos explícitamente de no mantener ninguna cantidad significativa de memoria del dispositivo atada por más tiempo del necesario.

De hecho, técnicamente tampoco necesitamos más la función `getGrade()` después de que la llamada `.map(getGrade)` se complete. Si hacer profiling de nuestra aplicación mostrara que esta es un área crítica de uso excesivo de memoria, posiblemente podríamos exprimir un poquito más de memoria liberando esa referencia para que su valor tampoco quede atado. Eso probablemente sea innecesario en este ejemplo de juguete, pero esta es una técnica general a tener en cuenta si estás optimizando el footprint de memoria de tu aplicación.

La conclusión: es importante saber dónde aparecen los closures en nuestros programas, y qué variables están incluidas. Deberíamos gestionar estos closures cuidadosamente para estar reteniendo solo lo mínimamente necesario y no desperdiciar memoria.

## Una Perspectiva Alternativa

Revisando nuestra definición de trabajo para closure, la afirmación es que las funciones son "valores de primera clase" ("first-class values") que pueden ser pasados por el programa, igual que cualquier otro valor. Closure es la asociación-enlace que conecta esa función con el scope/variables fuera de sí misma, no importa a dónde vaya esa función.

Recordemos un ejemplo de código de más temprano en este capítulo, nuevamente con los colores de burbuja de scope relevantes anotados:

```js
// outer/global scope: RED(1)

function adder(num1) {
    // function scope: BLUE(2)

    return function addTo(num2){
        // function scope: GREEN(3)

        return num1 + num2;
    };
}

var add10To = adder(10);
var add42To = adder(42);

add10To(15);    // 25
add42To(9);     // 51
```

Nuestra perspectiva actual sugiere que donde sea que una función sea pasada e invocada, closure preserva un enlace oculto de vuelta al scope original para facilitar el acceso a las variables cerradas. La Figura 4, repetida aquí por conveniencia, ilustra esta noción:

<figure>
    <img src="images/fig4.png" width="400" alt="Function instances linked to scopes via closure" align="center">
    <figcaption><em>Fig. 4 (repetida): Visualizando Closures</em></figcaption>
    <br><br>
</figure>

Pero hay otra manera de pensar sobre closure, y más precisamente sobre la naturaleza de las funciones siendo *pasadas de un lado a otro*, que puede ayudar a profundizar los modelos mentales.

Este modelo alternativo le resta énfasis a las "funciones como valores de primera clase", y en cambio abraza cómo las funciones (como todos los valores no primitivos) son retenidas por referencia en JS, y asignadas/pasadas por copia-de-referencia—ver el Apéndice A del libro *Get Started* para más información.

En lugar de pensar en que la instancia de la función interna `addTo(..)` se mueve al scope externo RED(1) mediante el `return` y la asignación, podemos imaginar que las instancias de función en realidad simplemente permanecen en su lugar en su propio entorno de scope, por supuesto con su scope-chain intacta.

Lo que se *envía* al scope RED(1) es **solo una referencia** a la instancia de función que está en su lugar, en lugar de la instancia de función en sí. La Figura 5 ilustra las instancias de función internas permaneciendo en su lugar, apuntadas por las referencias RED(1) `addTo10` y `addTo42`, respectivamente:

<figure>
    <img src="images/fig5.png" width="400" alt="Function instances inside scopes via closure, linked to by references" align="center">
    <figcaption><em>Fig. 5: Visualizando Closures (Alternativa)</em></figcaption>
    <br><br>
</figure>

Como se muestra en la Figura 5, cada llamada a `adder(..)` todavía crea un nuevo scope BLUE(2) que contiene una variable `num1`, así como una instancia del scope GREEN(3) `addTo(..)`. Pero lo que es diferente de la Figura 4 es que, ahora, estas instancias GREEN(3) permanecen en su lugar, naturalmente anidadas dentro de sus instancias de scope BLUE(2). Las referencias `addTo10` y `addTo42` se mueven al scope externo RED(1), no las instancias de función en sí.

Cuando se llama a `addTo10(15)`, la instancia de función `addTo(..)` (todavía en su lugar en su entorno de scope original BLUE(2)) es invocada. Dado que la instancia de función en sí nunca se movió, por supuesto todavía tiene acceso natural a su scope chain. Lo mismo con la llamada `addTo42(9)`—nada especial aquí más allá del lexical scope.

Entonces, ¿qué *es* closure, si no la *magia* que le permite a una función mantener un enlace a su scope chain original incluso mientras esa función se mueve por otros scopes? En este modelo alternativo, las funciones permanecen en su lugar y siguen accediendo a su scope chain original tal como siempre pudieron.

Closure en cambio describe la *magia* de **mantener viva una instancia de función**, junto con todo su entorno y scope chain, mientras haya al menos una referencia a esa instancia de función dando vueltas en cualquier otra parte del programa.

Esa definición de closure es menos observacional y suena un poco menos familiar en comparación con la perspectiva académica tradicional. Pero no obstante sigue siendo útil, porque el beneficio es que simplificamos la explicación de closure a una combinación directa de referencias e instancias de función en su lugar.

El modelo anterior (Figura 4) no está *equivocado* al describir closure en JS. Simplemente está más inspirado conceptualmente, es una perspectiva académica sobre closure. En contraste, el modelo alternativo (Figura 5) podría describirse como un poco más enfocado en la implementación, en cómo JS realmente funciona.

Ambas perspectivas/modelos son útiles para entender closure, pero el lector puede encontrar que uno es un poco más fácil de sostener que el otro. Cualquiera que elijas, los resultados observables en nuestro programa son los mismos.

| NOTA: |
| :--- |
| Este modelo alternativo para closure sí afecta si clasificamos los callbacks síncronos como ejemplos de closure o no. Más sobre este matiz en el Apéndice A. |

## ¿Por Qué Closure?

Ahora que tenemos un sentido completo de qué es closure y cómo funciona, exploremos algunas maneras en que puede mejorar la estructura y organización del código de un programa de ejemplo.

Imaginá que tenés un botón en una página que, al ser clickeado, debería recuperar y enviar algunos datos mediante una petición Ajax. Sin usar closure:

```js
var APIendpoints = {
    studentIDs:
        "https://some.api/register-students",
    // ..
};

var data = {
    studentIDs: [ 14, 73, 112, 6 ],
    // ..
};

function makeRequest(evt) {
    var btn = evt.target;
    var recordKind = btn.dataset.kind;
    ajax(
        APIendpoints[recordKind],
        data[recordKind]
    );
}

// <button data-kind="studentIDs">
//    Register Students
// </button>
btn.addEventListener("click",makeRequest);
```

La utilidad `makeRequest(..)` solo recibe un objeto `evt` de un evento de click. A partir de ahí, tiene que recuperar el atributo `data-kind` del elemento botón objetivo, y usar ese valor para buscar tanto una URL para el endpoint de la API como qué datos deberían incluirse en la petición Ajax.

Esto funciona OK, pero es una lástima (ineficiente, más confuso) que el manejador de eventos tenga que leer un atributo del DOM cada vez que se dispara. ¿Por qué no podría un manejador de eventos *recordar* este valor? Intentemos usar closure para mejorar el código:

```js
var APIendpoints = {
    studentIDs:
        "https://some.api/register-students",
    // ..
};

var data = {
    studentIDs: [ 14, 73, 112, 6 ],
    // ..
};

function setupButtonHandler(btn) {
    var recordKind = btn.dataset.kind;

    btn.addEventListener(
        "click",
        function makeRequest(evt){
            ajax(
                APIendpoints[recordKind],
                data[recordKind]
            );
        }
    );
}

// <button data-kind="studentIDs">
//    Register Students
// </button>

setupButtonHandler(btn);
```

Con el enfoque de `setupButtonHandler(..)`, el atributo `data-kind` se recupera una sola vez y se asigna a la variable `recordKind` en la configuración inicial. Luego `recordKind` es cerrado por el manejador de click interno `makeRequest(..)`, y su valor se usa en cada disparo del evento para buscar la URL y los datos que deberían enviarse.

| NOTA: |
| :--- |
| `evt` todavía se pasa a `makeRequest(..)`, aunque en este caso ya no lo estamos usando. Sigue listado, por consistencia con el fragmento anterior. |

Al colocar `recordKind` dentro de `setupButtonHandler(..)`, limitamos la exposición del scope de esa variable a un subconjunto más apropiado del programa; almacenarla globalmente habría sido peor para la organización y legibilidad del código. Closure le permite a la instancia de la función interna `makeRequest()` *recordar* esta variable y acceder a ella cuando sea necesario.

Construyendo sobre este patrón, podríamos haber buscado tanto la URL como los datos una sola vez, en la configuración:

```js
function setupButtonHandler(btn) {
    var recordKind = btn.dataset.kind;
    var requestURL = APIendpoints[recordKind];
    var requestData = data[recordKind];

    btn.addEventListener(
        "click",
        function makeRequest(evt){
            ajax(requestURL,requestData);
        }
    );
}
```

Ahora `makeRequest(..)` cierra sobre `requestURL` y `requestData`, lo que es un poco más limpio de entender, y también ligeramente más performante.

Dos técnicas similares del paradigma de Programación Funcional (FP) que se basan en closure son la aplicación parcial (partial application) y el currying. Brevemente, con estas técnicas alteramos la *forma* de las funciones que requieren múltiples entradas de modo que algunas entradas se proveen de antemano, y otras entradas se proveen después; las entradas iniciales se recuerdan mediante closure. Una vez que todas las entradas han sido provistas, se realiza la acción subyacente.

Al crear una instancia de función que encapsula alguna información adentro (mediante closure), la función-con-información-almacenada puede luego usarse directamente sin necesidad de volver a proveer esa entrada. Esto hace que esa parte del código sea más limpia, y también ofrece la oportunidad de etiquetar las funciones parcialmente aplicadas con mejores nombres semánticos.

Adaptando la aplicación parcial, podemos mejorar aún más el código precedente:

```js
function defineHandler(requestURL,requestData) {
    return function makeRequest(evt){
        ajax(requestURL,requestData);
    };
}

function setupButtonHandler(btn) {
    var recordKind = btn.dataset.kind;
    var handler = defineHandler(
        APIendpoints[recordKind],
        data[recordKind]
    );
    btn.addEventListener("click",handler);
}
```

Las entradas `requestURL` y `requestData` se proveen de antemano, resultando en la función parcialmente aplicada `makeRequest(..)`, que localmente etiquetamos como `handler`. Cuando el evento eventualmente se dispara, la entrada final (`evt`, aunque se ignora) se pasa a `handler()`, completando sus entradas y disparando la petición Ajax subyacente.

En términos de comportamiento, este programa es bastante similar al anterior, con el mismo tipo de closure. Pero al aislar la creación de `makeRequest(..)` en una utilidad separada (`defineHandler(..)`), hacemos que esa definición sea más reutilizable a lo largo del programa. También limitamos explícitamente el scope de closure solo a las dos variables necesarias.

## Más Cerca del Closure

A medida que cerramos un capítulo denso, tomá algunas respiraciones profundas y dejá que todo se asiente. En serio, ¡es mucha información para que cualquiera la consuma!

Exploramos dos modelos para abordar mentalmente closure:

* Observacional: closure es una instancia de función que recuerda sus variables externas incluso cuando esa función es pasada a e **invocada en** otros scopes.

* De implementación: closure es una instancia de función y su entorno de scope preservados en su lugar mientras cualquier referencia a ella es pasada de un lado a otro e **invocada desde** otros scopes.

Resumiendo los beneficios para nuestros programas:

* Closure puede mejorar la eficiencia al permitir que una instancia de función recuerde información previamente determinada en lugar de tener que computarla cada vez.

* Closure puede mejorar la legibilidad del código, acotando la exposición del scope al encapsular variable(s) dentro de instancias de función, mientras sigue asegurando que la información en esas variables sea accesible para uso futuro. Las instancias de función resultantes, más acotadas y especializadas, son más limpias para interactuar, ya que la información preservada no necesita ser pasada en cada invocación.

Antes de que sigas adelante, tomate un tiempo para reformular este resumen *en tus propias palabras*, explicando qué es closure y por qué es útil en tus programas. El texto principal del libro concluye con un capítulo final que se construye sobre closure con el patrón de módulo.
