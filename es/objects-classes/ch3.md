# You Don't Know JS Yet: Objects & Classes - 2nd Edition
# Capítulo 3: Objetos con Clase

| NOTA: |
| :--- |
| Trabajo en progreso |

El patrón de diseño de clases generalmente implica definir un *tipo de cosa* (clase), incluyendo datos (miembros) y comportamientos (métodos), y luego crear una o más *instancias* concretas de esta definición de clase como objetos reales que pueden interactuar y realizar tareas. Además, la orientación a clases permite declarar una relación entre dos o más clases, a través de lo que se llama "herencia", para derivar "subclases" nuevas y aumentadas que combinan y hasta redefinen comportamientos.

Antes de ES6 (2015), los desarrolladores de JS imitaban aspectos del diseño orientado a clases (también conocido como "orientado a objetos") usando funciones y objetos simples, junto con el mecanismo `[[Prototype]]` (como se explicó en el capítulo anterior) -- las llamadas "clases prototipales".

Pero para alegría y alivio de muchos desarrolladores, ES6 introdujo una sintaxis dedicada, incluyendo las palabras clave `class` y `extends`, para expresar el diseño orientado a clases de forma más declarativa.

En el momento en que se introdujo `class` en ES6, esta nueva sintaxis dedicada era casi enteramente *solo azúcar sintáctico* para hacer las definiciones de clases más convenientes y legibles. Sin embargo, en los muchos años desde ES6, `class` ha madurado y crecido hasta convertirse en un mecanismo de característica de primera clase por derecho propio, acumulando una cantidad significativa de sintaxis dedicada y comportamientos complejos que superan con creces las capacidades de las "clases prototipales" previas a ES6.

Aunque `class` ahora casi no se parece al estilo de código más antiguo de "clases prototipales", el engine de JS sigue *solo* conectando objetos entre sí a través del mecanismo `[[Prototype]]` existente. En otras palabras, `class` no es su propio pilar separado del lenguaje (como lo es `[[Prototype]]`), sino más bien el *Capitel* elegante y decorativo que corona el pilar/columna.

Dicho esto, dado que el código al estilo `class` ha reemplazado ahora prácticamente todo el código anterior de "clases prototipales", el texto principal aquí se enfoca solo en `class` y sus diversos pormenores. Con fines históricos, cubriremos brevemente el viejo estilo de "clases prototipales" en un apéndice.

## ¿Cuándo Debería Orientar Mi Código a Clases?

La orientación a clases es un patrón de diseño, lo que significa que es una elección sobre cómo organizás la información y el comportamiento en tu programa. Tiene pros y contras. No es una solución universal para todas las tareas.

Entonces, ¿cómo sabés cuándo deberías usar clases?

En un sentido teórico, la orientación a clases es una forma de dividir el dominio de negocio de un programa en una o más piezas que pueden cada una definirse mediante una clasificación de tipo "es-un": agrupar una cosa en el conjunto (o conjuntos) de características que esa cosa comparte con otras cosas similares. Dirías "X es un Y", lo que significa que X tiene (al menos) todas las características de una cosa de tipo Y.

Por ejemplo, consideremos las computadoras. Podríamos decir que una computadora es eléctrica, ya que usa corriente eléctrica (voltaje, amperios, etc.) como energía. Es además electrónica, porque manipula la corriente eléctrica más allá de simplemente enrutar electrones de un lado a otro (campos eléctricos/magnéticos), creando un circuito significativo para manipular la corriente y hacer que realice tareas más complejas. En contraste, una lámpara de escritorio básica es eléctrica, pero no realmente electrónica.

Así podríamos definir una clase `Electrical` para describir qué necesitan y qué pueden hacer los dispositivos eléctricos. Luego podríamos definir otra clase `Electronic`, y definir que además de ser eléctricas, las cosas `Electronic` manipulan la electricidad para crear resultados más especializados.

Acá es donde la orientación a clases empieza a brillar. En lugar de redefinir todas las características de `Electrical` en la clase `Electronic`, podemos definir `Electronic` de tal manera que "comparta" o "herede" esas características de `Electrical`, y luego aumente/redefina los comportamientos únicos que hacen que un dispositivo sea electrónico. Esta relación entre las dos clases -- llamada "herencia" -- es un aspecto clave de la orientación a clases.

Así que la orientación a clases es una forma de pensar en las entidades que nuestro programa necesita, y clasificarlas en agrupaciones basadas en sus características (qué información contienen, qué operaciones pueden realizarse sobre esos datos), y definir las relaciones entre las diferentes agrupaciones de características.

Pero pasando de lo teórico a una perspectiva un poco más pragmática: si tu programa necesita contener y usar múltiples colecciones (instancias) de datos/comportamiento similares a la vez, *puede que* te beneficies de la orientación a clases.

### Hora De Un Ejemplo

Acá va una breve ilustración.

Hace un par de décadas, justo después de haber cursado casi toda una carrera de Ciencias de la Computación en la universidad, me encontré sentado en mi primer trabajo profesional como desarrollador de software. Me encargaron construir, yo solo, un sistema de seguimiento de horas de trabajo y nómina. Construí el backend en PHP (usando MySQL para la BD) y usé JS para la interfaz (tan temprana como estaba en su madurez allá por el cambio de siglo).

Dado que mi carrera de CS había enfatizado fuertemente la orientación a clases a lo largo de mis cursos, estaba ansioso por poner toda esa teoría en práctica. Para el diseño de mi programa, definí el concepto de una entidad "timesheet" (planilla de horas) como una colección de 2-3 entidades "week" (semana), y cada "week" como una colección de 5-7 entidades "day" (día), y cada "day" como una colección de entidades "task" (tarea).

Si quería saber cuántas horas se habían registrado en una instancia de timesheet, podía llamar una operación `totalTime()` sobre esa instancia. El timesheet definía esta operación recorriendo su colección de semanas, llamando `totalTime()` en cada una de ellas y sumando los valores. Cada semana hacía lo mismo con todos sus días, y cada día hacía lo mismo con todas sus tareas.

La noción ilustrada acá, uno de los fundamentos de los patrones de diseño como la orientación a clases, se llama *encapsulamiento*. Cada nivel de entidad encapsulaba (es decir, controlaba, ocultaba, abstraía) detalles internos (datos y comportamiento) mientras presentaba una interfaz externa útil.

Pero el encapsulamiento por sí solo no es una justificación suficiente para la orientación a clases. Otros patrones de diseño ofrecen suficiente encapsulamiento.

¿Cómo aprovechó mi diseño de clases la herencia? Tenía una clase base que definía un conjunto de operaciones como `totalTime()`, y cada uno de mis tipos de clase de entidad extendía/subclaseaba esta clase base. Eso significaba que cada uno de ellos heredaba esta capacidad de sumatoria del tiempo total, pero donde cada uno aplicaba sus propias extensiones y definiciones para los detalles internos de *cómo* hacer ese trabajo.

Hay todavía otro aspecto del patrón de diseño en juego, que es la *composición*: cada entidad se definía como una colección de otras entidades.

### Una vs Múltiples

Mencioné arriba que una forma pragmática de decidir si necesitás orientación a clases es si tu programa va a tener múltiples instancias de un solo tipo de comportamiento (también conocido como "clase"). En el ejemplo de timesheet, teníamos 4 clases: Timesheet, Week, Day y Task. Pero para cada clase, teníamos múltiples instancias de cada una a la vez.

Si en cambio solo hubiéramos necesitado una única instancia de una clase, como una sola cosa `Computer` que fuera una instancia de la clase `Electronic`, que era una subclase de la clase `Electrical`, entonces la orientación a clases podría no ofrecer tanto beneficio. En particular, si el programa no necesita crear una instancia de la clase `Electrical`, entonces no hay beneficio particular en separar `Electrical` de `Electronic`, así que realmente no estamos obteniendo ninguna ayuda del aspecto de herencia de la orientación a clases.

