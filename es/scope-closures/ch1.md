# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Capítulo 1: ¿Qué es el scope?

Para cuando hayas escrito tus primeros programas, probablemente ya te sientas algo cómodo creando variables y almacenando valores en ellas. ¡Trabajar con variables es una de las cosas más fundamentales que hacemos al programar!

Pero quizás no hayas considerado muy de cerca los mecanismos subyacentes que utiliza el engine para organizar y administrar estas variables. No me refiero a cómo se asigna la memoria en la computadora, sino más bien a: ¿cómo sabe JS qué variables son accesibles por cualquier statement dado, y cómo maneja dos variables con el mismo nombre?

Las respuestas a preguntas como estas toman la forma de reglas bien definidas llamadas scope. Este libro profundizará en todos los aspectos del scope—cómo funciona, para qué sirve, los problemas que hay que evitar—y luego señalará patrones comunes de scope que guían la estructura de los programas.

Nuestro primer paso es descubrir cómo el engine de JS procesa nuestro programa **antes** de ejecutarlo.

## Sobre este libro

¡Bienvenido al libro 2 de la serie *You Don't Know JS Yet*! Si ya terminaste *Get Started* (el primer libro), ¡estás en el lugar correcto! Si no, antes de continuar te animo a *empezar por ahí* para tener la mejor base.

Nuestro enfoque será el primero de los tres pilares del lenguaje JS: el sistema de scope y sus closures de funciones, así como el poder del patrón de diseño de módulos.

JS suele clasificarse como un lenguaje de scripting interpretado, por lo que la mayoría asume que los programas de JS se procesan en una sola pasada de arriba hacia abajo. Pero en realidad JS se parsea/compila en una fase separada **antes de que comience la ejecución**. Las decisiones del autor del código sobre dónde colocar variables, funciones y bloques unos respecto de otros se analizan según las reglas del scope, durante la fase inicial de parsing/compilación. La estructura de scope resultante generalmente no se ve afectada por las condiciones de runtime.

Las funciones de JS son en sí mismas valores de primera clase; pueden asignarse y pasarse por ahí al igual que números o strings. Pero como estas funciones retienen y acceden a variables, mantienen su scope original sin importar en qué parte del programa se ejecuten finalmente. Esto se llama closure.

Los módulos son un patrón de organización de código caracterizado por métodos públicos que tienen acceso privilegiado (vía closure) a variables y funciones ocultas en el scope interno del módulo.

## Compilado vs. interpretado

Quizás hayas oído hablar antes de la *compilación de código*, pero tal vez te parezca una misteriosa caja negra donde el código fuente entra por un extremo y los programas ejecutables salen por el otro.

Sin embargo, no es misterioso ni mágico. La compilación de código es un conjunto de pasos que procesan el texto de tu código y lo convierten en una lista de instrucciones que la computadora puede entender. Normalmente, todo el código fuente se transforma de una sola vez, y esas instrucciones resultantes se guardan como salida (usualmente en un archivo) que luego puede ejecutarse.

También quizás hayas oído que el código puede ser *interpretado*, entonces, ¿en qué se diferencia eso de ser *compilado*?

La interpretación realiza una tarea similar a la compilación, en el sentido de que transforma tu programa en instrucciones comprensibles por la máquina. Pero el modelo de procesamiento es diferente. A diferencia de un programa que se compila todo de una vez, con la interpretación el código fuente se transforma línea por línea; cada línea o statement se ejecuta antes de proceder de inmediato a procesar la siguiente línea del código fuente.

<figure>
    <img src="images/fig1.png" width="650" alt="Code Compilation and Code Interpretation" align="center">
    <figcaption><em>Fig. 1: Código compilado vs. interpretado</em></figcaption>
    <br><br>
</figure>

La Figura 1 ilustra la compilación vs. la interpretación de programas.

¿Son estos dos modelos de procesamiento mutuamente excluyentes? Generalmente, sí. Sin embargo, el tema es más sutil, porque la interpretación en realidad puede tomar otras formas además de operar simplemente línea por línea sobre el texto del código fuente. Los engines modernos de JS en realidad emplean numerosas variaciones de compilación e interpretación en el manejo de programas de JS.

Recordá que examinamos este tema en el Capítulo 1 del libro *Get Started*. Nuestra conclusión allí es que JS se describe con mayor precisión como un **lenguaje compilado**. Para beneficio de los lectores aquí, las siguientes secciones revisarán y ampliarán esa afirmación.

## Compilando código

Pero primero, ¿por qué importa siquiera si JS es compilado o no?

