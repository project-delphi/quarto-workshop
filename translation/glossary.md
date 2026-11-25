# EN → ES glossary: *Prompt, Check, Publish*, Spanish edition

Neutral Latin American Spanish, "tú" form. Every term is decided once here and used the same
way in all 31 files. **EN** in the third column means the English word stays (in running text,
not only in code). Terms come first from Appendix J (`book/appendices/j-glossary.qmd`), then
from the book's recurring vocabulary and the labels its filter writes.

Conventions that apply everywhere:

- Anything in backticks, code fences, file names, column names, options and commands stays
  exactly as in English.
- English terms kept in Spanish prose are not italicised (Markdown, commit, prompt); the
  gender used is the one Spanish practitioners use (*el* prompt, *el* commit, *la* terminal,
  *el* dashboard, *el* kernel, *el* token, *el* clúster).
- The reader's gender is never assumed: "ya puedes renderizar", not "ya estás listo".
- A numbered reference is capitalised, as Quarto writes its own cross-references: "el
  Capítulo 3", "la Figura 1.1", "la Sección 3.2", "el Apéndice A", "la Parte II". Plurals are
  not: "los capítulos 2 y 3", "las partes II y III". A cross-reference takes the article of
  its noun: "la @sec-…" for a section, "el @sec-…" for a chapter or appendix.
- Colombian data terms use the official Spanish names from the sources (DANE, INS, Resolución
  2115 de 2007), since that is what the data call them.

## The book's frame (filter labels, structure)

| English | Spanish | EN? | Note |
|---|---|---|---|
| Preface | Prefacio | | |
| Part I, Part II | Parte I, Parte II | | |
| Chapter 3 | Capítulo 3 | | Quarto's `lang: es` writes it |
| Appendix A | Apéndice A | | |
| Appendices | Apéndices | | |
| Afterword | Epílogo | | |
| Contents | Contenido | | |
| Glossary | Glosario | | Re-sorted by the Spanish term, with new letter dividers |
| Summary | Resumen | | `## Summary {.unnumbered}` |
| Key ideas | Ideas clave | | |
| In this chapter | En este capítulo | | `::: opener` label |
| Start from / You build / Checkpoint | Partes de / Construyes / Punto de control | | opener terms |
| Pause and think / Answer | Detente y piensa / Respuesta | | `::: think` |
| Why this works | Por qué funciona | | `::: why` |
| Common pitfall | Error frecuente | | `::: pitfall` |
| In practice | En la práctica | | `::: practice` |
| Try it | Pruébalo | | `::: tryit` |
| Ask your coding agent | Pídele a tu agente | | `.prompt` box |
| Expect it to run | Probablemente ejecute | | `.agent` box |
| You do | Tú haces | | `.you` box |
| You're done when | Terminaste cuando | | `::: done` |
| Exercise | Ejercicio | | |
| website edition / EPUB edition | edición web / edición EPUB | | |

## The loop and the agent

| English | Spanish | EN? | Note |
|---|---|---|---|
| prompt (n.) | prompt | EN | *el* prompt, *los* prompts |
| to prompt (an agent) | pedirle (al agente) | | "prompt an agent for one small step" → "pídele al agente un paso pequeño" |
| Prompt, Check, Publish (the loop) | see title decision in `PLAN.md` | | |
| check (v.) | revisar | | "comprobar" only for a mechanical test |
| coding agent | agente de programación | | short form "el agente" |
| AI coding agent | agente de programación con IA | | |
| model | modelo | | |
| harness | harness | EN | first use: "el harness (el programa que…)"; no settled Spanish term |
| agent | agente | | |
| sub-agent | subagente | | |
| lead (session) | sesión principal | | |
| context | contexto | | |
| token | token | EN | |
| effort | esfuerzo | | "nivel de esfuerzo" |
| slash command | comando slash | EN+ES | as Spanish users of these tools say it |
| root folder | carpeta raíz | | |
| session | sesión | | |
| approve (a command) | aprobar | | |
| rules file | archivo de reglas | | `AGENTS.md` stays |
| API | API | EN | *la* API |
| catch-up box | recuadro para ponerte al día | | |
| catch up (v.) | ponerte al día | | |
| checkpoint | punto de control | | the folder `checkpoints/` stays |
| hands-on block | bloque práctico | | |
| three checks (scope, correctness, rebuild) | tres revisiones (alcance, corrección, reconstrucción) | | `sec-three-checks` |
| starter (`starters/first-report/`) | punto de partida | | the folder name stays |
| pre-work | trabajo previo | | |

