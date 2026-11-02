# You Don't Know JS Yet: Scope & Closures - 2nd Edition
# Apéndice B: Práctica

Este apéndice busca darte algunos ejercicios desafiantes e interesantes para poner a prueba y solidificar tu comprensión de los temas principales de este libro. Es buena idea intentar los ejercicios por tu cuenta —¡en un editor de código real!— en lugar de saltar directamente a las soluciones del final. ¡Nada de hacer trampa!

Estos ejercicios no tienen una respuesta correcta específica que debas obtener con exactitud. Tu enfoque puede diferir un poco (¡o mucho!) de las soluciones presentadas, y eso está bien.

Nadie te está juzgando por cómo escribes tu código. Mi esperanza es que termines este libro sintiéndote con la confianza de que puedes encarar este tipo de tareas de codificación, apoyado en una base sólida de conocimiento. Ese es el único objetivo acá. Si estás contento con tu código, ¡yo también lo estoy!

## Baldes de Canicas

¿Recuerdas la Figura 2 del Capítulo 2?

<figure>
    <img src="images/fig2.png" width="300" alt="Colored Scope Bubbles" align="center">
    <figcaption><em>Fig. 2 (Cap. 2): Burbujas de Scope Coloreadas</em></figcaption>
    <br><br>
</figure>

Este ejercicio te pide que escribas un programa —¡cualquier programa!— que contenga funciones anidadas y scopes de bloque, y que satisfaga estas restricciones:

* Si coloreas todos los scopes (¡incluyendo el scope global!) con colores diferentes, vas a necesitar al menos seis colores. Asegúrate de agregar un comentario en el código que etiquete cada scope con su color.

    BONUS: identifica cualquier scope implícito que pueda tener tu código.

* Cada scope tiene al menos un identificador.

* Contiene al menos dos scopes de función y al menos dos scopes de bloque.

* Al menos una variable de un scope externo debe quedar sombreada (shadowed) por una variable de un scope anidado (ver Capítulo 3).

* Al menos una referencia a una variable debe resolverse a una declaración de variable que esté al menos dos niveles más arriba en la cadena de scope.

| TIP: |
| :--- |
| *Puedes* simplemente escribir código basura tipo foo/bar/baz para este ejercicio, pero te sugiero que intentes crear algún tipo de código no trivial, más o menos realista, que al menos haga algo razonable. |

Intenta el ejercicio por tu cuenta y luego revisa la solución sugerida al final de este apéndice.

## Closure (PARTE 1)

Practiquemos primero el closure con algunas operaciones matemáticas comunes en computación: determinar si un valor es primo (no tiene divisores aparte de 1 y de sí mismo), y generar una lista de factores primos (divisores) para un número dado.

Por ejemplo:

```js
isPrime(11);        // true
isPrime(12);        // false

factorize(11);      // [ 11 ]
factorize(12);      // [ 3, 2, 2 ] --> 3*2*2=12
```

Aquí tienes una implementación de `isPrime(..)`, adaptada de la librería Math.js: [^MathJSisPrime]

```js
function isPrime(v) {
    if (v <= 3) {
        return v > 1;
    }
    if (v % 2 == 0 || v % 3 == 0) {
        return false;
    }
    var vSqrt = Math.sqrt(v);
    for (let i = 5; i <= vSqrt; i += 6) {
        if (v % i == 0 || v % (i + 2) == 0) {
            return false;
        }
    }
    return true;
}
```

Y aquí tienes una implementación bastante básica de `factorize(..)` (que no debe confundirse con `factorial(..)` del Capítulo 6):

```js
function factorize(v) {
    if (!isPrime(v)) {
        let i = Math.floor(Math.sqrt(v));
        while (v % i != 0) {
            i--;
        }
        return [
            ...factorize(i),
            ...factorize(v / i)
        ];
    }
    return [v];
}
```