Entonces, si te encontrás diseñando un programa dividiendo un dominio de problema de negocio en diferentes "clases" de entidades, pero en el código real del programa solo necesitás alguna vez una sola *cosa* concreta de un tipo/definición de comportamiento (también conocido como "clase"), muy posiblemente no necesites realmente la orientación a clases. Hay otros patrones de diseño que pueden ser una coincidencia más eficiente para tu esfuerzo.

Pero si te encontrás queriendo definir clases, y subclases que heredan de ellas, y si vas a instanciar una o más de esas clases múltiples veces, entonces la orientación a clases es una buena candidata. Y para hacer orientación a clases en JS, vas a necesitar la palabra clave `class`.

## Mantenelo con `class`e

`class` define ya sea una declaración o una expresión para una clase. Como declaración, una definición de clase aparece en una posición de sentencia y se ve así:

```js
class Point2d {
    // ..
}
```

Como expresión, una definición de clase aparece en una posición de valor y puede tener un nombre o ser anónima:

```js
// named class expression
const pointClass = class Point2d {
    // ..
};

// anonymous class expression
const anotherClass = class {
    // ..
};
```

El contenido del cuerpo de una `class` típicamente incluye una o más definiciones de métodos:

```js
class Point2d {
    setX(x) {
        // ..
    }
    setY(y) {
        // ..
    }
}
```

Dentro del cuerpo de una `class`, los métodos se definen sin la palabra clave `function`, y no hay separadores `,` o `;` entre las definiciones de métodos.

| NOTA: |
| :--- |
| Dentro de un bloque `class`, todo el código corre en strict-mode incluso sin la pragma `"use strict"` presente en el archivo o sus funciones. En particular, esto impacta el comportamiento de `this` para las llamadas a funciones, como se explica en el Capítulo 4. |

### El Constructor

Un método especial que todas las clases tienen se llama "constructor". Si se omite, se asume un constructor vacío por defecto en la definición.

El constructor se invoca cada vez que se crea una `new` instancia de la clase:

```js
class Point2d {
    constructor() {
        console.log("Here's your new instance!");
    }
}

var point = new Point2d();
// Here's your new instance!
```

Aunque la sintaxis implica que existe realmente una función llamada `constructor`, JS define una función según lo especificado, pero con el nombre de la clase (`Point2d` arriba):

```js
typeof Point2d;       // "function"
```

Sin embargo, no es *solo* una función regular; este tipo especial de función se comporta un poco diferente:

```js
Point2d.toString();
// class Point2d {
//   ..
// }

Point2d();
// TypeError: Class constructor Point2d cannot
// be invoked without 'new'

Point2d.call({});
// TypeError: Class constructor Point2d cannot
// be invoked without 'new'
```

Podés construir tantas instancias diferentes de una clase como necesites:

```js
var one = new Point2d();
var two = new Point2d();
var three = new Point2d();
```

Cada uno de `one`, `two` y `three` acá son objetos que son instancias independientes de la clase `Point2d`.

| NOTA: |
| :--- |
| Cada uno de los objetos `one`, `two` y `three` tiene un enlace `[[Prototype]]` al objeto `Point2d.prototype` (ver Capítulo 2). En este código, `Point2d` es tanto una definición de `class` como la función constructor del mismo nombre. |

Si agregás una propiedad al objeto `one`:

```js
one.value = 42;
```

Esa propiedad ahora existe solo en `one`, y no existe de ninguna manera que los objetos independientes `two` o `three` puedan acceder:

```js
two.value;      // undefined
three.value;    // undefined
```

### Métodos de Clase

Como se mostró arriba, una definición de clase puede incluir una o más definiciones de métodos:

```js
class Point2d {
    constructor() {
        console.log("Here's your new instance!");
    }
    setX(x) {
        console.log(`Setting x to: ${x}`);
        // ..
    }
}

var point = new Point2d();

point.setX(3);
// Setting x to: 3
```

La propiedad `setX` (método) *parece* existir en (ser propiedad de) el objeto `point` acá. Pero eso es un espejismo. Cada método de clase se agrega al objeto `prototype`, una propiedad de la función constructor.

Entonces, `setX(..)` solo existe como `Point2d.prototype.setX`. Dado que `point` está enlazado por `[[Prototype]]` a `Point2d.prototype` (ver Capítulo 2) a través de la instanciación con la palabra clave `new`, la referencia `point.setX(..)` recorre la cadena `[[Prototype]]` y encuentra el método para ejecutar.

Los métodos de clase solo deberían invocarse a través de una instancia; `Point2d.setX(..)` no funciona porque *no existe* tal propiedad. *Podrías* invocar `Point2d.prototype.setX(..)`, pero eso no es generalmente apropiado/aconsejable en la programación estándar orientada a clases. Siempre accedé a los métodos de clase a través de las instancias.

## El `this` de la Instancia de Clase

Cubriremos la palabra clave `this` con mucho más detalle en un capítulo posterior. Pero en lo que respecta al código orientado a clases, la palabra clave `this` generalmente se refiere a la instancia actual que es el contexto de cualquier invocación de método.

En el constructor, así como en cualquier método, podés usar `this.` ya sea para agregar o acceder a propiedades en la instancia actual:

```js
class Point2d {
    constructor(x,y) {
        // add properties to the current instance
        this.x = x;
        this.y = y;
    }
    toString() {
        // access the properties from the current instance
        console.log(`(${this.x},${this.y})`);
    }
}

var point = new Point2d(3,4);

point.x;                // 3
point.y;                // 4

point.toString();       // (3,4)
```

Cualquier propiedad que no contenga valores de función, que se agregue a una instancia de clase (usualmente a través del constructor), se denomina *miembro*, a diferencia del término *método* para las funciones ejecutables.

Mientras el método `point.toString()` está corriendo, su referencia `this` apunta al mismo objeto al que referencia `point`. Por eso tanto `point.x` como `this.x` revelan el mismo valor `3` que el constructor estableció con su operación `this.x = x`.

### Campos Públicos

En lugar de definir un miembro de instancia de clase de forma imperativa a través de `this.` en el constructor o un método, las clases pueden definir *campos* de forma declarativa en el cuerpo de la `class`, que corresponden directamente a miembros que se crearán en cada instancia:

```js
class Point2d {
    // these are public fields
    x = 0
    y = 0

    constructor(x,y) {
        // set properties (fields) on the current instance
        this.x = x;
        this.y = y;
    }
    toString() {
        // access the properties from the current instance
        console.log(`(${this.x},${this.y})`);
    }
}
```

Los campos públicos pueden tener una inicialización de valor, como se muestra arriba, pero eso no es obligatorio. Si no inicializás un campo en la definición de la clase, casi siempre deberías inicializarlo en el constructor.

Los campos también pueden referenciarse entre sí, a través de la sintaxis natural de acceso `this.`:

```js
class Point3d {
    // these are public fields
    x
    y = 4
    z = this.y * 5

    // ..
}
```

| TIP: |
| :--- |
| Mayormente podés pensar en las declaraciones de campos públicos como si aparecieran al principio del `constructor(..)`, cada una prefijada con un `this.` implícito que podés omitir en la forma declarativa del cuerpo de la `class`. ¡Pero hay una trampa! Mirá "¡Eso Es Super!" más adelante para más información al respecto. |

Al igual que los nombres de propiedad computados (ver Capítulo 1), los nombres de campos pueden computarse:

```js
var coordName = "x";

class Point2d {
    // computed public field
    [coordName.toUpperCase()] = 42

    // ..
}

var point = new Point2d(3,4);

point.x;        // 3
point.y;        // 4

point.X;        // 42
```

#### Evitá Esto

