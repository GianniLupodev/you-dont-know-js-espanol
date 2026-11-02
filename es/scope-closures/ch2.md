# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Capítulo 2: Ilustrando el Lexical Scope

En el Capítulo 1, exploramos cómo se determina el scope durante la compilación del código, un modelo llamado "lexical scope". El término "lexical" hace referencia a la primera etapa de la compilación (lexing/parsing).

Para *razonar* correctamente sobre nuestros programas, es importante tener una base conceptual sólida de cómo funciona el scope. Si nos apoyamos en conjeturas e intuición, puede que accidentalmente obtengamos las respuestas correctas algunas veces, pero muchas otras veces estaremos muy lejos. Esta no es una receta para el éxito.

Como allá en las clases de matemática de la primaria, ¡obtener la respuesta correcta no es suficiente si no mostramos los pasos correctos para llegar a ella! Necesitamos construir modelos mentales precisos y útiles como base para avanzar.

Este capítulo ilustrará el *scope* con varias metáforas. El objetivo acá es *pensar* en cómo tu programa es manejado por el engine de JS de maneras que se alineen más de cerca con cómo funciona realmente el engine de JS.

## Canicas, y Baldes, y Burbujas... ¡Dios Mío!

Una metáfora que me ha resultado efectiva para entender el scope es clasificar canicas de colores en baldes de su color correspondiente.

Imaginá que te encontrás con una pila de canicas y notás que todas las canicas son de color rojo, azul o verde. Clasifiquemos todas las canicas, dejando caer las rojas en un balde rojo, las verdes en un balde verde y las azules en un balde azul. Después de clasificarlas, cuando más tarde necesites una canica verde, ya sabés que el balde verde es el lugar al que ir para conseguirla.

En esta metáfora, las canicas son las variables de nuestro programa. Los baldes son los scopes (funciones y bloques), a los que conceptualmente les asignamos colores individuales para los fines de nuestra discusión. El color de cada canica está determinado por el *color* del scope en el que encontramos que la canica fue creada originalmente.

Anotemos el ejemplo del programa en ejecución del Capítulo 1 con etiquetas de color de scope:

```js
// outer/global scope: RED

var students = [
    { id: 14, name: "Kyle" },
    { id: 73, name: "Suzy" },
    { id: 112, name: "Frank" },
    { id: 6, name: "Sarah" }
];

function getStudentName(studentID) {
    // function scope: BLUE

    for (let student of students) {
        // loop scope: GREEN

        if (student.id == studentID) {
            return student.name;
        }
    }
}

var nextStudent = getStudentName(73);
console.log(nextStudent);   // Suzy
```

Hemos designado tres colores de scope con comentarios en el código: RED (el scope global más externo), BLUE (el scope de la función `getStudentName(..)`) y GREEN (el scope dentro del bucle `for`). Pero aún así puede ser difícil reconocer los límites de estos baldes de scope al mirar un listado de código.

La Figura 2 ayuda a visualizar los límites de los scopes dibujando burbujas de colores (es decir, baldes) alrededor de cada uno:

<figure>
    <img src="images/fig2.png" width="500" alt="Colored Scope Bubbles" align="center">
    <figcaption><em>Fig. 2: Colored Scope Bubbles</em></figcaption>
</figure>

1. La **Burbuja 1** (RED) abarca el scope global, que contiene tres identificadores/variables: `students` (línea 1), `getStudentName` (línea 8) y `nextStudent` (línea 16).

2. La **Burbuja 2** (BLUE) abarca el scope de la función `getStudentName(..)` (línea 8), que contiene solo un identificador/variable: el parámetro `studentID` (línea 8).

3. La **Burbuja 3** (GREEN) abarca el scope del bucle `for` (línea 9), que contiene solo un identificador/variable: `student` (línea 9).

| NOTA: |
| :--- |
| Técnicamente, el parámetro `studentID` no está exactamente en el scope BLUE(2). Desenredaremos esa confusión en "Implied Scopes" en el Apéndice A. Por ahora, es suficientemente cercano etiquetar a `studentID` como una canica BLUE(2). |

Las burbujas de scope se determinan durante la compilación en función de dónde se escriben las funciones/bloques de scope, el anidamiento unos dentro de otros, etcétera. Cada burbuja de scope está completamente contenida dentro de su burbuja de scope padre—un scope nunca está parcialmente en dos scopes externos diferentes.

Cada canica (variable/identificador) se colorea según la burbuja (balde) en la que se declara, no según el color del scope desde el que se puede acceder a ella (por ejemplo, `students` en la línea 9 y `studentID` en la línea 10).