| NOTA: |
| :--- |
| La llamo básica porque no está optimizada para el rendimiento. Es binaria-recursiva (lo cual no es optimizable con llamada de cola), y crea muchas copias intermedias de arreglos. Tampoco ordena de ninguna manera los factores descubiertos. Hay muchísimos otros algoritmos para esta tarea, pero quise usar algo corto y más o menos entendible para nuestro ejercicio. |

Si llamaras a `isPrime(4327)` múltiples veces en un programa, verías que recorrería todos sus docenas de pasos de comparación/cómputo cada vez. Si consideras `factorize(..)`, está llamando a `isPrime(..)` muchas veces mientras computa la lista de factores. Y hay buenas probabilidades de que la mayoría de esas llamadas sean repeticiones. ¡Eso es un montón de trabajo desperdiciado!

La primera parte de este ejercicio es usar closure para implementar una caché que recuerde los resultados de `isPrime(..)`, de modo que la primalidad (`true` o `false`) de un número dado se compute una sola vez. Pista: ya mostramos este tipo de caché en el Capítulo 6 con `factorial(..)`.

Si observas `factorize(..)`, está implementada con recursión, lo que significa que se llama a sí misma repetidamente. Eso de nuevo significa que probablemente veamos muchas llamadas desperdiciadas para computar los factores primos del mismo número. Así que la segunda parte del ejercicio es usar la misma técnica de caché con closure para `factorize(..)`.

Usa closures separados para el cacheo de `isPrime(..)` y de `factorize(..)`, en lugar de ponerlos dentro de un único scope.

Intenta el ejercicio por tu cuenta y luego revisa la solución sugerida al final de este apéndice.

### Una Palabra Sobre la Memoria

Quiero compartir una pequeña nota rápida sobre esta técnica de caché con closure y los impactos que tiene en el rendimiento de tu aplicación.

Podemos ver que, al ahorrarnos las llamadas repetidas, mejoramos la velocidad de cómputo (en algunos casos, de forma dramática). Pero este uso del closure implica una compensación explícita de la que debes estar muy consciente.

La compensación es la memoria. Básicamente estamos haciendo crecer nuestra caché (en memoria) de forma ilimitada. Si las funciones en cuestión se llamaran muchos millones de veces con entradas en su mayoría únicas, estaríamos consumiendo una gran cantidad de memoria. Esto definitivamente puede valer el costo, pero solo si creemos que es probable que veamos repetición de entradas comunes, de manera que estemos aprovechando la caché.

Si prácticamente toda llamada va a tener una entrada única, y la caché en esencia nunca se *usa* para algún beneficio, esta es una técnica inapropiada para emplear.

También podría ser buena idea tener un enfoque de cacheo más sofisticado, como una caché LRU (menos usada recientemente, por sus siglas en inglés), que limite su tamaño; a medida que llega al límite, una LRU desaloja los valores que son... bueno, ¡los menos usados recientemente!

La desventaja aquí es que la LRU es bastante no trivial por sí misma. Vas a querer usar una implementación altamente optimizada de LRU, y estar muy atento a todas las compensaciones en juego.

## Closure (PARTE 2)

En este ejercicio, vamos a practicar closure nuevamente definiendo una utilidad `toggle(..)` que nos da un alternador de valores.

Vas a pasar uno o más valores (como argumentos) a `toggle(..)`, y recuperarás una función. Esa función devuelta va a alternar/rotar entre todos los valores pasados, en orden, de a uno por vez, a medida que se la llama repetidamente.

```js
function toggle(/* .. */) {
    // ..
}

var hello = toggle("hello");
var onOff = toggle("on","off");
var speed = toggle("slow","medium","fast");

hello();      // "hello"
hello();      // "hello"

onOff();      // "on"
onOff();      // "off"
onOff();      // "on"

speed();      // "slow"
speed();      // "medium"
speed();      // "fast"
speed();      // "slow"
```

El caso límite de no pasar ningún valor a `toggle(..)` no es muy importante; una instancia de alternador así podría simplemente devolver siempre `undefined`.

Intenta el ejercicio por tu cuenta y luego revisa la solución sugerida al final de este apéndice.

