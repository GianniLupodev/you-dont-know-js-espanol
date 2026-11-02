# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Capítulo 4: Alrededor del Global Scope

El Capítulo 3 mencionó el "global scope" varias veces, pero quizás todavía te preguntes por qué el scope más externo de un programa es tan importante en el JS moderno. La gran mayoría del trabajo ahora se hace dentro de funciones y módulos en lugar de hacerlo globalmente.

¿Alcanza con solo afirmar "Evitá usar el global scope" y listo?

El global scope de un programa de JS es un tema rico, con mucha más utilidad y matices de los que probablemente supondrías. Este capítulo primero explora cómo el global scope es (todavía) útil y relevante para escribir programas de JS hoy en día, y luego examina las diferencias respecto a dónde y *cómo acceder* al global scope en distintos entornos de JS.

Entender completamente el global scope es crítico para dominar el uso del lexical scope para estructurar tus programas.

## ¿Por qué Global Scope?

Probablemente no sea ninguna sorpresa para los lectores que la mayoría de las aplicaciones están compuestas por múltiples (¡a veces muchos!) archivos de JS individuales. Entonces, ¿cómo se unen exactamente todos esos archivos separados en un único contexto de ejecución por parte del engine de JS?

Con respecto a las aplicaciones ejecutadas en el navegador, hay tres formas principales.

Primero, si estás usando directamente ES modules (sin transpilarlos a algún otro formato de bundle de módulos), estos archivos son cargados individualmente por el entorno de JS. Cada módulo entonces hace `import` de referencias a los otros módulos a los que necesita acceder. Los archivos de módulos separados cooperan entre sí exclusivamente a través de estos imports compartidos, sin necesitar ningún scope externo compartido.

Segundo, si estás usando un bundler en tu proceso de build, todos los archivos típicamente se concatenan antes de ser entregados al navegador y al engine de JS, que luego solo procesa un único archivo grande. Incluso con todas las piezas de la aplicación ubicadas en un único archivo, es necesario algún mecanismo para que cada pieza registre un *nombre* al que las otras piezas puedan referirse, así como alguna facilidad para que ese acceso ocurra.

En algunas configuraciones de build, todo el contenido del archivo se envuelve en un único scope envolvente, como una función envoltura, un módulo universal (UMD—ver Apéndice A), etc. Cada pieza puede registrarse a sí misma para el acceso desde otras piezas por medio de variables locales en ese scope compartido. Por ejemplo:

```js
(function wrappingOuterScope(){
    var moduleOne = (function one(){
        // ..
    })();

    var moduleTwo = (function two(){
        // ..

        function callModuleOne() {
            moduleOne.someMethod();
        }

        // ..
    })();
})();
```

Como se muestra, las variables locales `moduleOne` y `moduleTwo` dentro del function scope de `wrappingOuterScope()` se declaran para que estos módulos puedan acceder entre sí para su cooperación.

Si bien el scope de `wrappingOuterScope()` es una función y no el global scope completo del entorno, sí actúa como una especie de "scope a nivel de aplicación", un balde donde todos los identificadores de nivel superior pueden almacenarse, aunque no en el global scope real. En ese sentido, es una especie de reemplazo del global scope.

Y finalmente, la tercera forma: ya sea que se use una herramienta de bundler para una aplicación, o que los archivos (que no son ES modules) simplemente se carguen individualmente en el navegador (vía tags `<script>` u otra carga dinámica de recursos de JS), si no hay un único scope envolvente que abarque todas estas piezas, el **global scope** es la única forma en que pueden cooperar entre sí:

Un archivo agrupado de este tipo a menudo se ve más o menos así:

```js
var moduleOne = (function one(){
    // ..
})();
var moduleTwo = (function two(){
    // ..

    function callModuleOne() {
        moduleOne.someMethod();
    }

    // ..
})();
```