| NOTA: |
| :--- |
| Recordá que afirmamos en el Capítulo 1 que `id`, `name` y `log` son todas propiedades, no variables; en otras palabras, no son canicas en baldes, así que no se colorean según ninguna de las reglas que estamos discutiendo en este libro. Para entender cómo se manejan tales accesos a propiedades, consultá el tercer libro de la serie, *Objects & Classes*. |

A medida que el engine de JS procesa un programa (durante la compilación) y encuentra una declaración de una variable, esencialmente se pregunta: "¿En qué scope de qué *color* (burbuja o balde) estoy actualmente?" La variable se designa con ese mismo *color*, lo que significa que pertenece a ese balde/burbuja.

El balde GREEN(3) está totalmente anidado dentro del balde BLUE(2), y de manera similar el balde BLUE(2) está totalmente anidado dentro del balde RED(1). Los scopes pueden anidarse unos dentro de otros como se muestra, a cualquier profundidad de anidamiento que tu programa necesite.

Las referencias (no declaraciones) a variables/identificadores están permitidas si hay una declaración coincidente ya sea en el scope actual, o en cualquier scope por encima/fuera del scope actual, pero no con declaraciones de scopes inferiores/anidados.

Una expression en el balde RED(1) solo tiene acceso a las canicas RED(1), **no** a las BLUE(2) o GREEN(3). Una expression en el balde BLUE(2) puede referenciar canicas BLUE(2) o RED(1), **no** GREEN(3). Y una expression en el balde GREEN(3) tiene acceso a las canicas RED(1), BLUE(2) y GREEN(3).

Podemos conceptualizar el proceso de determinar estos colores de canicas que no son declaraciones durante el runtime como una búsqueda. Como la referencia a la variable `students` en el statement del bucle `for` en la línea 9 no es una declaración, no tiene color. Entonces le preguntamos al balde del scope BLUE(2) actual si tiene una canica que coincida con ese nombre. Como no la tiene, la búsqueda continúa con el siguiente scope externo/contenedor: RED(1). El balde RED(1) tiene una canica con el nombre `students`, así que se determina que la referencia a la variable `students` del statement del bucle es una canica RED(1).

El statement `if (student.id == studentID)` en la línea 10 se determina de manera similar que referencia una canica GREEN(3) llamada `student` y una canica BLUE(2) llamada `studentID`.

| NOTA: |
| :--- |
| El engine de JS generalmente no determina estos colores de canicas durante el runtime; la "búsqueda" acá es un recurso retórico para ayudarte a entender los conceptos. Durante la compilación, la mayoría o todas las referencias a variables coincidirán con baldes de scope ya conocidos, así que su color ya está determinado y almacenado con cada referencia de canica para evitar búsquedas innecesarias mientras el programa se ejecuta. Más sobre este matiz en el Capítulo 3. |

Las conclusiones clave de las canicas y los baldes (¡y las burbujas!):

* Las variables se declaran en scopes específicos, que pueden pensarse como canicas de colores de baldes del color correspondiente.

* Cualquier referencia a una variable que aparezca en el scope donde fue declarada, o que aparezca en cualquier scope anidado más profundo, será etiquetada como una canica de ese mismo color—a menos que un scope intermedio "sombree" (shadow) la declaración de la variable; consultá "Shadowing" en el Capítulo 3.

* La determinación de los baldes de colores, y de las canicas que contienen, ocurre durante la compilación. Esta información se usa para las "búsquedas" de variables (color de canica) durante la ejecución del código.

## Una Conversación Entre Amigos

Otra metáfora útil para el proceso de analizar variables y los scopes de los que provienen es imaginar varias conversaciones que ocurren dentro del engine a medida que el código se procesa y luego se ejecuta. Podemos "escuchar" estas conversaciones para obtener una mejor base conceptual de cómo funcionan los scopes.

Conozcamos ahora a los miembros del engine de JS que tendrán conversaciones a medida que procesan nuestro programa:

* *Engine*: responsable de la compilación y ejecución de principio a fin de nuestro programa JavaScript.

* *Compiler*: uno de los amigos de *Engine*; maneja todo el trabajo sucio de parsear y generar código (ver la sección anterior).

* *Scope Manager*: otro amigo de *Engine*; recopila y mantiene una lista de búsqueda de todas las variables/identificadores declarados, y hace cumplir un conjunto de reglas sobre cómo estos son accesibles para el código que se está ejecutando actualmente.

Para que *entiendas completamente* cómo funciona JavaScript, necesitás empezar a *pensar* como piensa *Engine* (y sus amigos), hacer las preguntas que ellos hacen y responder sus preguntas de la misma manera.