## Closure (PARTE 3)

En este tercer y último ejercicio sobre closure, vamos a implementar una calculadora básica. La función `calculator()` va a producir una instancia de una calculadora que mantiene su propio estado, en la forma de una función (`calc(..)`, más abajo):

```js
function calculator() {
    // ..
}

var calc = calculator();
```

Cada vez que se llame a `calc(..)`, pasarás un único carácter que representa la pulsación de un botón de la calculadora. Para mantener las cosas más sencillas, vamos a restringir nuestra calculadora a soportar el ingreso únicamente de dígitos (0-9), operaciones aritméticas (+, -, \*, /), y "=" para computar la operación. Las operaciones se procesan estrictamente en el orden ingresado; no hay agrupación con "( )" ni precedencia de operadores.

No soportamos el ingreso de decimales, pero la operación de división puede dar como resultado alguno. No soportamos el ingreso de números negativos, pero la operación "-" puede dar como resultado alguno. Así que deberías poder producir cualquier número negativo o decimal ingresando primero una operación que lo compute. Luego puedes seguir computando con ese valor.

El retorno de las llamadas a `calc(..)` debería imitar lo que se mostraría en una calculadora real, como reflejar lo que se acaba de presionar, o computar el total al presionar "=".

Por ejemplo:

```js
calc("4");     // 4
calc("+");     // +
calc("7");     // 7
calc("3");     // 3
calc("-");     // -
calc("2");     // 2
calc("=");     // 75
calc("*");     // *
calc("4");     // 4
calc("=");     // 300
calc("5");     // 5
calc("-");     // -
calc("5");     // 5
calc("=");     // 0
```

Dado que este uso es un poco engorroso, aquí tienes un ayudante `useCalc(..)`, que ejecuta la calculadora con los caracteres de a uno por vez desde una cadena, y computa el display cada vez:

```js
function useCalc(calc,keys) {
    return [...keys].reduce(
        function showDisplay(display,key){
            var ret = String( calc(key) );
            return (
                display +
                (
                  (ret != "" && key == "=") ?
                      "=" :
                      ""
                ) +
                ret
            );
        },
        ""
    );
}

useCalc(calc,"4+3=");           // 4+3=7
useCalc(calc,"+9=");            // +9=16
useCalc(calc,"*8=");            // *5=128
useCalc(calc,"7*2*3=");         // 7*2*3=42
useCalc(calc,"1/0=");           // 1/0=ERR
useCalc(calc,"+3=");            // +3=ERR
useCalc(calc,"51=");            // 51
```

El uso más sensato de este ayudante `useCalc(..)` es tener siempre "=" como el último carácter ingresado.

Parte del formateo de los totales mostrados por la calculadora requiere un manejo especial. Te proporciono esta función `formatTotal(..)`, que tu calculadora debería usar cada vez que vaya a devolver un total computado actual (después de ingresar un `"="`):

```js
function formatTotal(display) {
    if (Number.isFinite(display)) {
        // constrain display to max 11 chars
        let maxDigits = 11;
        // reserve space for "e+" notation?
        if (Math.abs(display) > 99999999999) {
            maxDigits -= 6;
        }
        // reserve space for "-"?
        if (display < 0) {
            maxDigits--;
        }

        // whole number?
        if (Number.isInteger(display)) {
            display = display
                .toPrecision(maxDigits)
                .replace(/\.0+$/,"");
        }
        // decimal
        else {
            // reserve space for "."
            maxDigits--;
            // reserve space for leading "0"?
            if (
                Math.abs(display) >= 0 &&
                Math.abs(display) < 1
            ) {
                maxDigits--;
            }
            display = display
                .toPrecision(maxDigits)
                .replace(/0+$/,"");
        }
    }
    else {
        display = "ERR";
    }
    return display;
}
```

No te preocupes demasiado por cómo funciona `formatTotal(..)`. La mayor parte de su lógica es un conjunto de manejos para limitar el display de la calculadora a un máximo de 11 caracteres, incluso si se requieren negativos, decimales periódicos, o incluso notación exponencial "e+".