Un patrón que ha surgido y crecido bastante en popularidad, pero que creo firmemente que es un anti-patrón para `class`, se ve de la siguiente manera:

```js
class Point2d {
    x = null
    y = null
    getDoubleX = () => this.x * 2

    constructor(x,y) {
        this.x = x;
        this.y = y;
    }
    toString() { /* .. */ }
}

var point = new Point2d(3,4);

point.getDoubleX();    // 6
```

¿Ves el campo que contiene una función flecha `=>`? Yo digo que esto es un no-no. ¿Pero por qué? Desenredemos lo que está pasando.

Primero, ¿por qué hacer esto? Porque los desarrolladores de JS parecen estar perpetuamente frustrados por las reglas dinámicas de binding de `this` (ver Capítulo 4), así que fuerzan un binding de `this` a través de la función flecha `=>`. De esa manera, sin importar cómo se invoque `getDoubleX()`, siempre está vinculado con `this` a la instancia particular. Esa es una conveniencia comprensible de desear, pero... traiciona la naturaleza misma del pilar `this` / `[[Prototype]]` del lenguaje. ¿Cómo?

Consideremos el código equivalente al fragmento anterior:

```js
class Point2d {
    constructor(x,y) {
        this.x = null;
        this.y = null;
        this.getDoubleX = () => this.x * 2;

        this.x = x;
        this.y = y;
    }
    toString() { /* .. */ }
}

var point = new Point2d(3,4);

point.getDoubleX();    // 6
```

¿Podés detectar el problema? Mirá de cerca. Te espero.

...

Hemos dejado claro repetidamente hasta ahora que las definiciones de `class` ponen sus métodos en el objeto `prototype` del constructor de la clase -- ¡ahí es donde pertenecen! -- de modo que haya solo uno de cada función y sea heredado (compartido) por todas las instancias. Eso es lo que pasará con `toString()` en el fragmento anterior.

¿Pero qué pasa con `getDoubleX()`? Eso es esencialmente un método de clase, pero no será manejado por JS de la misma manera que lo será `toString()`. Considerá:

```js
Object.hasOwn(point,"x");               // true -- good
Object.hasOwn(point,"toString");        // false -- good
Object.hasOwn(point,"getDoubleX");      // true -- oops :(
```

¿Ves ahora? Al definir un valor de función y adjuntarlo como una propiedad de campo/miembro, estamos perdiendo la característica de método prototipal compartido de la función, y se convierte en cualquier otra propiedad por instancia. Eso significa que estamos creando una nueva propiedad de función **para cada instancia**, en lugar de crearse solo una vez en el `prototype` del constructor de la clase.

Eso es un desperdicio en rendimiento y memoria, aunque sea por una pizca. Eso solo debería ser suficiente para evitarlo.

Pero yo argumentaría que, mucho más importante, lo que has hecho con este patrón es invalidar la razón misma por la que usar `class` y métodos conscientes de `this` es siquiera remotamente útil/poderoso!

Si te tomás todo el trabajo de definir métodos de clase con referencias `this.` a lo largo de ellos, pero luego bloqueás/vinculás la mayoría o todos esos métodos a una instancia de objeto específica, básicamente has viajado alrededor de todo el mundo solo para ir a la puerta de al lado.

Si todo lo que querés son función(es) que estén fijadas estáticamente a un "contexto" particular, y no necesitan ningún dinamismo o compartición, lo que querés es... **closure**. Y estás de suerte: escribí un libro entero en esta serie ("Scope & Closures") sobre cómo usar closure para que las funciones recuerden/accedan a su scope definido estáticamente (también conocido como "contexto"). Ese es un enfoque mucho más apropiado, y más simple de codificar, para obtener lo que buscás.

No abuses/maluses de `class` y lo conviertas en una colección sobrevalorada y glorificada de closure.

Para ser claro, *no* estoy diciendo: nunca uses funciones flecha `=>` dentro de las clases.

*Sí* estoy diciendo: nunca adjuntes una función flecha `=>` como propiedad de instancia en lugar de un método de clase prototipal dinámico, ya sea por hábito irreflexivo, o pereza de tipear menos caracteres, o conveniencia equivocada de binding de `this`.

En un capítulo posterior, nos sumergiremos profundamente en cómo entender y aprovechar correctamente todo el poder del mecanismo dinámico de `this`.

## Extensión de Clase

La forma de desbloquear el poder de la herencia de clases es a través de la palabra clave `extends`, que define una relación entre dos clases:

```js
class Point2d {
    x = 3
    y = 4

    getX() {
        return this.x;
    }
}

class Point3d extends Point2d {
    x = 21
    y = 10
    z = 5

    printDoubleX() {
        console.log(`double x: ${this.getX() * 2}`);
    }
}

var point = new Point2d();

point.getX();                   // 3

var anotherPoint = new Point3d();

anotherPoint.getX();            // 21
anotherPoint.printDoubleX();    // double x: 42
```

Tomate unos momentos para releer ese fragmento de código y asegurate de entender completamente lo que está pasando.

La clase base `Point2d` define campos (miembros) llamados `x` e `y`, y les da los valores iniciales `3` y `4`, respectivamente. También define un método `getX()` que accede a este miembro de instancia `x` y lo retorna. Vemos ese comportamiento ilustrado en la llamada al método `point.getX()`.

Pero la clase `Point3d` extiende `Point2d`, haciendo de `Point3d` una clase derivada, clase hija, o (más comúnmente) subclase. En `Point3d`, la misma propiedad `x` que se hereda de `Point2d` se reinicializa con un valor `21` diferente, al igual que `y` se sobrescribe del valor `4` a `10`.

También agrega un nuevo campo/miembro `z`, así como un método `printDoubleX()`, que a su vez llama a `this.getX()`.

Cuando se invoca `anotherPoint.printDoubleX()`, se invoca así el `this.getX()` heredado, y ese método hace referencia a `this.x`. Dado que `this` apunta a la instancia de clase (es decir, `anotherPoint`), el valor que encuentra es ahora `21` (en lugar de `3` del miembro `x` del objeto `point`).

### Extendiendo Expresiones

// TODO: cover `class Foo extends ..` where `..` is an expression, not a class-name

### Sobrescribiendo Métodos

Además de sobrescribir un campo/miembro en una subclase, también podés sobrescribir (redefinir) un método:

```js
class Point2d {
    x = 3
    y = 4

    getX() {
        return this.x;
    }
}

class Point3d extends Point2d {
    x = 21
    y = 10
    z = 5

    getX() {
        return this.x * 2;
    }
    printX() {
        console.log(`double x: ${this.getX()}`);
    }
}

var point = new Point3d();

point.printX();       // double x: 42
```

La subclase `Point3d` sobrescribe el método heredado `getX()` para darle un comportamiento diferente. Sin embargo, todavía podés instanciar la clase base `Point2d`, lo que entonces daría un objeto que usa la definición original (`return this.x;`) para `getX()`.

Si querés acceder a un método heredado desde una subclase incluso si ha sido sobrescrito, podés usar `super` en lugar de `this`:

```js
class Point2d {
    x = 3
    y = 4

    getX() {
        return this.x;
    }
}

class Point3d extends Point2d {
    x = 21
    y = 10
    z = 5

    getX() {
        return this.x * 2;
    }
    printX() {
        console.log(`x: ${super.getX()}`);
    }
}

var point = new Point3d();

point.printX();       // x: 21
```

La capacidad de que métodos con el mismo nombre, en diferentes niveles de la jerarquía de herencia, exhiban comportamientos diferentes cuando se acceden directamente, o relativamente con `super`, se llama *polimorfismo de métodos*. Es una parte muy poderosa de la orientación a clases, cuando se usa apropiadamente.

### ¡Eso Es Super!