Para explorar estas conversaciones, recordemos una vez más nuestro ejemplo del programa en ejecución:

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

Examinemos cómo JS va a procesar ese programa, específicamente empezando con el primer statement. El array y su contenido son solo valores literales básicos de JS (y por lo tanto no se ven afectados por ninguna cuestión de scoping), así que nuestro foco acá estará en las partes de declaración `var students = [ .. ]` y de inicialización-asignación.

Típicamente pensamos en eso como un solo statement, pero no es así como lo ve nuestro amigo *Engine*. De hecho, JS trata esto como dos operaciones distintas, una que *Compiler* manejará durante la compilación, y la otra que *Engine* manejará durante la ejecución.

Lo primero que *Compiler* hará con este programa es realizar el lexing para descomponerlo en tokens, que luego parseará en un árbol (AST).

Una vez que *Compiler* llega a la generación de código, hay más detalles que considerar de lo que podría ser obvio. Una suposición razonable sería que *Compiler* producirá código para el primer statement como: "Asignar memoria para una variable, etiquetarla `students`, y luego colocar una referencia al array en esa variable." Pero esa no es toda la historia.

Estos son los pasos que *Compiler* seguirá para manejar ese statement:

1. Al encontrar `var students`, *Compiler* le preguntará a *Scope Manager* para ver si ya existe una variable llamada `students` para ese balde de scope en particular. Si es así, *Compiler* ignoraría esta declaración y seguiría adelante. De lo contrario, *Compiler* producirá código que (en tiempo de ejecución) le pide a *Scope Manager* que cree una nueva variable llamada `students` en ese balde de scope.

2. *Compiler* luego produce código para que *Engine* lo ejecute más tarde, para manejar la asignación `students = []`. El código que *Engine* ejecuta primero le preguntará a *Scope Manager* si hay una variable llamada `students` accesible en el balde de scope actual. Si no, *Engine* sigue buscando en otro lado (ver "Nested Scope" más abajo). Una vez que *Engine* encuentra una variable, le asigna la referencia del array `[ .. ]`.

En forma conversacional, la primera fase de la compilación del programa podría desarrollarse entre *Compiler* y *Scope Manager* así:

> ***Compiler***: Hola, *Scope Manager* (del scope global), encontré una declaración formal de un identificador llamado `students`, ¿alguna vez escuchaste de él?

> ***(Global) Scope Manager***: No, nunca escuché de él, así que lo acabo de crear para vos.

> ***Compiler***: Hola, *Scope Manager*, encontré una declaración formal de un identificador llamado `getStudentName`, ¿alguna vez escuchaste de él?

> ***(Global) Scope Manager***: No, pero lo acabo de crear para vos.

> ***Compiler***: Hola, *Scope Manager*, `getStudentName` apunta a una función, así que necesitamos un nuevo balde de scope.

> ***(Function) Scope Manager***: Entendido, acá está el balde de scope.

> ***Compiler***: Hola, *Scope Manager* (de la función), encontré una declaración de parámetro formal para `studentID`, ¿alguna vez escuchaste de él?

> ***(Function) Scope Manager***: No, pero ahora está creado en este scope.

> ***Compiler***: Hola, *Scope Manager* (de la función), encontré un bucle `for` que necesitará su propio balde de scope.

> ...

La conversación es un intercambio de preguntas y respuestas, donde **Compiler** le pregunta al *Scope Manager* actual si una declaración de identificador que encontró ya fue encontrada antes. Si la respuesta es "no", *Scope Manager* crea esa variable en ese scope. Si la respuesta es "sí", entonces efectivamente se la saltea ya que no hay nada más que hacer para ese *Scope Manager*.

*Compiler* también avisa cuando se topa con funciones o bloques de scope, para que puedan instanciarse un nuevo balde de scope y un *Scope Manager*.

Más tarde, cuando llegue la ejecución del programa, la conversación cambiará a *Engine* y *Scope Manager*, y podría desarrollarse así:

> ***Engine***: Hola, *Scope Manager* (del scope global), antes de empezar, ¿podés buscar el identificador `getStudentName` para que pueda asignarle esta función?

> ***(Global) Scope Manager***: Sí, acá está la variable.

> ***Engine***: Hola, *Scope Manager*, encontré una referencia *target* para `students`, ¿alguna vez escuchaste de ella?

> ***(Global) Scope Manager***: Sí, fue declarada formalmente para este scope, así que acá está.

> ***Engine***: Gracias, estoy inicializando `students` a `undefined`, así que está lista para usar.

> Hola, *Scope Manager* (del scope global), encontré una referencia *target* para `nextStudent`, ¿alguna vez escuchaste de ella?

