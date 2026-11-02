# You Don't Know JS Yet: Get Started - 2nd Edition
# Capítulo 4: El panorama general

Este libro repasa aquello de lo que necesitás estar al tanto a medida que *empezás* con JS. El objetivo es llenar los vacíos con los que los lectores más nuevos en JS podrían haber tropezado en sus primeros encuentros con el lenguaje. También espero que a lo largo del libro hayamos insinuado suficiente detalle profundo como para despertar tu curiosidad y que quieras indagar más en el lenguaje.

El resto de los libros de esta serie es donde vamos a desglosar todo lo que queda del lenguaje, con muchísimo más detalle del que podríamos haber abarcado en unos pocos capítulos breves acá.

Pero acordate de tomarte tu tiempo. En lugar de lanzarte apresuradamente al siguiente libro en un intento de atravesar todos los libros con rapidez, dedicá algo de tiempo a repasar el material de este libro. Dedicá algo más de tiempo a revisar el código de tus proyectos actuales, y a comparar lo que ves con lo que se discutió hasta ahora.

Cuando estés listo, este capítulo final divide la organización del lenguaje JS en tres pilares principales, luego ofrece una breve hoja de ruta de qué esperar del resto de la serie de libros, y cómo te sugiero que procedas. Además, no te saltees los apéndices, especialmente el Apéndice B, "¡Práctica, práctica, práctica!".

## Pilar 1: Scope y Closure

La organización de las variables en unidades de scope (funciones, bloques) es una de las características más fundamentales de cualquier lenguaje; quizás ninguna otra característica tenga un impacto mayor en cómo se comportan los programas.

Los scopes son como baldes, y las variables son como las bolitas que ponés dentro de esos baldes. El modelo de scope de un lenguaje es como las reglas que te ayudan a determinar qué bolitas de qué color van en qué baldes del color que coincide.

Los scopes se anidan unos dentro de otros, y para cualquier expression o statement dado, solo las variables en ese nivel de anidamiento de scope, o en scopes superiores/externos, son accesibles; las variables de scopes inferiores/internos están ocultas y son inaccesibles.

Así es como se comportan los scopes en la mayoría de los lenguajes, lo que se denomina lexical scope. Los límites de la unidad de scope, y cómo se organizan las variables en ellos, se determinan en el momento en que el programa es parseado (compilado). En otras palabras, es una decisión en tiempo de autoría: dónde ubicás una función/scope en el programa determina cuál será la estructura de scope de esa parte del programa.

JS tiene lexical scope, aunque muchos afirman que no, debido a dos características particulares de su modelo que no están presentes en otros lenguajes con lexical scope.

La primera se llama comúnmente *hoisting*: cuando todas las variables declaradas en cualquier parte de un scope se tratan como si estuvieran declaradas al comienzo del scope. La otra es que las variables declaradas con `var` tienen function scope, incluso si aparecen dentro de un bloque.

Ni el hoisting ni el `var` con function scope son suficientes para respaldar la afirmación de que JS no tiene lexical scope. Las declaraciones `let`/`const` tienen un comportamiento de error peculiar llamado la "Temporal Dead Zone" (TDZ) que da como resultado variables observables pero inutilizables. Aunque encontrarse con la TDZ puede resultar extraño, *tampoco* es una invalidación del lexical scoping. Todas estas son simplemente partes únicas del lenguaje que todos los desarrolladores de JS deberían aprender y comprender.

El closure es un resultado natural del lexical scope cuando el lenguaje tiene funciones como valores de primera clase, como ocurre con JS. Cuando una función hace referencia a variables de un scope externo, y esa función se pasa de un lado a otro como un valor y se ejecuta en otros scopes, mantiene el acceso a las variables de su scope original; esto es el closure.

A lo largo de toda la programación, pero especialmente en JS, el closure impulsa muchos de los patrones de programación más importantes, incluidos los módulos. Tal como lo veo, los módulos son lo más *a favor de la veta* que podés llegar a estar, en lo que respecta a la organización del código en JS.

Para profundizar en el scope, los closures, y cómo funcionan los módulos, leé el Libro 2, *Scope & Closures*.

## Pilar 2: Prototypes

