# You Don't Know JS Yet: Get Started - 2nd Edition
# Capítulo 1: ¿Qué *Es* JavaScript?

Todavía no conocés JS. Yo tampoco, no del todo al menos. Ninguno lo conoce. Pero todos podemos empezar a conocer mejor a JS.

En este primer capítulo del primer libro de la serie *You Don't Know JS Yet* (YDKJSY), vamos a tomarnos un tiempo para construir una base sobre la cual avanzar. Necesitamos empezar cubriendo una variedad de detalles importantes de contexto, aclarando algunos mitos y conceptos erróneos sobre lo que el lenguaje realmente es (¡y lo que no es!).

Esto es una visión valiosa sobre la identidad y el proceso de cómo JS está organizado y mantenido; todos los desarrolladores de JS deberían entenderlo. Si querés conocer JS, así es como *empezás* a dar los primeros pasos en ese camino.

## Acerca de Este Libro

Pongo énfasis en la palabra camino porque *conocer JS* no es un destino, es una dirección. No importa cuánto tiempo pases con el lenguaje, siempre vas a poder encontrar algo más para aprender y entender un poco mejor. Así que no veas este libro como algo para apurar en busca de un logro rápido. En cambio, la paciencia y la persistencia son lo mejor mientras das estos primeros pasos.

Después de este capítulo de contexto, el resto del libro traza un mapa de alto nivel de lo que vas a encontrar a medida que profundices y estudies JS con los libros de YDKJSY.

En particular, el Capítulo 4 identifica tres pilares principales en torno a los cuales está organizado el lenguaje JS: scope/closures, prototypes/objetos y tipos/coerción. JS es un lenguaje amplio y sofisticado, con muchas características y capacidades. Pero todo JS está fundado sobre estos tres pilares fundamentales.

Tené en cuenta que, aunque este libro se titula "Get Started" (Empezá), **no está pensado como un libro para principiantes o de introducción**. El trabajo principal de este libro es prepararte para estudiar JS en profundidad a lo largo del resto de la serie; está escrito asumiendo que ya tenés familiaridad con JS, con al menos varios meses de experiencia, antes de avanzar en YDKJSY. Así que, para sacarle el máximo provecho a *Get Started*, asegurate de pasar bastante tiempo escribiendo código JS para acumular experiencia.

Incluso si ya escribiste mucho JS antes, este libro no debería leerse por encima ni saltearse; tomate tu tiempo para procesar completamente el material acá. **Un buen comienzo siempre depende de un primer paso sólido.**

## ¿Qué Pasa Con Ese Nombre?

El nombre JavaScript es probablemente el nombre de lenguaje de programación más equivocado y malentendido.

¿Este lenguaje está relacionado con Java? ¿Es solo la forma de script de Java? ¿Sirve solo para escribir scripts y no programas reales?

La verdad es que el nombre JavaScript es un artefacto de artimañas de marketing. Cuando Brendan Eich concibió el lenguaje por primera vez, le puso el nombre clave Mocha. Internamente en Netscape, se usaba la marca LiveScript. Pero cuando llegó el momento de nombrar públicamente el lenguaje, "JavaScript" ganó la votación.

¿Por qué? Porque este lenguaje fue originalmente diseñado para atraer a una audiencia compuesta en su mayoría por programadores de Java, y porque la palabra "script" era popular en ese momento para referirse a programas livianos. ¡Estos "scripts" livianos serían los primeros en incrustarse dentro de las páginas de esta cosa nueva llamada la web!

En otras palabras, JavaScript fue una estrategia de marketing para intentar posicionar este lenguaje como una alternativa aceptable a escribir el Java más pesado y más conocido de la época. De hecho, podría haberse llamado tranquilamente "WebJava".

Hay algunas semejanzas superficiales entre el código de JavaScript y el código de Java. Esas similitudes no vienen particularmente de un desarrollo compartido, sino de que ambos lenguajes apuntan a desarrolladores con expectativas de sintaxis asumidas provenientes de C (y en cierta medida, de C++).

Por ejemplo, usamos el `{` para comenzar un bloque de código y el `}` para terminar ese bloque de código, igual que C/C++ y Java. También usamos el `;` para puntuar el final de un statement.

En algunos sentidos, las relaciones legales van incluso más profundo que la sintaxis. Oracle (a través de Sun), la compañía que todavía posee y gestiona Java, también posee la marca registrada oficial del nombre "JavaScript" (a través de Netscape). Esta marca casi nunca se hace valer, y probablemente no podría hacerse a estas alturas.

Por estas razones, algunos han sugerido que usemos JS en lugar de JavaScript. Esa es una abreviatura muy común, aunque no sea un buen candidato para que un lenguaje oficial se identifique con ella. De hecho, estos libros usan JS casi exclusivamente para referirse al lenguaje.

Distanciando aún más al lenguaje de la marca registrada que posee Oracle, el nombre oficial del lenguaje especificado por TC39 y formalizado por el organismo de estándares ECMA es **ECMAScript**. Y, de hecho, desde 2016 el nombre oficial del lenguaje también lleva como sufijo el año de la revisión; al momento de escribir esto, ese es ECMAScript 2019, o abreviado de otra manera ES2019.

En otras palabras, el JavaScript/JS que corre en tu navegador o en Node.js es *una* implementación del estándar ES2019.

| NOTA: |
| :--- |
| No uses términos como "JS6" o "ES8" para referirte al lenguaje. Algunos lo hacen, pero esos términos solo sirven para perpetuar la confusión. "ES20xx" o simplemente "JS" son a lo que te deberías atener. |

Ya sea que lo llames JavaScript, JS, ECMAScript o ES2019, ¡definitivamente no es una variante del lenguaje Java!

> "Java es a JavaScript lo que jamón es a hámster." --Jeremy Keith, 2009

## Especificación del Lenguaje

Mencioné TC39, el comité técnico de dirección que gestiona JS. Su tarea principal es gestionar la especificación oficial del lenguaje. Se reúnen regularmente para votar cualquier cambio acordado, que luego presentan a ECMA, la organización de estándares.

