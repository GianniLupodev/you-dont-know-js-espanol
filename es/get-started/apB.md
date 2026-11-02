# You Don't Know JS Yet: Get Started - 2nd Edition
# Apéndice B: ¡Practicar, practicar, practicar!

En este apéndice, exploraremos algunos ejercicios y sus soluciones sugeridas. Estos sirven simplemente para que *empieces* a practicar con los conceptos del libro.

## Practicar comparaciones

Practiquemos trabajando con tipos de valores y comparaciones (Capítulo 4, Pilar 3), donde será necesario involucrar la coerción.

`scheduleMeeting(..)` debería tomar una hora de inicio (en formato de 24 horas como una cadena "hh:mm") y una duración de la reunión (número de minutos). Debería devolver `true` si la reunión cae completamente dentro de la jornada laboral (según las horas especificadas en `dayStart` y `dayEnd`); devolver `false` si la reunión viola los límites de la jornada laboral.

```js
const dayStart = "07:30";
const dayEnd = "17:45";

function scheduleMeeting(startTime,durationMinutes) {
    // ..TODO..
}

scheduleMeeting("7:00",15);     // false
scheduleMeeting("07:15",30);    // false
scheduleMeeting("7:30",30);     // true
scheduleMeeting("11:30",60);    // true
scheduleMeeting("17:00",45);    // true
scheduleMeeting("17:30",30);    // false
scheduleMeeting("18:00",15);    // false
```

Intenta resolverlo tú mismo primero. Considera el uso de los operadores de igualdad y de comparación relacional, y cómo la coerción impacta en este código. Una vez que tengas código que funcione, *compara* tu(s) solución(es) con el código en "Soluciones sugeridas" al final de este apéndice.

## Practicar closure

Ahora practiquemos con closure (Capítulo 4, Pilar 1).

La función `range(..)` toma un número como primer argumento, que representa el primer número de un rango de números deseado. El segundo argumento también es un número que representa el final del rango deseado (inclusive). Si se omite el segundo argumento, entonces debería devolverse otra función que espera ese argumento.

```js
function range(start,end) {
    // ..TODO..
}

range(3,3);    // [3]
range(3,8);    // [3,4,5,6,7,8]
range(3,0);    // []

var start3 = range(3);
var start4 = range(4);

start3(3);     // [3]
start3(8);     // [3,4,5,6,7,8]
start3(0);     // []

start4(6);     // [4,5,6]
```

Intenta resolverlo tú mismo primero.

Una vez que tengas código que funcione, *compara* tu(s) solución(es) con el código en "Soluciones sugeridas" al final de este apéndice.

## Practicar prototypes

Finalmente, trabajemos con `this` y objetos enlazados vía prototype (Capítulo 4, Pilar 2).

Define una máquina tragamonedas con tres rodillos que puedan girar individualmente con `spin()`, y luego mostrar con `display()` el contenido actual de todos los rodillos.

El comportamiento básico de un único rodillo está definido en el objeto `reel` más abajo. Pero la máquina tragamonedas necesita rodillos individuales: objetos que delegan a `reel`, y que cada uno tiene una propiedad `position`.

Un rodillo solo *sabe cómo* mostrar con `display()` su símbolo actual, pero una máquina tragamonedas típicamente muestra tres símbolos por rodillo: la posición actual (`position`), una posición por encima (`position - 1`) y una posición por debajo (`position + 1`). Así que mostrar la máquina tragamonedas debería terminar mostrando una cuadrícula de 3 x 3 de símbolos.

```js
function randMax(max) {
    return Math.trunc(1E9 * Math.random()) % max;
}

var reel = {
    symbols: [
        "♠", "♥", "♦", "♣", "☺", "★", "☾", "☀"
    ],
    spin() {
        if (this.position == null) {
            this.position = randMax(
                this.symbols.length - 1
            );
        }
        this.position = (
            this.position + 100 + randMax(100)
        ) % this.symbols.length;
    },
    display() {
        if (this.position == null) {
            this.position = randMax(
                this.symbols.length - 1
            );
        }
        return this.symbols[this.position];
    }
};

var slotMachine = {
    reels: [
        // this slot machine needs 3 separate reels
        // hint: Object.create(..)
    ],
    spin() {
        this.reels.forEach(function spinReel(reel){
            reel.spin();
        });
    },
    display() {
        // TODO
    }
};

slotMachine.spin();
slotMachine.display();
// ☾ | ☀ | ★
// ☀ | ♠ | ☾
// ♠ | ♥ | ☀

slotMachine.spin();
slotMachine.display();
// ♦ | ♠ | ♣
// ♣ | ♥ | ☺
// ☺ | ♦ | ★
```

Intenta resolverlo tú mismo primero.

Pistas:

* Usa el operador módulo `%` para envolver `position` a medida que accedes a los símbolos de forma circular alrededor de un rodillo.

* Usa `Object.create(..)` para crear un objeto y enlazarlo vía prototype a otro objeto. Una vez enlazados, la delegación permite que los objetos compartan el contexto de `this` durante la invocación de métodos.

* En lugar de modificar directamente el objeto reel para mostrar cada una de las tres posiciones, puedes usar otro objeto temporal (`Object.create(..)` de nuevo) con su propia `position`, desde el cual delegar.

