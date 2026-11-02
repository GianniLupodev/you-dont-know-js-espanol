# You Don't Know JS Yet: Objects & Classes - 2nd Edition
# Capítulo 5: Delegación

| NOTA: |
| :--- |
| Trabajo en progreso |

Exploramos a fondo los objetos, los prototipos, las clases y, ahora, la palabra clave `this`. Pero vamos a revisar lo que aprendimos hasta ahora desde una perspectiva un poco diferente.

¿Y si pudieras aprovechar todo el poder de los objetos, los prototipos y los mecanismos dinámicos de `this` en conjunto, sin usar nunca `class` ni ninguno de sus derivados?

De hecho, yo diría que JS es, en esencia, menos orientado a clases de lo que la palabra clave `class` pudiera aparentar. Dado que JS es un lenguaje dinámico y prototípico, su punto fuerte es, en realidad... la *delegación*.

## Preámbulo

Antes de empezar a mirar la delegación, quiero ofrecer una advertencia. Esta perspectiva sobre los mecanismos de `[[Prototype]]` de los objetos de JS y de contexto de función `this` *no* es la corriente principal. *No* es la forma en que los autores de frameworks y bibliotecas utilizan JS. Hasta donde sé, no vas a encontrar ninguna aplicación grande por ahí que use este patrón.

Entonces, ¿por qué demonios le dedicaría un capítulo a semejante patrón, si es tan impopular?

Buena pregunta. La respuesta descarada es: ¡porque es mi libro y puedo hacer lo que se me antoje!

Pero la respuesta más profunda es porque creo que desarrollar *esta* comprensión de uno de los pilares centrales del lenguaje te ayuda *incluso si* todo lo que vas a hacer es usar patrones de JS al estilo `class`.

Para ser claro, la delegación no es un invento mío. Existe como patrón de diseño desde hace décadas. Y durante mucho tiempo, los desarrolladores argumentaron que la delegación prototípica era *simplemente* la forma dinámica de la herencia.[^TreatyOfOrlando] Pero creo que fue un error confundir ambas.[^ClassVsPrototype]

Para los fines de este capítulo, voy a presentar la delegación, tal como se implementa mediante los mecanismos de JS, como un patrón de diseño alternativo, posicionado en algún punto entre la orientación a clases y los patrones de objeto-clausura/módulo.

El primer paso es *deconstruir* el mecanismo de `class` hasta sus partes individuales. Luego seleccionaremos y mezclaremos las partes de una forma un poco diferente.

## ¿Qué es un constructor, de todos modos?

En el Capítulo 3, vimos `constructor(..)` como el punto de entrada principal para la construcción de una instancia de `class`. Pero el `constructor(..)` en realidad no hace ningún trabajo de *creación*, solo hace trabajo de *inicialización*. En otras palabras, la instancia ya está creada para cuando el `constructor(..)` se ejecuta y la inicializa; por ejemplo, asignaciones del tipo `this.whatever`.

Entonces, ¿dónde ocurre realmente el trabajo de *creación*? En el operador `new`. Como explica la sección "Invocación de Contexto con New" del Capítulo 4, hay cuatro pasos que la palabra clave `new` realiza; el primero de ellos es la creación de un nuevo objeto vacío (la instancia). El `constructor(..)` ni siquiera se invoca hasta el paso 3 de la labor de `new`.

Pero `new` no es la única manera —ni quizás, siquiera, la mejor— de *crear* una "instancia" de objeto. Considerá:

```js
// a non-class "constructor"
function Point2d(x,y) {
    // create an object (1)
    var instance = {};

    // initialize the instance (3)
    instance.x = x;
    instance.y = y;

    // return the instance (4)
    return instance;
}

var point = Point2d(3,4);

point.x;                    // 3
point.y;                    // 4
```

No hay `class`, solo una definición de función regular (`Point2d(..)`). No hay invocación con `new`, solo una llamada de función regular (`Point2d(3,4)`). Y no hay referencias a `this`, solo asignaciones regulares de propiedades de objeto (`instance.x = ..`).