El segundo pilar del lenguaje es el sistema de prototypes. Cubrimos este tema en profundidad en el Capítulo 3 ("Prototypes"), pero solo quiero hacer algunos comentarios más sobre su importancia.

JS es uno de los muy pocos lenguajes en los que tenés la opción de crear objetos directa y explícitamente, sin definir primero su estructura en una clase.

Durante muchos años, la gente implementó el patrón de diseño de clases sobre los prototypes —la llamada "herencia prototipal" (ver Apéndice A, "'Clases' prototipales")— y luego, con la llegada de la palabra clave `class` de ES6, el lenguaje redobló la apuesta por su inclinación hacia la programación al estilo OO/clases.

Pero creo que ese enfoque ha opacado la belleza y el poder del sistema de prototypes: la capacidad de que dos objetos simplemente se conecten entre sí y cooperen dinámicamente (durante la ejecución de una función/método) a través de compartir un contexto `this`.

Las clases son solo uno de los patrones que podés construir sobre ese poder. Pero otro enfoque, en una dirección muy diferente, es simplemente abrazar los objetos como objetos, olvidarse por completo de las clases, y dejar que los objetos cooperen a través de la prototype chain. Esto se llama *delegación de comportamiento*. Creo que la delegación es más poderosa que la herencia de clases, como medio para organizar el comportamiento y los datos en nuestros programas.

Pero la herencia de clases se lleva casi toda la atención. Y el resto se va a la programación funcional (FP), como una especie de forma "anticlase" de diseñar programas. Esto me entristece, porque sofoca cualquier posibilidad de explorar la delegación como una alternativa viable.

Te animo a que dediques bastante tiempo a sumergirte en el Libro 3, *Objects & Classes*, para ver cómo la delegación de objetos encierra mucho más potencial del que quizás hayamos reconocido. Este no es un mensaje anti-`class`, pero sí es intencionalmente un mensaje de "las clases no son la única forma de usar objetos" que quiero que más desarrolladores de JS consideren.

La delegación de objetos es, yo argumentaría, mucho más *a favor de la veta* de JS que las clases (más sobre las *vetas* en un rato).

## Pilar 3: Tipos y Coerción

El tercer pilar de JS es, por lejos, la parte más ignorada de la naturaleza de JS.

La gran mayoría de los desarrolladores tiene fuertes ideas equivocadas sobre cómo funcionan los *tipos* en los lenguajes de programación, y especialmente sobre cómo funcionan en JS. Una ola de interés en la comunidad más amplia de JS ha comenzado a inclinarse hacia enfoques de "tipado estático", usando herramientas con conciencia de tipos como TypeScript o Flow.

Estoy de acuerdo en que los desarrolladores de JS deberían aprender más sobre los tipos, y deberían aprender más sobre cómo JS maneja las conversiones de tipos. También estoy de acuerdo en que las herramientas con conciencia de tipos pueden ayudar a los desarrolladores, ¡asumiendo que primero hayan adquirido y usado este conocimiento!

Pero no estoy en absoluto de acuerdo con que la conclusión inevitable de esto sea decidir que el mecanismo de tipos de JS es malo y que necesitamos encubrir los tipos de JS con soluciones externas al lenguaje. No tenemos que seguir el camino del "tipado estático" para ser inteligentes y sólidos con los tipos en nuestros programas. Hay otras opciones, si estás dispuesto a ir *en contra de la veta* de la multitud, y *a favor de la veta* de JS (de nuevo, más sobre eso está por venir).

Se podría argumentar que este pilar es más importante que los otros dos, en el sentido de que ningún programa de JS hará nada útil si no aprovecha correctamente los tipos de valor de JS, así como la conversión (coerción) de valores entre tipos.

Incluso si amás TypeScript/Flow, no vas a sacarles el máximo provecho a esas herramientas o enfoques de codificación si no estás profundamente familiarizado con cómo el lenguaje en sí maneja los tipos de valor.

Para aprender más sobre los tipos y la coerción de JS, mirá el Libro 4, *Types & Grammar*. Pero por favor no te saltees este tema solo porque siempre escuchaste que deberíamos usar `===` y olvidarnos de todo lo demás.