La sintaxis y el comportamiento de JS están definidos en la especificación de ES.

ES2019 resulta ser la décima especificación/revisión numerada importante desde el inicio de JS en 1995, así que en la URL oficial de la especificación alojada por ECMA vas a encontrar "10.0":

https://www.ecma-international.org/ecma-262/10.0/

El comité TC39 está compuesto por entre 50 y alrededor de 100 personas distintas de una amplia variedad de compañías con intereses en la web, como fabricantes de navegadores (Mozilla, Google, Apple) y fabricantes de dispositivos (Samsung, etc.). Todos los miembros del comité son voluntarios, aunque muchos de ellos son empleados de estas compañías y por lo tanto pueden recibir compensación en parte por sus funciones en el comité.

TC39 se reúne generalmente cada dos meses, usualmente por unos tres días, para revisar el trabajo hecho por los miembros desde la última reunión, discutir problemas y votar propuestas. Las ubicaciones de las reuniones rotan entre las compañías miembro dispuestas a ser anfitrionas.

Todas las propuestas de TC39 avanzan a través de un proceso de cinco etapas —por supuesto, como somos programadores, ¡es base 0!— de la Etapa 0 a la Etapa 4. Podés leer más sobre el proceso de Etapas acá: https://tc39.es/process-document/

La Etapa 0 significa, a grandes rasgos, que alguien en TC39 piensa que es una idea que vale la pena y planea promoverla y trabajar en ella. Eso significa que muchas ideas que los no miembros de TC39 "proponen", a través de medios informales como redes sociales o posts de blog, son en realidad "pre-etapa 0". Tenés que conseguir que un miembro de TC39 promueva una propuesta para que sea considerada oficialmente "Etapa 0".

Una vez que una propuesta alcanza el estado de "Etapa 4", es elegible para ser incluida en la próxima revisión anual del lenguaje. Puede llevar desde varios meses hasta algunos años que una propuesta recorra todas estas etapas.

Todas las propuestas se gestionan de forma abierta, en el repositorio de Github de TC39: https://github.com/tc39/proposals

Cualquiera, sea miembro de TC39 o no, es bienvenido a participar en estas discusiones públicas y en los procesos de trabajo de las propuestas. Sin embargo, solo los miembros de TC39 pueden asistir a las reuniones y votar las propuestas y cambios. Así que, en efecto, la voz de un miembro de TC39 tiene mucho peso en hacia dónde irá JS.

Contrario a cierto mito establecido y frustrantemente perpetuado, *no* hay múltiples versiones de JavaScript dando vueltas. Hay solo **un JS**, el estándar oficial mantenido por TC39 y ECMA.

A principios de los años 2000, cuando Microsoft mantenía una versión bifurcada y sometida a ingeniería inversa (y no del todo compatible) de JS llamada "JScript", existían legítimamente "múltiples versiones" de JS. Pero esos días quedaron muy atrás. Es anticuado e inexacto hacer tales afirmaciones sobre JS hoy en día.

Todos los principales fabricantes de navegadores y dispositivos se han comprometido a mantener sus implementaciones de JS conformes con esta única especificación central. Por supuesto, los engines implementan características en momentos distintos. Pero nunca debería ser el caso que el engine v8 (el engine de JS de Chrome) implemente una característica especificada de manera diferente o incompatible en comparación con el engine SpiderMonkey (el engine de JS de Mozilla).

Eso significa que podés aprender **un JS** y confiar en ese mismo JS en todas partes.

### La Web Domina Todo Acerca de (JS)

Si bien la variedad de entornos que corren JS se expande constantemente (desde navegadores, a servidores (Node.js), a robots, a lamparitas, a...), el único entorno que domina JS es la web. En otras palabras, cómo se implementa JS para los navegadores web es, en toda su practicidad, la única realidad que importa.

En su mayor parte, el JS definido en la especificación y el JS que corre en los engines de JS basados en navegador son el mismo. Pero hay algunas diferencias que deben considerarse.

A veces la especificación de JS va a dictar algún comportamiento nuevo o refinado, y sin embargo eso no va a coincidir exactamente con cómo funciona en los engines de JS basados en navegador. Tal desajuste es histórico: los engines de JS han tenido más de 20 años de comportamientos observables en torno a casos límite de características de las que el contenido web ha llegado a depender. Por eso, a veces los engines de JS se negarán a conformarse a un cambio dictado por la especificación porque rompería ese contenido web.

En estos casos, a menudo TC39 dará marcha atrás y simplemente elegirá conformar la especificación a la realidad de la web. Por ejemplo, TC39 planeaba agregar un método `contains(..)` para los Arrays, pero se descubrió que este nombre entraba en conflicto con viejos frameworks de JS todavía en uso en algunos sitios, así que cambiaron el nombre a uno sin conflicto, `includes(..)`. Lo mismo pasó con una *crisis comunitaria* de JS cómica/trágica apodada "smooshgate", donde el método planeado `flatten(..)` finalmente fue renombrado a `flat(..)`.

Pero ocasionalmente, TC39 decidirá que la especificación debe mantenerse firme en algún punto, aunque sea poco probable que los engines de JS basados en navegador alguna vez se conformen.

¿La solución? El Apéndice B, "Additional ECMAScript Features for Web Browsers" (Características Adicionales de ECMAScript para Navegadores Web).[^specApB] La especificación de JS incluye este apéndice para detallar cualquier desajuste conocido entre la especificación oficial de JS y la realidad de JS en la web. En otras palabras, estas son excepciones permitidas *solo* para el JS de la web; otros entornos de JS deben atenerse a la letra de la ley.

Las secciones B.1 y B.2 cubren *adiciones* a JS (sintaxis y APIs) que el JS de la web incluye, nuevamente por razones históricas, pero que TC39 no planea especificar formalmente en el núcleo de JS. Los ejemplos incluyen literales octales con prefijo `0`, las utilidades globales `escape(..)` / `unescape(..)`, "ayudantes" de String como `anchor(..)` y `blink()`, y el método `compile(..)` de RegExp.