El término que se usa con más frecuencia para referirse a este patrón de código es que `Point2d(..)` aquí es una *función fábrica* (*factory function*). Invocarla provoca la construcción (creación e inicialización) de un objeto, y nos lo devuelve. Ese es un patrón extremadamente común, al menos tan común como el código orientado a clases.

Anoté con comentarios `(1)`, `(3)` y `(4)` en ese fragmento, que corresponden aproximadamente a los pasos 1, 3 y 4 de la operación `new`. Pero ¿dónde está el paso 2?

Si recordás, el paso 2 de `new` consiste en enlazar el objeto (creado en el paso 1) a otro objeto, mediante su slot `[[Prototype]]` (ver Capítulo 2). Entonces, ¿a qué objeto querríamos enlazar nuestro objeto `instance`? Podríamos enlazarlo a un objeto que contenga funciones que quisiéramos asociar/usar con nuestra instancia.

Modifiquemos el fragmento anterior:

```js
var prototypeObj = {
    toString() {
        return `(${this.x},${this.y})`;
    },
}

// a non-class "constructor"
function Point2d(x,y) {
    // create an object (1)
    var instance = {
        // link the instance's [[Prototype]] (2)
        __proto__: prototypeObj,
    };

    // initialize the instance (3)
    instance.x = x;
    instance.y = y;

    // return the instance (4)
    return instance;
}

var point = Point2d(3,4);

point.toString();           // (3,4)
```

Ahora ves la asignación de `__proto__` que establece el enlace interno de `[[Prototype]]`, que era el paso 2 faltante. Usé `__proto__` acá meramente con fines ilustrativos; usar `setPrototypeOf(..)` como se mostró en el Capítulo 4 habría logrado la misma tarea.

### Instancia de Fábrica con *New*

¿Qué pensás que pasaría si usáramos `new` para invocar la función `Point2d(..)` tal como se muestra acá?

```js
var anotherPoint = new Point2d(5,6);

anotherPoint.toString(5,6);         // (5,6)
```

¡Esperá! ¿Qué está pasando acá? Una función fábrica regular, no-`class`, se invoca con la palabra clave `new`, como si fuera una `class`. ¿Eso cambia algo en el resultado del código?

No... y sí. `anotherPoint` acá es exactamente el mismo objeto que habría sido si no hubiera usado `new`. ¡Pero! ¿El objeto que `new` crea, enlaza y asigna como contexto `this`? *Ese* objeto fue completamente ignorado y descartado, para terminar siendo recolectado por el recolector de basura de JS. Lamentablemente, el engine de JS no puede predecir que no vas a usar el objeto que le pediste a `new` que creara, así que siempre se crea igual, aunque quede sin usar.

¡Así es! Usar una palabra clave `new` contra una función fábrica puede *sentirse* más ergonómico o familiar, pero es bastante derrochador, en el sentido de que crea **dos** objetos y descarta inútilmente uno de ellos.

### Inicialización de Fábrica

En el ejemplo de código actual, la función `Point2d(..)` todavía se parece muchísimo a un `constructor(..)` normal de una definición de `class`. Pero ¿y si moviéramos el código de inicialización a una función aparte, digamos llamada `init(..)`?

```js
var prototypeObj = {
    init(x,y) {
        // initialize the instance (3)
        this.x = x;
        this.y = y;
    },
    toString() {
        return `(${this.x},${this.y})`;
    },
}

// a non-class "constructor"
function Point2d(x,y) {
    // create an object (1)
    var instance = {
        // link the instance's [[Prototype]] (2)
        __proto__: prototypeObj,
    };

    // initialize the instance (3)
    instance.init(x,y);

    // return the instance (4)
    return instance;
}

var point = Point2d(3,4);

point.toString();           // (3,4)
```

La llamada `instance.init(..)` hace uso del enlace de `[[Prototype]]` establecido mediante la asignación de `__proto__`. Por lo tanto, *delega* hacia arriba por la cadena de prototipos hasta `prototypeObj.init(..)`, y lo invoca con un contexto `this` de `instance`; mediante asignación de *contexto implícito* (ver Capítulo 4).