Además de que un método de subclase acceda a una definición de método heredado (incluso si está sobrescrito en la subclase) a través de la referencia `super.`, un constructor de subclase debe invocar manualmente el constructor de la clase base heredada a través de la invocación de función `super(..)`:

```js
class Point2d {
    x
    y
    constructor(x,y) {
        this.x = x;
        this.y = y;
    }
}

class Point3d extends Point2d {
    z
    constructor(x,y,z) {
        super(x,y);
        this.z = z;
    }
    toString() {
        console.log(`(${this.x},${this.y},${this.z})`);
    }
}

var point = new Point3d(3,4,5);

point.toString();       // (3,4,5)
```

| ADVERTENCIA: |
| :--- |
| Un constructor de subclase definido explícitamente *debe* llamar a `super(..)` para ejecutar la inicialización de la clase heredada, y eso debe ocurrir antes de que el constructor de la subclase haga cualquier referencia a `this` o termine/retorne. De lo contrario, se lanzará una excepción en tiempo de ejecución cuando ese constructor de subclase sea invocado (a través de `new`). Si omitís el constructor de la subclase, el constructor por defecto automáticamente -- ¡por suerte! -- invoca `super()` por vos. |

Un matiz a tener en cuenta: si definís un campo (público o privado) dentro de una subclase, y definís explícitamente un `constructor(..)` para esta subclase, las inicializaciones de campos se procesarán no al principio del constructor, sino *entre* la llamada a `super(..)` y cualquier código subsiguiente en el constructor.

Prestá mucha atención al orden de los mensajes de consola acá:

```js
class Point2d {
    x
    y
    constructor(x,y) {
        console.log("Running Point2d(..) constructor");
        this.x = x;
        this.y = y;
    }
}

class Point3d extends Point2d {
    z = console.log("Initializing field 'z'")

    constructor(x,y,z) {
        console.log("Running Point3d(..) constructor");
        super(x,y);

        console.log(`Setting instance property 'z' to ${z}`);
        this.z = z;
    }
    toString() {
        console.log(`(${this.x},${this.y},${this.z})`);
    }
}

var point = new Point3d(3,4,5);
// Running Point3d(..) constructor
// Running Point2d(..) constructor
// Initializing field 'z'
// Setting instance property 'z' to 5
```

Como ilustran los mensajes de consola, la inicialización del campo `z = ..` ocurre *inmediatamente después* de la llamada `super(x,y)`, *antes* de que se ejecute el ``console.log(`Setting instance...`)``. Quizás pensalo como si las inicializaciones de campos estuvieran adjuntas al final de la llamada `super(..)`, de modo que corren antes que cualquier otra cosa en el constructor.

#### ¿Cuál Clase?

Puede que necesites determinar en un constructor si esa clase está siendo instanciada directamente, o siendo instanciada desde una subclase con una llamada `super()`. Podemos usar una "pseudo propiedad" especial `new.target`:

```js
class Point2d {
    // ..

    constructor(x,y) {
        if (new.target === Point2d) {
            console.log("Constructing 'Point2d' instance");
        }
    }

    // ..
}

class Point3d extends Point2d {
    // ..

    constructor(x,y,z) {
        super(x,y);

        if (new.target === Point3d) {
            console.log("Constructing 'Point3d' instance");
        }
    }

    // ..
}

var point = new Point2d(3,4);
// Constructing 'Point2d' instance

var anotherPoint = new Point3d(3,4,5);
// Constructing 'Point3d' instance
```

### ¿Pero Qué Tipo De Instancia?

Puede que quieras hacer introspección de cierta instancia de objeto para ver si es una instancia de una clase específica. Hacemos esto con el operador `instanceof`:

```js
class Point2d { /* .. */ }
class Point3d extends Point2d { /* .. */ }

var point = new Point2d(3,4);

point instanceof Point2d;           // true
point instanceof Point3d;           // false

var anotherPoint = new Point3d(3,4,5);

anotherPoint instanceof Point2d;    // true
anotherPoint instanceof Point3d;    // true
```

Puede parecer extraño ver que `anotherPoint instanceof Point2d` resulte en `true`. Para entender mejor por qué, quizás sea útil visualizar ambas cadenas `[[Prototype]]`:

```
Point2d.prototype
        /       \
       /         \
      /           \
  point   Point3d.prototype
                    \
                     \
                      \
                    anotherPoint
```

El operador `instanceof` no solo mira el objeto actual, sino que recorre toda la jerarquía de herencia de clases (la cadena `[[Prototype]]`) hasta que encuentra una coincidencia. Así, `anotherPoint` es una instancia tanto de `Point3d` como de `Point2d`.

Para ilustrar este hecho un poco más obviamente, otra forma (menos ergonómica) de hacer el mismo tipo de verificación que `instanceof` es con la utilidad (heredada de `Object.prototype`), `isPrototypeOf(..)`:

```js
Point2d.prototype.isPrototypeOf(point);             // true
Point3d.prototype.isPrototypeOf(point);             // false

Point2d.prototype.isPrototypeOf(anotherPoint);      // true
Point3d.prototype.isPrototypeOf(anotherPoint);      // true
```

Esta utilidad hace un poco más claro por qué tanto `Point2d.prototype.isPrototypeOf(anotherPoint)` como `anotherPoint instanceof Point2d` resultan en `true`: el objeto `Point2d.prototype` *está* en la cadena `[[Prototype]]` de `anotherPoint`.

Si en cambio quisieras verificar si la instancia de objeto fue creada *única y directamente* por una cierta clase, verificá la propiedad `constructor` de la instancia.

```js
point.constructor === Point2d;          // true
point.constructor === Point3d;          // false

anotherPoint.constructor === Point2d;   // false
anotherPoint.constructor === Point3d;   // true
```

| NOTA: |
| :--- |
| La propiedad `constructor` que se muestra acá *no* está realmente presente en (es propiedad de) los objetos de instancia `point` o `anotherPoint`. Entonces, ¿de dónde viene!? Está en el objeto prototype enlazado por `[[Prototype]]` de cada objeto: `Point2d.prototype.constructor === Point2d` y `Point3d.prototype.constructor === Point3d`. |

### "Herencia" Es Compartir, No Copiar

Puede parecer como si `Point3d`, cuando hace `extends` de la clase `Point2d`, estuviera en esencia obteniendo una *copia* de todo el comportamiento definido en `Point2d`. Además, puede parecer como si la instancia de objeto concreta `anotherPoint` recibiera, *copiados hacia abajo*, todos los métodos de `Point3d` (y por extensión, también de `Point2d`).

Sin embargo, ese no es el modelo mental correcto para usar con la implementación de orientación a clases de JS. Recordá esta definición de clase base y subclase, así como la instanciación de `anotherPoint`:

```js
class Point2d {
    x
    y
    constructor(x,y) {
        this.x = x;
        this.y = y;
    }
}

class Point3d extends Point2d {
    z
    constructor(x,y,z) {
        super(x,y);
        this.z = z;
    }
    toString() {
        console.log(`(${this.x},${this.y},${this.z})`);
    }
}

var anotherPoint = new Point3d(3,4,5);
```

Si inspeccionás el objeto `anotherPoint`, verás que solo tiene las propiedades `x`, `y` y `z` (miembros de instancia) en él, pero no el método `toString()`:

```js
Object.hasOwn(anotherPoint,"x");                       // true
Object.hasOwn(anotherPoint,"y");                       // true
Object.hasOwn(anotherPoint,"z");                       // true

Object.hasOwn(anotherPoint,"toString");                // false
```

¿Dónde está ubicado ese método `toString()`? En el objeto prototype:

```js
Object.hasOwn(Point3d.prototype,"toString");    // true
```

Y `anotherPoint` tiene acceso a ese método a través de su enlace `[[Prototype]]` (ver Capítulo 2). En otras palabras, los objetos prototype **comparten acceso** a su(s) método(s) con la(s) subclase(s) e instancia(s). El/los método(s) permanecen en su lugar, y no se copian hacia abajo en la cadena de herencia.