La sección B.3 incluye algunos conflictos donde el código puede correr tanto en engines de JS de la web como fuera de ella, pero donde el comportamiento *podría* ser observablemente diferente, resultando en distintos desenlaces. La mayoría de los cambios listados involucran situaciones que se etiquetan como errores tempranos cuando el código corre en strict mode.

Los *gotchas* (trucos engañosos) del Apéndice B no se encuentran muy a menudo, pero aun así es buena idea evitar estas construcciones para estar a salvo a futuro. Siempre que sea posible, atenete a la especificación de JS y no dependas de comportamiento que solo es aplicable en ciertos entornos de engine de JS.

### No Todo el JS (de la Web)...

¿Es este código un programa JS?

```js
alert("Hello, JS!");
```

Depende de cómo lo mires. La función `alert(..)` que se muestra acá no está incluida en la especificación de JS, pero *sí* está en todos los entornos de JS de la web. Sin embargo, no la vas a encontrar en el Apéndice B, entonces, ¿qué pasa?

Varios entornos de JS (como los engines de JS de navegador, Node.js, etc.) agregan APIs al scope global de tus programas JS que te dan capacidades específicas del entorno, como poder mostrar una caja tipo alerta en el navegador del usuario.

De hecho, una amplia gama de APIs que parecen JS, como `fetch(..)`, `getCurrentLocation(..)` y `getUserMedia(..)`, son todas APIs web que parecen JS. En Node.js, podemos acceder a cientos de métodos de API de varios módulos integrados, como `fs.write(..)`.

Otro ejemplo común es `console.log(..)` (¡y todos los demás métodos `console.*`!). Estos no están especificados en JS, pero debido a su utilidad universal están definidos por prácticamente todo entorno de JS, según un consenso aproximadamente acordado.

Así que `alert(..)` y `console.log(..)` no están definidos por JS. Pero *parecen* JS. Son funciones y métodos de objetos y obedecen las reglas de sintaxis de JS. Los comportamientos detrás de ellos están controlados por el entorno que corre el engine de JS, pero en la superficie definitivamente tienen que respetar JS para poder jugar en el patio de JS.

La mayoría de las diferencias entre navegadores de las que la gente se queja con afirmaciones del tipo "¡JS es tan inconsistente!" se deben en realidad a diferencias en cómo funcionan esos comportamientos del entorno, no en cómo funciona el JS en sí.

Entonces, una llamada a `alert(..)` *es* JS, pero `alert` en sí mismo es en realidad solo un invitado, no parte de la especificación oficial de JS.

### No Siempre Es JS

Usar la consola/REPL (Read-Evaluate-Print-Loop) en las Herramientas de Desarrollador de tu navegador (o Node) se siente como un entorno de JS bastante directo a primera vista. Pero en realidad no lo es.

Las Herramientas de Desarrollador son... herramientas para desarrolladores. Su propósito principal es hacerles la vida más fácil a los desarrolladores. Priorizan la DX (Experiencia del Desarrollador). *No* es un objetivo de tales herramientas reflejar con precisión y pureza todos los matices del comportamiento de JS según la especificación estricta. Por eso, hay muchas rarezas que pueden actuar como "gotchas" si estás tratando a la consola como un entorno de JS *puro*.

Esta conveniencia es algo bueno, dicho sea de paso. ¡Me alegra que las Herramientas de Desarrollador les hagan la vida más fácil a los desarrolladores! Me alegra que tengamos encantos de UX agradables como el autocompletado de variables/propiedades, etc. Solo estoy señalando que no podemos ni deberíamos esperar que tales herramientas *siempre* se adhieran estrictamente a la manera en que se manejan los programas JS, porque ese no es el propósito de estas herramientas.

Dado que tales herramientas varían en comportamiento de navegador a navegador, y dado que cambian (a veces con bastante frecuencia), no voy a "hardcodear" ninguno de los detalles específicos en este texto, para asegurarme de que el texto de este libro no quede desactualizado rápidamente.

Pero voy a dar pistas de algunos ejemplos de rarezas que han sido ciertas en varios momentos en distintos entornos de consola de JS, para reforzar mi punto sobre no asumir comportamiento nativo de JS mientras los usás:

* Si una declaración `var` o `function` en el "scope global" de nivel superior de la consola realmente crea una variable global real (y una propiedad `window` reflejada, ¡y viceversa!).

* Qué pasa con múltiples declaraciones `let` y `const` en el "scope global" de nivel superior.

* Si `"use strict";` en una entrada de una línea (presionando `<enter>` después) habilita strict mode para el resto de esa sesión de consola, de la forma en que lo haría en la primera línea de un archivo .js, así como si podés usar `"use strict";` más allá de la "primera línea" y aun así lograr que strict mode se active para esa sesión.

* Cómo funciona el default-binding de `this` en modo no estricto para las llamadas a funciones, y si el "objeto global" usado va a contener las variables globales esperadas.

* Cómo funciona el hoisting (ver Libro 2, *Scope & Closures*) a través de múltiples entradas de líneas.

* ...varias otras

La consola de desarrollador no está tratando de fingir ser un compilador de JS que maneja tu código ingresado exactamente de la misma manera que el engine de JS maneja un archivo .js. Está tratando de hacerte fácil ingresar rápidamente unas pocas líneas de código y ver los resultados de inmediato. Estos son casos de uso completamente diferentes y, por eso, no es razonable esperar que una sola herramienta maneje ambos por igual.

No confíes en que el comportamiento que ves en una consola de desarrollador representa las semánticas de JS *exactas* al pie de la letra; para eso, leé la especificación. En cambio, pensá en la consola como un entorno "amigable con JS". Eso es útil por derecho propio.

## Muchas Caras

El término "paradigma" en el contexto de los lenguajes de programación se refiere a una mentalidad y enfoque amplio (casi universal) para estructurar código. Dentro de un paradigma, hay un sinfín de variaciones de estilo y forma que distinguen a los programas, incluyendo incontables librerías y frameworks diferentes que dejan su firma única en cualquier código dado.

