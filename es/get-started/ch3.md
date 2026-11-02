# You Don't Know JS Yet: Get Started - 2nd Edition
# Capítulo 3: Cavando hasta las raíces de JS

Si leíste los Capítulos 1 y 2, y te tomaste el tiempo para digerirlos y asimilarlos, con suerte estarás empezando a *entender* un poco más JS. Si te los salteaste o los leíste por encima (especialmente el Capítulo 2), te recomiendo volver y pasar un poco más de tiempo con ese material.

En el Capítulo 2, examinamos la sintaxis, los patrones y los comportamientos a un nivel alto. En este capítulo, nuestra atención se desplaza hacia algunas de las características de raíz, de más bajo nivel, de JS, que sustentan prácticamente cada línea de código que escribimos.

Tené en cuenta: este capítulo cava mucho más profundo de lo que probablemente estés acostumbrado a pensar sobre un lenguaje de programación. Mi objetivo es ayudarte a apreciar el núcleo de cómo funciona JS, qué lo hace funcionar. Este capítulo debería empezar a responder algunas de las preguntas de "¿Por qué?" que puedan estar surgiendo a medida que explorás JS. Sin embargo, este material todavía no es una exposición exhaustiva del lenguaje; ¡para eso está el resto de la serie de libros! Nuestro objetivo acá sigue siendo simplemente *empezar* y sentirnos más cómodos con la *sensación* de JS, con cómo fluye y refluye.

No corras tan rápido a través de este material que termines perdido entre la maleza. Como ya dije una docena de veces, **tomate tu tiempo**. Aun así, probablemente termines este capítulo con preguntas pendientes. Está bien, ¡porque tenés una serie de libros entera por delante para seguir explorando!

## Iteración

Dado que los programas se construyen esencialmente para procesar datos (y tomar decisiones sobre esos datos), los patrones usados para recorrer los datos tienen un gran impacto en la legibilidad del programa.

El patrón iterador existe desde hace décadas, y sugiere un enfoque "estandarizado" para consumir datos de una fuente de a un *fragmento* por vez. La idea es que es más común y útil iterar la fuente de datos—manejar progresivamente la colección de datos procesando la primera parte, luego la siguiente, y así sucesivamente, en lugar de manejar todo el conjunto de una sola vez.

Imaginá una estructura de datos que representa una consulta `SELECT` a una base de datos relacional, que típicamente organiza los resultados como filas. Si esta consulta tuviera solo una o un par de filas, podrías manejar todo el conjunto de resultados de una vez, y asignar cada fila a una variable local, y realizar sobre esos datos cualquier operación que fuera apropiada.

Pero si la consulta tiene 100 o 1.000 (¡o más!) filas, vas a necesitar un procesamiento iterativo para lidiar con estos datos (típicamente, un bucle).

El patrón iterador define una estructura de datos llamada "iterador" que tiene una referencia a una fuente de datos subyacente (como las filas de resultado de la consulta), la cual expone un método como `next()`. Llamar a `next()` devuelve la siguiente pieza de datos (es decir, un "registro" o "fila" de una consulta a la base de datos).

No siempre sabés cuántas piezas de datos vas a necesitar iterar, así que el patrón típicamente indica la finalización mediante algún valor especial o excepción una vez que iterás a través de todo el conjunto y *pasás el final*.

La importancia del patrón iterador radica en adherir a una forma *estándar* de procesar datos iterativamente, lo que genera un código más limpio y fácil de entender, en contraposición a que cada estructura/fuente de datos defina su propia forma personalizada de manejar sus datos.

Después de muchos años de diversos esfuerzos de la comunidad de JS en torno a técnicas de iteración mutuamente acordadas, ES6 estandarizó un protocolo específico para el patrón iterador directamente en el lenguaje. El protocolo define un método `next()` cuyo retorno es un objeto llamado *resultado de iterador* (*iterator result*); el objeto tiene las propiedades `value` y `done`, donde `done` es un booleano que es `false` hasta que la iteración sobre la fuente de datos subyacente se completa.

### Consumiendo iteradores

Con el protocolo de iteración de ES6 en su lugar, es viable consumir una fuente de datos de a un valor por vez, comprobando después de cada llamada a `next()` si `done` es `true` para detener la iteración. Pero este enfoque es bastante manual, así que ES6 también incluyó varios mecanismos (sintaxis y APIs) para el consumo estandarizado de estos iteradores.

Uno de esos mecanismos es el bucle `for..of`:

```js
// given an iterator of some data source:
var it = /* .. */;

// loop over its results one at a time
for (let val of it) {
    console.log(`Iterator value: ${ val }`);
}
// Iterator value: ..
// Iterator value: ..
// ..
```

| NOTA: |
| :--- |
| Omitiremos acá el equivalente del bucle manual, ¡pero definitivamente es menos legible que el bucle `for..of`! |

Otro mecanismo que se usa a menudo para consumir iteradores es el operador `...`. Este operador tiene en realidad dos formas simétricas: *spread* (dispersión) y *rest* (o *gather* / reunión, como prefiero llamarlo). La forma *spread* es un consumidor de iteradores.

Para hacer *spread* de un iterador, tenés que tener *algo* en lo cual dispersarlo. Hay dos posibilidades en JS: un array o una lista de argumentos para una llamada a función.

Un spread de array:

```js
// spread an iterator into an array,
// with each iterated value occupying
// an array element position.
var vals = [ ...it ];
```

Un spread de llamada a función:

```js
// spread an iterator into a function,
// call with each iterated value
// occupying an argument position.
doSomethingUseful( ...it );
```

En ambos casos, la forma de iterator-spread de `...` sigue el protocolo de consumo de iteradores (el mismo que el bucle `for..of`) para recuperar todos los valores disponibles de un iterador y colocarlos (es decir, dispersarlos) en el contexto receptor (array, lista de argumentos).

### Iterables

El protocolo de consumo de iteradores está técnicamente definido para consumir *iterables*; un iterable es un valor que puede ser iterado.

El protocolo crea automáticamente una instancia de iterador a partir de un iterable, y consume *solo esa instancia de iterador* hasta su finalización. Esto significa que un único iterable podría consumirse más de una vez; cada vez, se crearía y usaría una nueva instancia de iterador.

Entonces, ¿dónde encontramos iterables?

ES6 definió como iterables los tipos básicos de estructura de datos/colección en JS. Esto incluye strings, arrays, maps, sets y otros.

Consideremos:

```js
// an array is an iterable
var arr = [ 10, 20, 30 ];

for (let val of arr) {
    console.log(`Array value: ${ val }`);
}
// Array value: 10
// Array value: 20
// Array value: 30
```

Dado que los arrays son iterables, podemos hacer una copia superficial de un array usando el consumo de iteradores a través del operador spread `...`:

```js
var arrCopy = [ ...arr ];
```

También podemos iterar los caracteres de un string de a uno por vez:

```js
var greeting = "Hello world!";
var chars = [ ...greeting ];

chars;
// [ "H", "e", "l", "l", "o", " ",
//   "w", "o", "r", "l", "d", "!" ]
```

Una estructura de datos `Map` usa objetos como claves, asociando un valor (de cualquier tipo) con ese objeto. Los maps tienen una iteración por defecto diferente a la vista acá, en el sentido de que la iteración no es solo sobre los valores del map sino sobre sus *entradas* (*entries*). Una *entrada* es una tupla (array de 2 elementos) que incluye tanto una clave como un valor.

Consideremos:

```js
// given two DOM elements, `btn1` and `btn2`

var buttonNames = new Map();
buttonNames.set(btn1,"Button 1");
buttonNames.set(btn2,"Button 2");

for (let [btn,btnName] of buttonNames) {
    btn.addEventListener("click",function onClick(){
        console.log(`Clicked ${ btnName }`);
    });
}
```

En el bucle `for..of` sobre la iteración por defecto del map, usamos la sintaxis `[btn,btnName]` (llamada "desestructuración de array") para descomponer cada tupla consumida en los respectivos pares clave/valor (`btn1` / `"Button 1"` y `btn2` / `"Button 2"`).

Cada uno de los iterables incorporados en JS expone una iteración por defecto, una que probablemente coincida con tu intuición. Pero también podés elegir una iteración más específica si es necesario. Por ejemplo, si queremos consumir solo los valores del map `buttonNames` anterior, podemos llamar a `values()` para obtener un iterador solo de valores:

```js
for (let btnName of buttonNames.values()) {
    console.log(btnName);
}
// Button 1
// Button 2
```

O si queremos el índice *y* el valor en una iteración de array, podemos crear un iterador de entradas con el método `entries()`:

```js
var arr = [ 10, 20, 30 ];

for (let [idx,val] of arr.entries()) {
    console.log(`[${ idx }]: ${ val }`);
}
// [0]: 10
// [1]: 20
// [2]: 30
```