Continuemos la deconstrucción. ¡Preparate para un cambiazo!

```js
var Point2d = {
    init(x,y) {
        // initialize the instance (3)
        this.x = x;
        this.y = y;
    },
    toString() {
        return `(${this.x},${this.y})`;
    },
};
```

¡Pará, qué! Descarté la función `Point2d(..)` y, en su lugar, renombré `prototypeObj` como `Point2d`. Raro.

Pero miremos el resto del código ahora:

```js
// steps 1, 2, and 4
var point = { __proto__: Point2d, };

// step 3
point.init(3,4);

point.toString();           // (3,4)
```

Y un último refinamiento: usemos una utilidad integrada que JS nos provee, llamada `Object.create(..)`:

```js
// steps 1, 2, and 4
var point = Object.create(Point2d);

// step 3
point.init(3,4);

point.toString();           // (3,4)
```

¿Qué operaciones realiza `Object.create(..)`?

1. crea un objeto vacío nuevo, de la nada.

2. enlaza el `[[Prototype]]` de ese nuevo objeto vacío al objeto `.prototype` de la función.

Si eso te resulta familiar, es porque son exactamente los mismos dos primeros pasos de la palabra clave `new` (ver Capítulo 4).

Volvamos a juntar esto ahora:

```js
var Point2d = {
    init(x,y) {
        this.x = x;
        this.y = y;
    },
    toString() {
        return `(${this.x},${this.y})`;
    },
};

var point = Object.create(Point2d);

point.init(3,4);

point.toString();           // (3,4)
```

Mmm. Tomate unos momentos para reflexionar sobre lo que se derivó acá. ¿Cómo se compara con el enfoque de `class`?

Este patrón descarta las palabras clave `class` y `new`, pero logra exactamente el mismo resultado. ¿El *costo*? La única operación `new` se dividió en dos sentencias: `Object.create(Point2d)` y `point.init(3,4)`.

#### ¡Ayudame a Reconstruir!

Si tener esas dos operaciones separadas te molesta —¿está *demasiado deconstruido*!?—, siempre pueden recombinarse en un pequeño helper de fábrica:

```js
function make(objType,...args) {
    var instance = Object.create(objType);
    instance.init(...args);
    return instance;
}

var point = make(Point2d,3,4);

point.toString();           // (3,4)
```

| TIP: |
| :--- |
| Semejante helper de función fábrica `make(..)` funciona de forma general para cualquier tipo de objeto, siempre que sigas la convención implícita de que cada `objType` al que enlaces tenga una función llamada `init(..)` en él. |

Y, por supuesto, todavía podés crear tantas instancias como quieras:

```js
var point = make(Point2d,3,4);

var anotherPoint = make(Point2d,5,6);
```

## Dejando de Lado el Pensamiento de Clase

Francamente, la *deconstrucción* que acabamos de atravesar solo termina en código ligeramente diferente, y quizás ligeramente mejor o ligeramente peor, comparado con el estilo `class`. Si eso fuera todo lo que trata la delegación, probablemente ni siquiera sería lo suficientemente útil como para más que una nota al pie, mucho menos un capítulo entero.

Pero acá es donde vamos a empezar a dejar de lado en serio el pensamiento orientado a clases en sí mismo, no solo la sintaxis.

El diseño orientado a clases crea inherentemente una jerarquía de *clasificación*, es decir, cómo dividimos y agrupamos características, y luego las apilamos verticalmente en una cadena de herencia. Además, definir una subclase es una especialización de la clase base generalizada. Instanciar es una especialización de la clase generalizada.

El comportamiento en una jerarquía de clases tradicional es una composición vertical a través de las capas de la cadena de herencia. A lo largo de las décadas se han hecho intentos, e incluso se han vuelto bastante populares en ciertos momentos, de aplanar jerarquías profundas de herencia y favorecer una composición más horizontal mediante *mixins* e ideas relacionadas.