El scope se determina principalmente durante la compilación, por lo que entender cómo se relacionan la compilación y la ejecución es clave para dominar el scope.

En la teoría clásica de compiladores, un compilador procesa un programa en tres etapas básicas:

1. **Tokenizing/Lexing:** dividir una cadena de caracteres en fragmentos significativos (para el lenguaje), llamados tokens. Por ejemplo, considerá el programa: `var a = 2;`. Este programa probablemente se dividiría en los siguientes tokens: `var`, `a`, `=`, `2` y `;`. Los espacios en blanco pueden o no persistirse como un token, dependiendo de si son significativos o no.

    (La diferencia entre tokenizing y lexing es sutil y académica, pero se centra en si estos tokens se identifican de una manera *sin estado* (stateless) o *con estado* (stateful). Dicho de manera simple, si el tokenizer invocara reglas de parsing con estado para determinar si `a` debe considerarse un token distinto o solo parte de otro token, *eso* sería **lexing**.)

2. **Parsing:** tomar un stream (array) de tokens y convertirlo en un árbol de elementos anidados que, en conjunto, representan la estructura gramatical del programa. Esto se llama Árbol de Sintaxis Abstracta (AST, por sus siglas en inglés).

    Por ejemplo, el árbol para `var a = 2;` podría comenzar con un nodo de nivel superior llamado `VariableDeclaration`, con un nodo hijo llamado `Identifier` (cuyo valor es `a`), y otro hijo llamado `AssignmentExpression` que a su vez tiene un hijo llamado `NumericLiteral` (cuyo valor es `2`).

3. **Generación de código:** tomar un AST y convertirlo en código ejecutable. Esta parte varía mucho según el lenguaje, la plataforma a la que se dirige y otros factores.

    El engine de JS toma el AST recién descrito para `var a = 2;` y lo convierte en un conjunto de instrucciones de máquina para efectivamente *crear* una variable llamada `a` (incluyendo reservar memoria, etc.), y luego almacenar un valor en `a`.

| NOTA: |
| :--- |
| Los detalles de implementación de un engine de JS (utilizar recursos de memoria del sistema, etc.) son mucho más profundos de lo que indagaremos aquí. Mantendremos nuestro enfoque en el comportamiento observable de nuestros programas y dejaremos que el engine de JS administre esas abstracciones más profundas a nivel de sistema. |

El engine de JS es muchísimo más complejo que *solo* estas tres etapas. En el proceso de parsing y generación de código, hay pasos para optimizar el rendimiento de la ejecución (es decir, colapsar elementos redundantes). De hecho, el código puede incluso recompilarse y reoptimizarse durante el progreso de la ejecución.

Así que aquí estoy pintando solo con trazos gruesos. Pero pronto verás por qué *estos* detalles que *sí* cubrimos, aunque sea a alto nivel, son relevantes.

Los engines de JS no tienen el lujo de abundante tiempo para realizar su trabajo y optimizaciones, porque la compilación de JS no ocurre en un paso de build por adelantado, como en otros lenguajes. Usualmente debe ocurrir en meros microsegundos (¡o menos!) justo antes de que el código se ejecute. Para asegurar el rendimiento más rápido bajo estas restricciones, los engines de JS usan todo tipo de trucos (como los JIT, que compilan de forma perezosa e incluso recompilan en caliente); estos están mucho más allá del "scope" de nuestra discusión aquí.

### Requerido: dos fases

Para decirlo de la manera más simple posible, la observación más importante que podemos hacer sobre el procesamiento de programas de JS es que ocurre en (al menos) dos fases: primero parsing/compilación, luego ejecución.

La separación de una fase de parsing/compilación de la posterior fase de ejecución es un hecho observable, no teoría ni opinión. Si bien la especificación de JS no requiere explícitamente la "compilación", sí requiere un comportamiento que es esencialmente práctico solo con un enfoque de compilar-luego-ejecutar.

Hay tres características del programa que podés observar para probártelo a vos mismo: syntax errors, early errors y hoisting.

#### Syntax errors desde el principio

Considerá este programa:

```js
var greeting = "Hello";

console.log(greeting);

greeting = ."Hi";
// SyntaxError: unexpected token .
```

Este programa no produce ninguna salida (`"Hello"` no se imprime), sino que en cambio lanza un `SyntaxError` sobre el token `.` inesperado justo antes del string `"Hi"`. Dado que el syntax error ocurre después del statement `console.log(..)` bien formado, si JS estuviera ejecutándose de arriba hacia abajo línea por línea, uno esperaría que el mensaje `"Hello"` se imprimiera antes de que se lanzara el syntax error. Eso no sucede.

