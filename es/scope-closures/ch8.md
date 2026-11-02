# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Capítulo 8: El Patrón Módulo

En este capítulo cerramos el texto principal del libro explorando uno de los patrones de organización de código más importantes de toda la programación: el módulo. Como veremos, los módulos están construidos inherentemente a partir de lo que ya hemos cubierto: la recompensa por tu esfuerzo en aprender el scope léxico y el closure.

Hemos examinado cada ángulo del scope léxico, desde la amplitud del scope global hacia abajo a través de los block scopes anidados, hasta las complejidades del ciclo de vida de las variables. Luego aprovechamos el scope léxico para entender todo el poder del closure.

Tomate un momento para reflexionar sobre lo lejos que has llegado en este viaje hasta ahora; ¡has dado grandes pasos para conocer JS más profundamente!

El tema central de este libro ha sido que entender y dominar el scope y el closure es clave para estructurar y organizar correctamente nuestro código, especialmente las decisiones sobre dónde almacenar información en las variables.

Nuestro objetivo en este capítulo final es apreciar cómo los módulos encarnan la importancia de estos temas, elevándolos de conceptos abstractos a mejoras concretas y prácticas en la construcción de programas.

## Encapsulamiento y Mínima Exposición (POLE)

El encapsulamiento suele citarse como un principio de la programación orientada a objetos (OO), pero es más fundamental y de aplicación más amplia que eso. El objetivo del encapsulamiento es agrupar o ubicar juntos la información (datos) y el comportamiento (funciones) que en conjunto sirven a un propósito común.

Independientemente de cualquier sintaxis o mecanismo de código, el espíritu del encapsulamiento puede materializarse en algo tan simple como usar archivos separados para contener fragmentos del programa general con un propósito común. Si agrupamos todo lo que potencia una lista de resultados de búsqueda en un único archivo llamado "search-list.js", estamos encapsulando esa parte del programa.

La tendencia reciente en la programación front-end moderna a organizar las aplicaciones en torno a la arquitectura de Componentes lleva el encapsulamiento aún más lejos. Para muchos, resulta natural consolidar todo lo que constituye la lista de resultados de búsqueda —incluso más allá del código, incluyendo el marcado de presentación y los estilos— en una única unidad de lógica de programa, algo tangible con lo que podemos interactuar. Y luego etiquetamos esa colección como el componente "SearchList".

Otro objetivo clave es el control de la visibilidad de ciertos aspectos de los datos y la funcionalidad encapsulados. Recordá del Capítulo 6 el principio de *mínima exposición* (POLE), que busca protegerse defensivamente contra varios *peligros* de la sobreexposición del scope; estos afectan tanto a variables como a funciones. En JS, lo más frecuente es que implementemos el control de visibilidad a través de la mecánica del scope léxico.

La idea es agrupar juntos fragmentos de programa similares, y limitar selectivamente el acceso programático a las partes que consideramos detalles *privados*. Lo que no se considera *privado* se marca entonces como *público*, accesible para todo el programa.

El efecto natural de este esfuerzo es una mejor organización del código. Es más fácil construir y mantener software cuando sabemos dónde están las cosas, con límites y puntos de conexión claros y evidentes. También es más fácil mantener la calidad si evitamos las trampas de los datos y la funcionalidad sobreexpuestos.

Estos son algunos de los principales beneficios de organizar los programas JS en módulos.

## ¿Qué Es un Módulo?

Un módulo es una colección de datos y funciones relacionados (a menudo llamados métodos en este contexto), caracterizada por una división entre detalles *privados* ocultos y detalles *públicos* accesibles, usualmente llamados la "API pública".

Un módulo también tiene estado: mantiene cierta información a lo largo del tiempo, junto con funcionalidad para acceder a esa información y actualizarla.

| NOTA: |
| :--- |
| Una preocupación más amplia del patrón módulo es abrazar plenamente la modularización a nivel de sistema a través del bajo acoplamiento y otras técnicas de arquitectura de programas. Ese es un tema complejo que excede ampliamente los límites de nuestra discusión, pero vale la pena estudiarlo más allá de este libro. |