No estoy afirmando que haya algo malo en esas formas de abordar el código. Pero sí estoy diciendo que no son *naturalmente* cómo funciona JS, así que adoptarlas en JS ha sido un camino largo, sinuoso y complicado, y ha acumulado, de diversas maneras, mucha sintaxis llena de matices para adaptarlas por encima del pilar central de `[[Prototype]]` y `this` de JS.

Durante el resto de este capítulo, pretendo descartar tanto la sintaxis de `class` *como* el pensamiento de *clase*.

## La Delegación Ilustrada

Entonces, ¿de qué trata la delegación? En su esencia, trata de que dos o más *cosas* compartan el esfuerzo de completar una tarea.

En lugar de definir una *cosa* padre general `Point2d` que representa un comportamiento compartido del que un conjunto de una o más *cosas* hijas `point` / `anotherPoint` heredan, la delegación nos lleva a construir nuestro programa con *cosas* pares discretas que cooperan entre sí.

Voy a esbozar eso en algo de código:

```js
var Coordinates = {
    setX(x) {
        this.x = x;
    },
    setY(y) {
        this.y = y;
    },
    setXY(x,y) {
        this.setX(x);
        this.setY(y);
    },
};

var Inspect = {
    toString() {
        return `(${this.x},${this.y})`;
    },
};

var point = {};

Coordinates.setXY.call(point,3,4);
Inspect.toString.call(point);         // (3,4)

var anotherPoint = Object.create(Coordinates);

anotherPoint.setXY(5,6);
Inspect.toString.call(anotherPoint);  // (5,6)
```

Desglosemos lo que está pasando acá.

Definí `Coordinates` como un objeto concreto que contiene algunos comportamientos que asocio con el establecimiento de coordenadas de puntos (`x` e `y`). También definí `Inspect` como un objeto concreto que contiene algo de lógica de inspección para depuración, como `toString()`.

Luego creo dos objetos concretos más, `point` y `anotherPoint`.

`point` no tiene un `[[Prototype]]` específico (por defecto: `Object.prototype`). Usando asignación de *contexto explícito* (ver Capítulo 4), invoco las utilidades `Coordinates.setXY(..)` e `Inspect.toString()` en el contexto de `point`. A eso lo llamo *delegación explícita*.

`anotherPoint` está enlazado por `[[Prototype]]` a `Coordinates`, principalmente por una cuestión de conveniencia. Eso me permite usar asignación de *contexto implícito* con `anotherPoint.setXY(..)`. Pero todavía puedo compartir *explícitamente* `anotherPoint` como contexto para la llamada `Inspect.toString()`. A eso lo llamo *delegación implícita*.

**No te pierdas *esto*:** De todas formas logramos la composición: compusimos los comportamientos de `Coordinates` e `Inspect`, durante invocaciones de funciones en tiempo de ejecución con compartición del contexto `this`. No tuvimos que combinar en el código esos comportamientos dentro de una única `class` (o una jerarquía de `class` base-subclase) de la que `point` / `anotherPoint` heredaran. Me gusta llamar a esto composición en tiempo de ejecución, **composición virtual**.

El *punto* acá es: ninguno de estos cuatro objetos es un padre o un hijo. Todos son pares entre sí, y todos tienen propósitos diferentes. Podemos organizar nuestro comportamiento en fragmentos lógicos (en cada objeto respectivo) y compartir el contexto mediante `this` (y, opcionalmente, el enlace de `[[Prototype]]`), lo que termina con los mismos resultados de composición que los otros patrones que examinamos hasta ahora en el libro.

*Eso* es el corazón del patrón de **delegación**, tal como JS lo encarna.

| TIP: |
| :--- |
| En la primera edición de esta serie de libros, este libro ("this & Object Prototypes") acuñó un término, "OLOO", que significa "Objects Linked to Other Objects" (Objetos Enlazados a Otros Objetos), para contrastar con "OO" ("Object Oriented", Orientado a Objetos). En este ejemplo precedente, podés ver la esencia de OLOO: todo lo que tenemos son objetos, enlazados a y cooperando con, otros objetos. Encuentro esto hermoso en su simplicidad. |