En su mayor parte, todos los iterables incorporados en JS tienen tres formas de iterador disponibles: solo claves (`keys()`), solo valores (`values()`) y entradas (`entries()`).

Más allá de simplemente usar los iterables incorporados, también podés asegurarte de que tus propias estructuras de datos adhieran al protocolo de iteración; hacer esto significa que optás por la capacidad de consumir tus datos con bucles `for..of` y el operador `...`. "Estandarizar" sobre este protocolo significa un código que, en general, es más fácilmente reconocible y legible.

| NOTA: |
| :--- |
| Puede que hayas notado un cambio sutil que ocurrió en esta discusión. Empezamos hablando de consumir **iteradores**, pero luego pasamos a hablar de iterar sobre **iterables**. El protocolo de consumo de iteración espera un *iterable*, pero la razón por la que podemos proporcionar un *iterador* directamente es que ¡un iterador es simplemente un iterable de sí mismo! Al crear una instancia de iterador a partir de un iterador existente, el iterador mismo es devuelto. |

## Closure

Quizás sin darse cuenta, casi todo desarrollador de JS ha hecho uso de closure. De hecho, closure es una de las funcionalidades de programación más omnipresentes en la mayoría de los lenguajes. Hasta podría ser tan importante de entender como las variables o los bucles; así de fundamental es.

Sin embargo, se siente como algo oculto, casi mágico. Y a menudo se habla de él en términos muy abstractos o muy informales, lo que poco ayuda a precisar exactamente qué es.

Necesitamos ser capaces de reconocer dónde se usa closure en los programas, ya que la presencia o ausencia de closure es a veces la causa de bugs (o incluso la causa de problemas de rendimiento).

Así que definamos closure de una manera pragmática y concreta:

> Closure es cuando una función recuerda y continúa accediendo a variables de fuera de su scope, incluso cuando la función se ejecuta en un scope diferente.

Vemos acá dos características definitorias. Primero, closure es parte de la naturaleza de una función. Los objetos no obtienen closures, las funciones sí. Segundo, para observar un closure, debés ejecutar una función en un scope diferente de aquel donde esa función fue originalmente definida.

Consideremos:

```js
function greeting(msg) {
    return function who(name) {
        console.log(`${ msg }, ${ name }!`);
    };
}

var hello = greeting("Hello");
var howdy = greeting("Howdy");

hello("Kyle");
// Hello, Kyle!

hello("Sarah");
// Hello, Sarah!

howdy("Grant");
// Howdy, Grant!
```

Primero, la función externa `greeting(..)` se ejecuta, creando una instancia de la función interna `who(..)`; esa función cierra (closes over) sobre la variable `msg`, que es el parámetro del scope externo de `greeting(..)`. Cuando esa función interna es devuelta, su referencia se asigna a la variable `hello` en el scope externo. Luego llamamos a `greeting(..)` una segunda vez, creando una nueva instancia de función interna, con un nuevo closure sobre un nuevo `msg`, y devolvemos esa referencia para que se asigne a `howdy`.

Cuando la función `greeting(..)` termina de ejecutarse, normalmente esperaríamos que todas sus variables fueran recolectadas por el garbage collector (eliminadas de la memoria). Esperaríamos que cada `msg` desapareciera, pero no lo hacen. La razón es closure. Dado que las instancias de la función interna siguen vivas (asignadas a `hello` y `howdy`, respectivamente), sus closures siguen preservando las variables `msg`.

Estos closures no son una instantánea del valor de la variable `msg`; son un enlace directo y una preservación de la variable misma. Eso significa que closure puede en realidad observar (¡o hacer!) actualizaciones a estas variables a lo largo del tiempo.

```js
function counter(step = 1) {
    var count = 0;
    return function increaseCount(){
        count = count + step;
        return count;
    };
}

var incBy1 = counter(1);
var incBy3 = counter(3);

incBy1();       // 1
incBy1();       // 2

incBy3();       // 3
incBy3();       // 6
incBy3();       // 9
```

Cada instancia de la función interna `increaseCount()` cierra sobre las variables `count` y `step` del scope de su función externa `counter(..)`. `step` permanece igual a lo largo del tiempo, pero `count` se actualiza en cada invocación de esa función interna. Dado que closure es sobre las variables y no solo sobre instantáneas de los valores, estas actualizaciones se preservan.

Closure es más común cuando se trabaja con código asíncrono, como con callbacks. Consideremos:

```js
function getSomeData(url) {
    ajax(url,function onResponse(resp){
        console.log(
            `Response (from ${ url }): ${ resp }`
        );
    });
}

getSomeData("https://some.url/wherever");
// Response (from https://some.url/wherever): ...
```

La función interna `onResponse(..)` cierra sobre `url`, y por lo tanto la preserva y la recuerda hasta que la llamada Ajax retorna y ejecuta `onResponse(..)`. Aunque `getSomeData(..)` termina de inmediato, la variable del parámetro `url` se mantiene viva en el closure durante todo el tiempo que sea necesario.

No es necesario que el scope externo sea una función—usualmente lo es, pero no siempre—solo que haya al menos una variable en un scope externo a la que se acceda desde una función interna:

```js
for (let [idx,btn] of buttons.entries()) {
    btn.addEventListener("click",function onClick(){
       console.log(`Clicked on button (${ idx })!`);
    });
}
```

Debido a que este bucle usa declaraciones `let`, cada iteración obtiene nuevas variables `idx` y `btn` con scope de bloque (es decir, locales); el bucle también crea una nueva función interna `onClick(..)` cada vez. Esa función interna cierra sobre `idx`, preservándolo durante todo el tiempo que el manejador de clic esté asignado al `btn`. Así que cuando se hace clic en cada botón, su manejador puede imprimir su valor de índice asociado, porque el manejador recuerda su respectiva variable `idx`.

Recordá: este closure no es sobre el valor (como `1` o `3`), sino sobre la variable `idx` misma.

Closure es uno de los patrones de programación más prevalentes e importantes en cualquier lenguaje. Pero eso es especialmente cierto en JS; es difícil imaginar hacer algo útil sin aprovechar closure de una forma u otra.

Si todavía te sentís poco claro o inseguro respecto a closure, la mayor parte del Libro 2, *Scope & Closures*, está enfocada en el tema.

## La palabra clave `this`

Uno de los mecanismos más poderosos de JS es también uno de los más malentendidos: la palabra clave `this`. Una idea errónea común es que el `this` de una función se refiere a la función misma. Debido a cómo funciona `this` en otros lenguajes, otra idea errónea es que `this` apunta a la instancia a la que pertenece un método. Ambas son incorrectas.

Como se discutió anteriormente, cuando una función se define, queda *adjuntada* a su scope circundante a través de closure. El scope es el conjunto de reglas que controla cómo se resuelven las referencias a las variables.

Pero las funciones también tienen otra característica, además de su scope, que influye en lo que pueden acceder. Esta característica se describe mejor como un *contexto de ejecución* (*execution context*), y se expone a la función a través de su palabra clave `this`.

El scope es estático y contiene un conjunto fijo de variables disponibles en el momento y lugar donde definís una función, pero el *contexto* de ejecución de una función es dinámico, enteramente dependiente de **cómo es llamada** (independientemente de dónde esté definida o incluso desde dónde sea llamada).

`this` no es una característica fija de una función basada en la definición de la función, sino más bien una característica dinámica que se determina cada vez que la función es llamada.

Una forma de pensar sobre el *contexto de ejecución* es que es un objeto tangible cuyas propiedades se ponen a disposición de una función mientras se ejecuta. Compará eso con el scope, que también puede pensarse como un *objeto*; excepto que el *objeto de scope* está oculto dentro del engine de JS, siempre es el mismo para esa función, y sus *propiedades* toman la forma de variables identificadoras disponibles dentro de la función.

```js
function classroom(teacher) {
    return function study() {
        console.log(
            `${ teacher } says to study ${ this.topic }`
        );
    };
}
var assignment = classroom("Kyle");
```

La función externa `classroom(..)` no hace ninguna referencia a una palabra clave `this`, así que es simplemente como cualquier otra función que vimos hasta ahora. Pero la función interna `study()` sí hace referencia a `this`, lo que la convierte en una función consciente de `this` (*`this`-aware*). En otras palabras, es una función que depende de su *contexto de ejecución*.

| NOTA: |
| :--- |
| `study()` también cierra sobre la variable `teacher` de su scope externo. |

La función interna `study()` devuelta por `classroom("Kyle")` se asigna a una variable llamada `assignment`. Entonces, ¿cómo puede llamarse `assignment()` (es decir, `study()`)?

```js
assignment();
// Kyle says to study undefined  -- Oops :(
```

En este fragmento, llamamos a `assignment()` como una función común y corriente, sin proporcionarle ningún *contexto de ejecución*.