Acá, dado que no hay un function scope envolvente, estas declaraciones de `moduleOne` y `moduleTwo` simplemente se dejan caer en el global scope. Esto es efectivamente lo mismo que si los archivos no se hubieran concatenado, sino cargado por separado:

module1.js:

```js
var moduleOne = (function one(){
    // ..
})();
```

module2.js:

```js
var moduleTwo = (function two(){
    // ..

    function callModuleOne() {
        moduleOne.someMethod();
    }

    // ..
})();
```

Si estos archivos se cargan por separado como archivos .js independientes normales en un entorno de navegador, cada declaración de variable de nivel superior terminará siendo una variable global, ya que el global scope es el único recurso compartido entre estos dos archivos separados—son programas independientes, desde la perspectiva del engine de JS.

Además de (potencialmente) dar cuenta de dónde reside el código de una aplicación durante la ejecución, y de cómo cada pieza puede acceder a las otras piezas para cooperar, el global scope también es donde:

* JS expone sus built-ins:

    - primitivos: `undefined`, `null`, `Infinity`, `NaN`
    - nativos: `Date()`, `Object()`, `String()`, etc.
    - funciones globales: `eval()`, `parseInt()`, etc.
    - namespaces: `Math`, `Atomics`, `JSON`
    - amigos de JS: `Intl`, `WebAssembly`

* El entorno que aloja al engine de JS expone sus propios built-ins:

    - `console` (y sus métodos)
    - el DOM (`window`, `document`, etc)
    - timers (`setTimeout(..)`, etc)
    - APIs de la plataforma web: `navigator`, `history`, geolocalización, WebRTC, etc.

Estos son solo algunos de los muchos *globales* con los que tus programas van a interactuar.

| NOTA: |
| :--- |
| Node también expone varios elementos "globalmente", pero técnicamente no están en el `global` scope: `require()`, `__dirname`, `module`, `URL`, y demás. |

La mayoría de los desarrolladores coinciden en que el global scope no debería ser simplemente un vertedero para cada variable de tu aplicación. Eso es un desastre de bugs esperando a suceder. Pero también es innegable que el global scope es un *pegamento* importante para prácticamente toda aplicación de JS.

## ¿Dónde Está Exactamente este Global Scope?

Podría parecer obvio que el global scope está ubicado en la porción más externa de un archivo; es decir, no dentro de ninguna función u otro bloque. Pero no es tan simple como eso.

Distintos entornos de JS manejan los scopes de tus programas, especialmente el global scope, de manera diferente. Es bastante común que los desarrolladores de JS alberguen conceptos erróneos sin siquiera darse cuenta.

### El "Window" del Navegador

Con respecto al tratamiento del global scope, el entorno más *puro* en el que se puede ejecutar JS es como un archivo .js independiente cargado en el entorno de una página web en un navegador. No quiero decir "puro" como en que no se agregue nada automáticamente—¡puede agregarse mucho!—sino más bien en términos de una intrusión mínima en el código o interferencia con su comportamiento esperado del global scope.

Considerá este archivo .js:

```js
var studentName = "Kyle";

function hello() {
    console.log(`Hello, ${ studentName }!`);
}

hello();
// Hello, Kyle!
```

Este código puede cargarse en el entorno de una página web usando un tag `<script>` inline, un tag de script `<script src=..>` en el markup, o incluso un elemento `<script>` del DOM creado dinámicamente. En los tres casos, los identificadores `studentName` y `hello` se declaran en el global scope.

Eso significa que si accedés al global object (comúnmente, `window` en el navegador), vas a encontrar propiedades con esos mismos nombres ahí:

```js
var studentName = "Kyle";

function hello() {
    console.log(`Hello, ${ window.studentName }!`);
}

window.hello();
// Hello, Kyle!
```

Ese es el comportamiento por defecto que uno esperaría de una lectura de la especificación de JS: el scope externo *es* el global scope y `studentName` se crea legítimamente como variable global.