De hecho, la única manera en que el engine de JS podría enterarse del syntax error en la tercera línea, antes de ejecutar la primera y la segunda línea, es que el engine de JS primero parsee todo el programa antes de que se ejecute cualquier parte de él.

#### Early errors

A continuación, considerá:

```js
console.log("Howdy");

saySomething("Hello","Hi");
// Uncaught SyntaxError: Duplicate parameter name not
// allowed in this context

function saySomething(greeting,greeting) {
    "use strict";
    console.log(greeting);
}
```

El mensaje `"Howdy"` no se imprime, a pesar de ser un statement bien formado.

En cambio, al igual que el fragmento de la sección anterior, el `SyntaxError` aquí se lanza antes de que el programa se ejecute. En este caso, es porque el strict-mode (habilitado aquí solo para la función `saySomething(..)`) prohíbe, entre muchas otras cosas, que las funciones tengan nombres de parámetros duplicados; esto siempre ha estado permitido en el modo no estricto.

El error lanzado no es un syntax error en el sentido de ser una cadena de tokens mal formada (como `."Hi"` anteriormente), pero en strict-mode la especificación requiere de todos modos que se lance como un "early error" antes de que comience cualquier ejecución.

Pero, ¿cómo sabe el engine de JS que el parámetro `greeting` ha sido duplicado? ¿Cómo sabe que la función `saySomething(..)` está incluso en strict-mode mientras procesa la lista de parámetros (el pragma `"use strict"` aparece solo más tarde, en el cuerpo de la función)?

De nuevo, la única explicación razonable es que el código primero debe parsearse *por completo* antes de que ocurra cualquier ejecución.

#### Hoisting

Finalmente, considerá:

```js
function saySomething() {
    var greeting = "Hello";
    {
        greeting = "Howdy";  // error comes from here
        let greeting = "Hi";
        console.log(greeting);
    }
}

saySomething();
// ReferenceError: Cannot access 'greeting' before
// initialization
```

El `ReferenceError` mencionado ocurre desde la línea con el statement `greeting = "Howdy"`. Lo que sucede es que la variable `greeting` para ese statement pertenece a la declaración de la línea siguiente, `let greeting = "Hi"`, en lugar de al statement anterior `var greeting = "Hello"`.

La única manera en que el engine de JS podría saber, en la línea donde se lanza el error, que el *siguiente statement* declararía una variable con scope de bloque del mismo nombre (`greeting`) es si el engine de JS ya hubiera procesado este código en una pasada anterior, y ya hubiera configurado todos los scopes y sus asociaciones de variables. Este procesamiento de scopes y declaraciones solo puede lograrse con precisión parseando el programa antes de la ejecución.

El `ReferenceError` aquí técnicamente proviene de que `greeting = "Howdy"` accede a la variable `greeting` **demasiado pronto**, un conflicto al que se hace referencia como la Temporal Dead Zone (TDZ). El Capítulo 5 cubrirá esto con más detalle.

| ADVERTENCIA: |
| :--- |
| A menudo se afirma que las declaraciones `let` y `const` no sufren hoisting, como explicación del comportamiento de la TDZ que se acaba de ilustrar. Pero esto no es exacto. Volveremos y explicaremos tanto el hoisting como la TDZ de `let`/`const` en el Capítulo 5. |

Con suerte ahora estás convencido de que los programas de JS se parsean antes de que comience cualquier ejecución. Pero, ¿prueba eso que son compilados?

Esta es una pregunta interesante para reflexionar. ¿Podría JS parsear un programa, pero luego ejecutar ese programa *interpretando* operaciones representadas en el AST **sin** compilar primero el programa? Sí, eso es *posible*. Pero es extremadamente improbable, principalmente porque sería extremadamente ineficiente en términos de rendimiento.

Es difícil imaginar que un engine de JS de calidad de producción se tome todo el trabajo de parsear un programa en un AST, pero que luego no convierta (es decir, "compile") ese AST en la representación (binaria) más eficiente para que el engine luego la ejecute.

Muchos se han esforzado por hilar fino con esta terminología, ya que hay abundantes matices e interjecciones de "bueno, en realidad..." dando vueltas. Pero en espíritu y en la práctica, lo que el engine está haciendo al procesar programas de JS **se parece mucho más a la compilación** que a lo contrario.

Clasificar a JS como un lenguaje compilado no tiene que ver con el modelo de distribución de sus representaciones ejecutables binarias (o de byte-code), sino más bien con mantener una distinción clara en nuestra mente sobre la fase en la que el código JS se procesa y analiza; esta fase ocurre de manera observable e indiscutible *antes* de que el código comience a ejecutarse.

