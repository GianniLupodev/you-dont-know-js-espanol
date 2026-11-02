# You Don't Know JS Yet — Traducción al Español (uso personal)

Traducción al español de la serie **You Don't Know JS Yet** (2ª edición) de Kyle Simpson,
con un lector HTML colorido y didáctico generado a medida.

## ⚠️ IMPORTANTE — Licencia y distribución

El contenido original está bajo **Creative Commons BY-NC-ND 4.0**
(Atribución · No Comercial · **Sin Obras Derivadas**).

Una traducción es una **obra derivada** ("Adapted Material"). La licencia permite
**crear** la traducción para uso propio, pero **NO permite compartirla públicamente**
(`Share Adapted Material`).

> Por eso este repositorio es **PRIVADO** y es solo para estudio personal.
> **No lo hagas público** sin permiso explícito de Kyle Simpson.

Contenido original © 2019-2025 Kyle Simpson — https://github.com/getify/You-Dont-Know-JS

## Estructura

```
es/<libro>/<cap>.md   → markdown traducido (el contenido)
build.py              → fábrica: convierte es/ en el sitio HTML (site/)
site/                 → sitio generado: index + 1 página por capítulo
```

El contenido vive **separado** de la presentación: cambiás un color en `build.py`
o corregís una traducción en `es/`, corrés el build, y se regenera todo.

## Cómo generar y ver el sitio

```bash
# Regenerar el sitio (tras cambios en es/ o en build.py)
python3 build.py

# Levantar un servidor local y abrir en el navegador
cd site && python3 -m http.server 8777
# → http://localhost:8777
```

Se usa un servidor local (en vez de abrir el `file://`) porque el navegador
bloquea `localStorage` (el toggle de tema oscuro/claro) sobre `file://`.

## Libros

| Libro | Estado |
|-------|--------|
| Get Started | ✅ completo |
| Scope & Closures | ✅ completo |
| Objects & Classes | ✅ completo |
| Types & Grammar | ✅ completo |
| Sync & Async | ✅ (stub — cancelado por el autor) |
| ES.Next & Beyond | ✅ (stub — cancelado por el autor) |