Eso es lo que quiero decir con *puro*. Pero lamentablemente, eso no siempre será cierto en todos los entornos de JS con los que te encuentres, y eso a menudo sorprende a los desarrolladores de JS.

#### Globales que Hacen Shadowing de Globales

Recordá la discusión sobre shadowing (y el unshadowing global) del Capítulo 3, donde la declaración de una variable puede anular e impedir el acceso a una declaración del mismo nombre de un scope externo.

Una consecuencia inusual de la diferencia entre una variable global y una propiedad global del mismo nombre es que, dentro del global scope mismo, una propiedad del global object puede ser objeto de shadowing por una variable global:

```js
window.something = 42;

let something = "Kyle";

console.log(something);
// Kyle

console.log(window.something);
// 42
```

La declaración `let` agrega una variable global `something` pero no una propiedad del global object (ver Capítulo 3). El efecto entonces es que el identificador léxico `something` hace shadowing de la propiedad del global object `something`.

Es casi con certeza una mala idea crear una divergencia entre el global object y el global scope. Los lectores de tu código casi con certeza se van a confundir.

Una forma simple de evitar este problema con las declaraciones globales: siempre usá `var` para los globales. Reservá `let` y `const` para los block scopes (ver "Scoping con Bloques" en el Capítulo 6).

#### Globales del DOM

Afirmé que un entorno de JS alojado en un navegador tiene el comportamiento de global scope más *puro* que veremos. Sin embargo, no es del todo *puro*.

Un comportamiento sorprendente en el global scope que podés encontrar con aplicaciones de JS basadas en el navegador: un elemento del DOM con un atributo `id` crea automáticamente una variable global que lo referencia.

Considerá este markup:

```text
<ul id="my-todo-list">
   <li id="first">Write a book</li>
   ..
</ul>
```

Y el JS para esa página podría incluir:

```js
first;
// <li id="first">..</li>

window["my-todo-list"];
// <ul id="my-todo-list">..</ul>
```

Si el valor del `id` es un nombre léxico válido (como `first`), se crea la variable léxica. Si no, la única forma de acceder a ese global es a través del global object (`window[..]`).

El auto-registro de todos los elementos del DOM que llevan `id` como variables globales es un comportamiento legacy antiguo de los navegadores que, no obstante, debe permanecer porque muchos sitios viejos todavía dependen de él. Mi consejo es nunca usar estas variables globales, aunque siempre vayan a crearse silenciosamente.

#### ¿Qué Hay en un Nombre (de Window)?

Otra rareza del global scope en el JS basado en el navegador:

```js
var name = 42;

console.log(name, typeof name);
// "42" string
```

`window.name` es un "global" predefinido en un contexto de navegador; es una propiedad del global object, así que parece una variable global normal (y sin embargo es todo menos "normal").

Usamos `var` para nuestra declaración, lo cual **no** hace shadowing de la propiedad global predefinida `name`. Eso significa que, efectivamente, la declaración `var` se ignora, ya que ya existe una propiedad del global scope object con ese nombre. Como discutimos antes, si hubiéramos usado `let name`, habríamos hecho shadowing de `window.name` con una variable global `name` separada.

Pero el comportamiento verdaderamente sorprendente es que aunque asignamos el número `42` a `name` (y por lo tanto a `window.name`), cuando luego recuperamos su valor, ¡es el string `"42"`! En este caso, la rareza se debe a que `name` en realidad es un getter/setter predefinido en el objeto `window`, que insiste en que su valor sea un valor string. ¡Uf!

Con la excepción de algunos casos extremos raros como los ID de elementos del DOM y `window.name`, el JS que se ejecuta como un archivo independiente en una página de navegador tiene algunos de los comportamientos de global scope más *puros* que vamos a encontrar.

### Web Workers

Los Web Workers son una extensión de la plataforma web por encima del comportamiento del JS del navegador, que permite que un archivo de JS se ejecute en un thread completamente separado (a nivel de sistema operativo) del thread que está ejecutando el programa principal de JS.