Para entender mejor qué es un módulo, comparemos algunas características de los módulos con patrones de código útiles que no son del todo módulos.

### Namespaces (Agrupación sin Estado)

Si agrupás un conjunto de funciones relacionadas, sin datos, entonces en realidad no tenés el encapsulamiento esperado que un módulo implica. El mejor término para esta agrupación de funciones *sin estado* es namespace:

```js
// namespace, not module
var Utils = {
    cancelEvt(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        evt.stopImmediatePropagation();
    },
    wait(ms) {
        return new Promise(function c(res){
            setTimeout(res,ms);
        });
    },
    isValidEmail(email) {
        return /[^@]+@[^@.]+\.[^@.]+/.test(email);
    }
};
```

`Utils` aquí es una colección útil de utilidades, pero todas son funciones independientes del estado. Reunir funcionalidad junta es en general una buena práctica, pero eso no hace que esto sea un módulo. Más bien, hemos definido un namespace `Utils` y organizado las funciones bajo él.

### Estructuras de Datos (Agrupación con Estado)

Incluso si agrupás datos y funciones con estado juntos, si no estás limitando la visibilidad de nada de eso, entonces te quedás corto en el aspecto POLE del encapsulamiento; no resulta particularmente útil etiquetar eso como un módulo.

Considerá:

```js
// data structure, not module
var Student = {
    records: [
        { id: 14, name: "Kyle", grade: 86 },
        { id: 73, name: "Suzy", grade: 87 },
        { id: 112, name: "Frank", grade: 75 },
        { id: 6, name: "Sarah", grade: 91 }
    ],
    getName(studentID) {
        var student = this.records.find(
            student => student.id == studentID
        );
        return student.name;
    }
};

Student.getName(73);
// Suzy
```

Dado que `records` es un dato accesible públicamente, no oculto detrás de una API pública, `Student` aquí no es realmente un módulo.

`Student` sí tiene el aspecto de datos-y-funcionalidad del encapsulamiento, pero no el aspecto de control de visibilidad. Lo mejor es etiquetar esto como una instancia de una estructura de datos.

### Módulos (Control de Acceso con Estado)

Para encarnar el espíritu completo del patrón módulo, no solo necesitamos agrupación y estado, sino también control de acceso a través de la visibilidad (privado vs. público).

Convirtamos `Student` de la sección anterior en un módulo. Empezaremos con una forma que yo llamo el "módulo clásico", que originalmente se conocía como el "módulo revelador" (revealing module) cuando surgió por primera vez a comienzos de los años 2000. Considerá:

```js
var Student = (function defineStudent(){
    var records = [
        { id: 14, name: "Kyle", grade: 86 },
        { id: 73, name: "Suzy", grade: 87 },
        { id: 112, name: "Frank", grade: 75 },
        { id: 6, name: "Sarah", grade: 91 }
    ];

    var publicAPI = {
        getName
    };

    return publicAPI;

    // ************************

    function getName(studentID) {
        var student = records.find(
            student => student.id == studentID
        );
        return student.name;
    }
})();

Student.getName(73);   // Suzy
```

`Student` es ahora una instancia de un módulo. Cuenta con una API pública con un único método: `getName(..)`. Este método puede acceder al dato privado oculto `records`.

| ADVERTENCIA: |
| :--- |
| Debería señalar que los datos explícitos de estudiantes codificados de forma fija dentro de esta definición de módulo son solo para fines ilustrativos. Un módulo típico en tu programa recibirá estos datos de una fuente externa, cargados típicamente desde bases de datos, archivos de datos JSON, llamadas Ajax, etc. Luego los datos se inyectan en la instancia del módulo típicamente a través de método(s) en la API pública del módulo. |

¿Cómo funciona el formato de módulo clásico?

Observá que la instancia del módulo se crea mediante la ejecución de la IIFE `defineStudent()`. Esta IIFE devuelve un objeto (llamado `publicAPI`) que tiene una propiedad que referencia la función interna `getName(..)`.

Nombrar al objeto `publicAPI` es una preferencia estilística de mi parte. El objeto puede nombrarse como quieras (a JS no le importa), o podés simplemente devolver un objeto directamente sin asignarlo a ninguna variable interna con nombre. Más sobre esta elección en el Apéndice A.