## Componiendo Objetos Pares

Llevemos *esta delegación* aún más lejos.

En el fragmento precedente, `point` y `anotherPoint` solo contenían datos, y los comportamientos a los que delegaban estaban en otros objetos (`Coordinates` e `Inspect`). Pero podemos agregar comportamientos directamente a cualquiera de los objetos en una cadena de delegación, y esos comportamientos pueden incluso interactuar entre sí, todo mediante la magia de la *composición virtual* (compartición del contexto `this`).

Para ilustrarlo, vamos a evolucionar bastante nuestro ejemplo actual del *point*. Y, como bonus, vamos a dibujar realmente nuestros puntos en un elemento `<canvas>` del DOM. Echémosle un vistazo:

```js
var Canvas = {
    setOrigin(x,y) {
        this.ctx.translate(x,y);

        // flip the canvas context vertically,
        // so coordinates work like on a normal
        // 2d (x,y) graph
        this.ctx.scale(1,-1);
    },
    pixel(x,y) {
        this.ctx.fillRect(x,y,1,1);
    },
    renderScene() {
        // clear the canvas
        var matrix = this.ctx.getTransform();
        this.ctx.resetTransform();
        this.ctx.clearRect(
            0, 0,
            this.ctx.canvas.width,
            this.ctx.canvas.height
        );
        this.ctx.setTransform(matrix);

        this.draw();  // <-- where is draw()?
    },
};

var Coordinates = {
    setX(x) {
        this.x = Math.round(x);
    },
    setY(y) {
        this.y = Math.round(y);
    },
    setXY(x,y) {
        this.setX(x);
        this.setY(y);
        this.render();   // <-- where is render()?
    },
};

var ControlPoint = {
    // delegate to Coordinates
    __proto__: Coordinates,

    // NOTE: must have a <canvas id="my-canvas">
    // element in the DOM
    ctx: document.getElementById("my-canvas")
        .getContext("2d"),

    rotate(angleRadians) {
        var rotatedX = this.x * Math.cos(angleRadians) -
            this.y * Math.sin(angleRadians);
        var rotatedY = this.x * Math.sin(angleRadians) +
            this.y * Math.cos(angleRadians);
        this.setXY(rotatedX,rotatedY);
    },
    draw() {
        // plot the point
        Canvas.pixel.call(this,this.x,this.y);
    },
    render() {
        // clear the canvas, and re-render
        // our control-point
        Canvas.renderScene.call(this);
    },
};

// set the logical (0,0) origin at this
// physical location on the canvas
Canvas.setOrigin.call(ControlPoint,100,100);

ControlPoint.setXY(30,40);
// [renders point (30,40) on the canvas]

// ..
// later:

// rotate the point about the (0,0) origin
// 90 degrees counter-clockwise
ControlPoint.rotate(Math.PI / 2);
// [renders point (-40,30) on the canvas]
```

OK, eso es un montón de código para digerir. Tomate tu tiempo y releé el fragmento varias veces. Agregué un par de objetos concretos nuevos (`Canvas` y `ControlPoint`) junto al objeto `Coordinates` anterior.

Asegurate de ver y entender las interacciones entre estos tres objetos concretos.

`ControlPoint` está enlazado (mediante `__proto__`) para *delegar implícitamente* (cadena de `[[Prototype]]`) a `Coordinates`.

Acá hay una *delegación explícita*: `Canvas.setOrigin.call(ControlPoint,100,100);`; estoy invocando la llamada `Canvas.setOrigin(..)` en el contexto de `ControlPoint`. Eso tiene el efecto de compartir `ctx` con `setOrigin(..)`, mediante `this`.