Necesitamos modelos mentales adecuados de cómo el engine de JS trata nuestro código si queremos entender JS y el scope de manera efectiva.

## La jerga del compilador

Con conciencia del procesamiento en dos fases de un programa de JS (compilar, luego ejecutar), dirijamos nuestra atención a cómo el engine de JS identifica variables y determina los scopes de un programa a medida que se compila.

Primero, examinemos un programa de JS simple para usar en el análisis a lo largo de los próximos capítulos:

```js
var students = [
    { id: 14, name: "Kyle" },
    { id: 73, name: "Suzy" },
    { id: 112, name: "Frank" },
    { id: 6, name: "Sarah" }
];

function getStudentName(studentID) {
    for (let student of students) {
        if (student.id == studentID) {
            return student.name;
        }
    }
}

var nextStudent = getStudentName(73);

console.log(nextStudent);
// Suzy
```

Aparte de las declaraciones, todas las apariciones de variables/identificadores en un programa cumplen uno de dos "roles": o son el *target* (destino) de una asignación o son el *source* (origen) de un valor.

(Cuando aprendí teoría de compiladores por primera vez mientras cursaba mi carrera de ciencias de la computación, nos enseñaron los términos "LHS" (es decir, *target*) y "RHS" (es decir, *source*) para estos roles, respectivamente. Como podrás adivinar por la "L" y la "R", las siglas significan "Left-Hand Side" (lado izquierdo) y "Right-Hand Side" (lado derecho), como en los lados izquierdo y derecho de un operador de asignación `=`. Sin embargo, los targets y sources de asignación no siempre aparecen literalmente a la izquierda o a la derecha de un `=`, así que probablemente sea más claro pensar en términos de *target* / *source* en lugar de *izquierda* / *derecha*.)

¿Cómo sabés si una variable es un *target*? Verificá si hay un valor que se le esté asignando; si es así, es un *target*. Si no, entonces la variable es un *source*.

Para que el engine de JS maneje correctamente las variables de un programa, primero debe etiquetar cada aparición de una variable como *target* o *source*. Ahora profundizaremos en cómo se determina cada rol.

### Targets

¿Qué hace que una variable sea un *target*? Considerá:

```js
students = [ // ..
```

Este statement es claramente una operación de asignación; recordá que la parte `var students` se maneja completamente como una declaración en tiempo de compilación, y por lo tanto es irrelevante durante la ejecución; la dejamos afuera por claridad y enfoque. Lo mismo con el statement `nextStudent = getStudentName(73)`.

Pero hay otras tres operaciones de asignación de *target* en el código que quizás sean menos obvias. Una de ellas:

```js
for (let student of students) {
```

Ese statement asigna un valor a `student` en cada iteración del bucle. Otra referencia de *target*:

```js
getStudentName(73)
```

Pero, ¿cómo es eso una asignación a un *target*? Mirá de cerca: el argumento `73` se asigna al parámetro `studentID`.

Y hay una última (sutil) referencia de *target* en nuestro programa. ¿Podés detectarla?

..

..

..

¿Identificaste esta?

```js
function getStudentName(studentID) {
```

Una declaración `function` es un caso especial de referencia de *target*. Podés pensarla como algo similar a `var getStudentName = function(studentID)`, pero eso no es del todo exacto. Un identificador `getStudentName` se declara (en tiempo de compilación), pero la parte `= function(studentID)` también se maneja en la compilación; la asociación entre `getStudentName` y la función se configura automáticamente al comienzo del scope en lugar de esperar a que se ejecute un statement de asignación `=`.

| NOTA: |
| :--- |
| Esta asociación automática de función y variable se denomina "function hoisting", y se cubre en detalle en el Capítulo 5. |

### Sources

Así que hemos identificado las cinco referencias de *target* en el programa. Las otras referencias a variables deben ser entonces referencias de *source* (¡porque esa es la única otra opción!).

En `for (let student of students)`, dijimos que `student` es un *target*, pero `students` es una referencia de *source*. En el statement `if (student.id == studentID)`, tanto `student` como `studentID` son referencias de *source*. `student` también es una referencia de *source* en `return student.name`.

En `getStudentName(73)`, `getStudentName` es una referencia de *source* (que esperamos se resuelva en un valor de referencia a función). En `console.log(nextStudent)`, `console` es una referencia de *source*, al igual que `nextStudent`.