Por más agradable que sea la sintaxis de `class`, no olvides lo que realmente está pasando bajo la sintaxis: JS *solo* está conectando objetos entre sí a lo largo de una cadena `[[Prototype]]`.

## Comportamiento Estático de Clase

Hasta ahora hemos enfatizado dos ubicaciones diferentes para que residan los datos o el comportamiento (métodos): en el prototype del constructor, o en la instancia. Pero hay una tercera opción: en el constructor (objeto función) mismo.

En un sistema orientado a clases tradicional, los métodos definidos en una clase no son cosas concretas que podrías alguna vez invocar o con las que interactuar. Tenés que instanciar una clase para tener un objeto concreto con el cual invocar esos métodos. Los lenguajes prototipales como JS difuminan esta línea un poco: todos los métodos definidos en la clase son funciones "reales" que residen en el prototype del constructor, y por lo tanto podrías invocarlos. Pero como afirmé anteriormente, realmente *no deberías* hacerlo, ya que no es así como JS asume que vas a escribir tus `class`es, y hay algunos comportamientos extraños de casos límite con los que podrías toparte. Lo mejor es mantenerte en el camino estrecho que `class` traza para vos.

No todo comportamiento que definimos y queremos asociar/organizar con una clase *necesita* ser consciente de una instancia. Además, a veces una clase necesita definir públicamente datos (como constantes) a los que los desarrolladores que usan esa clase necesitan acceder, independientemente de cualquier instancia que puedan o no haber creado.

Entonces, ¿cómo permite un sistema de clases definir tales datos y comportamiento que deberían estar disponibles con una clase pero independientes de (inconscientes de) los objetos instanciados? **Propiedades y funciones estáticas**.

| NOTA: |
| :--- |
| Usaré "propiedad estática" / "función estática", en lugar de "miembro" / "método", solo para que quede más claro que hay una distinción entre miembros vinculados a instancias / métodos conscientes de instancias, y propiedades no vinculadas a instancias y funciones inconscientes de instancias. |

Usamos la palabra clave `static` en los cuerpos de nuestras `class` para distinguir estas definiciones:

```js
class Point2d {
    // class statics
    static origin = new Point2d(0,0)
    static distance(point1,point2) {
        return Math.sqrt(
            ((point2.x - point1.x) ** 2) +
            ((point2.y - point1.y) ** 2)
        );
    }

    // instance members and methods
    x
    y
    constructor(x,y) {
        this.x = x;
        this.y = y;
    }
    toString() {
        return `(${this.x},${this.y})`;
    }
}

console.log(`Starting point: ${Point2d.origin}`);
// Starting point: (0,0)

var next = new Point2d(3,4);
console.log(`Next point: ${next}`);
// Next point: (3,4)

console.log(`Distance: ${
    Point2d.distance( Point2d.origin, next )
}`);
// Distance: 5
```

El `Point2d.origin` es una propiedad estática, que justamente resulta contener una instancia construida de nuestra clase. Y `Point2d.distance(..)` es una función estática que computa la distancia cartesiana bidimensional entre dos puntos.

Por supuesto, podríamos haber puesto estos dos en algún lugar que no fuera como `static`s en la definición de la clase. Pero dado que están directamente relacionados con la clase `Point2d`, tiene *más sentido* organizarlos ahí.

| NOTA: |
| :--- |
| No olvides que cuando usás la sintaxis `class`, el nombre `Point2d` es en realidad el nombre de una función constructor que JS define. Así que `Point2d.origin` es solo un acceso de propiedad regular sobre ese objeto función. Eso es lo que quise decir al principio de esta sección cuando me referí a una tercera ubicación para almacenar *cosas* relacionadas con las clases; en JS, los `static`s se almacenan como propiedades en la función constructor. Tené cuidado de no confundirlos con las propiedades almacenadas en el `prototype` del constructor (métodos) y las propiedades almacenadas en la instancia (miembros). |

### Inicializaciones de Propiedades Estáticas

El valor en una inicialización estática (`static whatever = ..`) puede incluir referencias a `this`, que se refiere a la clase misma (en realidad, al constructor) en lugar de a una instancia:

```js
class Point2d {
    // class statics
    static originX = 0
    static originY = 0
    static origin = new this(this.originX,this.originY)

    // ..
}
```

| ADVERTENCIA: |
| :--- |
| No recomiendo realmente hacer el truco de `new this(..)` que ilustré acá. Eso es solo con fines ilustrativos. El código se leería más limpio con `new Point2d(this.originX,this.originY)`, así que preferí ese enfoque. |

Un detalle importante que no hay que pasar por alto: a diferencia de las inicializaciones de campos públicos, que solo ocurren una vez que ocurre una instanciación (con `new`), las inicializaciones estáticas de clase siempre corren *inmediatamente* después de que la `class` ha sido definida. Además, el orden de las inicializaciones estáticas importa; podés pensar en las sentencias como si estuvieran siendo evaluadas una a la vez.

También, al igual que los miembros de clase, las propiedades estáticas no tienen que ser inicializadas (por defecto: `undefined`), pero es mucho más común hacerlo. No hay mucha utilidad en declarar una propiedad estática sin valor inicializado (`static whatever`); acceder a `Point2d.whatever` o `Point2d.nonExistent` ambos resultarían en `undefined`.

Recientemente (en ES2022), la palabra clave `static` fue extendida para que ahora pueda definir un bloque dentro del cuerpo de la `class` para una inicialización más sofisticada de `static`s:

```js
class Point2d {
    // class statics
    static origin = new Point2d(0,0)
    static distance(point1,point2) {
        return Math.sqrt(
            ((point2.x - point1.x) ** 2) +
            ((point2.y - point1.y) ** 2)
        );
    }

    // static initialization block (as of ES2022)
    static {
        let outerPoint = new Point2d(6,8);
        this.maxDistance = this.distance(
            this.origin,
            outerPoint
        );
    }

    // ..
}

Point2d.maxDistance;        // 10
```

El `let outerPoint = ..` acá no es una característica especial de `class`; es exactamente como una declaración normal `let` en cualquier bloque de scope normal (ver el libro "Scope & Closures" de esta serie). Simplemente estamos declarando una instancia localizada de `Point2d` asignada a `outerPoint`, y luego usando ese valor para derivar la asignación a la propiedad estática `maxDistance`.

Los bloques de inicialización estática también son útiles para cosas como sentencias `try..catch` alrededor de computaciones de expresiones.

### Herencia Estática

Las estáticas de clase son heredadas por las subclases (¡obviamente, como estáticas!), pueden ser sobrescritas, y `super` puede usarse para referencias a la clase base (y polimorfismo de funciones estáticas), todo de manera muy similar a como funciona la herencia con los miembros/métodos de instancia:

```js
class Point2d {
    static origin = /* .. */
    static distance(x,y) { /* .. */ }

    static {
        // ..
        this.maxDistance = /* .. */;
    }

    // ..
}

class Point3d extends Point2d {
    // class statics
    static origin = new Point3d(
        // here, `this.origin` references wouldn't
        // work (self-referential), so we use
        // `super.origin` references instead
        super.origin.x, super.origin.y, 0
    )
    static distance(point1,point2) {
        // here, super.distance(..) is Point2d.distance(..),
        // if we needed to invoke it

        return Math.sqrt(
            ((point2.x - point1.x) ** 2) +
            ((point2.y - point1.y) ** 2) +
            ((point2.z - point1.z) ** 2)
        );
    }

    // instance members/methods
    z
    constructor(x,y,z) {
        super(x,y);     // <-- don't forget this line!
        this.z = z;
    }
    toString() {
        return `(${this.x},${this.y},${this.z})`;
    }
}

Point2d.maxDistance;        // 10
Point3d.maxDistance;        // 10
```