Dado que estos programas Web Worker se ejecutan en un thread separado, están restringidos en sus comunicaciones con el thread de la aplicación principal, para evitar/limitar las race conditions y otras complicaciones. El código de Web Worker no tiene acceso al DOM, por ejemplo. Sin embargo, algunas web APIs sí están disponibles para el worker, como `navigator`.

Dado que un Web Worker se trata como un programa completamente separado, no comparte el global scope con el programa principal de JS. Sin embargo, el engine de JS del navegador sigue ejecutando el código, así que podemos esperar una *pureza* similar en su comportamiento del global scope. Dado que no hay acceso al DOM, el alias `window` para el global scope no existe.

En un Web Worker, la referencia al global object típicamente se hace usando `self`:

```js
var studentName = "Kyle";
let studentID = 42;

function hello() {
    console.log(`Hello, ${ self.studentName }!`);
}

self.hello();
// Hello, Kyle!

self.studentID;
// undefined
```

Al igual que con los programas principales de JS, las declaraciones `var` y `function` crean propiedades espejadas en el global object (es decir, `self`), mientras que otras declaraciones (`let`, etc) no.

Así que, de nuevo, el comportamiento del global scope que estamos viendo acá es casi tan *puro* como puede serlo para ejecutar programas de JS; ¡quizás sea incluso más *puro* ya que no hay un DOM que enrede las cosas!

### La Consola/REPL de las Developer Tools

Recordá del Capítulo 1 de *Get Started* que las Developer Tools no crean un entorno de JS completamente apegado. Sí procesan código de JS, pero también se inclinan a favor de que la interacción de UX sea lo más amigable posible para los desarrolladores (es decir, la experiencia de desarrollo, o DX).

En algunos casos, favorecer la DX al escribir fragmentos cortos de JS, por sobre los pasos estrictos normales esperados para procesar un programa completo de JS, produce diferencias observables en el comportamiento del código entre programas y herramientas. Por ejemplo, ciertas condiciones de error aplicables a un programa de JS podrían relajarse y no mostrarse cuando el código se ingresa en una herramienta de desarrollo.

Con respecto a nuestras discusiones acá sobre el scope, tales diferencias observables en el comportamiento pueden incluir:

* El comportamiento del global scope

* Hoisting (ver Capítulo 5)

* Declaradores de block-scoping (`let` / `const`, ver Capítulo 6) cuando se usan en el scope más externo

Aunque podría parecer, mientras usás la consola/REPL, que las sentencias ingresadas en el scope más externo están siendo procesadas en el global scope real, eso no es del todo exacto. Tales herramientas típicamente emulan la posición del global scope hasta cierto punto; es emulación, no apego estricto. Estos entornos de herramientas priorizan la conveniencia del desarrollador, lo que significa que a veces (como en nuestras discusiones actuales sobre el scope), el comportamiento observado puede desviarse de la especificación de JS.

La conclusión es que las Developer Tools, si bien están optimizadas para ser convenientes y útiles para una variedad de actividades de desarrollo, **no** son entornos adecuados para determinar o verificar comportamientos explícitos y matizados del contexto real de un programa de JS.

### ES Modules (ESM)

ES6 introdujo soporte de primera clase para el patrón de módulos (cubierto en el Capítulo 8). Uno de los impactos más obvios de usar ESM es cómo cambia el comportamiento del scope de nivel superior observable en un archivo.

Recordá este fragmento de código de antes (que ajustaremos al formato ESM usando la palabra clave `export`):

```js
var studentName = "Kyle";

function hello() {
    console.log(`Hello, ${ studentName }!`);
}

hello();
// Hello, Kyle!

export hello;
```

Si ese código está en un archivo que se carga como un ES module, seguirá ejecutándose exactamente igual. Sin embargo, los efectos observables, desde la perspectiva general de la aplicación, serán diferentes.