| NOTA: |
| :--- |
| Por si te lo estabas preguntando, `id`, `name` y `log` son todas propiedades, no referencias a variables. |

¿Cuál es la importancia práctica de entender *targets* vs. *sources*? En el Capítulo 2, revisaremos este tema y cubriremos cómo el rol de una variable impacta en su búsqueda (lookup) (específicamente, si la búsqueda falla).

## Haciendo trampa: modificaciones del scope en runtime

A esta altura debería estar claro que el scope se determina a medida que el programa se compila, y generalmente no debería verse afectado por las condiciones de runtime. Sin embargo, en el modo no estricto, técnicamente todavía hay dos maneras de hacer trampa con esta regla, modificando los scopes de un programa durante el runtime.

Ninguna de estas técnicas *debería* usarse—ambas son peligrosas y confusas, y de todos modos deberías estar usando strict-mode (donde no están permitidas). Pero es importante estar al tanto de ellas por si te las cruzás en algún programa.

La función `eval(..)` recibe un string de código para compilar y ejecutar sobre la marcha durante el runtime del programa. Si ese string de código tiene una declaración `var` o `function` en él, esas declaraciones modificarán el scope actual en el que `eval(..)` se está ejecutando:

```js
function badIdea() {
    eval("var oops = 'Ugh!';");
    console.log(oops);
}
badIdea();   // Ugh!
```

Si `eval(..)` no hubiera estado presente, la variable `oops` en `console.log(oops)` no existiría, y lanzaría un `ReferenceError`. Pero `eval(..)` modifica el scope de la función `badIdea()` en runtime. Esto es malo por muchas razones, incluyendo el impacto en el rendimiento de modificar el scope ya compilado y optimizado, cada vez que se ejecuta `badIdea()`.

La segunda trampa es la palabra clave `with`, que esencialmente convierte dinámicamente un objeto en un scope local—sus propiedades se tratan como identificadores en el bloque de ese nuevo scope:

```js
var badIdea = { oops: "Ugh!" };

with (badIdea) {
    console.log(oops);   // Ugh!
}
```

El scope global no se modificó aquí, pero `badIdea` se convirtió en un scope en runtime en lugar de en tiempo de compilación, y su propiedad `oops` se convierte en una variable en ese scope. De nuevo, esta es una idea terrible, por razones de rendimiento y legibilidad.

A toda costa, evitá `eval(..)` (al menos, un `eval(..)` que cree declaraciones) y `with`. De nuevo, ninguna de estas trampas está disponible en strict-mode, así que si simplemente usás strict-mode (¡deberías!), entonces la tentación desaparece.

## Lexical scope

Hemos demostrado que el scope de JS se determina en tiempo de compilación; el término para este tipo de scope es "lexical scope". "Lexical" está asociado con la etapa de "lexing" de la compilación, como se discutió anteriormente en este capítulo.

Para reducir este capítulo a una conclusión útil, la idea clave del "lexical scope" es que está controlado por completo por la ubicación de funciones, bloques y declaraciones de variables, en relación unos con otros.

Si colocás una declaración de variable dentro de una función, el compilador maneja esta declaración a medida que parsea la función, y asocia esa declaración con el scope de la función. Si una variable se declara con scope de bloque (`let` / `const`), entonces se asocia con el bloque `{ .. }` envolvente más cercano, en lugar de con su función envolvente (como ocurre con `var`).

Además, una referencia (rol de *target* o *source*) para una variable debe resolverse como proveniente de uno de los scopes que están *léxicamente disponibles* para ella; de lo contrario se dice que la variable está "undeclared" (no declarada) (¡lo que usualmente resulta en un error!). Si la variable no está declarada en el scope actual, se consultará el siguiente scope externo/envolvente. Este proceso de salir un nivel del anidamiento de scope continúa hasta que se pueda encontrar una declaración de variable coincidente, o hasta que se alcance el scope global y ya no haya más adónde ir.

Es importante notar que la compilación en realidad no *hace nada* en términos de reservar memoria para scopes y variables. Todavía no se ha ejecutado nada del programa.

En cambio, la compilación crea un mapa de todos los lexical scopes que establece lo que el programa necesitará mientras se ejecuta. Podés pensar en este plan como código insertado para su uso en runtime, que define todos los scopes (es decir, "entornos léxicos") y registra todos los identificadores (variables) de cada scope.

En otras palabras, aunque los scopes se identifican durante la compilación, en realidad no se crean hasta runtime, cada vez que un scope necesita ejecutarse. En el próximo capítulo, esbozaremos las bases conceptuales del lexical scope.