> ***(Global) Scope Manager***: Sí, fue declarada formalmente para este scope, así que acá está.

> ***Engine***: Gracias, estoy inicializando `nextStudent` a `undefined`, así que está lista para usar.

> Hola, *Scope Manager* (del scope global), encontré una referencia *source* para `getStudentName`, ¿alguna vez escuchaste de ella?

> ***(Global) Scope Manager***: Sí, fue declarada formalmente para este scope. Acá está.

> ***Engine***: Genial, el valor en `getStudentName` es una función, así que voy a ejecutarla.

> ***Engine***: Hola, *Scope Manager*, ahora necesitamos instanciar el scope de la función.

> ...

Esta conversación es otro intercambio de preguntas y respuestas, donde *Engine* primero le pide al *Scope Manager* actual que busque el identificador `getStudentName` hoisteado, para poder asociar la función con él. *Engine* luego procede a preguntarle a *Scope Manager* sobre la referencia *target* para `students`, y así sucesivamente.

Para repasar y resumir cómo se procesa un statement como `var students = [ .. ]`, en dos pasos distintos:

1. *Compiler* configura la declaración de la variable del scope (ya que no fue declarada previamente en el scope actual).

2. Mientras *Engine* se está ejecutando, para procesar la parte de asignación del statement, *Engine* le pide a *Scope Manager* que busque la variable, la inicializa a `undefined` para que esté lista para usar, y luego le asigna el valor del array.

## Nested Scope

Cuando llega el momento de ejecutar la función `getStudentName()`, *Engine* pide una instancia de *Scope Manager* para el scope de esa función, y luego procederá a buscar el parámetro (`studentID`) al que asignarle el valor del argumento `73`, y así sucesivamente.

El scope de la función `getStudentName(..)` está anidado dentro del scope global. El scope de bloque del bucle `for` está de manera similar anidado dentro de ese scope de función. Los scopes pueden anidarse léxicamente a cualquier profundidad arbitraria que defina el programa.

Cada scope obtiene su propia instancia de *Scope Manager* cada vez que ese scope se ejecuta (una o más veces). Cada scope tiene automáticamente todos sus identificadores registrados al inicio de la ejecución del scope (esto se llama "variable hoisting"; ver Capítulo 5).

Al comienzo de un scope, si algún identificador provino de una declaración `function`, esa variable se inicializa automáticamente a su referencia de función asociada. Y si algún identificador provino de una declaración `var` (a diferencia de `let`/`const`), esa variable se inicializa automáticamente a `undefined` para que pueda usarse; de lo contrario, la variable permanece sin inicializar (es decir, en su "TDZ", ver Capítulo 5) y no puede usarse hasta que se ejecuten su declaración e inicialización completas.

En el statement `for (let student of students) {`, `students` es una referencia *source* que debe buscarse. Pero ¿cómo se manejará esa búsqueda, ya que el scope de la función no encontrará tal identificador?

Para explicarlo, imaginemos que ese fragmento de conversación se desarrolla así:

> ***Engine***: Hola, *Scope Manager* (de la función), tengo una referencia *source* para `students`, ¿alguna vez escuchaste de ella?

> ***(Function) Scope Manager***: No, nunca escuché de ella. Probá con el siguiente scope externo.

> ***Engine***: Hola, *Scope Manager* (del scope global), tengo una referencia *source* para `students`, ¿alguna vez escuchaste de ella?

> ***(Global) Scope Manager***: Sí, fue declarada formalmente, acá está.

> ...

Uno de los aspectos clave del lexical scope es que cada vez que una referencia de identificador no puede encontrarse en el scope actual, se consulta el siguiente scope externo en el anidamiento; ese proceso se repite hasta que se encuentra una respuesta o no hay más scopes para consultar.

### Fallas de Búsqueda

Cuando *Engine* agota todos los scopes *léxicamente disponibles* (moviéndose hacia afuera) y aún no puede resolver la búsqueda de un identificador, entonces existe una condición de error. Sin embargo, dependiendo del modo del programa (strict-mode o no) y del rol de la variable (es decir, *target* vs. *source*; ver Capítulo 1), esta condición de error se manejará de manera diferente.

#### El Lío de Undefined

Si la variable es una *source*, una búsqueda de identificador no resuelta se considera una variable no declarada (desconocida, faltante), lo que siempre resulta en que se lance un `ReferenceError`. Además, si la variable es una *target*, y el código en ese momento se está ejecutando en strict-mode, la variable se considera no declarada y de manera similar lanza un `ReferenceError`.