A pesar de ser declarados en el nivel superior del archivo (módulo), en el scope más externo obvio, `studentName` y `hello` no son variables globales. En cambio, son de alcance a todo el módulo, o si preferís, "module-global".

Sin embargo, en un módulo no hay un "objeto de scope a nivel de módulo" implícito al que estas declaraciones de nivel superior se agreguen como propiedades, como sí lo hay cuando las declaraciones aparecen en el nivel superior de archivos de JS que no son módulos. Esto no quiere decir que las variables globales no puedan existir o ser accedidas en tales programas. Es solo que las variables globales no se *crean* al declarar variables en el scope de nivel superior de un módulo.

El scope de nivel superior del módulo desciende del global scope, casi como si todo el contenido del módulo estuviera envuelto en una función. Por lo tanto, todas las variables que existen en el global scope (¡estén o no en el global object!) están disponibles como identificadores léxicos desde dentro del scope del módulo.

ESM fomenta una minimización de la dependencia del global scope, donde importás los módulos que necesites para que el módulo actual opere. Como tal, ves con menos frecuencia el uso del global scope o de su global object.

Sin embargo, como se señaló antes, ¡todavía hay montones de globales de JS y de la web a los que vas a seguir accediendo desde el global scope, te des cuenta o no!

### Node

Un aspecto de Node que a menudo toma desprevenidos a los desarrolladores de JS es que Node trata cada archivo .js que carga, incluyendo el principal con el que iniciás el proceso de Node, como un *módulo* (ES module o módulo CommonJS, ver Capítulo 8). El efecto práctico es que el nivel superior de tus programas de Node **nunca es en realidad el global scope**, de la forma en que lo es al cargar un archivo que no es un módulo en el navegador.

Al momento de escribir esto, Node agregó recientemente soporte para ES modules. Pero además, Node ha soportado desde sus inicios un formato de módulos conocido como "CommonJS", que se ve así:

```js
var studentName = "Kyle";

function hello() {
    console.log(`Hello, ${ studentName }!`);
}

hello();
// Hello, Kyle!

module.exports.hello = hello;
```

Antes de procesarlo, Node efectivamente envuelve tal código en una función, de modo que las declaraciones `var` y `function` queden contenidas en el scope de esa función envoltura, **no** tratadas como variables globales.

Imaginá el código anterior tal como lo ve Node, de esta manera (ilustrativo, no real):

```js
function Module(module,require,__dirname,...) {
    var studentName = "Kyle";

    function hello() {
        console.log(`Hello, ${ studentName }!`);
    }

    hello();
    // Hello, Kyle!

    module.exports.hello = hello;
}
```

Node entonces esencialmente invoca la función `Module(..)` agregada para ejecutar tu módulo. Podés ver claramente acá por qué los identificadores `studentName` y `hello` no son globales, sino que están declarados en el scope del módulo.

Como se señaló antes, Node define una cantidad de "globales" como `require()`, pero en realidad no son identificadores en el global scope (ni propiedades del global object). Se inyectan en el scope de cada módulo, esencialmente un poco como los parámetros listados en la declaración de la función `Module(..)`.

Entonces, ¿cómo definís variables globales reales en Node? La única forma de hacerlo es agregar propiedades a otro de los "globales" provistos automáticamente por Node, que irónicamente se llama `global`. `global` es una referencia al objeto real del global scope, algo parecido a usar `window` en un entorno de JS de navegador.

Considerá:

```js
global.studentName = "Kyle";

function hello() {
    console.log(`Hello, ${ studentName }!`);
}

hello();
// Hello, Kyle!

module.exports.hello = hello;
```

Acá agregamos `studentName` como una propiedad del objeto `global`, y luego en la sentencia `console.log(..)` podemos acceder a `studentName` como una variable global normal.

Recordá que el identificador `global` no está definido por JS; está definido específicamente por Node.

