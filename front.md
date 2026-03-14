# Prompt Maestro para Rediseñar el Frontend en HTML, CSS y JavaScript

Actua como un frontend engineer senior y como un UI/UX designer experto en experiencias digitales premium para marcas de lujo. Tu tarea es rediseñar por completo el frontend de una aplicacion actualmente hecha en Streamlit, sustituyendolo por una implementacion tradicional basada unicamente en archivos `HTML`, `CSS` y `JavaScript` vanilla.

No uses Streamlit. No uses React, Vue, Svelte ni frameworks CSS. El resultado debe ser un frontend elegante, realista, implementable y listo para integrarse despues con un backend o API.

## Objetivo del proyecto

Debes crear el frontend de una aplicacion llamada `Fashion Campaign Shooting AI`, una herramienta que permite subir una prenda, definir direccion creativa y generar un shooting editorial de moda asistido por IA.

La interfaz debe transmitir:

- lujo
- glamour
- sofisticacion editorial
- precision premium
- sensacion de producto de alto valor

No quiero un diseño generico de SaaS. Quiero una web con identidad visual fuerte, refinada, sensual y moderna, con una estetica de lujo contemporaneo inspirada en editoriales de moda, direction boards de marcas premium y experiencias digitales high-end.

## Paleta obligatoria

Usa exclusivamente esta paleta como base del sistema visual:

- `#323944` fondo profundo azul carbon
- `#fbf4f2` marfil rosado claro
- `#8b1616` burdeos intenso
- `#c7aea1` beige rosado sofisticado

Puedes usar transparencias, sombras, gradientes, overlays y mezclas derivadas de esta paleta, pero no introduzcas nuevos colores dominantes fuera de estos tonos.

## Contexto funcional actual

La app actual tiene este flujo y debes conservarlo en la nueva interfaz:

1. Header principal con el titulo `Fashion Campaign Shooting AI` y un subtitulo explicando que genera imagenes editoriales photorealistas en formato cuadrado.
2. Formulario principal con estos campos:
   - `Google API Key` como password input
   - `Fotografia de la prenda` como file uploader
   - `Modo de generacion` con dos opciones:
     - `Final`: 4 imagenes 4K
     - `Draft`: 2 imagenes 1K
3. Seccion `Estilo de campana`:
   - selector entre `Preset optimizado` y `Prompt personalizado`
   - si es preset, mostrar un `select`
   - si es personalizado, mostrar un `textarea`
4. Seccion `Ubicacion del shooting`:
   - selector entre `Preset optimizado` y `Prompt personalizado`
   - si es preset, mostrar un `select`
   - si es personalizado, mostrar un `textarea`
5. Seccion `Referencia del modelo`:
   - selector entre:
     - `Preset de descripcion`
     - `Descripcion personalizada`
     - `Subir imagen del modelo`
   - si es preset, mostrar un `select`
   - si es descripcion personalizada, mostrar un `textarea`
   - si es subida, mostrar un uploader de imagen
6. CTA principal: `Generar shooting`
7. Durante la ejecucion debe existir una zona visual de estado/logs donde se vean mensajes de progreso.
8. Al finalizar deben mostrarse:
   - prompts generados
   - imagen de referencia del modelo
   - galeria con las imagenes del shooting
   - boton para descargar el ZIP completo
   - botones para descargar cada imagen individual

## Requisitos de producto

Debes diseñar la experiencia completa de una sola pagina, pero con una estructura visual clara y muy cuidada. Piensa en un producto premium con narrativa visual, no en un simple formulario.

La aplicacion debe incluir como minimo estas zonas:

- hero superior con presencia visual y mensaje de marca
- panel/formulario principal
- panel de estado de generacion
- seccion de resultados
- area de prompts generados
- galeria final

## Direccion creativa obligatoria

La web debe sentirse:

- editorial
- cinematica
- sensual pero sobria
- lujosa sin ser barroca
- muy cuidada en tipografia, espaciado y composicion

Evita por completo:

- look generico de dashboard corporativo
- cajas grises aburridas
- botones de estilo bootstrap
- tipografias por defecto
- aspecto "AI tool" barato
- exceso de bordes duros o componentes cuadrados sin criterio

## Direccion visual sugerida

Usa una combinacion de:

- una tipografia serif de aire editorial para titulares
- una sans refinada y limpia para UI y cuerpo

Puedes sugerir fuentes como:

- `Cormorant Garamond`, `Bodoni Moda`, `Playfair Display` o similar para headings
- `Manrope`, `Plus Jakarta Sans`, `DM Sans` o similar para UI

La pagina debe incluir:

- fondo con gradientes sutiles y profundidad visual
- capas translúcidas sofisticadas
- tarjetas o paneles con acabado premium
- detalles en burdeos para enfasis
- acentos en beige rosado para calidez
- bloques amplios, respirables y elegantes
- microinteracciones sobrias y fluidas

## Layout y experiencia

Quiero una solucion pensada primero para desktop premium, pero totalmente responsive en tablet y movil.

### Desktop

- Hero superior ancho con una composicion fuerte
- Debajo, layout a dos columnas
- Columna izquierda:
  - formulario completo
  - CTA principal
- Columna derecha:
  - panel de estado
  - resumen del shooting
  - preview de resultados cuando existan

### Mobile

- estructura apilada
- hero simplificado
- botones y campos comodos de tocar
- galeria adaptada a una columna
- jerarquia muy clara

## Comportamiento e interacciones

Genera una interfaz realista con JavaScript para manejar estado visual y comportamiento. Aunque no conectes un backend real, prepara la estructura para integracion posterior.

Debes contemplar:

- toggles/radios elegantes para cambiar modos
- mostrar u ocultar campos dinamicamente segun la seleccion del usuario
- preview del nombre del archivo subido
- validacion visual de campos obligatorios
- estado loading del boton principal
- panel de progreso con logs en tiempo real simulados o preparados
- renderizado del bloque de resultados cuando existan datos
- botones de descarga visualmente premium

## Datos mock y estructura de JS

Incluye datos mock para:

- presets de estilo
- presets de ubicacion
- presets de descripcion de modelo
- resultados generados de ejemplo
- prompts generados de ejemplo

El JavaScript debe estar organizado y ser limpio. Usa una estructura mantenible con funciones claras y estado central simple.

## Archivos que debes generar

Quiero que la solucion se plantee en estos archivos:

- `index.html`
- `styles.css`
- `app.js`

Si necesitas assets simulados, indicalo de forma clara, pero prioriza que el frontend pueda ejecutarse sin dependencias complejas.

## Requisitos tecnicos

- HTML semantico y limpio
- CSS moderno, bien estructurado y con variables en `:root`
- JavaScript vanilla, modular y entendible
- nada de librerias externas innecesarias
- accesibilidad razonable
- focus states visibles
- contraste correcto
- animaciones sutiles, no exageradas
- buena experiencia de hover y active
- preparacion para integrar peticiones reales mas adelante

## Sistema visual y componentes esperados

Define un mini design system con:

- variables de color
- variables tipograficas
- espaciados
- radios
- sombras
- estilos de botones
- estilos de inputs
- estilos de chips/toggles
- estilos de tarjetas
- estilos de panel de logs

Quiero que el resultado tenga componentes como:

- hero de marca
- card de formulario
- segmented controls elegantes
- upload zones estilizadas
- textareas editoriales
- status panel tipo consola premium
- galeria de resultados con captions
- download actions refinadas

## Criterios de calidad del diseño

El diseño debe parecer digno de:

- una marca de moda premium
- una agencia creativa de lujo
- una experiencia high-fashion digital

Debe sentirse intencional en:

- la escala tipografica
- la composicion
- la direccion artistica
- el ritmo vertical
- la armonia cromatica
- los estados interactivos

## Importante sobre el tono del resultado

No entregues una solucion plana o mediocre. Quiero una propuesta visual fuerte, glamurosa y premium, pero tambien usable. Si hay que elegir entre un dashboard generico y una experiencia mas editorial, elige la opcion editorial siempre que siga siendo funcional.

## Entregable esperado

Devuelve:

1. El contenido completo de `index.html`
2. El contenido completo de `styles.css`
3. El contenido completo de `app.js`

El codigo debe ser coherente entre si y ejecutable como frontend estatico.

## Restricciones finales

- No uses Streamlit
- No uses frameworks frontend
- No simplifiques el flujo funcional actual
- No uses una estetica de dashboard generico
- No uses morado
- No uses negro puro como base dominante
- No uses blanco puro como fondo dominante

## Mejora adicional deseada

Haz que el hero y el contenedor principal tengan una presencia visual memorable. Me interesa especialmente que el primer impacto transmita lujo y glamour, y que el formulario se sienta como una herramienta editorial premium, no como un formulario tecnico cualquiera.

## Instruccion final

Genera una propuesta frontend completa, cuidada y lista para implementar, con codigo de alta calidad en `HTML`, `CSS` y `JavaScript`, manteniendo todas las funcionalidades de la app actual y elevando radicalmente la calidad visual hacia una experiencia premium y glamourosa.