## Quarto, Markdown and publishing

| English | Spanish | EN? | Note |
|---|---|---|---|
| Quarto, Pandoc, Jupyter, Typst | (same) | EN | names |
| Markdown | Markdown | EN | |
| Pandoc's Markdown | el Markdown de Pandoc | | |
| GitHub Flavored Markdown (GFM), CommonMark | (same) | EN | names |
| render (v.) | renderizar | | |
| render (n.) | renderizado | | |
| source | fuente; archivo fuente | | "one source" → "una sola fuente" |
| output | salida | | "formats" → "formatos de salida" |
| front matter | encabezado YAML | | |
| YAML | YAML | EN | |
| heading | título | | "encabezado" is kept for front matter |
| code cell | celda de código | | |
| cell options | opciones de celda | | |
| inline code | código en línea | | |
| code fence | bloque de código delimitado | | |
| display-only fence | bloque solo de muestra | | |
| kernel | kernel | EN | |
| engine | motor | | |
| div | div | EN | |
| callout, box | recuadro | | |
| cross-reference | referencia cruzada | | |
| blank line | línea en blanco | | |
| line break | salto de línea | | |
| block quote | cita en bloque | | |
| horizontal rule | línea horizontal | | |
| escape (v.) | escapar | | |
| strikethrough | tachado | | |
| task list | lista de tareas | | |
| alt text | texto alternativo | | |
| caption | pie de figura | | "pie de tabla" for tables |
| link | enlace | | |
| footnote | nota al pie | | |
| preview | vista previa | | `quarto preview` stays |
| Quarto project | proyecto de Quarto | | |
| listing | listado | | |
| dashboard | dashboard | EN | *el* dashboard |
| value box | cuadro de valor | | |
| slides, deck | diapositivas; presentación | | |
| e-book | libro electrónico | | |
| EPUB, PDF, Word, HTML, SVG, CSV, Parquet | (same) | EN | |
| website | sitio web | | |
| static site | sitio estático | | |
| blog, post | blog, entrada | | |
| raw block | bloque sin procesar | | |
| publish | publicar | | |
| hosting, host | alojamiento; servicio de alojamiento | | |
| CI job | trabajo de CI | | |
| freeze | `freeze` | EN | "el caché de resultados de Quarto (`freeze`)" |
| guard | guarda | | as in "cláusula de guarda" |
| cited copy | copia citada | | |
| reproducible | reproducible | | |
| live-link card | tarjeta de enlace en vivo | | |

## Git and GitHub

| English | Spanish | EN? | Note |
|---|---|---|---|
| Git, GitHub, `gh` | (same) | EN | |
| repository | repositorio | | |
| commit (n., v.) | commit; hacer commit | EN | |
| branch | rama | | |
| push (n., v.) | push; hacer push | EN | |
| pull request | pull request | EN | |
| merge | hacer merge | EN | |
| clone | clonar | | |
| diff | diff | EN | |
| version control | control de versiones | | |
| untracked | sin seguimiento | | |
| working tree | árbol de trabajo | | "clean" → "limpio" |

## Terminal and environment

| English | Spanish | EN? | Note |
|---|---|---|---|
| terminal | terminal | | *la* terminal |
| shell | shell | EN | |
| command line | línea de comandos | | |
| command-line program | programa de línea de comandos | | |
| prompt (terminal) | indicador de la terminal | | kept apart from "prompt", the request |
| home folder | carpeta personal | | written `~` |
| PATH | PATH | EN | |
| folder, file | carpeta, archivo | | |
| path; absolute path; relative path | ruta; ruta absoluta; ruta relativa | | |
| stack trace | traza de la pila | | "traza de la pila (stack trace)" in the glossary; Quarto's `Stack trace:` stays |
| Tab completion | completar con Tab | | |
| caret (`^`) | acento circunflejo | | |
| environment | entorno | | |
| package | paquete | | |
| lockfile | archivo de bloqueo (lockfile) | | "(lockfile)" on first use only |
| platform tag | etiqueta de plataforma | | |
| install | instalar | | |
| uv, `uv run`, `sudo`, nano, WSL | (same) | EN | |

## Analysis (Part III)