Como podés ver, la propiedad estática `maxDistance` que definimos en `Point2d` fue heredada como una propiedad estática en `Point3d`.

| TIP: |
| :--- |
| Recordá: cada vez que definís un constructor de subclase, vas a necesitar llamar a `super(..)` en él, usualmente como la primera sentencia. Me resulta demasiado fácil olvidarlo. |

No saltees el comportamiento subyacente de JS acá. Al igual que la herencia de métodos discutida anteriormente, la "herencia" estática *no* es una copia de estas propiedades/funciones estáticas de la clase base a la subclase; es compartición a través de la cadena `[[Prototype]]`. Específicamente, la función constructor `Point3d()` tiene su enlace `[[Prototype]]` cambiado por JS (del valor por defecto de `Function.prototype`) a `Point2d`, que es lo que permite que `Point3d.maxDistance` delegue a `Point2d.maxDistance`.

También es interesante, quizás solo históricamente ahora, notar que la herencia estática -- ¡que era parte del conjunto de características del mecanismo original de `class` de ES6! -- fue una característica específica que fue más allá de "solo azúcar sintáctico". La herencia estática, como la vemos ilustrada acá, *no* era posible de lograr/emular en JS antes de ES6, en el viejo estilo de código de clases prototipales. Es un comportamiento nuevo y especial introducido solo a partir de ES6.

## Comportamiento Privado de Clase

Todo lo que hemos discutido hasta ahora como parte de una definición de `class` es visible/accesible públicamente, ya sea como propiedades/funciones estáticas en la clase, métodos en el `prototype` del constructor, o propiedades miembro en la instancia.

¿Pero cómo almacenás información que no pueda verse desde fuera de la clase? Esta fue una de las características más pedidas, y una de las mayores quejas con la `class` de JS, hasta que finalmente se abordó en ES2022.

`class` ahora soporta nueva sintaxis para declarar campos privados (miembros de instancia) y métodos privados. Además, las propiedades/funciones estáticas privadas son posibles.

### ¿Motivación?

Antes de ilustrar cómo hacer privados de `class`, vale la pena contemplar por qué es una característica útil.

Con los patrones de diseño orientados a closure (de nuevo, ver el libro "Scope & Closures" de esta serie), automáticamente obtenemos "privacidad" incorporada. Cuando declarás una variable dentro de un scope, no puede verse fuera de ese scope. Punto. Reducir la visibilidad del scope de una declaración es útil para prevenir colisiones de nombres (nombres de variables idénticos).

Pero es incluso más importante para asegurar un diseño "defensivo" apropiado del software, el llamado "Principio del Menor Privilegio" [^POLP]. POLP establece que solo deberíamos exponer una pieza de información o capacidad en nuestro software a la menor superficie necesaria.

La sobre-exposición abre nuestro software a varios problemas que complican la seguridad/mantenimiento del software, incluyendo que otra pieza de código actúe maliciosamente para hacer algo que nuestro código no esperaba o pretendía. Además, está la preocupación menos crítica pero igual de problemática de que otras partes de nuestro software dependan de (usen) partes de nuestro código que deberíamos haber reservado como detalle de implementación oculto. Una vez que otro código depende de los detalles de implementación de nuestro código, dejamos de poder refactorizar nuestro código sin potencialmente romper otras partes del programa.

Entonces, en resumen, *deberíamos* ocultar los detalles de implementación si no es necesario exponerlos. En este sentido, el sistema de `class` de JS se siente un poco demasiado permisivo en que todo por defecto es público. Las características de clase privadas son una adición bienvenida a un diseño de software más apropiado.

#### ¿Demasiado Privado?

Dicho todo eso, tengo que echarle un poco de agua fría a la fiesta de lo privado en las clases.

He sugerido fuertemente que solo deberías usar `class` si vas a aprovechar realmente la mayoría o todo lo que la orientación a clases te da. De lo contrario, estarías mejor usando otras características de pilar central de JS para organizar código, como con el patrón de closure.

Uno de los aspectos más importantes de la orientación a clases es la herencia de subclases, como hemos visto ilustrado numerosas veces hasta ahora en este capítulo. ¿Adiviná qué le pasa a un miembro/método privado en una clase base, cuando es extendido por una subclase?

Los miembros/métodos privados son privados **solo para la clase en la que están definidos**, y **no** son heredados de ninguna manera por una subclase. Uy.

Eso puede no parecer una preocupación demasiado grande, hasta que empezás a trabajar con `class` y miembros/métodos privados en software real. Podrías toparte rápidamente con una situación donde necesitás acceder a un método privado, o incluso más a menudo, solo un miembro privado, desde la subclase, para que la subclase pueda extender/aumentar el comportamiento de la clase base como se desee. Y podrías gritar de frustración bastante rápido una vez que te des cuenta de que esto no es posible.

Lo que viene después es inevitablemente una decisión incómoda: ¿simplemente volvés a hacerlo público, para que la subclase pueda acceder a él? Puaj. O, peor, ¿intentás rediseñar la clase base para contorsionar el diseño de sus miembros/métodos, de modo que la falta de acceso se resuelva parcialmente? Eso a menudo implica una agotadora sobre-parametrización (con privados como valores de parámetro por defecto) de los métodos, y otros trucos similares. Doble puaj.

No hay una respuesta particularmente buena acá, para ser honesto. Si tenés experiencia con la orientación a clases en lenguajes de clases más tradicionales como Java o C++, probablemente estés dudoso de por qué no tenemos visibilidad *protected* entre *public* y *private*. Eso es exactamente para lo que sirve *protected*: mantener algo privado para una clase Y cualquiera de sus subclases. Esos lenguajes también tienen características *friend*, pero eso está más allá del alcance de nuestra discusión acá.

Lamentablemente, no solo JS no tiene visibilidad *protected*, sino que parece (¡por más útil que sea!) poco probable como característica de JS. Se ha discutido en gran detalle por más de una década (antes de que ES6 fuera siquiera una cosa), y ha habido múltiples propuestas para ello.

No debería decir que *nunca* pasará, porque ese no es un terreno sólido donde apostar en ningún software. Pero es muy improbable, porque en realidad traiciona el pilar mismo sobre el que se construye `class`. Si tenés curiosidad, o (más probable) estás seguro de que *tiene que haber una manera*, cubriré la incompatibilidad de la visibilidad *protected* dentro de los mecanismos de JS en un apéndice.

El punto acá es, a día de hoy, JS no tiene visibilidad *protected*, y no la tendrá en el corto plazo. Y la visibilidad *protected* es en realidad, en la práctica, mucho más útil que la visibilidad *private*.

Entonces volvemos a la pregunta: **¿Por qué deberías preocuparte por hacer privado algún contenido de `class`?**

Si soy honesto: quizás no deberías. O quizás sí. Eso depende de vos. Solo entrá en ello consciente de los tropiezos.

### Miembros/Métodos Privados

Estás ansioso por ver finalmente la sintaxis de la mágica visibilidad *private*, ¿no? Por favor no le dispares al mensajero si te sentís enojado o triste por lo que estás a punto de ver.

```js
class Point2d {
    // statics
    static samePoint(point1,point2) {
        return point1.#ID === point2.#ID;
    }

    // privates
    #ID = null
    #assignID() {
        this.#ID = Math.round(Math.random() * 1e9);
    }

    // publics
    x
    y
    constructor(x,y) {
        this.#assignID();
        this.x = x;
        this.y = y;
    }
}

var one = new Point2d(3,4);
var two = new Point2d(3,4);

Point2d.samePoint(one,two);         // false
Point2d.samePoint(one,one);         // true
```