Desde afuera, `Student.getName(..)` invoca esta función interna expuesta, que mantiene el acceso a la variable interna `records` vía closure.

No *tenés* que devolver un objeto con una función como una de sus propiedades. Podrías simplemente devolver una función directamente, en lugar del objeto. Eso igual satisface todas las partes centrales de un módulo clásico.

En virtud de cómo funciona el scope léxico, definir variables y funciones dentro de tu función externa de definición de módulo hace que todo sea *por defecto* privado. Solo las propiedades agregadas al objeto de API pública devuelto por la función se exportarán para uso público externo.

El uso de una IIFE implica que nuestro programa solo necesita una única instancia central del módulo, comúnmente llamada "singleton". De hecho, este ejemplo específico es lo bastante simple como para que no haya una razón obvia por la cual necesitaríamos algo más que una sola instancia del módulo `Student`.

#### Fábrica de Módulos (Múltiples Instancias)

Pero si quisiéramos definir un módulo que soportara múltiples instancias en nuestro programa, podemos ajustar ligeramente el código:

```js
// factory function, not singleton IIFE
function defineStudent() {
    var records = [
        { id: 14, name: "Kyle", grade: 86 },
        { id: 73, name: "Suzy", grade: 87 },
        { id: 112, name: "Frank", grade: 75 },
        { id: 6, name: "Sarah", grade: 91 }
    ];

    var publicAPI = {
        getName
    };

    return publicAPI;

    // ************************

    function getName(studentID) {
        var student = records.find(
            student => student.id == studentID
        );
        return student.name;
    }
}

var fullTime = defineStudent();
fullTime.getName(73);            // Suzy
```

En lugar de especificar `defineStudent()` como una IIFE, simplemente la definimos como una función independiente normal, que en este contexto comúnmente se llama función "fábrica de módulos" (module factory).

Luego llamamos a la fábrica de módulos, produciendo una instancia del módulo que etiquetamos como `fullTime`. Esta instancia del módulo implica una nueva instancia del scope interno, y por lo tanto un nuevo closure que `getName(..)` mantiene sobre `records`. `fullTime.getName(..)` ahora invoca el método sobre esa instancia específica.

#### Definición del Módulo Clásico

Entonces, para aclarar qué hace que algo sea un módulo clásico:

* Debe haber un scope externo, típicamente de una función fábrica de módulos que se ejecuta al menos una vez.

* El scope interno del módulo debe tener al menos una pieza de información oculta que represente el estado del módulo.

* El módulo debe devolver en su API pública una referencia a al menos una función que tenga closure sobre el estado oculto del módulo (para que ese estado se preserve efectivamente).

Es probable que te cruces con otras variaciones de este enfoque de módulo clásico, que veremos en más detalle en el Apéndice A.

## Módulos CommonJS de Node

En el Capítulo 4, presentamos el formato de módulo CommonJS usado por Node. A diferencia del formato de módulo clásico descrito antes, donde podías agrupar la fábrica de módulos o la IIFE junto con cualquier otro código incluyendo otros módulos, los módulos CommonJS están basados en archivos; un módulo por archivo.

Ajustemos nuestro ejemplo de módulo para adherirse a ese formato:

```js
module.exports.getName = getName;

// ************************

var records = [
    { id: 14, name: "Kyle", grade: 86 },
    { id: 73, name: "Suzy", grade: 87 },
    { id: 112, name: "Frank", grade: 75 },
    { id: 6, name: "Sarah", grade: 91 }
];

function getName(studentID) {
    var student = records.find(
        student => student.id == studentID
    );
    return student.name;
}
```

Los identificadores `records` y `getName` están en el scope de nivel superior de este módulo, pero ese no es el scope global (como se explicó en el Capítulo 4). Como tal, todo aquí es *por defecto* privado al módulo.

Para exponer algo en la API pública de un módulo CommonJS, agregás una propiedad al objeto vacío provisto como `module.exports`. En algún código heredado más antiguo, podés cruzarte con referencias a solo un `exports` desnudo, pero por claridad del código siempre deberías calificar completamente esa referencia con el prefijo `module.`.