`ControlPoint.setXY(..)` delega *implícitamente* a `Coordinates.setXY(..)`, pero todavía en el contexto de `ControlPoint`. Acá hay un detalle clave que es fácil pasar por alto: ¿ves el `this.render()` dentro de `Coordinates.setXY(..)`? ¿De dónde sale eso? Dado que el contexto `this` es `ControlPoint` (no `Coordinates`), está invocando `ControlPoint.render()`.

`ControlPoint.render()` *delega explícitamente* a `Canvas.renderScene()`, nuevamente todavía en el contexto de `ControlPoint`. `renderScene()` llama a `this.draw()`, pero ¿de dónde sale eso? Sí, todavía de `ControlPoint` (mediante el contexto `this`).

¿Y `ControlPoint.draw()`? *Delega explícitamente* a `Canvas.pixel(..)`, una vez más todavía en el contexto de `ControlPoint`.

Los tres objetos tienen métodos que terminan invocándose entre sí. Pero estas llamadas no están particularmente cableadas de forma rígida. `Canvas.renderScene()` no llama a `ControlPoint.draw()`, llama a `this.draw()`. Eso es importante, porque significa que `Canvas.renderScene()` es más flexible de usar en un contexto `this` diferente; por ejemplo, contra otro tipo de objeto *point* además de `ControlPoint`.

Es a través del contexto `this`, y de la cadena de `[[Prototype]]`, que estos tres objetos básicamente quedan mezclados (compuestos) virtualmente juntos, según se necesite en cada paso, de modo que trabajan juntos **como si fueran un solo objeto en lugar de tres objetos separados**.

Esa es la *belleza* de la composición virtual tal como la realiza el patrón de delegación en JS.

### Contexto Flexible

Mencioné arriba que podemos agregar con bastante facilidad otros objetos concretos a la mezcla. Acá hay un ejemplo:

```js
var Coordinates = { /* .. */ };

var Canvas = {
    /* .. */
    line(start,end) {
        this.ctx.beginPath();
        this.ctx.moveTo(start.x,start.y);
        this.ctx.lineTo(end.x,end.y);
        this.ctx.stroke();
    },
};

function lineAnchor(x,y) {
    var anchor = {
        __proto__: Coordinates,
        render() {},
    };
    anchor.setXY(x,y);
    return anchor;
}

var GuideLine = {
    // NOTE: must have a <canvas id="my-canvas">
    // element in the DOM
    ctx: document.getElementById("my-canvas")
        .getContext("2d"),

    setAnchors(sx,sy,ex,ey) {
        this.start = lineAnchor(sx,sy);
        this.end = lineAnchor(ex,ey);
        this.render();
    },
    draw() {
        // plot the point
        Canvas.line.call(this,this.start,this.end);
    },
    render() {
        // clear the canvas, and re-render
        // our line
        Canvas.renderScene.call(this);
    },
};

// set the logical (0,0) origin at this
// physical location on the canvas
Canvas.setOrigin.call(GuideLine,100,100);

GuideLine.setAnchors(-30,65,45,-17);
// [renders line from (-30,65) to (45,-17)
//   on the canvas]
```

¡Eso está bastante bueno, me parece!

Pero creo que otro beneficio menos obvio es que tener objetos enlazados dinámicamente mediante el contexto `this` tiende a hacer que probar diferentes partes del programa de forma independiente sea, en cierto modo, más fácil.

Por ejemplo, `Object.setPrototypeOf(..)` puede usarse para cambiar dinámicamente el enlace de `[[Prototype]]` de un objeto, delegándolo a un objeto diferente, como un objeto mock. O podrías redefinir dinámicamente `GuideLine.draw()` y `GuideLine.render()` para que *deleguen explícitamente* a un `MockCanvas` en lugar de a `Canvas`.

La palabra clave `this`, y el enlace de `[[Prototype]]`, son un mecanismo tremendamente flexible cuando los entendés y los aprovechás por completo.

## ¿Por qué *This*?

OK, así que con suerte está claro que el patrón de delegación se apoya fuertemente en la entrada implícita, compartiendo el contexto mediante `this` en lugar de a través de un parámetro explícito.