Una vez que tengas código que funcione, *compara* tu(s) solución(es) con el código en "Soluciones sugeridas" al final de este apéndice.

## Soluciones sugeridas

Ten en cuenta que estas soluciones sugeridas son solo eso: sugerencias. Hay muchas formas distintas de resolver estos ejercicios de práctica. Compara tu enfoque con lo que ves aquí, y considera los pros y los contras de cada uno.

Solución sugerida para la práctica de "Comparaciones" (Pilar 3):

```js
const dayStart = "07:30";
const dayEnd = "17:45";

function scheduleMeeting(startTime,durationMinutes) {
    var [ , meetingStartHour, meetingStartMinutes ] =
        startTime.match(/^(\d{1,2}):(\d{2})$/) || [];

    durationMinutes = Number(durationMinutes);

    if (
        typeof meetingStartHour == "string" &&
        typeof meetingStartMinutes == "string"
    ) {
        let durationHours =
            Math.floor(durationMinutes / 60);
        durationMinutes =
            durationMinutes - (durationHours * 60);
        let meetingEndHour =
            Number(meetingStartHour) + durationHours;
        let meetingEndMinutes =
            Number(meetingStartMinutes) +
            durationMinutes;

        if (meetingEndMinutes >= 60) {
            meetingEndHour = meetingEndHour + 1;
            meetingEndMinutes =
                meetingEndMinutes - 60;
        }

        // re-compose fully-qualified time strings
        // (to make comparison easier)
        let meetingStart = `${
            meetingStartHour.padStart(2,"0")
        }:${
            meetingStartMinutes.padStart(2,"0")
        }`;
        let meetingEnd = `${
            String(meetingEndHour).padStart(2,"0")
        }:${
            String(meetingEndMinutes).padStart(2,"0")
        }`;

        // NOTE: since expressions are all strings,
        // comparisons here are alphabetic, but it's
        // safe here since they're fully qualified
        // time strings (ie, "07:15" < "07:30")
        return (
            meetingStart >= dayStart &&
            meetingEnd <= dayEnd
        );
    }

    return false;
}

scheduleMeeting("7:00",15);     // false
scheduleMeeting("07:15",30);    // false
scheduleMeeting("7:30",30);     // true
scheduleMeeting("11:30",60);    // true
scheduleMeeting("17:00",45);    // true
scheduleMeeting("17:30",30);    // false
scheduleMeeting("18:00",15);    // false
```

----

Solución sugerida para la práctica de "Closure" (Pilar 1):

```js
function range(start,end) {
    start = Number(start) || 0;

    if (end === undefined) {
        return function getEnd(end) {
            return getRange(start,end);
        };
    }
    else {
        end = Number(end) || 0;
        return getRange(start,end);
    }


    // **********************

    function getRange(start,end) {
        var ret = [];
        for (let i = start; i <= end; i++) {
            ret.push(i);
        }
        return ret;
    }
}

range(3,3);    // [3]
range(3,8);    // [3,4,5,6,7,8]
range(3,0);    // []

var start3 = range(3);
var start4 = range(4);

start3(3);     // [3]
start3(8);     // [3,4,5,6,7,8]
start3(0);     // []

start4(6);     // [4,5,6]
```

----

Solución sugerida para la práctica de "Prototypes" (Pilar 2):

```js
function randMax(max) {
    return Math.trunc(1E9 * Math.random()) % max;
}

var reel = {
    symbols: [
        "♠", "♥", "♦", "♣", "☺", "★", "☾", "☀"
    ],
    spin() {
        if (this.position == null) {
            this.position = randMax(
                this.symbols.length - 1
            );
        }
        this.position = (
            this.position + 100 + randMax(100)
        ) % this.symbols.length;
    },
    display() {
        if (this.position == null) {
            this.position = randMax(
                this.symbols.length - 1
            );
        }
        return this.symbols[this.position];
    }
};

var slotMachine = {
    reels: [
        Object.create(reel),
        Object.create(reel),
        Object.create(reel)
    ],
    spin() {
        this.reels.forEach(function spinReel(reel){
            reel.spin();
        });
    },
    display() {
        var lines = [];

        // display all 3 lines on the slot machine
        for (
            let linePos = -1; linePos <= 1; linePos++
        ) {
            let line = this.reels.map(
                function getSlot(reel){
                    var slot = Object.create(reel);
                    slot.position = (
                        reel.symbols.length +
                        reel.position +
                        linePos
                    ) % reel.symbols.length;
                    return slot.display();
                }
            );
            lines.push(line.join(" | "));
        }

        return lines.join("\n");
    }
};

slotMachine.spin();
slotMachine.display();
// ☾ | ☀ | ★
// ☀ | ♠ | ☾
// ♠ | ♥ | ☀

slotMachine.spin();
slotMachine.display();
// ♦ | ♠ | ♣
// ♣ | ♥ | ☺
// ☺ | ♦ | ★
```

Eso es todo por este libro. Pero ahora es momento de buscar proyectos reales en los que practicar estas ideas. ¡Simplemente sigue programando, porque esa es la mejor manera de aprender!