Sin aprender este pilar, tu base en JS es, en el mejor de los casos, inestable e incompleta.

## A favor de la veta

Tengo algún consejo para compartir sobre cómo continuar tu camino de aprendizaje con JS, y tu recorrido a través del resto de esta serie de libros: estate atento a la *veta* (recordá las diversas referencias a la *veta* más temprano en este capítulo).

Primero, considerá la *veta* (como en la madera) de cómo la mayoría de la gente aborda y usa JS. Probablemente ya hayas notado que estos libros van en contra de esa *veta* en muchos aspectos. En YDKJSY, te respeto a vos, el lector, lo suficiente como para explicarte todas las partes de JS, no solo algunas partes populares seleccionadas. Creo que sos capaz de ese conocimiento y que lo merecés.

Pero eso no es lo que vas a encontrar en gran parte del resto del material que hay por ahí. También significa que cuanto más sigas y te adhieras a la orientación de estos libros —que pienses cuidadosamente y analices por vos mismo qué es lo mejor para tu código— más vas a destacar. Eso puede ser algo bueno y malo. Si alguna vez querés diferenciarte de la multitud, ¡vas a tener que romper con la forma en que la multitud lo hace!

Pero también mucha gente me ha dicho que citó algún tema/explicación de estos libros durante una entrevista de trabajo, y el entrevistador le dijo al candidato que estaba equivocado; de hecho, según se reporta, hay gente que ha perdido ofertas de trabajo como resultado.

En la medida de lo posible, me esfuerzo en estos libros por brindar información completamente precisa sobre JS, informada en general a partir de la propia especificación. Pero también dosifico bastante de mis opiniones sobre cómo podés interpretar y usar JS para el mejor beneficio en tus programas. No presento opinión como hecho, ni viceversa. Siempre vas a saber cuál es cuál en estos libros.

Los hechos sobre JS no están realmente sujetos a debate. O bien la especificación dice algo, o no lo dice. Si no te gusta lo que dice la especificación, o mi forma de transmitirlo, ¡reclamáselo a TC39! Si estás en una entrevista y afirman que estás equivocado respecto de los hechos, preguntales ahí mismo si podés buscarlo en la especificación. Si el entrevistador no quiere reconsiderarlo, entonces de todos modos no deberías querer trabajar ahí.

Pero si elegís alinearte con mis opiniones, tenés que estar preparado para respaldar esas elecciones con el *porqué* sentís de esa manera. No te limites a repetir como un loro lo que digo. Adueñate de tus opiniones. Defendelas. Y si alguien con quien esperabas trabajar no está de acuerdo, retirate con la cabeza todavía en alto. Es un gran JS, y hay mucho espacio para un montón de formas diferentes.

En otras palabras, no tengas miedo de ir en contra de la *veta*, como lo he hecho yo con estos libros y con todas mis enseñanzas. Nadie puede decirte cómo vas a aprovechar mejor JS; eso te toca decidirlo a vos. Yo simplemente intento empoderarte para que llegues a tus propias conclusiones, cualesquiera que sean.

Por otro lado, hay una *veta* a la que realmente deberías prestarle atención y seguir: la *veta* de cómo funciona JS, a nivel del lenguaje. Hay cosas que funcionan bien y de forma natural en JS, dada la práctica y el enfoque correctos, y hay cosas que realmente no deberías intentar hacer en el lenguaje.

¿Podés hacer que tu programa de JS se vea como un programa de Java, C# o Perl? ¿Qué tal como Python o Ruby, o incluso PHP? En distintos grados, claro que podés. ¿Pero deberías?

No, no creo que debas. Creo que deberías aprender y abrazar la forma de JS, y hacer que tus programas de JS sean tan "JS-eros" como sea práctico. Algunos pensarán que eso significa una programación descuidada e informal, pero no quiero decir eso en absoluto. Solo quiero decir que JS tiene un montón de patrones e idiomas que son reconociblemente "JS", y ir a favor de esa *veta* es el camino general hacia el mejor éxito.

Finalmente, quizás la *veta* más importante que reconocer es cómo hacen las cosas el o los programas existentes en los que estás trabajando, y los desarrolladores con los que trabajás. No leas estos libros y luego intentes cambiar *toda esa veta* en tus proyectos existentes de la noche a la mañana. Ese enfoque siempre va a fracasar.