Por cuestiones de estilo, me gusta poner mis "exports" arriba y la implementación de mi módulo abajo. Pero estos exports pueden ubicarse en cualquier parte. Recomiendo encarecidamente agruparlos todos juntos, ya sea al principio o al final de tu archivo.

Algunos desarrolladores tienen la costumbre de reemplazar el objeto exports por defecto, así:

```js
// defining a new object for the API
module.exports = {
    // ..exports..
};
```

Hay algunas peculiaridades con este enfoque, incluyendo comportamiento inesperado si varios de esos módulos dependen circularmente unos de otros. Por eso recomiendo no reemplazar el objeto. Si querés asignar múltiples exports a la vez, usando el estilo de definición de objeto literal, podés hacer esto en su lugar:

```js
Object.assign(module.exports,{
   // .. exports ..
});
```

Lo que sucede aquí es que se define el objeto literal `{ .. }` con la API pública de tu módulo especificada, y luego `Object.assign(..)` realiza una copia superficial de todas esas propiedades sobre el objeto `module.exports` existente, en lugar de reemplazarlo. Este es un buen equilibrio entre conveniencia y un comportamiento de módulo más seguro.

Para incluir otra instancia de módulo dentro de tu módulo/programa, usá el método `require(..)` de Node. Suponiendo que este módulo se encuentra en "/path/to/student.js", así podemos acceder a él:

```js
var Student = require("/path/to/student.js");

Student.getName(73);
// Suzy
```

`Student` ahora referencia la API pública de nuestro módulo de ejemplo.

Los módulos CommonJS se comportan como instancias singleton, de forma similar al estilo de definición de módulo IIFE presentado antes. No importa cuántas veces hagas `require(..)` del mismo módulo, solo obtenés referencias adicionales a la única instancia compartida del módulo.

`require(..)` es un mecanismo de todo-o-nada; incluye una referencia a toda la API pública expuesta del módulo. Para acceder efectivamente solo a parte de la API, el enfoque típico se ve así:

```js
var getName = require("/path/to/student.js").getName;

// or alternately:

var { getName } = require("/path/to/student.js");
```

De forma similar al formato de módulo clásico, los métodos exportados públicamente de la API de un módulo CommonJS mantienen closures sobre los detalles internos del módulo. Así es como el estado singleton del módulo se mantiene a lo largo de la vida de tu programa.

| NOTA: |
| :--- |
| En las sentencias `require("student")` de Node, las rutas no absolutas (`"student"`) asumen una extensión de archivo ".js" y buscan en "node_modules". |

## Módulos ES Modernos (ESM)

El formato ESM comparte varias similitudes con el formato CommonJS. ESM está basado en archivos, y las instancias de módulo son singletons, con todo privado *por defecto*. Una diferencia notable es que se asume que los archivos ESM están en strict mode, sin necesidad de una pragma `"use strict"` arriba. No hay forma de definir un ESM en modo no estricto.

En lugar de `module.exports` en CommonJS, ESM usa la palabra clave `export` para exponer algo en la API pública del módulo. La palabra clave `import` reemplaza a la sentencia `require(..)`. Ajustemos "students.js" para usar el formato ESM:

```js
export { getName };

// ************************

var records = [
    { id: 14, name: "Kyle", grade: 86 },
    { id: 73, name: "Suzy", grade: 87 },
    { id: 112, name: "Frank", grade: 75 },
    { id: 6, name: "Sarah", grade: 91 }
];

function getName(studentID) {
    var student = records.find(
        student => student.id == studentID
    );
    return student.name;
}
```

El único cambio aquí es la sentencia `export { getName }`. Como antes, las sentencias `export` pueden aparecer en cualquier parte a lo largo del archivo, aunque `export` debe estar en el scope de nivel superior; no puede estar dentro de ningún otro bloque o función.

ESM ofrece bastante variación en cómo se pueden especificar las sentencias `export`. Por ejemplo:

```js
export function getName(studentID) {
    // ..
}
```