El mensaje de error para una condición de variable no declarada, en la mayoría de los entornos de JS, se verá como "Reference Error: XYZ is not defined." La frase "not defined" parece casi idéntica a la palabra "undefined", en lo que respecta al idioma inglés. Pero estas dos son muy diferentes en JS, y este mensaje de error lamentablemente genera una confusión persistente.

"Not defined" realmente significa "not declared"—o, más bien, "undeclared", como en una variable que no tiene ninguna declaración formal coincidente en ningún scope *léxicamente disponible*. En cambio, "undefined" realmente significa que se encontró una variable (declarada), pero la variable por lo demás no tiene ningún otro valor en ese momento, así que toma por defecto el valor `undefined`.

Para perpetuar la confusión aún más, el operador `typeof` de JS devuelve el string `"undefined"` para referencias de variables en cualquiera de los dos estados:

```js
var studentName;
typeof studentName;     // "undefined"

typeof doesntExist;     // "undefined"
```

Estas dos referencias de variables están en condiciones muy diferentes, pero JS sin dudas enturbia las aguas. El lío de terminología es confuso y terriblemente desafortunado. Lamentablemente, los desarrolladores de JS simplemente tienen que prestar mucha atención para no mezclar *qué tipo* de "undefined" están manejando!

#### Global... ¡¿Qué?!

Si la variable es una *target* y strict-mode no está en efecto, entra en juego un comportamiento heredado confuso y sorprendente. El resultado problemático es que el *Scope Manager* del scope global simplemente creará una **variable global accidental** para cumplir con esa asignación target!

Considerá:

```js
function getStudentName() {
    // assignment to an undeclared variable :(
    nextStudent = "Suzy";
}

getStudentName();

console.log(nextStudent);
// "Suzy" -- oops, an accidental-global variable!
```

Así es como procederá esa *conversación*:

> ***Engine***: Hola, *Scope Manager* (de la función), tengo una referencia *target* para `nextStudent`, ¿alguna vez escuchaste de ella?

> ***(Function) Scope Manager***: No, nunca escuché de ella. Probá con el siguiente scope externo.

> ***Engine***: Hola, *Scope Manager* (del scope global), tengo una referencia *target* para `nextStudent`, ¿alguna vez escuchaste de ella?

> ***(Global) Scope Manager***: No, pero como estamos en non-strict-mode, te di una mano y acabo de crear una variable global para vos, ¡acá está!

Qué asco.

Este tipo de accidente (casi con certeza llevará a bugs eventualmente) es un gran ejemplo de las protecciones beneficiosas que ofrece strict-mode, y de por qué es tan mala idea *no* estar usando strict-mode. En strict-mode, el ***Global Scope Manager*** en cambio habría respondido:

> ***(Global) Scope Manager***: No, nunca escuché de ella. Lo siento, tengo que lanzar un `ReferenceError`.

Asignar a una variable nunca declarada *es* un error, así que está bien que recibamos un `ReferenceError` acá.

Nunca confíes en variables globales accidentales. Usá siempre strict-mode, y declará siempre formalmente tus variables. Entonces obtendrás un útil `ReferenceError` si alguna vez intentás por error asignar a una variable no declarada.

### Construyendo Sobre Metáforas

Para visualizar la resolución de scope anidado, prefiero otra metáfora más, un edificio de oficinas, como en la Figura 3:

<figure>
    <img src="images/fig3.png" width="250" alt="Scope &quot;Building&quot;" align="center">
    <figcaption><em>Fig. 3: Scope "Building"</em></figcaption>
    <br><br>
</figure>

El edificio representa la colección de scopes anidados de nuestro programa. El primer piso del edificio representa el scope que se está ejecutando actualmente. El nivel más alto del edificio es el scope global.

Resolvés una referencia de variable *target* o *source* buscando primero en el piso actual, y si no la encontrás, tomando el ascensor al siguiente piso (es decir, un scope externo), buscando ahí, luego el siguiente, y así sucesivamente. Una vez que llegás al piso más alto (el scope global), o encontrás lo que estás buscando, o no. Pero tenés que parar de todos modos.

## Continuá la Conversación

A esta altura, deberías estar desarrollando modelos mentales más ricos sobre qué es el scope y cómo el engine de JS lo determina y lo usa a partir de tu código.

Antes de *continuar*, andá a buscar algo de código en uno de tus proyectos y recorré estas conversaciones. En serio, hablá en voz alta de verdad. Buscá un amigo y practicá cada rol con él. Si alguno de los dos se encuentra confundido o trabado, dediquen más tiempo a repasar este material.

A medida que nos movemos (hacia arriba) al siguiente capítulo (externo), exploraremos cómo los lexical scopes de un programa están conectados en una cadena.