| English | Spanish | EN? | Note |
|---|---|---|---|
| cluster (n.) | clúster | | RAE spelling; plural "clústeres" |
| to cluster; clustering | agrupar; agrupamiento | | |
| k-means, k-means++, k | (same) | EN | |
| feature | característica | | the variables the clustering sees |
| outcome | variable de resultado | | never "resultado" alone, which means *result* |
| profile | perfil | | |
| kind (of place) | tipo (de lugar) | | |
| inertia | inercia | | |
| elbow | codo | | |
| silhouette | silueta | | |
| adjusted Rand index (ARI) | índice de Rand ajustado (ARI) | | |
| bootstrap | bootstrap | EN | |
| hyperparameter | hiperparámetro | | |
| random seed | semilla aleatoria | | |
| Euclidean distance | distancia euclidiana | | |
| standard deviation (SD) | desviación estándar (DE) | | figures keep "SD" if drawn by code |
| z-score | puntaje z | | |
| variance | varianza | | |
| mean, median | media, mediana | | |
| percentile | percentil | | |
| box plot | diagrama de caja | | |
| correlation coefficient (r) | coeficiente de correlación (r) | | |
| Spearman's ρ | ρ de Spearman | | |
| monotonic | monótona (relación) | | |
| principal component analysis (PCA) | análisis de componentes principales (PCA) | | acronym kept, as in scikit-learn |
| principal component | componente principal | | |
| loadings | cargas | | |
| skewed | asimétrica | | |
| logarithm | logaritmo | | |
| impute | imputar | | |
| flag column | columna indicadora | | |
| join | unir; unión (join) | | |
| confounder | variable de confusión | | |
| control (for) | controlar (por) | | |
| ecological fallacy | falacia ecológica | | |
| difference-in-differences | diferencias en diferencias | | |
| selection on the outcome | selección según la variable de resultado | | |
| small numbers | números pequeños | | |
| missing not at random | faltantes no aleatorios | | |
| unit of analysis | unidad de análisis | | |
| causal effect | efecto causal | | |

## The Colombian data

| English | Spanish | EN? | Note |
|---|---|---|---|
| IRCA | IRCA (Índice de Riesgo de la Calidad del Agua para Consumo Humano) | | official name |
| IRCA risk bands: no risk, low, medium, high, unfit | sin riesgo, bajo, medio, alto, inviable sanitariamente | | Resolución 2115 de 2007's own words |
| utility-supplied IRCA | IRCA de prestadores | | as the INS table labels it |
| self-supplied system | sistema de autoabastecimiento | | |
| municipality, department | municipio, departamento | | |
| department capital | capital de departamento | | |
| urban zone | zona urbana (cabecera municipal) | | |
| rural zone | zona rural (centros poblados y rural disperso) | | DANE's term |
| zone-year | zona-año | | |
| municipality-year | municipio-año | | |
| zone variable / municipal variable | variable de zona / variable municipal | | |
| piped-water coverage | cobertura de acueducto | | |
| sewer coverage | cobertura de alcantarillado | | |
| low-coverage (in a name) | de baja cobertura | | |
| naming rule | regla de nombres | | |
| IPM (poverty) | IPM (Índice de Pobreza Multidimensional) | | |
| MDM | MDM (Medición del Desempeño Municipal) | | |
| SGP | SGP (Sistema General de Participaciones) | | |
| DIVIPOLA, DANE, DNP, INS, ICFES, SIVIGILA | (same) | EN | Spanish acronyms already |
| Saber 11 | Saber 11 | | |
| infant mortality | mortalidad infantil | | |
| dropout | deserción escolar | | |
| nominal pesos | pesos corrientes | | |
| rainfall, altitude, rural share | precipitación, altitud, proporción rural | | |
| choropleth | mapa coroplético | | |
| ShareAlike | CompartirIgual | | Creative Commons' Spanish licence text |
| DOI | DOI | EN | |

## The London project

| English | Spanish | EN? | Note |
|---|---|---|---|
| ALVA | ALVA (Association of Leading Visitor Attractions) | EN | name kept, explained once |
| ALVA member attractions | atracciones miembro de ALVA | | wording the repository requires |
| visitor guide | guía para visitantes | | |
| attraction visits | visitas a atracciones | | |
| WebGL | WebGL | EN | |

## The 2026-11 revision (professional and start-up readers)

GitHub's and Quarto's interface words stay in English where the reader meets them on screen
(*workflow*, *runner*, *status check*, *pull request*), as section 6 of `PLAN.md` does for code.
The Acme example (`examples/eval/`, its checkpoints and `starters/eval-repo/`) stays in English:
its names, files, columns, labels and quoted page text are literals.