No, JS no hizo lo sensato e introdujo una palabra clave `private` como lo hicieron con `static`. En cambio, introdujeron el `#`. (insertá un chiste malo sobre los millennials de las redes sociales que aman los hashtags, o algo así)

| TIP: |
| :--- |
| Y sí, hay un millón y una discusiones sobre por qué no. Podría pasar capítulos relatando toda la historia, pero honestamente simplemente no me interesa. Creo que esta sintaxis es fea, y muchos otros también. ¡Y a algunos les encanta! Si estás en el último grupo, aunque rara vez hago algo como esto, simplemente voy a decir: **simplemente aceptalo**. Es demasiado tarde para más debate o súplicas. |

La sintaxis `#whatever` (incluyendo la forma `this.#whatever`) solo es válida dentro de los cuerpos de `class`. Lanzará errores de sintaxis si se usa fuera de una `class`.

A diferencia de los campos públicos/miembros de instancia, los campos privados/miembros de instancia *deben* declararse en el cuerpo de la `class`. No podés agregar dinámicamente un miembro privado a una declaración de clase mientras estás en el método constructor; las asignaciones del tipo `this.#whatever = ..` solo funcionan si el campo privado `#whatever` está declarado en el cuerpo de la clase. Además, aunque los campos privados pueden reasignarse, no pueden `delete`arse de una instancia, de la manera en que un campo público/miembro de clase sí puede.

#### Subclases + Privados

Advertí anteriormente que subclasear con clases que tienen miembros/métodos privados puede ser una trampa limitante. Pero eso no significa que no puedan usarse juntos.

Dado que la "herencia" en JS es compartir (a través de la cadena `[[Prototype]]`), si invocás un método heredado en una subclase, y ese método heredado a su vez accede/invoca privados en su clase anfitriona (base), esto funciona bien:

```js
class Point2d { /* .. */ }

class Point3d extends Point2d {
    z
    constructor(x,y,z) {
        super(x,y);
        this.z = z;
    }
}

var one = new Point3d(3,4,5);
```

La llamada `super(x,y)` en este constructor invoca el constructor de la clase base heredada (`Point2d(..)`), que a su vez accede al método privado `#assignID()` de `Point2d` (ver el fragmento anterior). No se lanza ninguna excepción, aunque `Point3d` no puede ver ni acceder directamente a los privados `#ID` / `#assignID()` que efectivamente están almacenados en la instancia (llamada `one` acá).

De hecho, incluso la función heredada `static samePoint(..)` funcionará desde ya sea `Point3d` o `Point2d`:

```js
Point2d.samePoint(one,one);         // true
Point3d.samePoint(one,one);         // true
```

En realidad, eso no debería ser tan sorprendente, ya que:

```js
Point2d.samePoint === Point3d.samePoint;
```

La referencia de función heredada es *exactamente la misma función* que la referencia de función base; no es una copia de la función. Dado que la función en cuestión no tiene ninguna referencia a `this`, sin importar desde dónde se invoque, debería producir el mismo resultado.

Sigue siendo una lástima que `Point3d` no tenga forma de acceder/influir, o de hecho ni siquiera conocer, los privados `#ID` / `#assignID()` de `Point2d`:

```js
class Point2d { /* .. */ }

class Point3d extends Point2d {
    z
    constructor(x,y,z) {
        super(x,y);
        this.z = z;

        console.log(this.#ID);      // will throw!
    }
}
```

| ADVERTENCIA: |
| :--- |
| Notá que este fragmento lanza un error temprano de sintaxis estática en el momento de definir la clase `Point3d`, antes incluso de tener la oportunidad de crear una instancia de la clase. La misma excepción se lanzaría si la referencia fuera `super.#ID` en lugar de `this.#ID`. |

#### Verificación de Existencia

Tené en cuenta que solo la `class` misma conoce, y por lo tanto puede verificar, tal campo/método privado.

Puede que quieras verificar si un campo/método privado existe en una instancia de objeto. Por ejemplo (como se muestra abajo), puede que tengas una función estática o método en una clase, que recibe una referencia de objeto externo pasada. Para verificar si la referencia de objeto pasada es de esta misma clase (y por lo tanto tiene los mismos miembros/métodos privados en ella), básicamente necesitás hacer una "verificación de marca" (brand check) contra el objeto.

Tal verificación podría ser bastante enrevesada, porque si accedés a un campo privado que no existe ya en el objeto, obtenés una excepción de JS lanzada, requiriendo una fea lógica `try..catch`.

Pero hay un enfoque más limpio, la llamada "verificación de marca ergonómica" (ergonomic brand check), usando la palabra clave `in`:

```js
class Point2d {
    // statics
    static samePoint(point1,point2) {
        // "ergonomic brand checks"
        if (#ID in point1 && #ID in point2) {
            return point1.#ID === point2.#ID;
        }
        return false;
    }

    // privates
    #ID = null
    #assignID() {
        this.#ID = Math.round(Math.random() * 1e9);
    }

    // publics
    x
    y
    constructor(x,y) {
        this.#assignID();
        this.x = x;
        this.y = y;
    }
}

var one = new Point2d(3,4);
var two = new Point2d(3,4);

Point2d.samePoint(one,two);         // false
Point2d.samePoint(one,one);         // true
```

La verificación `#privateField in someObject` no lanzará una excepción si el campo no se encuentra, así que es seguro usarla sin `try..catch` y usar su simple resultado booleano.

#### Exfiltración

Aunque un miembro/método pueda declararse con visibilidad *private*, todavía puede ser exfiltrado (extraído) de una instancia de clase:

```js
var id, func;

class Point2d {
    // privates
    #ID = null
    #assignID() {
        this.#ID = Math.round(Math.random() * 1e9);
    }

    // publics
    x
    y
    constructor(x,y) {
        this.#assignID();
        this.x = x;
        this.y = y;

        // exfiltration
        id = this.#ID;
        func = this.#assignID;
    }
}

var point = new Point2d(3,4);

id;                     // 7392851012 (...for example)

func;                   // function #assignID() { .. }
func.call(point,42);

func.call({},100);
// TypeError: Cannot write private member #ID to an
// object whose class did not declare it
```

La principal preocupación acá es tener cuidado al pasar métodos privados como callbacks (o al exponer de cualquier manera privados a otras partes del programa). No hay nada que te impida hacerlo, lo que puede crear un poco de una divulgación no intencionada de privacidad.

### Estáticas Privadas

Las propiedades y funciones estáticas también pueden usar `#` para ser marcadas como privadas:

```js
class Point2d {
    static #errorMsg = "Out of bounds."
    static #printError() {
        console.log(`Error: ${this.#errorMsg}`);
    }

    // publics
    x
    y
    constructor(x,y) {
        if (x > 100 || y > 100) {
            Point2d.#printError();
        }
        this.x = x;
        this.y = y;
    }
}

var one = new Point2d(30,400);
// Error: Out of bounds.
```

La función estática privada `#printError()` acá tiene un `this`, pero eso referencia a la clase `Point2d`, no a una instancia. Como tal, `#errorMsg` y `#printError()` son independientes de las instancias y por lo tanto están mejor como estáticas. Además, no hay razón para que sean accesibles fuera de la clase, así que están marcadas como privadas.

Recordá: las estáticas privadas de forma similar no son heredadas por las subclases, al igual que los miembros/métodos privados no lo son.

#### Gotcha: Subclasear Con Estáticas Privadas y `this`

Recordá que los métodos heredados, invocados desde una subclase, no tienen problema en acceder (a través de referencias del estilo `this.#whatever`) a cualquier privado de su propia clase base:

```js
class Point2d {
    // ..

    getID() {
        return this.#ID;
    }

    // ..
}

class Point3d extends Point2d {
    // ..

    printID() {
        console.log(`ID: ${this.getID()}`);
    }
}

var point = new Point3d(3,4,5);
point.printID();
// ID: ..
```