Podrías preguntar, con razón, ¿por qué no simplemente pasar siempre ese contexto de forma explícita? Ciertamente podemos hacerlo, pero... para pasar manualmente el contexto necesario, vamos a tener que cambiar prácticamente cada una de las firmas de función, y cualquier sitio de llamada correspondiente.

Revisitemos el ejemplo anterior de delegación de `ControlPoint`, e implementémoslo sin ninguna compartición de contexto `this` orientada a la delegación. Prestá mucha atención a las diferencias:

```js
var Canvas = {
    setOrigin(ctx,x,y) {
        ctx.translate(x,y);
        ctx.scale(1,-1);
    },
    pixel(ctx,x,y) {
        ctx.fillRect(x,y,1,1);
    },
    renderScene(ctx,entity) {
        // clear the canvas
        var matrix = ctx.getTransform();
        ctx.resetTransform();
        ctx.clearRect(
            0, 0,
            ctx.canvas.width,
            ctx.canvas.height
        );
        ctx.setTransform(matrix);

        entity.draw();
    },
};

var Coordinates = {
    setX(entity,x) {
        entity.x = Math.round(x);
    },
    setY(entity,y) {
        entity.y = Math.round(y);
    },
    setXY(entity,x,y) {
        this.setX(entity,x);
        this.setY(entity,y);
        entity.render();
    },
};

var ControlPoint = {
    // NOTE: must have a <canvas id="my-canvas">
    // element in the DOM
    ctx: document.getElementById("my-canvas")
        .getContext("2d"),

    setXY(x,y) {
        Coordinates.setXY(this,x,y);
    },
    rotate(angleRadians) {
        var rotatedX = this.x * Math.cos(angleRadians) -
            this.y * Math.sin(angleRadians);
        var rotatedY = this.x * Math.sin(angleRadians) +
            this.y * Math.cos(angleRadians);
        this.setXY(rotatedX,rotatedY);
    },
    draw() {
        // plot the point
        Canvas.pixel(this.ctx,this.x,this.y);
    },
    render() {
        // clear the canvas, and re-render
        // our control-point
        Canvas.renderScene(this.ctx,this);
    },
};

// set the logical (0,0) origin at this
// physical location on the canvas
Canvas.setOrigin(ControlPoint.ctx,100,100);

// ..
```

Para ser honesto, a algunos de ustedes quizás les guste más ese estilo de código. Y está bien si estás en ese bando. Este fragmento evita `[[Prototype]]` por completo, y solo se apoya en muchas menos referencias básicas al estilo `this.` a propiedades y métodos.

En contraste, el estilo de delegación que defiendo en este capítulo es poco familiar y usa la compartición de `[[Prototype]]` y `this` de maneras con las que probablemente no estés familiarizado. Para usar semejante estilo con eficacia, vas a tener que invertir el tiempo y la práctica para construir una familiaridad más profunda.

Pero, en mi opinión, el "costo" de evitar la composición virtual mediante la delegación puede sentirse a lo largo de todas las firmas de función y los sitios de llamada; los encuentro mucho más recargados. Ese paso de contexto explícito es todo un impuesto.

De hecho, yo nunca recomendaría ese estilo de código en absoluto. Si querés evitar la delegación, probablemente lo mejor sea simplemente quedarte con el código al estilo `class`, como se ve en el Capítulo 3. Como ejercicio que le queda al lector, intentá convertir los fragmentos de código anteriores de `ControlPoint` / `GuideLine` para que usen `class`.

[^TreatyOfOrlando]: "Treaty of Orlando"; Henry Lieberman, Lynn Andrea Stein, David Ungar; 6 de octubre de 1987; https://web.media.mit.edu/~lieber/Publications/Treaty-of-Orlando-Treaty-Text.pdf ; PDF; Consultado en julio de 2022

[^ClassVsPrototype]: "Classes vs. Prototypes, Some Philosophical and Historical Observations"; Antero Taivalsaari; 22 de abril de 1996; https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.56.4713&rep=rep1&type=pdf ; PDF; Consultado en julio de 2022