| English | Spanish | EN? | Note |
|---|---|---|---|
| start-up | startup | | *la* startup, *las* startups |
| fast path (the route) | vía rápida | | "The Fast Path" → "La vía rápida" |
| route (reading route) | ruta | | "reading path" → "ruta de lectura" |
| professional (reader) | profesional | | |
| evaluation (of a model); eval | evaluación | | `evaluate.py` stays |
| model card | ficha del modelo (model card) | | "(model card)" on first use only |
| ROC AUC, precision, recall | ROC AUC, precisión, recall | EN+ES | recall stays, as scikit-learn names it |
| threshold | umbral | | |
| baseline | línea base | | |
| calibration | calibración | | |
| slice (of the data) | subgrupo | | "a slice of the test set" → "un subgrupo del conjunto de prueba" |
| leakage, leak (target) | fuga de información (leakage) | | "(leakage)" on first use only |
| test set, training set | conjunto de prueba, conjunto de entrenamiento | | |
| notebook | notebook | EN | *el* notebook; Jupyter's term as Spanish users say it |
| results file | archivo de resultados | | `results.json` stays |
| investor update | informe para inversionistas | | |
| white paper | white paper | EN | *el* white paper; first use "documento técnico (white paper)" |
| brand file | archivo de marca | | `_brand.yml` stays |
| theme | tema | | |
| contrast ratio | relación de contraste | | |
| reference document | documento de referencia | | `reference-doc` stays |
| template partial | parcial de plantilla | | |
| fragment (slides) | fragmento | | |
| speaker notes | notas de presentación | | gender-neutral |
| print view | vista de impresión | | |
| social card | tarjeta para redes sociales | | |
| description (page metadata) | descripción | | |
| citeproc, CSL, BibTeX | (same) | EN | |
| bibliography; citation | bibliografía; cita | | |
| parameter; parameterised report | parámetro; informe parametrizado | | |
| papermill, cron, `curl`, `apt`, Homebrew | (same) | EN | |
| continuous integration (CI) | integración continua (CI) | | |
| workflow (GitHub Actions) | workflow | EN | *el* workflow; a general "way of working" stays "flujo de trabajo" |
| runner | runner | EN | *el* runner |
| status check | status check | EN | *el* status check |
| protected branch | rama protegida | | |
| ruleset | ruleset | EN | GitHub's setting |
| pinned action | acción fijada | | "pinned to a commit" → "fijada a un commit" |
| artifact (CI) | artefacto | | GitHub's Spanish docs say it |
| secret (GitHub) | secreto | | |
| pull request template | plantilla de pull request | | |
| reviewer | revisor o revisora; quien revisa | | gender-neutral where it reads well |
| package manager | gestor de paquetes | | |
| codespace; GitHub Codespaces | codespace; GitHub Codespaces | EN | *el* codespace |
| dev container | contenedor de desarrollo (dev container) | | |
| API key | clave de API | | |
| spending limit | límite de gasto | | |
| zero data retention | retención cero de datos | | |
| VPN, proxy | VPN, proxy | EN | *la* VPN, *el* proxy |
| plan (subscription) | plan | | "free plan" → "plan gratuito" |
| free tier | nivel gratuito | | |
| consumer / commercial terms | condiciones para consumidores / comerciales | | |
| facts that change | datos que cambian | | Appendix K |
| checked (a date) | consultado el | | "checked 2026-11-18" → "consultado el 2026-11-18", as the edition already writes it |
| release (of a model: v1, v2, v3) | versión | | |
| build (n., CI) | build | EN | *el* build; "rebuild" stays "reconstrucción" |
| check (CI job, automated) | comprobación | | the job named *Check* stays |
| trigger (workflow) | disparador | | |
| log (CI) | registro | | |
| house template | plantilla de la casa | | |
| feedback sheet | hoja de retroalimentación | | |
| gradebook | registro de calificaciones | | |
| educator | docente | | |
| About page | página About | | the page's own English title |
| speaker view | vista del presentador | | Reveal.js's own view |
| founder; technical founder | quien funda; persona fundadora con perfil técnico | | gender-neutral |
| runway; burn | autonomía (runway); gasto mensual (burn) | | |
| free allowances | cuotas gratuitas | | |
| the water analysis (Part V) | el análisis del agua | | as the English now says instead of a part number |
| base rate | tasa base | | the share of test contacts who subscribed |
| bootstrap interval | intervalo bootstrap | | |
| lift | lift | EN | as scikit-learn and marketing practice say it |
| age band | franja de edad | | `age_band` stays |
| checksum | suma de verificación (checksum) | | "(checksum)" on first use in a chapter |
| protected characteristic | característica protegida | | the Equality Act 2010's term, translated |
| navbar | barra de navegación | | `navbar:` stays |
| wordmark (logo) | logotipo de texto | | |
| stub (page) | esbozo (stub) | | "(stub)" kept in prompts, so the agent reads the usual word |
| headline (result, title) | titular; resultado principal | | "titular" for a deck's title, "resultado principal" for a sentence |
| personal plan; company plan | plan personal; plan de empresa | | the vendors' consumer and business plans |
| managed settings (Claude Code) | managed settings (configuración administrada) | EN | Claude Code's own term, glossed once |
| synthetic stand-in | sustituto sintético | | data made up to look like the real thing |
| data room | sala de datos (data room) | | "(data room)" on first use |
| registry (DOI) | agencia de registro | | Crossref, DataCite; "registro" stays the record itself |
| section (of a course) | grupo | | a class group on the feedback sheet; the parameter `section` stays |
| batch; batch script | lote; script por lotes | | |
| statute (BibTeX entry) | ley | | the Equality Act's entry in `references.bib` |