## Global This

Repasando los entornos de JS que hemos examinado hasta ahora, un programa puede o no:

* Declarar una variable global en el scope de nivel superior con declaraciones `var` o `function`—o `let`, `const`, y `class`.

* También agregar las declaraciones de variables globales como propiedades del global scope object si se usa `var` o `function` para la declaración.

* Referirse al global scope object (para agregar o recuperar variables globales, como propiedades) con `window`, `self`, o `global`.

Creo que es justo decir que el acceso y comportamiento del global scope es más complicado de lo que la mayoría de los desarrolladores supone, como ilustraron las secciones anteriores. Pero la complejidad nunca es más obvia que al intentar precisar una referencia universalmente aplicable al global scope object.

Otro "truco" más para obtener una referencia al global scope object se ve así:

```js
const theGlobalScopeObject =
    (new Function("return this"))();
```

| NOTA: |
| :--- |
| Una función puede construirse dinámicamente a partir de código almacenado en un valor string con el constructor `Function()`, similar a `eval(..)` (ver "Haciendo Trampa: Modificaciones del Scope en Tiempo de Ejecución" en el Capítulo 1). Tal función se ejecutará automáticamente en modo non-strict (por razones de legado) cuando se invoque con la invocación de función normal `()` como se muestra; su `this` apuntará al global object. Ver el tercer libro de la serie, *Objects & Classes*, para más información sobre cómo se determinan los bindings de `this`. |

Entonces, tenemos `window`, `self`, `global`, y este feo truco de `new Function(..)`. Esas son muchas formas distintas de intentar llegar a este global object. Cada una tiene sus pros y sus contras.

¿¡¿Por qué no introducir una más?!?

A partir de ES2020, JS finalmente definió una referencia estandarizada al global scope object, llamada `globalThis`. Así que, sujeto a lo reciente que sean los engines de JS en los que se ejecuta tu código, podés usar `globalThis` en lugar de cualquiera de esos otros enfoques.

Hasta podríamos intentar definir un polyfill multi-entorno que sea más seguro en los entornos de JS previos a `globalThis`, como por ejemplo:

```js
const theGlobalScopeObject =
    (typeof globalThis != "undefined") ? globalThis :
    (typeof global != "undefined") ? global :
    (typeof window != "undefined") ? window :
    (typeof self != "undefined") ? self :
    (new Function("return this"))();
```

¡Uf! Eso sin duda no es lo ideal, pero funciona si te encontrás necesitando una referencia confiable al global scope.

(El nombre propuesto `globalThis` fue bastante controvertido mientras se agregaba la funcionalidad a JS. Específicamente, yo y muchos otros sentíamos que la referencia a "this" en su nombre era engañosa, ya que la razón por la que referenciás este objeto es para acceder al global scope, nunca para acceder a algún tipo de binding global/por defecto de `this`. Se consideraron muchos otros nombres, pero por una variedad de razones fueron descartados. Lamentablemente, el nombre elegido terminó siendo un último recurso. Si planeás interactuar con el global scope object en tus programas, para reducir la confusión, te recomiendo enfáticamente elegir un mejor nombre, como (¡el ridículamente largo pero preciso!) `theGlobalScopeObject` usado acá.)

## Globalmente Consciente

El global scope está presente y es relevante en todo programa de JS, aunque los patrones modernos para organizar código en módulos restan énfasis a gran parte de la dependencia de almacenar identificadores en ese namespace.

Aun así, a medida que nuestro código prolifera cada vez más allá de los confines del navegador, es especialmente importante que tengamos un dominio sólido de las diferencias en cómo el global scope (¡y el global scope object!) se comportan en los distintos entornos de JS.

Con el panorama general del global scope ahora más nítidamente enfocado, el próximo capítulo desciende nuevamente a los detalles más profundos del lexical scope, examinando cómo y cuándo pueden usarse las variables.