Pero no importa cuál sea el estilo individual de un programa, las grandes divisiones en torno a los paradigmas casi siempre son evidentes a primera vista en cualquier programa.

Las categorías de código típicas a nivel de paradigma incluyen la procedural, la orientada a objetos (OO/clases) y la funcional (FP):

* El estilo procedural organiza el código en una progresión lineal de arriba hacia abajo a través de un conjunto predeterminado de operaciones, usualmente agrupadas juntas en unidades relacionadas llamadas procedimientos.

* El estilo OO organiza el código reuniendo la lógica y los datos juntos en unidades llamadas clases.

* El estilo FP organiza el código en funciones (cómputos puros en oposición a procedimientos), y las adaptaciones de esas funciones como valores.

Los paradigmas no son ni correctos ni incorrectos. Son orientaciones que guían y moldean cómo los programadores abordan los problemas y las soluciones, cómo estructuran y mantienen su código.

Algunos lenguajes están fuertemente inclinados hacia un paradigma: C es procedural, Java/C++ están casi enteramente orientados a clases, y Haskell es FP de principio a fin.

Pero muchos lenguajes también soportan patrones de código que pueden venir de, e incluso combinar y mezclar de, distintos paradigmas. Los llamados "lenguajes multiparadigma" ofrecen una flexibilidad total. En algunos casos, un solo programa puede incluso tener dos o más expresiones de estos paradigmas conviviendo lado a lado.

JavaScript es definitivamente un lenguaje multiparadigma. Podés escribir código de estilo procedural, orientado a clases o FP, y podés tomar esas decisiones línea por línea en lugar de verte forzado a una elección de todo o nada.

## Hacia Atrás y Hacia Adelante

Uno de los principios más fundamentales que guían a JavaScript es la preservación de la *compatibilidad hacia atrás* (backwards compatibility). Muchos se confunden por las implicancias de este término, y a menudo lo confunden con un término relacionado pero diferente: la *compatibilidad hacia adelante* (forwards compatibility).

Aclaremos las cosas.

La compatibilidad hacia atrás significa que una vez que algo es aceptado como JS válido, no habrá un cambio futuro en el lenguaje que haga que ese código se vuelva JS inválido. El código escrito en 1995 —¡por más primitivo o limitado que haya sido!— debería seguir funcionando hoy. Como los miembros de TC39 suelen proclamar, "¡no rompemos la web!".

La idea es que los desarrolladores de JS puedan escribir código con la confianza de que su código no va a dejar de funcionar de manera impredecible porque se lance una actualización del navegador. Esto hace que la decisión de elegir JS para un programa sea una inversión más sabia y segura, por años hacia el futuro.

Esa "garantía" no es cualquier cosa. Mantener la compatibilidad hacia atrás, extendida a lo largo de casi 25 años de historia del lenguaje, crea una carga enorme y toda una serie de desafíos únicos. Te costaría encontrar muchos otros ejemplos en la computación de semejante compromiso con la compatibilidad hacia atrás.

Los costos de atenerse a este principio no deberían descartarse a la ligera. Necesariamente crea una barrera muy alta para incluir cambios o extensiones al lenguaje; cualquier decisión se vuelve efectivamente permanente, errores incluidos. Una vez que está en JS, no se puede sacar porque podría romper programas, ¡incluso si de verdad, de verdad quisiéramos eliminarlo!

Hay algunas pequeñas excepciones a esta regla. JS ha tenido algunos cambios incompatibles hacia atrás, pero TC39 es extremadamente cauteloso al hacerlo. Estudian el código existente en la web (a través de la recolección de datos de los navegadores) para estimar el impacto de tal ruptura, y los navegadores en última instancia deciden y votan sobre si están dispuestos a aguantar las críticas de los usuarios por una ruptura de muy pequeña escala, sopesada contra los beneficios de arreglar o mejorar algún aspecto del lenguaje para muchos más sitios (y usuarios).

Esta clase de cambios son raros, y casi siempre están en casos límite de uso que es poco probable que rompan de forma observable en muchos sitios.

Comparemos la *compatibilidad hacia atrás* con su contraparte, la *compatibilidad hacia adelante*. Ser compatible hacia adelante significa que incluir una nueva adición al lenguaje en un programa no causaría que ese programa se rompa si fuera ejecutado en un engine de JS más viejo. **JS no es compatible hacia adelante**, a pesar de que muchos lo desean, e incluso creen incorrectamente el mito de que lo es.

HTML y CSS, en contraste, son compatibles hacia adelante pero no compatibles hacia atrás. Si desenterraras algo de HTML o CSS escrito allá por 1995, es completamente posible que no funcionara (o no funcionara igual) hoy. Pero, si usás una característica nueva de 2019 en un navegador de 2010, la página no está "rota": el CSS/HTML no reconocido se saltea, mientras que el resto del CSS/HTML se procesaría en consecuencia.

Puede parecer deseable que la compatibilidad hacia adelante se incluya en el diseño de un lenguaje de programación, pero en general no es práctico hacerlo. El marcado (HTML) o el estilo (CSS) son declarativos por naturaleza, así que es mucho más fácil "saltearse" declaraciones no reconocidas con un impacto mínimo en otras declaraciones reconocidas.

Pero el caos y el no determinismo surgirían si el engine de un lenguaje de programación se salteara selectivamente statements (¡o incluso expressions!) que no entendiera, ya que es imposible asegurar que una parte posterior del programa no estuviera esperando que la parte salteada hubiera sido procesada.

Aunque JS no es, y no puede ser, compatible hacia adelante, es crítico reconocer la compatibilidad hacia atrás de JS, incluyendo los beneficios duraderos para la web y las restricciones y dificultades que como resultado le impone a JS.

### Saltando las Brechas

Dado que JS no es compatible hacia adelante, significa que siempre existe el potencial de una brecha entre el código que podés escribir que es JS válido, y el engine más viejo que tu sitio o aplicación necesita soportar. Si corrés un programa que usa una característica de ES2019 en un engine de 2016, es muy probable que veas que el programa se rompe y colapsa.