Vas a tener que ir modificando estas cosas de a poco, con el tiempo. Trabajá en construir consenso con tus compañeros desarrolladores sobre por qué es importante revisar y reconsiderar un enfoque. Pero hacelo con un solo tema pequeño a la vez, y dejá que las comparaciones de código de antes y después hagan la mayor parte del trabajo. Reuní a todo el equipo para discutir, e impulsá decisiones que se basen en el análisis y la evidencia del código, en lugar de en la inercia de "nuestros desarrolladores senior siempre lo hicieron de esta manera".

Ese es el consejo más importante que puedo transmitirte para ayudarte a aprender JS. Seguí siempre buscando mejores formas de usar lo que JS nos da para escribir código más legible. ¡Todos los que trabajen en tu código, incluido tu yo futuro, te lo van a agradecer!

## En orden

Así que ahora tenés una perspectiva más amplia de lo que queda por explorar en JS, y la actitud correcta para abordar el resto de tu camino.

Pero una de las preguntas prácticas más comunes que recibo en este punto es: "¿En qué orden debería leer los libros?". Hay una respuesta directa... pero también depende.

Mi sugerencia para la mayoría de los lectores es avanzar por esta serie en este orden:

1. Arrancá con una base sólida de JS con *Get Started* (Libro 1) -- buenas noticias, ¡ya casi terminaste este libro!

2. En *Scope & Closures* (Libro 2), indagá en el primer pilar de JS: lexical scope, cómo eso sustenta el closure, y cómo el patrón de módulos organiza el código.

3. En *Objects & Classes* (Libro 3), enfocate en el segundo pilar de JS: cómo funciona el `this` de JS, cómo los prototypes de objetos sustentan la delegación, y cómo los prototypes habilitan el mecanismo `class` para la organización del código al estilo OO.

4. En *Types & Grammar* (Libro 4), abordá el tercer y último pilar de JS: los tipos y la coerción de tipos, así como la forma en que la sintaxis y la gramática de JS definen cómo escribimos nuestro código.

5. Con los **tres pilares** sólidamente en su lugar, *Sync & Async* (Libro 5) explora luego cómo usamos el control de flujo para modelar el cambio de estado en nuestros programas, tanto de forma síncrona (de inmediato) como asíncrona (a lo largo del tiempo).

6. La serie concluye con *ES.Next & Beyond* (Libro 6), una mirada hacia adelante al futuro cercano y a mediano plazo de JS, incluida una variedad de características que probablemente lleguen a tus programas de JS dentro de no mucho tiempo.

Ese es el orden previsto para leer esta serie de libros.

Sin embargo, los Libros 2, 3 y 4 generalmente pueden leerse en cualquier orden, dependiendo de qué tema sientas más curiosidad y comodidad por explorar primero. Pero no te recomiendo que te saltees ninguno de estos tres libros —ni siquiera *Types & Grammar*, ¡como algunos de ustedes estarán tentados de hacer!— incluso si creés que ya tenés ese tema dominado.

El Libro 5 (*Sync & Async*) es crucial para entender JS en profundidad, pero si empezás a meterte y te resulta demasiado intimidante, este libro puede posponerse hasta que tengas más experiencia con el lenguaje. Cuanto más JS hayas escrito (¡y con cuánto más hayas batallado!), más vas a llegar a apreciar este libro. Así que no tengas miedo de volver a él más adelante.

El último libro de la serie, *ES.Next & Beyond*, en algunos aspectos se sostiene por sí solo. Puede leerse al final, como sugiero, o justo después de *Get Started* si estás buscando un atajo para ampliar tu radar sobre de qué se trata JS. Este libro también será más propenso a recibir actualizaciones en el futuro, así que probablemente quieras volver a visitarlo de vez en cuando.

Sin importar cómo elijas avanzar con YDKJSY, mirá primero los apéndices de este libro, especialmente practicando los fragmentos del Apéndice B, "¡Práctica, práctica, práctica!". ¿Mencioné que deberías ir a practicar? No hay mejor manera de aprender a programar que escribiendo código.