Eso funciona perfectamente.

Lamentablemente, y (para mí) de forma bastante inesperada/inconsistente, lo mismo no es cierto para las estáticas privadas accedidas desde funciones estáticas públicas heredadas:

```js
class Point2d {
    static #errorMsg = "Out of bounds."
    static printError() {
        console.log(`Error: ${this.#errorMsg}`);
    }

    // ..
}

class Point3d extends Point2d {
    // ..
}

Point2d.printError();
// Error: Out of bounds.

Point3d.printError === Point2d.printError;
// true

Point3d.printError();
// TypeError: Cannot read private member #errorMsg
// from an object whose class did not declare it
```

La estática `printError()` es heredada (compartida a través de `[[Prototype]]`) de `Point2d` a `Point3d` perfectamente, que es por lo que las referencias de función son idénticas. Como el fragmento no estático justo arriba, podrías haber esperado que la invocación estática `Point3d.printError()` se resolviera a través de la cadena `[[Prototype]]` a su ubicación original en la clase base (`Point2d`), permitiéndole así acceder a la estática privada `#errorMsg` de la clase base.

Pero falla, como se muestra en la última sentencia de ese fragmento. La razón por la que falla acá, pero no con el fragmento anterior, es un rompecabezas mental enrevesado. No voy a profundizar en la explicación del *por qué* acá, francamente porque me hierve la sangre hacerlo.

Hay un *arreglo*, sin embargo. En la función estática, en lugar de `this.#errorMsg`, cambiá eso por `Point2d.#errorMsg`, y ahora funciona:

```js
class Point2d {
    static #errorMsg = "Out of bounds."
    static printError() {
        // the fixed reference vvvvvv
        console.log(`Error: ${Point2d.#errorMsg}`);
    }

    // ..
}

class Point3d extends Point2d {
    // ..
}

Point2d.printError();
// Error: Out of bounds.

Point3d.printError();
// Error: Out of bounds.  <-- phew, it works now!
```

Si se están heredando funciones estáticas públicas, usá el nombre de la clase para acceder a cualquier estática privada en lugar de usar referencias `this.`. ¡Cuidado con ese gotcha!

## Ejemplo de Clase

OK, hemos presentado un montón de características dispares de clases. Quiero cerrar este capítulo intentando ilustrar una muestra de estas capacidades en un único ejemplo que sea un poco menos básico/artificial.

```js
class CalendarItem {
    static #UNSET = Symbol("unset")
    static #isUnset(v) {
        return v === this.#UNSET;
    }
    static #error(num) {
        return this[`ERROR_${num}`];
    }
    static {
        for (let [idx,msg] of [
            "ID is already set.",
            "ID is unset.",
            "Don't instantiate 'CalendarItem' directly.",
        ].entries()) {
            this[`ERROR_${(idx+1)*100}`] = msg;
        }
    }
    static isSameItem(item1,item2) {
        if (#ID in item1 && #ID in item2) {
            return item1.#ID === item2.#ID;
        }
        else {
            return false;
        }
    }

    #ID = CalendarItem.#UNSET
    #setID(id) {
        if (CalendarItem.#isUnset(this.#ID)) {
            this.#ID = id;
        }
        else {
            throw new Error(CalendarItem.#error(100));
        }
    }

    description = null
    startDateTime = null

    constructor() {
        if (new.target !== CalendarItem) {
            let id = Math.round(Math.random() * 1e9);
            this.#setID(id);
        }
        else {
            throw new Error(CalendarItem.#error(300));
        }
    }
    getID() {
        if (!CalendarItem.#isUnset(this.#ID)) {
            return this.#ID;
        }
        else {
            throw new Error(CalendarItem.#error(200));
        }
    }
    getDateTimeStr() {
        if (this.startDateTime instanceof Date) {
            return this.startDateTime.toUTCString();
        }
    }
    summary() {
        console.log(`(${
            this.getID()
        }) ${
            this.description
        } at ${
            this.getDateTimeStr()
        }`);
    }
}

class Reminder extends CalendarItem {
    #complete = false;  // <-- no ASI, semicolon needed

    [Symbol.toStringTag] = "Reminder"
    constructor(description,startDateTime) {
        super();

        this.description = description;
        this.startDateTime = startDateTime;
    }
    isComplete() {
        return !!this.#complete;
    }
    markComplete() {
        this.#complete = true;
    }
    summary() {
        if (this.isComplete()) {
            console.log(`(${this.getID()}) Complete.`);
        }
        else {
            super.summary();
        }
    }
}

class Meeting extends CalendarItem {
    #getEndDateTimeStr() {
        if (this.endDateTime instanceof Date) {
            return this.endDateTime.toUTCString();
        }
    }

    endDateTime = null;  // <-- no ASI, semicolon needed

    [Symbol.toStringTag] = "Meeting"
    constructor(description,startDateTime,endDateTime) {
        super();

        this.description = description;
        this.startDateTime = startDateTime;
        this.endDateTime = endDateTime;
    }
    getDateTimeStr() {
        return `${
            super.getDateTimeStr()
        } - ${
            this.#getEndDateTimeStr()
        }`;
    }
}
```

Tomate un tiempo para leer y digerir esas definiciones de `class`. ¿Detectaste la mayoría de las características de `class` de las que hablamos en este capítulo?

| NOTA: |
| :--- |
| Una pregunta que podés tener: ¿por qué no moví la lógica repetida de establecer `description` y `startDateTime` de ambos constructores de subclase hacia el único constructor base? Este es un punto matizado, pero no es mi intención que `CalendarItem` sea alguna vez instanciado directamente; es lo que en términos de orientación a clases llamamos una "clase abstracta". ¡Por eso estoy usando `new.target` para lanzar un error si la clase `CalendarItem` es alguna vez instanciada directamente! Así que no quiero implicar por la firma que el constructor `CalendarItem(..)` deba usarse alguna vez directamente. |

Veamos ahora estas tres clases en uso:

```js
var callMyParents = new Reminder(
    "Call my parents to say hi",
    new Date("July 7, 2022 11:00:00 UTC")
);
callMyParents.toString();
// [object Reminder]
callMyParents.summary();
// (586380912) Call my parents to say hi at
// Thu, 07 Jul 2022 11:00:00 GMT
callMyParents.markComplete();
callMyParents.summary();
// (586380912) Complete.
callMyParents instanceof Reminder;
// true
callMyParents instanceof CalendarItem;
// true
callMyParents instanceof Meeting;
// false


var interview = new Meeting(
    "Job Interview: ABC Tech",
    new Date("June 23, 2022 08:30:00 UTC"),
    new Date("June 23, 2022 09:15:00 UTC")
);
interview.toString();
// [object Meeting]
interview.summary();
// (994337604) Job Interview: ABC Tech at Thu,
// 23 Jun 2022 08:30:00 GMT - Thu, 23 Jun 2022
// 09:15:00 GMT
interview instanceof Meeting;
// true
interview instanceof CalendarItem;
// true
interview instanceof Reminder;
// false


Reminder.isSameItem(callMyParents,callMyParents);
// true
Meeting.isSameItem(callMyParents,interview);
// false
```

Reconozco que algunas partes de este ejemplo son un poco artificiales. Pero honestamente, creo que casi todo esto son usos plausibles y razonables de las diversas características de `class`.

Por cierto, probablemente hay un millón de formas diferentes de estructurar la lógica del código de arriba. De ninguna manera estoy afirmando que esta sea la forma *correcta* o *mejor* de hacerlo. Como ejercicio para el lector, probá escribirlo vos mismo, y tomá nota de las cosas que hiciste diferente a mi enfoque.

[^POLP]: "Principle of Least Privilege", Wikipedia; https://en.wikipedia.org/wiki/Principle_of_least_privilege ; Accedido en Julio 2022