## Titles

Sentence case, as Spanish titles are written. Exercise headings read "Ejercicio II.1: …".

| English | Spanish |
|---|---|
| Part I: Foundations | Parte I: Fundamentos |
| Part II: One Guide, Many Audiences | Parte II: Una guía, muchos públicos |
| Part I: Start Here | Parte I: Empieza aquí |
| Part III: The Craft of Outputs | Parte III: El oficio de los formatos de salida |
| Part IV: Working in a Team | Parte IV: Trabajar en equipo |
| Part V: One Analysis, Many Publications | Parte V: Un análisis, muchas publicaciones |
| 1 Publishing That Rebuilds Itself | Publicar algo que se reconstruye solo |
| 2 Working With a Coding Agent | Trabajar con un agente de programación |
| The Fast Path | La vía rápida |
| 3 Setting Up Your Machine | Preparar tu computadora |
| A First Report, by Hand | Un primer informe, a mano |
| 4 Markdown, Rendering and Project Rules | Markdown, renderizado y reglas del proyecto |
| 5 Documents That Compute | Documentos que calculan |
| 6 One Guide, Five Audiences | Una guía, cinco públicos |
| 7 Publishing and Proving the Rebuild | Publicar y demostrar la reconstrucción |
| Exercises for Part II | Ejercicios de la Parte II |
| One Set of Results | Un solo conjunto de resultados |
| Slides That Carry a Decision | Diapositivas que sostienen una decisión |
| A Site and One Brand | Un sitio y una sola marca |
| White Papers and References | White papers y referencias |
| Reports That Run Themselves | Informes que se generan solos |
| Pull Requests and Builds You Can Trust | Pull requests y builds confiables |
| At Work and in a Start-up | En el trabajo y en una startup |
| 8 The Question, the Data and the Rules | La pregunta, los datos y las reglas |
| 9 Look Before You Model | Mira antes de modelar |
| 10 From Table to Features | De la tabla a las características |
| 11 Finding Kinds of Places: k-Means | Encontrar tipos de lugares: k-means |
| 12 Interpreting Clusters | Interpretar los clústeres |
| 13 Correlation Is Not Causation | Correlación no es causalidad |
| 14 Publish Many | Publicar en muchos formatos |
| Exercises for the Water Analysis | Ejercicios del análisis del agua |
| Afterword: What You Built, and Where Next | Epílogo: lo que construiste y cómo seguir |
| A Windows: Get Ubuntu Ready | Windows: prepara Ubuntu |
| B Keys, Symbols and Terminal Habits | Teclas, símbolos y hábitos de la terminal |
| C Cheatsheet | Hoja de referencia |
| D Troubleshooting | Solución de problemas |
| E Checkpoints at a Glance, and Answers | Los puntos de control de un vistazo, y respuestas |
| F Reading in Another Language | Leer en otro idioma |
| G Data Sources, Licences and Credits | Fuentes de datos, licencias y créditos |
| H How This Book Is Built | Cómo está hecho este libro |
| I Running This as a Workshop | Darlo como taller |
| J Glossary | Glosario |
| K Facts That Change | Datos que cambian |