Si la característica es una nueva sintaxis, el programa en general fallará por completo al compilar y correr, generalmente arrojando un error de sintaxis. Si la característica es una API (como `Object.is(..)` de ES6), el programa puede correr hasta cierto punto pero luego arrojar una excepción en tiempo de ejecución y detenerse una vez que encuentra la referencia a la API desconocida.

¿Significa esto que los desarrolladores de JS deberían quedarse siempre rezagados respecto al ritmo del progreso, usando solo código que esté en el borde trasero de los entornos de engine de JS más viejos que necesitan soportar? ¡No!

Pero sí significa que los desarrolladores de JS necesitan tener especial cuidado al abordar esta brecha.

Para la sintaxis nueva e incompatible, la solución es el transpiling (transpilación). Transpiling es un término inventado por la comunidad para describir el uso de una herramienta para convertir el código fuente de un programa de una forma a otra (pero todavía como código fuente textual). Típicamente, los problemas de compatibilidad hacia adelante relacionados con la sintaxis se resuelven usando un transpiler (el más común siendo Babel (https://babeljs.io)) para convertir desde esa versión de sintaxis de JS más nueva a una sintaxis más vieja equivalente.

Por ejemplo, un desarrollador puede escribir un fragmento de código como:

```js
if (something) {
    let x = 3;
    console.log(x);
}
else {
    let x = 4;
    console.log(x);
}
```

Así es como se vería el código en el árbol de código fuente de esa aplicación. Pero al producir los archivos para desplegar en el sitio web público, el transpiler Babel podría convertir ese código para que se vea así:

```js
var x$0, x$1;
if (something) {
    x$0 = 3;
    console.log(x$0);
}
else {
    x$1 = 4;
    console.log(x$1);
}
```

El fragmento original dependía de `let` para crear variables `x` con scope de bloque tanto en la cláusula `if` como en la `else`, que no interferían entre sí. Un programa equivalente (con una reelaboración mínima) que Babel puede producir simplemente elige nombrar dos variables diferentes con nombres únicos, produciendo el mismo resultado de no interferencia.

| NOTA: |
| :--- |
| La palabra clave `let` se agregó en ES6 (en 2015). El ejemplo anterior de transpilación solo necesitaría aplicarse si una aplicación necesitara correr en un entorno de JS que soporta una versión anterior a ES6. El ejemplo acá es solo por simplicidad de ilustración. Cuando ES6 era nuevo, la necesidad de tal transpilación era bastante prevalente, pero en 2020 es mucho menos común necesitar soportar entornos anteriores a ES6. El "objetivo" (target) usado para la transpilación es, entonces, una ventana deslizante que se desplaza hacia arriba solo a medida que se toman decisiones para que un sitio/aplicación deje de soportar algún navegador/engine viejo. |

Quizás te preguntes: ¿por qué tomarse la molestia de usar una herramienta para convertir de una versión de sintaxis más nueva a una más vieja? ¿No podríamos simplemente escribir las dos variables y saltearnos el uso de la palabra clave `let`? La razón es que se recomienda enfáticamente que los desarrolladores usen la última versión de JS para que su código sea limpio y comunique sus ideas de la manera más efectiva.

Los desarrolladores deberían enfocarse en escribir las formas de sintaxis limpias y nuevas, y dejar que las herramientas se encarguen de producir una versión compatible hacia adelante de ese código que sea adecuada para desplegar y correr en los entornos de engine de JS más viejos que se soportan.

### Rellenando las Brechas

Si el problema de compatibilidad hacia adelante no está relacionado con sintaxis nueva, sino más bien con un método de API faltante que se agregó recientemente, la solución más común es proporcionar una definición para ese método de API faltante que lo reemplace y actúe como si el entorno más viejo ya lo hubiera tenido definido de forma nativa. Este patrón se llama polyfill (también conocido como "shim").

Considerá este código:

```js
// getSomeRecords() nos devuelve una promesa para
// algunos datos que buscará
var pr = getSomeRecords();

// mostrar el spinner de la UI mientras obtenemos los datos
startSpinner();

pr
.then(renderRecords)   // renderizar si tiene éxito
.catch(showError)      // mostrar un error si no
.finally(hideSpinner)  // siempre ocultar el spinner
```

Este código usa una característica de ES2019, el método `finally(..)` sobre el prototype de la promesa. Si este código se usara en un entorno anterior a ES2019, el método `finally(..)` no existiría y ocurriría un error.

Un polyfill para `finally(..)` en entornos anteriores a ES2019 podría verse así:

```js
if (!Promise.prototype.finally) {
    Promise.prototype.finally = function f(fn){
        return this.then(
            function t(v){
                return Promise.resolve( fn() )
                    .then(function t(){
                        return v;
                    });
            },
            function c(e){
                return Promise.resolve( fn() )
                    .then(function t(){
                        throw e;
                    });
            }
        );
    };
}
```

| ADVERTENCIA: |
| :--- |
| Esta es solo una ilustración simple de un polyfill básico (no del todo conforme a la especificación) para `finally(..)`. No uses este polyfill en tu código; siempre usá un polyfill robusto y oficial siempre que sea posible, como la colección de polyfills/shims en ES-Shim. |

El statement `if` protege la definición del polyfill evitando que corra en cualquier entorno donde el engine de JS ya haya definido ese método. En los entornos más viejos, el polyfill se define, pero en los entornos más nuevos el statement `if` se saltea silenciosamente.

Los transpilers como Babel típicamente detectan qué polyfills necesita tu código y te los proporcionan automáticamente. Pero ocasionalmente puede que necesites incluirlos/definirlos explícitamente, lo cual funciona de manera similar al fragmento que acabamos de ver.

Siempre escribí código usando las características más apropiadas para comunicar sus ideas e intención de manera efectiva. En general, esto significa usar la versión estable más reciente de JS. Evitá impactar negativamente la legibilidad del código tratando de ajustar manualmente las brechas de sintaxis/API. ¡Para eso están las herramientas!

La transpilación y el polyfilling son dos técnicas muy efectivas para abordar esa brecha entre el código que usa las últimas características estables del lenguaje y los entornos viejos que un sitio o aplicación todavía necesita soportar. Dado que JS no va a dejar de mejorar, la brecha nunca va a desaparecer. Ambas técnicas deberían adoptarse como una parte estándar de la cadena de producción de todo proyecto JS de ahora en adelante.

## ¿Qué Hay en una Interpretación?

Una pregunta largamente debatida para el código escrito en JS: ¿es un script interpretado o un programa compilado? La opinión mayoritaria parece ser que JS es un lenguaje interpretado (de scripting). Pero la verdad es más complicada que eso.

Durante gran parte de la historia de los lenguajes de programación, se ha mirado con desprecio a los lenguajes "interpretados" y a los lenguajes de "scripting" como inferiores en comparación con sus contrapartes compiladas. Las razones de esta hostilidad son numerosas, incluyendo la percepción de que hay una falta de optimización del rendimiento, así como el desagrado por ciertas características del lenguaje, como que los lenguajes de scripting generalmente usan tipado dinámico en lugar de los lenguajes de tipado estático "más maduros".

Los lenguajes considerados "compilados" usualmente producen una representación portable (binaria) del programa que se distribuye para su ejecución posterior. Dado que realmente no observamos ese tipo de modelo con JS (distribuimos el código fuente, no la forma binaria), muchos afirman que eso descalifica a JS de la categoría. En realidad, el modelo de distribución para la forma "ejecutable" de un programa se ha vuelto drásticamente más variado y también menos relevante en las últimas décadas; para la pregunta en cuestión, ya no importa tanto qué forma de un programa se termina pasando de un lado a otro.

Estas afirmaciones y críticas mal informadas deberían dejarse de lado. La verdadera razón por la que importa tener una imagen clara de si JS es interpretado o compilado se relaciona con la naturaleza de cómo se manejan los errores.

Históricamente, los lenguajes de scripting o interpretados se ejecutaban generalmente de arriba hacia abajo y línea por línea; típicamente no hay una pasada inicial a través del programa para procesarlo antes de que comience la ejecución (ver Figura 1).

<figure>
    <img src="images/fig1.png" width="650" alt="Interpreting a script to execute it" align="center">
    <figcaption><em>Fig. 1: Ejecución Interpretada/Scripting</em></figcaption>
    <br><br>
</figure>

En los lenguajes de scripting o interpretados, un error en la línea 5 de un programa no se descubrirá hasta que las líneas 1 a 4 ya se hayan ejecutado. Notablemente, el error en la línea 5 podría deberse a una condición de tiempo de ejecución, como que alguna variable o valor tenga un valor inadecuado para una operación, o podría deberse a un statement/comando mal formado en esa línea. Dependiendo del contexto, diferir el manejo de errores hasta la línea en la que ocurre el error puede ser un efecto deseable o indeseable.

Comparalo con los lenguajes que sí pasan por un paso de procesamiento (típicamente llamado parsing) antes de que ocurra cualquier ejecución, como se ilustra en la Figura 2:

<figure>
    <img src="images/fig2.png" width="650" alt="Parsing, compiling, and executing a program" align="center">
    <figcaption><em>Fig. 2: Parsing + Compilación + Ejecución</em></figcaption>
    <br><br>
</figure>

En este modelo de procesamiento, un comando inválido (como sintaxis rota) en la línea 5 sería atrapado durante la fase de parsing, antes de que haya comenzado cualquier ejecución, y nada del programa correría. Para atrapar errores de sintaxis (o de otro modo "estáticos"), generalmente se prefiere saber sobre ellos antes de cualquier ejecución parcial condenada al fracaso.

Entonces, ¿qué tienen en común los lenguajes "parseados" con los lenguajes "compilados"? Primero, todos los lenguajes compilados son parseados. Así que un lenguaje parseado ya está bastante avanzado en el camino hacia ser compilado. En la teoría clásica de compilación, el último paso restante después del parsing es la generación de código: producir una forma ejecutable.

Una vez que cualquier programa fuente ha sido completamente parseado, es muy común que su ejecución posterior incluya, de alguna forma u otra, una traducción de la forma parseada del programa —usualmente llamada Árbol de Sintaxis Abstracta (AST, Abstract Syntax Tree)— a esa forma ejecutable.

En otras palabras, los lenguajes parseados usualmente también realizan generación de código antes de la ejecución, así que no es tanto una exageración decir que, en espíritu, son lenguajes compilados.

El código fuente de JS es parseado antes de ser ejecutado. La especificación lo exige, porque reclama que los "errores tempranos" —errores determinados estáticamente en el código, como un nombre de parámetro duplicado— se reporten antes de que el código comience a ejecutarse. Esos errores no pueden reconocerse sin que el código haya sido parseado.

Entonces **JS es un lenguaje parseado**, pero, ¿es *compilado*?

La respuesta está más cerca del sí que del no. El JS parseado se convierte a una forma optimizada (binaria), y ese "código" se ejecuta posteriormente (Figura 2); el engine comúnmente no vuelve a cambiar al modo de ejecución línea por línea (como la Figura 1) después de haber terminado todo el trabajo duro del parsing; la mayoría de los lenguajes/engines no lo harían, porque eso sería altamente ineficiente.

Para ser específicos, esta "compilación" produce una especie de byte code binario, que luego se le entrega a la "máquina virtual de JS" para ejecutarlo. A algunos les gusta decir que esta VM está "interpretando" el byte code. Pero entonces eso significa que Java, y una docena de otros lenguajes impulsados por JVM, por cierto, son interpretados en lugar de compilados. Por supuesto, eso contradice la afirmación típica de que Java/etc. son lenguajes compilados.

Curiosamente, aunque Java y JavaScript son lenguajes muy diferentes, ¡la cuestión de interpretado/compilado está bastante estrechamente relacionada entre ellos!

Otra complicación es que los engines de JS pueden emplear múltiples pasadas de procesamiento/optimización JIT (Just-In-Time) sobre el código generado (después del parsing), lo cual nuevamente podría razonablemente etiquetarse como "compilación" o "interpretación" según la perspectiva. En realidad, es una situación fantásticamente compleja bajo el capó de un engine de JS.

Entonces, ¿a qué se reducen estos detalles minuciosos? Dá un paso atrás y considerá el flujo entero de un programa fuente de JS:

1. Después de que un programa sale del editor de un desarrollador, es transpilado por Babel, luego empaquetado por Webpack (y quizás media docena de otros procesos de build), y luego se entrega en esa forma muy diferente a un engine de JS.

2. El engine de JS parsea el código a un AST.

3. Luego el engine convierte ese AST a una especie de byte code, una representación intermedia binaria (IR, Intermediate Representation), que luego es refinada/convertida aún más por el compilador JIT optimizador.

4. Finalmente, la VM de JS ejecuta el programa.

Para visualizar esos pasos, de nuevo:

<figure>
    <img src="images/fig3.png" width="650" alt="Steps of JS compilation and execution" align="center">
    <figcaption><em>Fig. 3: Parsing, Compilación y Ejecución de JS</em></figcaption>
    <br><br>
</figure>

¿JS se maneja más como un script interpretado línea por línea, como en la Figura 1, o se maneja más como un lenguaje compilado que se procesa en una o varias pasadas primero, antes de la ejecución (como en las Figuras 2 y 3)?

Creo que está claro que en espíritu, si no en la práctica, **JS es un lenguaje compilado**.

Y nuevamente, la razón por la que eso importa es que, dado que JS es compilado, se nos informa de los errores estáticos (como sintaxis mal formada) antes de que nuestro código se ejecute. Ese es un modelo de interacción sustancialmente diferente del que obtenemos con los programas tradicionales de "scripting", ¡y posiblemente más útil!

### Web Assembly (WASM)

Una preocupación dominante que ha impulsado una cantidad significativa de la evolución de JS es el rendimiento, tanto en qué tan rápido JS puede ser parseado/compilado como en qué tan rápido ese código compilado puede ser ejecutado.

En 2013, ingenieros de Mozilla Firefox demostraron un port del motor de juegos Unreal 3 de C a JS. La capacidad de este código para correr en un engine de JS de navegador a un rendimiento pleno de 60fps se basaba en un conjunto de optimizaciones que el engine de JS podía realizar específicamente porque la versión en JS del código del motor Unreal usaba un estilo de código que favorecía un subconjunto del lenguaje JS, llamado "ASM.js".

Este subconjunto es JS válido escrito de maneras que son algo poco comunes en la codificación normal, pero que señalan cierta información importante de tipado al engine que le permiten hacer optimizaciones clave. ASM.js fue introducido como una forma de abordar las presiones sobre el rendimiento en tiempo de ejecución de JS.

Pero es importante notar que ASM.js nunca tuvo la intención de ser código escrito por desarrolladores, sino más bien una representación de un programa que había sido transpilado desde otro lenguaje (como C), donde estas "anotaciones" de tipado eran insertadas automáticamente por el herramental.

Varios años después de que ASM.js demostrara la validez de versiones de programas creadas por herramientas que pueden ser procesadas más eficientemente por el engine de JS, otro grupo de ingenieros (también, inicialmente, de Mozilla) lanzó Web Assembly (WASM).

WASM es similar a ASM.js en que su intención original era proporcionar un camino para que programas que no son JS (C, etc.) se convirtieran a una forma que pudiera correr en el engine de JS. A diferencia de ASM.js, WASM eligió adicionalmente sortear algunas de las demoras inherentes al parsing/compilación de JS antes de que un programa pueda ejecutarse, representando el programa en una forma que es completamente distinta a JS.

WASM es un formato de representación más parecido a Assembly (de ahí, su nombre) que puede ser procesado por un engine de JS salteándose el parsing/compilación que el engine de JS normalmente hace. El parsing/compilación de un programa que apunta a WASM ocurre con antelación (AOT, Ahead-Of-Time); lo que se distribuye es un programa empaquetado en binario, listo para que el engine de JS lo ejecute con un procesamiento muy mínimo.

Una motivación inicial para WASM fue claramente las potenciales mejoras de rendimiento. Si bien eso sigue siendo un foco, WASM está adicionalmente motivado por el deseo de traer más paridad para los lenguajes que no son JS a la plataforma web. Por ejemplo, si un lenguaje como Go soporta programación con hilos (threads), pero JS (el lenguaje) no, WASM ofrece el potencial de que tal programa de Go se convierta a una forma que el engine de JS pueda entender, sin necesidad de una característica de hilos en el propio lenguaje JS.

En otras palabras, WASM alivia la presión de agregar características a JS que están destinadas mayoritaria/exclusivamente a ser usadas por programas transpilados desde otros lenguajes. Eso significa que el desarrollo de características de JS puede ser juzgado (por TC39) sin estar sesgado por los intereses/demandas de los ecosistemas de otros lenguajes, mientras que aun así se les permite a esos lenguajes tener un camino viable hacia la web.

Otra perspectiva sobre WASM que está emergiendo es, curiosamente, ni siquiera estar directamente relacionada con la web (W). WASM está evolucionando para convertirse en una especie de máquina virtual (VM) multiplataforma, donde los programas pueden ser compilados una sola vez y correr en una variedad de entornos de sistema diferentes.

Así que WASM no es solo para la web, y WASM tampoco es JS. Irónicamente, aunque WASM corre en el engine de JS, el lenguaje JS es uno de los lenguajes menos adecuados para generar programas WASM, porque WASM depende en gran medida de la información de tipado estático. Incluso TypeScript (TS) —supuestamente, JS + tipos estáticos— no es del todo adecuado (tal como está) para transpilar a WASM, aunque variantes del lenguaje como AssemblyScript están intentando salvar la brecha entre JS/TS y WASM.

Este libro no trata sobre WASM, así que no voy a pasar mucho más tiempo discutiéndolo, excepto para hacer un punto final. *Algunos* han sugerido que WASM apunta a un futuro donde JS es extirpado de, o minimizado en, la web. Estas personas a menudo albergan malos sentimientos sobre JS, y quieren que algún otro lenguaje —¡cualquier otro lenguaje!— lo reemplace. Dado que WASM permite que otros lenguajes corran en el engine de JS, en su superficie esto no es un cuento de hadas del todo fantasioso.

Pero déjenme decirlo simplemente: WASM no va a reemplazar a JS. WASM aumenta significativamente lo que la web (incluyendo JS) puede lograr. Eso es algo grandioso, enteramente ortogonal a si algunas personas lo usarán como una vía de escape para no tener que escribir JS.

## Hablando *Estrict*amente

Allá por 2009, con el lanzamiento de ES5, JS agregó el *strict mode* como un mecanismo opcional (opt-in) para fomentar mejores programas JS.

Los beneficios del strict mode superan por lejos los costos, pero las viejas costumbres son difíciles de abandonar y la inercia de las bases de código existentes (también conocidas como "legacy") es realmente difícil de cambiar. Así que, tristemente, más de 10 años después, la *opcionalidad* del strict mode significa que todavía no es necesariamente el default para los programadores de JS.

¿Por qué el strict mode? El strict mode no debería pensarse como una restricción sobre lo que no podés hacer, sino más bien como una guía hacia la mejor manera de hacer las cosas, para que el engine de JS tenga la mejor oportunidad de optimizar y correr el código eficientemente. La mayoría del código JS lo trabajan equipos de desarrolladores, así que la *estrictez* del strict mode (junto con herramientas como los linters) a menudo ayuda a la colaboración en el código al evitar algunos de los errores más problemáticos que se escapan en modo no estricto.

La mayoría de los controles del strict mode tienen la forma de *errores tempranos*, es decir, errores que no son estrictamente errores de sintaxis pero que aun así se arrojan en tiempo de compilación (antes de que el código se ejecute). Por ejemplo, el strict mode no permite nombrar dos parámetros de función igual, y resulta en un error temprano. Algunos otros controles del strict mode solo son observables en tiempo de ejecución, como la forma en que `this` toma por default `undefined` en lugar del objeto global.

En lugar de pelear y discutir con el strict mode, como un chico que solo quiere desafiar lo que sea que sus padres le digan que no haga, la mejor mentalidad es que el strict mode es como un linter recordándote cómo *debería* escribirse JS para tener la más alta calidad y la mejor oportunidad de rendimiento. Si te encontrás sintiéndote esposado, tratando de sortear el strict mode, eso debería ser una estridente bandera roja de advertencia de que necesitás dar marcha atrás y repensar todo el enfoque.

El strict mode se activa por archivo con una pragma especial (no se permite nada antes de ella excepto comentarios/espacios en blanco):

```js
// solo se permiten espacios en blanco y comentarios
// antes de la pragma use-strict
"use strict";
// el resto del archivo corre en strict mode
```

| ADVERTENCIA: |
| :--- |
| Algo a tener en cuenta es que incluso un `;` suelto por sí solo apareciendo antes de la pragma de strict mode dejará a la pragma inservible; no se arrojan errores porque es JS válido tener una expresión de literal de string en una posición de statement, ¡pero tampoco va a activar el strict mode silenciosamente! |

El strict mode puede, alternativamente, activarse por scope de función, con exactamente las mismas reglas sobre su entorno:

```js
function someOperations() {
    // los espacios en blanco y comentarios están bien acá
    "use strict";

    // todo este código correrá en strict mode
}
```

Curiosamente, si un archivo tiene el strict mode activado, las pragmas de strict mode a nivel de función no están permitidas. Así que tenés que elegir una u otra.

La **única** razón válida para usar un enfoque de strict mode por función es cuando estás convirtiendo un archivo de programa en modo no estricto existente y necesitás hacer los cambios de a poco con el tiempo. De lo contrario, es muchísimo mejor simplemente activar el strict mode para el archivo/programa entero.

Muchos se han preguntado si alguna vez habría un momento en que JS hiciera que el strict mode fuera el default. La respuesta es, casi con certeza, que no. Como discutimos antes en torno a la compatibilidad hacia atrás, si una actualización de un engine de JS empezara a asumir que el código es strict mode aunque no esté marcado como tal, es posible que este código se rompiera como resultado de los controles del strict mode.

Sin embargo, hay algunos factores que reducen el impacto futuro de esta "oscuridad" del strict mode al no ser el default.

Por un lado, prácticamente todo el código transpilado termina en strict mode incluso si el código fuente original no está escrito como tal. La mayoría del código JS en producción ha sido transpilado, así que eso significa que la mayoría del JS ya está adhiriendo al strict mode. Es posible deshacer esa suposición, pero realmente tenés que esforzarte mucho para hacerlo, así que es altamente improbable.

Más aún, está ocurriendo un amplio cambio hacia que más/la mayoría del código JS nuevo se escriba usando el formato de módulos de ES6. Los módulos de ES6 asumen el strict mode, así que todo el código en tales archivos automáticamente toma por default el strict mode.

Tomados en conjunto, el strict mode es en gran medida el default de facto aunque técnicamente no sea en realidad el default.

## Definido

JS es una implementación del estándar ECMAScript (versión ES2019 al momento de escribir esto), que es guiado por el comité TC39 y alojado por ECMA. Corre en navegadores y otros entornos de JS como Node.js.

JS es un lenguaje multiparadigma, lo que significa que la sintaxis y las capacidades le permiten a un desarrollador combinar y mezclar (¡y doblar y reformar!) conceptos de varios paradigmas importantes, como el procedural, el orientado a objetos (OO/clases) y el funcional (FP).

JS es un lenguaje compilado, lo que significa que las herramientas (incluyendo el engine de JS) procesan y verifican un programa (¡reportando cualquier error!) antes de que se ejecute.

Con nuestro lenguaje ahora *definido*, empecemos a conocer sus entresijos.

[^specApB]: ECMAScript 2019 Language Specification, Appendix B: Additional ECMAScript Features for Web Browsers, https://www.ecma-international.org/ecma-262/10.0/#sec-additional-ecmascript-features-for-web-browsers (última versión al momento de escribir esto en enero de 2020)