Aunque `export` aparece antes de la palabra clave `function` aquí, esta forma sigue siendo una declaración de `function` que además resulta ser exportada. Es decir, el identificador `getName` tiene *function hoisting* (ver Capítulo 5), por lo que está disponible a lo largo de todo el scope del módulo.

Otra variación permitida:

```js
export default function getName(studentID) {
    // ..
}
```

Este es un llamado "default export", que tiene una semántica diferente de otros exports. En esencia, un "default export" es un atajo para los consumidores del módulo cuando hacen `import`, dándoles una sintaxis más breve cuando solo necesitan este único miembro de API por defecto.

Los exports que no son `default` se conocen como "named exports".

La palabra clave `import` —al igual que `export`, debe usarse solo en el nivel superior de un ESM fuera de cualquier bloque o función— también tiene varias variaciones en su sintaxis. La primera se conoce como "named import":

```js
import { getName } from "/path/to/students.js";

getName(73);   // Suzy
```

Como podés ver, esta forma importa solo los miembros de la API pública nombrados específicamente de un módulo (omitiendo cualquier cosa no nombrada explícitamente), y agrega esos identificadores al scope de nivel superior del módulo actual. Este tipo de import es un estilo familiar para quienes están acostumbrados a los imports de paquetes en lenguajes como Java.

Se pueden listar múltiples miembros de la API dentro del conjunto `{ .. }`, separados por comas. Un named import también puede ser *renombrado* con la palabra clave `as`:

```js
import { getName as getStudentName }
   from "/path/to/students.js";

getStudentName(73);
// Suzy
```

Si `getName` es un "default export" del módulo, podemos importarlo así:

```js
import getName from "/path/to/students.js";

getName(73);   // Suzy
```

La única diferencia aquí es quitar los `{ }` alrededor del binding de import. Si querés mezclar un default import con otros named imports:

```js
import { default as getName, /* .. others .. */ }
   from "/path/to/students.js";

getName(73);   // Suzy
```

En contraste, la otra variación mayor de `import` se llama "namespace import":

```js
import * as Student from "/path/to/students.js";

Student.getName(73);   // Suzy
```

Como probablemente sea obvio, el `*` importa todo lo exportado a la API, default y named, y lo almacena todo bajo el único identificador de namespace especificado. Este enfoque es el que más se acerca a la forma de los módulos clásicos durante la mayor parte de la historia de JS.

| NOTA: |
| :--- |
| Al momento de escribir esto, los navegadores modernos han soportado ESM durante algunos años ya, pero el soporte más o menos estable de Node para ESM es bastante reciente, y ha estado evolucionando durante bastante tiempo. Es probable que la evolución continúe durante un año o más; la introducción de ESM a JS allá en ES6 creó varias preocupaciones de compatibilidad desafiantes para la interoperabilidad de Node con los módulos CommonJS. Consultá la documentación de ESM de Node para todos los detalles más recientes: https://nodejs.org/api/esm.html |

## Saliendo del Scope

Ya sea que uses el formato de módulo clásico (navegador o Node), el formato CommonJS (en Node), o el formato ESM (navegador o Node), los módulos son una de las formas más efectivas de estructurar y organizar la funcionalidad y los datos de tu programa.

El patrón módulo es la conclusión de nuestro viaje en este libro de aprender cómo podemos usar las reglas del scope léxico para colocar variables y funciones en ubicaciones apropiadas. POLE es la postura defensiva de *privado por defecto* que siempre adoptamos, asegurándonos de evitar la sobreexposición e interactuar solo con la mínima superficie de API pública necesaria.

Y debajo de los módulos, la *magia* de cómo se mantiene todo el estado de nuestro módulo son los closures aprovechando el sistema de scope léxico.

Eso es todo para el texto principal. ¡Felicitaciones por tremendo viaje hasta aquí! Como he dicho numerosas veces a lo largo del libro, es una muy buena idea pausar, reflexionar y practicar lo que acabamos de discutir.

Cuando te sientas cómodo y listo, revisá los apéndices, que profundizan en algunos de los rincones de estos temas, y también te desafían con algunos ejercicios de práctica para solidificar lo que has aprendido.