Dado que este programa no está en strict mode (ver Capítulo 1, "Hablando estrictamente"), las funciones conscientes del contexto que son llamadas **sin ningún contexto especificado** usan por defecto como contexto el objeto global (`window` en el navegador). Como no existe una variable global llamada `topic` (y por lo tanto no existe tal propiedad en el objeto global), `this.topic` se resuelve a `undefined`.

Ahora consideremos:

```js
var homework = {
    topic: "JS",
    assignment: assignment
};

homework.assignment();
// Kyle says to study JS
```

Una copia de la referencia a la función `assignment` se establece como una propiedad en el objeto `homework`, y luego se llama como `homework.assignment()`. Eso significa que el `this` para esa llamada a función será el objeto `homework`. Por lo tanto, `this.topic` se resuelve a `"JS"`.

Por último:

```js
var otherHomework = {
    topic: "Math"
};

assignment.call(otherHomework);
// Kyle says to study Math
```

Una tercera forma de invocar una función es con el método `call(..)`, que toma un objeto (`otherHomework` acá) para usarlo al establecer la referencia `this` para la llamada a función. La referencia a la propiedad `this.topic` se resuelve a `"Math"`.

La misma función consciente del contexto, invocada de tres formas diferentes, da respuestas diferentes cada vez respecto a qué objeto referenciará `this`.

El beneficio de las funciones conscientes de `this`—y su contexto dinámico—es la capacidad de reutilizar de forma más flexible una única función con datos de distintos objetos. Una función que cierra sobre un scope nunca puede referenciar un scope o conjunto de variables diferente. Pero una función que tiene conciencia dinámica de contexto `this` puede ser bastante útil para ciertas tareas.

## Prototypes

Mientras que `this` es una característica de la ejecución de funciones, un prototype es una característica de un objeto, y específicamente de la resolución de un acceso a propiedad.

Pensá en un prototype como un enlace entre dos objetos; el enlace está oculto detrás de escena, aunque hay formas de exponerlo y observarlo. Este enlace de prototype ocurre cuando se crea un objeto; queda enlazado a otro objeto que ya existe.

Una serie de objetos enlazados entre sí a través de prototypes se llama la "cadena de prototypes" (*prototype chain*).

El propósito de este enlace de prototype (es decir, de un objeto B a otro objeto A) es que los accesos contra B para propiedades/métodos que B no tiene sean *delegados* a A para que los maneje. La delegación del acceso a propiedad/método permite que dos (¡o más!) objetos cooperen entre sí para realizar una tarea.

Consideremos definir un objeto como un literal normal:

```js
var homework = {
    topic: "JS"
};
```

El objeto `homework` solo tiene una única propiedad: `topic`. Sin embargo, su enlace de prototype por defecto conecta con el objeto `Object.prototype`, que tiene métodos comunes incorporados como `toString()` y `valueOf()`, entre otros.

Podemos observar esta *delegación* mediante el enlace de prototype desde `homework` hacia `Object.prototype`:

```js
homework.toString();    // [object Object]
```

`homework.toString()` funciona aunque `homework` no tenga un método `toString()` definido; la delegación invoca `Object.prototype.toString()` en su lugar.

### Enlace de objetos

Para definir un enlace de prototype de objeto, podés crear el objeto usando la utilidad `Object.create(..)`:

```js
var homework = {
    topic: "JS"
};

var otherHomework = Object.create(homework);

otherHomework.topic;   // "JS"
```

El primer argumento de `Object.create(..)` especifica un objeto al cual enlazar el objeto recién creado, y luego devuelve el objeto recién creado (¡y enlazado!).

La Figura 4 muestra cómo los tres objetos (`otherHomework`, `homework` y `Object.prototype`) están enlazados en una cadena de prototypes:

<figure>
    <img src="images/fig4.png" width="200" alt="Prototype chain with 3 objects" align="center">
    <figcaption><em>Fig. 4: Objetos en una cadena de prototypes</em></figcaption>
    <br><br>
</figure>

La delegación a través de la cadena de prototypes solo se aplica a los accesos para buscar el valor de una propiedad. Si asignás a una propiedad de un objeto, eso se aplicará directamente al objeto, sin importar a dónde esté enlazado por prototype ese objeto.

| TIP: |
| :--- |
| `Object.create(null)` crea un objeto que no está enlazado por prototype a ningún lado, así que es puramente un objeto independiente; en algunas circunstancias, eso puede ser preferible. |

Consideremos:

```js
homework.topic;
// "JS"

otherHomework.topic;
// "JS"

otherHomework.topic = "Math";
otherHomework.topic;
// "Math"

homework.topic;
// "JS" -- not "Math"
```

La asignación a `topic` crea una propiedad con ese nombre directamente en `otherHomework`; no hay ningún efecto sobre la propiedad `topic` en `homework`. La siguiente sentencia luego accede a `otherHomework.topic`, y vemos la respuesta no delegada de esa nueva propiedad: `"Math"`.

La Figura 5 muestra los objetos/propiedades después de la asignación que crea la propiedad `otherHomework.topic`:

<figure>
    <img src="images/fig5.png" width="200" alt="3 objects linked, with shadowed property" align="center">
    <figcaption><em>Fig. 5: Propiedad 'topic' ensombrecida (shadowed)</em></figcaption>
    <br><br>
</figure>

El `topic` en `otherHomework` está "ensombreciendo" (*shadowing*) a la propiedad del mismo nombre en el objeto `homework` dentro de la cadena.

| NOTA: |
| :--- |
| Otra forma, francamente más enrevesada pero quizás aún más común, de crear un objeto con un enlace de prototype es usando el patrón de "clase prototípica" (*prototypal class*), de antes de que se agregara `class` (ver Capítulo 2, "Clases") en ES6. Cubriremos este tema con más detalle en el Apéndice A, "'Clases' prototípicas". |

### `this` revisitado

Cubrimos la palabra clave `this` antes, pero su verdadera importancia brilla cuando se considera cómo potencia las llamadas a funciones delegadas por prototype. De hecho, una de las razones principales por las que `this` soporta un contexto dinámico basado en cómo se llama la función es para que las llamadas a métodos sobre objetos que delegan a través de la cadena de prototypes mantengan igualmente el `this` esperado.

Consideremos:

```js
var homework = {
    study() {
        console.log(`Please study ${ this.topic }`);
    }
};

var jsHomework = Object.create(homework);
jsHomework.topic = "JS";
jsHomework.study();
// Please study JS

var mathHomework = Object.create(homework);
mathHomework.topic = "Math";
mathHomework.study();
// Please study Math
```

Los dos objetos `jsHomework` y `mathHomework` cada uno se enlazan por prototype al único objeto `homework`, que tiene la función `study()`. A `jsHomework` y `mathHomework` se les da a cada uno su propia propiedad `topic` (ver Figura 6).

<figure>
    <img src="images/fig6.png" width="495" alt="4 objects prototype linked" align="center">
    <figcaption><em>Fig. 6: Dos objetos enlazados a un padre común</em></figcaption>
    <br><br>
</figure>

`jsHomework.study()` delega a `homework.study()`, pero su `this` (`this.topic`) para esa ejecución se resuelve a `jsHomework` debido a cómo se llama la función, así que `this.topic` es `"JS"`. De forma similar, `mathHomework.study()` delega a `homework.study()` pero igualmente resuelve `this` a `mathHomework`, y por lo tanto `this.topic` como `"Math"`.

El fragmento de código anterior sería mucho menos útil si `this` se resolviera a `homework`. Sin embargo, en muchos otros lenguajes, parecería que `this` sería `homework` porque el método `study()` está efectivamente definido en `homework`.

A diferencia de muchos otros lenguajes, el hecho de que el `this` de JS sea dinámico es un componente crítico que permite que la delegación de prototype, y de hecho `class`, ¡funcionen como se espera!

## Preguntando "¿Por qué?"

La conclusión que se pretende extraer de este capítulo es que hay mucho más en JS bajo el capó de lo que resulta obvio al echar un vistazo a la superficie.

A medida que estás *empezando* a aprender y conocer JS más de cerca, una de las habilidades más importantes que podés practicar y reforzar es la curiosidad, y el arte de preguntar "¿Por qué?" cuando te encontrás con algo en el lenguaje.

Aunque este capítulo profundizó bastante en algunos de los temas, muchos detalles todavía fueron pasados por alto por completo. Hay mucho más para aprender acá, y el camino hacia eso empieza con vos haciéndole las preguntas *correctas* a tu código. Hacer las preguntas correctas es una habilidad crítica para convertirse en un mejor desarrollador.

En el capítulo final de este libro, vamos a ver brevemente cómo está dividido JS, tal como se cubre a lo largo del resto de la serie de libros *You Don't Know JS Yet*. Además, no te saltees el Apéndice B de este libro, que tiene algo de código de práctica para repasar algunos de los temas principales cubiertos en este libro.