Nuevamente, no te quedes demasiado empantanado con el comportamiento específico de la calculadora. Enfócate en la *memoria* del closure.

Intenta el ejercicio por tu cuenta y luego revisa la solución sugerida al final de este apéndice.

## Módulos

Este ejercicio consiste en convertir la calculadora de Closure (PARTE 3) en un módulo.

No estamos agregando ninguna funcionalidad adicional a la calculadora, solo cambiando su interfaz. En lugar de llamar a una única función `calc(..)`, vamos a llamar a métodos específicos de la API pública para cada "pulsación de tecla" de nuestra calculadora. Las salidas se mantienen igual.

Este módulo debería expresarse como una función fábrica de módulo clásico llamada `calculator()`, en lugar de un IIFE singleton, de modo que se puedan crear múltiples calculadoras si se desea.

La API pública debería incluir los siguientes métodos:

* `number(..)` (entrada: el carácter/número "presionado")
* `plus()`
* `minus()`
* `mult()`
* `div()`
* `eq()`

El uso se vería así:

```js
var calc = calculator();

calc.number("4");     // 4
calc.plus();          // +
calc.number("7");     // 7
calc.number("3");     // 3
calc.minus();         // -
calc.number("2");     // 2
calc.eq();            // 75
```

`formatTotal(..)` se mantiene igual que en ese ejercicio anterior. Pero el ayudante `useCalc(..)` necesita ser ajustado para funcionar con la API del módulo:

```js
function useCalc(calc,keys) {
    var keyMappings = {
        "+": "plus",
        "-": "minus",
        "*": "mult",
        "/": "div",
        "=": "eq"
    };

    return [...keys].reduce(
        function showDisplay(display,key){
            var fn = keyMappings[key] || "number";
            var ret = String( calc[fn](key) );
            return (
                display +
                (
                  (ret != "" && key == "=") ?
                      "=" :
                      ""
                ) +
                ret
            );
        },
        ""
    );
}

useCalc(calc,"4+3=");           // 4+3=7
useCalc(calc,"+9=");            // +9=16
useCalc(calc,"*8=");            // *5=128
useCalc(calc,"7*2*3=");         // 7*2*3=42
useCalc(calc,"1/0=");           // 1/0=ERR
useCalc(calc,"+3=");            // +3=ERR
useCalc(calc,"51=");            // 51
```

Intenta el ejercicio por tu cuenta y luego revisa la solución sugerida al final de este apéndice.

A medida que trabajas en este ejercicio, dedica también algo de tiempo a considerar los pros/contras de representar la calculadora como un módulo en contraposición al enfoque de función con closure del ejercicio anterior.

BONUS: escribe unas cuantas oraciones explicando tus reflexiones.

BONUS #2: intenta convertir tu módulo a otros formatos de módulo, incluyendo: UMD, CommonJS, y ESM (ES Modules).

## Soluciones Sugeridas

Con suerte, ya has intentado los ejercicios antes de estar leyendo hasta acá. ¡Nada de hacer trampa!

Recuerda, cada solución sugerida es solo una de un montón de maneras diferentes de abordar los problemas. No son "la respuesta correcta", pero sí ilustran una forma razonable de encarar cada ejercicio.

El beneficio más importante que puedes obtener de leer estas soluciones sugeridas es compararlas con tu código y analizar por qué cada uno tomó decisiones similares o diferentes. No te metas demasiado en discusiones triviales (bikeshedding); intenta mantenerte enfocado en el tema principal en lugar de los pequeños detalles.

### Sugerencia: Baldes de Canicas

El *Ejercicio de Baldes de Canicas* se puede resolver así:

```js
// RED(1)
const howMany = 100;

// Sieve of Eratosthenes
function findPrimes(howMany) {
    // BLUE(2)
    var sieve = Array(howMany).fill(true);
    var max = Math.sqrt(howMany);

    for (let i = 2; i < max; i++) {
        // GREEN(3)
        if (sieve[i]) {
            // ORANGE(4)
            let j = Math.pow(i,2);
            for (let k = j; k < howMany; k += i) {
                // PURPLE(5)
                sieve[k] = false;
            }
        }
    }

    return sieve
        .map(function getPrime(flag,prime){
            // PINK(6)
            if (flag) return prime;
            return flag;
        })
        .filter(function onlyPrimes(v){
            // YELLOW(7)
            return !!v;
        })
        .slice(1);
}

findPrimes(howMany);
// [
//    2, 3, 5, 7, 11, 13, 17,
//    19, 23, 29, 31, 37, 41,
//    43, 47, 53, 59, 61, 67,
//    71, 73, 79, 83, 89, 97
// ]
```

### Sugerencia: Closure (PARTE 1)

El *Ejercicio de Closure (PARTE 1)* para `isPrime(..)` y `factorize(..)`, se puede resolver así:

```js
var isPrime = (function isPrime(v){
    var primes = {};

    return function isPrime(v) {
        if (v in primes) {
            return primes[v];
        }
        if (v <= 3) {
            return (primes[v] = v > 1);
        }
        if (v % 2 == 0 || v % 3 == 0) {
            return (primes[v] = false);
        }
        let vSqrt = Math.sqrt(v);
        for (let i = 5; i <= vSqrt; i += 6) {
            if (v % i == 0 || v % (i + 2) == 0) {
                return (primes[v] = false);
            }
        }
        return (primes[v] = true);
    };
})();

var factorize = (function factorize(v){
    var factors = {};

    return function findFactors(v) {
        if (v in factors) {
            return factors[v];
        }
        if (!isPrime(v)) {
            let i = Math.floor(Math.sqrt(v));
            while (v % i != 0) {
                i--;
            }
            return (factors[v] = [
                ...findFactors(i),
                ...findFactors(v / i)
            ]);
        }
        return (factors[v] = [v]);
    };
})();
```

Los pasos generales que usé para cada utilidad:

1. Envolver en un IIFE para definir el scope donde residirá la variable de la caché.

2. En la llamada subyacente, revisar primero la caché, y si ya se conoce un resultado, retornarlo.

3. En cada lugar donde originalmente ocurría un `return`, asignar a la caché y simplemente retornar los resultados de esa operación de asignación—este es un truco de ahorro de espacio, mayormente por brevedad en el libro.

También renombré la función interna de `factorize(..)` a `findFactors(..)`. Eso no es técnicamente necesario, pero ayuda a dejar más claro qué función invocan las llamadas recursivas.

### Sugerencia: Closure (PARTE 2)

El *Ejercicio de Closure (PARTE 2)* `toggle(..)` se puede resolver así:

```js
function toggle(...vals) {
    var unset = {};
    var cur = unset;

    return function next(){
        // save previous value back at
        // the end of the list
        if (cur != unset) {
            vals.push(cur);
        }
        cur = vals.shift();
        return cur;
    };
}

var hello = toggle("hello");
var onOff = toggle("on","off");
var speed = toggle("slow","medium","fast");

hello();      // "hello"
hello();      // "hello"

onOff();      // "on"
onOff();      // "off"
onOff();      // "on"

speed();      // "slow"
speed();      // "medium"
speed();      // "fast"
speed();      // "slow"
```

### Sugerencia: Closure (PARTE 3)

El *Ejercicio de Closure (PARTE 3)* `calculator()` se puede resolver así:

```js
// from earlier:
//
// function useCalc(..) { .. }
// function formatTotal(..) { .. }

function calculator() {
    var currentTotal = 0;
    var currentVal = "";
    var currentOper = "=";

    return pressKey;

    // ********************

    function pressKey(key){
        // number key?
        if (/\d/.test(key)) {
            currentVal += key;
            return key;
        }
        // operator key?
        else if (/[+*/-]/.test(key)) {
            // multiple operations in a series?
            if (
                currentOper != "=" &&
                currentVal != ""
            ) {
                // implied '=' keypress
                pressKey("=");
            }
            else if (currentVal != "") {
                currentTotal = Number(currentVal);
            }
            currentOper = key;
            currentVal = "";
            return key;
        }
        // = key?
        else if (
            key == "=" &&
            currentOper != "="
        ) {
            currentTotal = op(
                currentTotal,
                currentOper,
                Number(currentVal)
            );
            currentOper = "=";
            currentVal = "";
            return formatTotal(currentTotal);
        }
        return "";
    };

    function op(val1,oper,val2) {
        var ops = {
            // NOTE: using arrow functions
            // only for brevity in the book
            "+": (v1,v2) => v1 + v2,
            "-": (v1,v2) => v1 - v2,
            "*": (v1,v2) => v1 * v2,
            "/": (v1,v2) => v1 / v2
        };
        return ops[oper](val1,val2);
    }
}

var calc = calculator();

useCalc(calc,"4+3=");           // 4+3=7
useCalc(calc,"+9=");            // +9=16
useCalc(calc,"*8=");            // *5=128
useCalc(calc,"7*2*3=");         // 7*2*3=42
useCalc(calc,"1/0=");           // 1/0=ERR
useCalc(calc,"+3=");            // +3=ERR
useCalc(calc,"51=");            // 51
```

| NOTA: |
| :--- |
| Recuerda: este ejercicio es sobre closure. No te enfoques demasiado en la mecánica real de una calculadora, sino más bien en si estás *recordando* correctamente el estado de la calculadora a lo largo de las llamadas a funciones. |

### Sugerencia: Módulos

El *Ejercicio de Módulos* `calculator()` se puede resolver así:

```js
// from earlier:
//
// function useCalc(..) { .. }
// function formatTotal(..) { .. }

function calculator() {
    var currentTotal = 0;
    var currentVal = "";
    var currentOper = "=";

    var publicAPI = {
        number,
        eq,
        plus() { return operator("+"); },
        minus() { return operator("-"); },
        mult() { return operator("*"); },
        div() { return operator("/"); }
    };

    return publicAPI;

    // ********************

    function number(key) {
        // number key?
        if (/\d/.test(key)) {
            currentVal += key;
            return key;
        }
    }

    function eq() {
        // = key?
        if (currentOper != "=") {
            currentTotal = op(
                currentTotal,
                currentOper,
                Number(currentVal)
            );
            currentOper = "=";
            currentVal = "";
            return formatTotal(currentTotal);
        }
        return "";
    }

    function operator(key) {
        // multiple operations in a series?
        if (
            currentOper != "=" &&
            currentVal != ""
        ) {
            // implied '=' keypress
            eq();
        }
        else if (currentVal != "") {
            currentTotal = Number(currentVal);
        }
        currentOper = key;
        currentVal = "";
        return key;
    }

    function op(val1,oper,val2) {
        var ops = {
            // NOTE: using arrow functions
            // only for brevity in the book
            "+": (v1,v2) => v1 + v2,
            "-": (v1,v2) => v1 - v2,
            "*": (v1,v2) => v1 * v2,
            "/": (v1,v2) => v1 / v2
        };
        return ops[oper](val1,val2);
    }
}

var calc = calculator();

useCalc(calc,"4+3=");           // 4+3=7
useCalc(calc,"+9=");            // +9=16
useCalc(calc,"*8=");            // *5=128
useCalc(calc,"7*2*3=");         // 7*2*3=42
useCalc(calc,"1/0=");           // 1/0=ERR
useCalc(calc,"+3=");            // +3=ERR
useCalc(calc,"51=");            // 51
```

¡Eso es todo para este libro, felicitaciones por tu logro! Cuando estés listo, continúa con el Libro 3, *Objects & Classes*.

[^MathJSisPrime]: *Math.js: isPrime(..)*, https://github.com/josdejong/mathjs/blob/develop/src/function/utils/isPrime.js, 3 de marzo de 2020.
