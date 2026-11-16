"""Make the Spanish edition's own media: diagrams, cover and QR code (translation/PLAN.md).

The diagrams are the English edition's SVGs with their words replaced (every replacement must
match exactly once, so a changed English diagram stops this script); the cover is the English
cover with the Spanish title; the QR code points to the Spanish website edition. The PNGs are
drawn by book/media/build.py's own rasteriser, at the same scales. Roadmaps come from
book/scripts/roadmaps.py --book ../book-es.

    cd book && uv run --with playwright --with segno python ../translation/media_es.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN, ES = ROOT / "book" / "media", ROOT / "book-es" / "media"
sys.path.insert(0, str(EN))
import build  # noqa: E402

DIAGRAMS = {
    "agent-loop.svg": [
        (">How a coding agent works<", ">Cómo funciona un agente de programación<"),
        ("You give the harness a prompt, and it shows you results and asks you to approve commands. The harness (Claude Code, Codex or Antigravity) sends the conversation and tool results to the model (Claude, GPT or Gemini), which runs on the vendor's servers and replies with text or a request to use a tool. The harness carries out tool requests in the project folder, its root: it reads AGENTS.md first, then reads and edits files and runs commands there. The model decides, the harness does, and you direct and check.",
         "Tú le das un prompt al harness, y este te muestra los resultados y te pide aprobar comandos. El harness (Claude Code, Codex o Antigravity) le envía la conversación y los resultados de las herramientas al modelo (Claude, GPT o Gemini), que corre en los servidores del proveedor y responde con texto o con una solicitud para usar una herramienta. El harness lleva a cabo las solicitudes en la carpeta del proyecto, su raíz: primero lee AGENTS.md y luego lee y edita archivos y ejecuta comandos ahí. El modelo decide, el harness hace, y tú diriges y revisas."),
        (">You<", ">Tú<"), (">direct and check<", ">diriges y revisas<"),
        (">results,<", ">resultados,<"), (">\"approve this?\"<", ">\"¿apruebas esto?\"<"),
        (">reads and writes files<", ">lee y escribe archivos<"), (">runs commands<", ">ejecuta comandos<"),
        (">searches<", ">busca<"), (">asks before acting<", ">pregunta antes de actuar<"),
        (">Model<", ">Modelo<"), (">or Gemini<", ">o Gemini<"), (">on the vendor's<", ">en los servidores<"),
        (">servers<", ">del proveedor<"), (">edits, runs<", ">edita, ejecuta<"),
        (">reads AGENTS.md first<", ">primero lee AGENTS.md<"),
        (">Project folder, the root<", ">Carpeta del proyecto, la raíz<"),
        (">the agent's world: start it here<", ">el mundo del agente: inícialo aquí<"),
        (">The model decides · the harness does · you check<", ">El modelo decide · el harness hace · tú revisas<"),
    ],
    "catch-up.svg": [
        (">Catching up from a checkpoint<", ">Ponerse al día desde un punto de control<"),
        ("Stuck for two minutes, you paste the line Catch me up: follow ../quarto-workshop/checkpoints/NN/README.md into the agent. It follows four steps. One, back up your project folder, all but its .venv environment, to a new time-stamped folder beside it. Two, copy the checkpoint in, and for the water project the data if they are missing. Three, render and check a named output. Four, carry on reading from the catch-up box: the project now matches the book at that point.",
         "Después de dos minutos sin avanzar, pegas en el agente la línea Catch me up: follow ../quarto-workshop/checkpoints/NN/README.md. El agente sigue cuatro pasos. Uno, respalda la carpeta de tu proyecto, todo menos su entorno .venv, en una carpeta nueva con fecha y hora, al lado. Dos, copia el punto de control y, en el proyecto del agua, los datos si faltan. Tres, renderiza y revisa una salida con nombre. Cuatro, sigues leyendo desde el recuadro para ponerte al día: el proyecto ahora coincide con el libro en ese punto."),
        (">Stuck for two minutes?<", ">¿Dos minutos sin avanzar?<"),
        (">paste into your agent:<", ">pega en tu agente:<"),
        (">Back up your folder<", ">Respalda tu carpeta<"),
        (">all but <tspan", ">todo menos <tspan"), ("</tspan>, to a new time-stamped copy<", "</tspan>, en una copia nueva con fecha<"),
        (">Copy the checkpoint in<", ">Copia el punto de control<"),
        (">water projects: copy <tspan", ">proyecto del agua: copia <tspan"), ("</tspan> if missing<", "</tspan> si falta<"),
        (">Render and check<", ">Renderiza y revisa<"),
        (">the README names the output to open<", ">el README nombra la salida que hay que abrir<"),
        (">Carry on from the box<", ">Sigue desde el recuadro<"),
        (">your project now matches the book<", ">tu proyecto ya coincide con el libro<"),
    ],
    "compute-once.svg": [
        (">Compute once, publish many<", ">Calcular una vez, publicar muchas<"),
        ("The data file water_municipal.csv feeds one script, scripts/analysis.py, which Quarto runs before every render. The script prepares the features, chooses k, fits k-means, and computes cluster profiles and outcome comparisons, then writes them once to outputs/: clusters.parquet, cluster_profiles.csv, k_selection.csv, outcomes_by_year.csv, irca_infant.csv and summary.json. Every page reads those files and none recomputes them: the explore and clusters pages, the report in html, docx, pdf and epub, the council slides in revealjs and pptx, a blog post and a dashboard. Together they are one website, published on GitHub Pages.",
         "El archivo de datos water_municipal.csv alimenta un solo script, scripts/analysis.py, que Quarto ejecuta antes de cada renderizado. El script prepara las características, elige k, ajusta k-means y calcula los perfiles de los clústeres y las comparaciones de las variables de resultado, y luego los escribe una vez en outputs/: clusters.parquet, cluster_profiles.csv, k_selection.csv, outcomes_by_year.csv, irca_infant.csv y summary.json. Cada página lee esos archivos y ninguna los vuelve a calcular: las páginas de exploración y de clústeres, el informe en html, docx, pdf y epub, las diapositivas para el concejo en revealjs y pptx, una entrada de blog y un dashboard. Juntas forman un sitio web, publicado en GitHub Pages."),
        (">real public data, unchanged<", ">datos públicos reales, sin cambios<"),
        (">prepare · choose k · fit k-means<", ">preparar · elegir k · ajustar k-means<"),
        (">profiles · outcome comparisons<", ">perfiles · comparación de resultados<"),
        (">run by Quarto before every render (pre-render)<", ">lo ejecuta Quarto antes de renderizar (pre-render)<"),
        (">written once<", ">escritos una vez<"),
        (">pages read them, none recomputes<", ">las páginas los leen, ninguna recalcula<"),
        (">explore<", ">exploración<"), (">clusters<", ">clústeres<"), (">blog post<", ">entrada de blog<"),
        (">report: html · docx · pdf · epub<", ">informe: html · docx · pdf · epub<"),
        (">council slides: revealjs · pptx<", ">diapositivas: revealjs · pptx<"),
        (">one website<", ">un sitio web<"), (">published on GitHub Pages<", ">publicado en GitHub Pages<"),
    ],
    "confounders.svg": [
        (">What else could explain it<", ">Qué más podría explicarlo<"),
        ("The question is whether unsafe water raises infant mortality, a dashed arrow from water safety to infant deaths. Other paths connect the two. Poverty and rurality make water less safe and also make infant deaths more likely, so they can create an association without any effect of water: a confounder. Poverty also limits health-service access, which affects infant deaths. And poverty weakens reporting quality: places with weak registration record fewer of their real deaths, and blank rates are left out of the data, which can hide a real effect. Finally the data meet at different levels: IRCA is measured for a zone, infant mortality for the whole municipality, so a pattern across places need not hold for the people in them.",
         "La pregunta es si el agua insegura aumenta la mortalidad infantil, una flecha discontinua de la calidad del agua a las muertes infantiles. Otros caminos conectan las dos. La pobreza y lo rural hacen el agua menos segura y también hacen más probables las muertes infantiles, así que pueden crear una asociación sin ningún efecto del agua: una variable de confusión. La pobreza también limita el acceso a los servicios de salud, que afecta las muertes infantiles. Y la pobreza debilita la calidad del registro: los lugares con un registro débil anotan menos de sus muertes reales, y las tasas vacías quedan fuera de los datos, lo que puede esconder un efecto real. Por último, los datos se encuentran en niveles distintos: el IRCA se mide para una zona y la mortalidad infantil para todo el municipio, así que un patrón entre lugares no tiene por qué valer para las personas que viven en ellos."),
        (">Poverty, rurality<", ">Pobreza, lo rural<"),
        (">a confounder: touches both<", ">confusión: afecta a las dos<"),
        (">Health-service<", ">Acceso a<"), (">access<", ">la salud<"),
        (">Water safety<", ">Calidad del agua<"), (">IRCA, per zone<", ">IRCA, por zona<"),
        (">Infant deaths<", ">Muertes infantiles<"), (">real, per municipality<", ">reales, por municipio<"),
        (">the question?<", ">¿la pregunta?<"),
        (">Reporting quality<", ">Calidad del registro<"),
        (">weak registration hides deaths<", ">un registro débil esconde muertes<"),
        (">Recorded deaths<", ">Muertes registradas<"), (">what the data hold<", ">lo que contienen los datos<"),
        (">blank rates are left out<", ">las tasas vacías quedan fuera<"),
        (">Ecological level: IRCA per zone, deaths per municipality.<", ">Nivel ecológico: IRCA por zona, muertes por municipio.<"),
        (">A pattern across places need not hold for the people in them.<", ">Un patrón entre lugares no tiene por qué valer para su gente.<"),
    ],
    "drift.svg": [
        (">Why reports drift<", ">Por qué los informes se desactualizan<"),
        ("Two ways to publish the London guide's attraction counts after ALVA corrects one figure in attractions.csv. By hand: each number is copied into each output, one at a time, so the web guide and the dashboard get the new number while the Word brief, the social card and the white paper still show the old one. One source: code cells in the project's .qmd pages read attractions.csv, and one quarto render rebuilds the web guide, the dashboard, the Word brief, the social card and the white paper, all with the corrected number.",
         "Dos maneras de publicar los conteos de atracciones de la guía de Londres después de que ALVA corrige una cifra en attractions.csv. A mano: cada número se copia en cada salida, una por una, así que la guía web y el dashboard reciben el número nuevo mientras el informe en Word, la tarjeta para redes sociales y el documento técnico siguen mostrando el viejo. Una sola fuente: las celdas de código de las páginas .qmd del proyecto leen attractions.csv, y un solo quarto render reconstruye la guía web, el dashboard, el informe en Word, la tarjeta para redes sociales y el documento técnico, todos con el número corregido."),
        (">By hand<", ">A mano<"),
        (">each number is copied into each output<", ">cada número se copia en cada salida<"),
        (">ALVA corrects a figure<", ">ALVA corrige una cifra<", 2),
        (">retyped by hand, one at a time<", ">reescrito a mano, una a la vez<"),
        (">One source<", ">Una sola fuente<"),
        (">every number is computed from the data<", ">cada número se calcula a partir de los datos<"),
        (">read by code cells<", ">lo leen las celdas de código<"),
        (">The project's pages<", ">Las páginas del proyecto<"),
        (">every output updated by one command<", ">cada salida, actualizada con un solo comando<"),
        ("</tspan> web guide<", "</tspan> guía web<", 2), ("</tspan> Word brief<", "</tspan> informe Word<", 2),
        ("</tspan> social card<", "</tspan> tarjeta social<", 2), ("</tspan> white paper<", "</tspan> doc. técnico<", 2),
        ("</tspan> new number   <tspan", "</tspan> número nuevo   <tspan"), ("</tspan> still the old one<", "</tspan> sigue el viejo<"),
        ("</tspan> sources you edit and check<", "</tspan>: las fuentes que editas y revisas<"),
    ],
    "git-cycle.svg": [
        (">Every change, safely: the Git loop<", ">Cada cambio, con seguridad: el ciclo de Git<"),
        ("Six steps. Branch: work on a branch, so main stays untouched. Commit: save a snapshot of the files with a message saying why. Push: copy the commits to GitHub. Pull request: propose the change and show the difference. Review: someone reads the difference and comments, approves or asks for changes. Merge: the commits join main. Working alone, you commit to main and push; in a team, every change goes round the whole loop.",
         "Seis pasos. Rama: trabaja en una rama, para que main quede intacta. Commit: guarda una instantánea de los archivos con un mensaje que diga por qué. Push: copia los commits a GitHub. Pull request: propone el cambio y muestra la diferencia. Revisión: alguien lee la diferencia y comenta, aprueba o pide cambios. Merge: los commits se suman a main. Si trabajas sin equipo, haces commit en main y push; en un equipo, cada cambio recorre el ciclo entero."),
        (">Branch<", ">Rama<"), (">main stays untouched<", ">main queda intacta<"),
        (">a snapshot, with why<", ">una instantánea, con el porqué<"),
        (">copy the commits to GitHub<", ">copia los commits a GitHub<"),
        (">propose it; show the diff<", ">propónlo; muestra el diff<"),
        (">Review<", ">Revisión<"), (">someone reads the diff<", ">alguien lee el diff<"),
        (">the change joins main<", ">el cambio se suma a main<"),
        (">a team:<", ">en equipo:<"), (">every change<", ">cada cambio<"), (">goes round<", ">da la vuelta<"),
        (">Alone, as in this book: commit to main and push.<", ">Sin equipo, como en este libro: commit en main y push.<"),
        (">The agent runs Git; you read its diffs and approve.<", ">El agente ejecuta Git; tú lees sus diffs y apruebas.<"),
    ],
    "loop.svg": [
        (">Prompt, Check, Publish<", ">Pide, revisa, publica<"),
        ("The loop this book teaches, run at every step of both projects. Prompt: you ask a coding agent for one small step, naming the files and columns and ending with a check; Chapter 2. The agent does the work: it writes files and runs commands. Check: you read what changed, open the result and compare it with the data; this step is always yours. If it is not right, you fix the prompt, or catch up from a checkpoint, and prompt again. The checked source goes to Publish: Quarto rebuilds every output from it with quarto render, the same way every time; Chapter 1. Then the next step begins with a new prompt.",
         "El ciclo que enseña este libro, en cada paso de los dos proyectos. Pide: le pides a un agente de programación un paso pequeño, nombrando los archivos y las columnas y terminando con una comprobación; Capítulo 2. El agente hace el trabajo: escribe archivos y ejecuta comandos. Revisa: lees lo que cambió, abres el resultado y lo comparas con los datos; este paso siempre es tuyo. Si no está bien, corriges el prompt, o te pones al día desde un punto de control, y vuelves a pedir. La fuente revisada pasa a Publica: Quarto reconstruye cada salida a partir de ella con quarto render, siempre de la misma manera; Capítulo 1. Luego el siguiente paso empieza con un prompt nuevo."),
        (">next step<", ">otro paso<"), (">not right?<", ">¿no está bien?<"), (">fix the prompt<", ">corrígelo<"),
        (">YOU → AGENT<", ">TÚ → AGENTE<"),
        (">Ch. 2<", ">Cap. 2<", 2), (">Ch. 1<", ">Cap. 1<"),
        (">Prompt<", ">Pide<"),
        (">one small step, files named,<", ">un paso pequeño, con archivos,<"),
        (">ending with a check<", ">y una comprobación al final<"),
        (">the agent works<", ">el agente trabaja<"),
        (">YOU<", ">TÚ<"), (">Check<", ">Revisa<"),
        (">read what changed, open the<", ">lee lo que cambió, abre el<"),
        (">result, compare with the data<", ">resultado, compáralo con los datos<"),
        (">the checked source<", ">la fuente revisada<"),
        (">Publish<", ">Publica<"),
        ("</tspan> rebuilds every<", "</tspan> reconstruye cada<"),
        (">output, the same way every time<", ">salida, siempre de la misma manera<"),
        (">Small steps, each one checked,<", ">Pasos pequeños, cada uno revisado,<"),
        (">every output rebuilt from one source.<", ">cada salida reconstruida desde una sola fuente.<"),
    ],
    "publish-flow.svg": [
        (">Publishing to GitHub Pages<", ">Publicar en GitHub Pages<"),
        ("Your project folder holds the source, which git pushes to the main branch of a GitHub repository. quarto publish gh-pages renders the site on your computer and pushes only the rendered HTML to a separate branch, gh-pages. GitHub Pages serves that branch at https://user.github.io/repo/. Anyone with the address can read the site.",
         "La carpeta de tu proyecto contiene la fuente, que git sube a la rama main de un repositorio de GitHub. quarto publish gh-pages renderiza el sitio en tu computadora y sube solo el HTML renderizado a una rama aparte, gh-pages. GitHub Pages sirve esa rama en https://user.github.io/repo/. Cualquiera que tenga la dirección puede leer el sitio."),
        (">Your project folder<", ">La carpeta de tu proyecto<"),
        (">source: <tspan", ">fuente: <tspan"),
        (">rendered site: <tspan", ">sitio renderizado: <tspan"), ("</tspan> (not committed)<", "</tspan> (sin commit)<"),
        (">GitHub repository<", ">Repositorio de GitHub<"),
        (">the source and<", ">la fuente y<"), (">its history<", ">su historial<"),
        (">rendered HTML only,<", ">solo el HTML renderizado,<"),
        (">written by Quarto<", ">escrito por Quarto<"), (">served by<", ">lo sirve<"),
        (">The live site<", ">El sitio en vivo<"),
        (">Free static hosting: anyone with the address can read it.<", ">Alojamiento estático gratuito: lo lee quien tenga la dirección.<"),
    ],
    "render-pipeline.svg": [
        (">What quarto render does<", ">Lo que hace quarto render<"),
        ("A source file, london.qmd, holding Markdown, YAML and code cells, goes through three steps. Step 1, execute: Jupyter for Python or knitr for R runs each code cell. The result is Markdown with the results in place of the code. Step 2, convert: Pandoc turns that Markdown into html, docx, epub, pptx and revealjs. Step 3, typeset: for PDF, Pandoc writes Typst source and Typst typesets it into a pdf. One command, quarto render, runs all three steps.",
         "Un archivo fuente, london.qmd, con Markdown, YAML y celdas de código, pasa por tres pasos. Paso 1, ejecutar: Jupyter para Python o knitr para R ejecuta cada celda de código. El resultado es Markdown con los resultados en lugar del código. Paso 2, convertir: Pandoc convierte ese Markdown en html, docx, epub, pptx y revealjs. Paso 3, componer: para el PDF, Pandoc escribe fuente de Typst y Typst la compone en un pdf. Un solo comando, quarto render, ejecuta los tres pasos."),
        (">Markdown · YAML · code cells<", ">Markdown · YAML · celdas<"),
        (">1 Execute<", ">1 Ejecutar<"), (">Jupyter (Python) or knitr (R)<", ">Jupyter (Python) o knitr (R)<"),
        (">runs each code cell<", ">ejecuta cada celda de código<"),
        (">Markdown with results<", ">Markdown con resultados<"),
        (">2 Convert<", ">2 Convertir<"), (">3 Typeset<", ">3 Componer<"),
        (">One command, <tspan", ">Un solo comando, <tspan"), ("</tspan>, runs every step;<", "</tspan>, ejecuta cada paso;<"),
        ("</tspan> reruns them on each save.<", "</tspan> los repite cada vez que guardas.<"),
    ],
    "sub-agents.svg": [
        (">One lead, three sub-agents<", ">Una sesión principal, tres subagentes<"),
        ("Your agent, the lead, reads the prompt and starts three sub-agents at once. Each has its own context and writes only its own files: one writes london-dashboard.qmd, one london-email.qmd and london-email-message.md, one london-flyer.qmd. None of them renders. When all three report back, the lead renders the three files one at a time and checks each. Three tasks take about as long as the slowest one, and use more tokens.",
         "Tu agente, la sesión principal, lee el prompt e inicia tres subagentes a la vez. Cada uno tiene su propio contexto y escribe solo sus propios archivos: uno escribe london-dashboard.qmd, otro london-email.qmd y london-email-message.md, otro london-flyer.qmd. Ninguno renderiza. Cuando los tres informan, la sesión principal renderiza los tres archivos uno por uno y revisa cada uno. Tres tareas tardan más o menos lo que la más lenta, y usan más tokens."),
        (">Lead: your agent<", ">Principal: tu agente<"),
        (">splits the work and waits<", ">reparte el trabajo y espera<"),
        (">all at once<", ">todos a la vez<"),
        (">Sub-agent 1<", ">Subagente 1<"), (">Sub-agent 2<", ">Subagente 2<"), (">Sub-agent 3<", ">Subagente 3<"),
        (">own context<", ">contexto propio<", 3), (">renders nothing<", ">no renderiza<", 3),
        (">Lead renders and checks<", ">La principal renderiza y revisa<"),
        (">one file at a time:<", ">un archivo a la vez:<"),
        (">two renders in one folder collide<", ">dos renderizados en una carpeta chocan<"),
        (">time ≈ the slowest task · more tokens<", ">tiempo ≈ la tarea más lenta · más tokens<"),
    ],
}

COVER = [
    ("<title id=\"t\">Prompt, Check, Publish</title>", "<title id=\"t\">Pide, revisa, publica</title>"),
    ("Title: Prompt, Check, Publish. Subtitle: Reproducible Data Publishing with Quarto and AI Coding Agents.",
     "Título: Pide, revisa, publica. Subtítulo: Publicación reproducible de datos con Quarto y agentes de programación con IA."),
    ("Book cover.", "Cubierta del libro."), ("Author:", "Autoría:"),
    (">A PRACTITIONER’S GUIDE<", ">UNA GUÍA PRÁCTICA<"),
    (">Prompt,<", ">Pide,<"), (">Check,<", ">revisa,<"), (">Publish<", ">publica<"),
    (">Reproducible Data Publishing with Quarto<", ">Publicación reproducible de datos con Quarto<"),
    (">and AI Coding Agents<", ">y agentes de programación con IA<"),
]


BACK_COVER = [
    ("<title id=\"t\">Prompt, Check, Publish: back cover</title>", "<title id=\"t\">Pide, revisa, publica: contracubierta</title>"),
    ("Back cover. Write once. Check every step. Publish everywhere. Change one number in a dataset, and every document built from it should change too. This book shows how: you write prose and code once, in plain text, and Quarto rebuilds a web page, Word, PDF, slides, an e-book, a website, a blog and a dashboard from that one source. A coding agent writes the code at a speed that was out of reach until recently; you direct it one small step at a time and check its work against the data. Two real projects: a London visitor guide, with cited figures, maps and openly licensed photographs; and drinking-water risk in Colombia, with public data for every municipality, explored and clustered. No programming is assumed. Ravi Kalia.",
     "Contracubierta. Escribe una vez. Revisa cada paso. Publica en todas partes. Cambia un número en un conjunto de datos, y cada documento hecho con él debería cambiar también. Este libro enseña cómo: escribes prosa y código una vez, en texto plano, y Quarto reconstruye una página web, Word, PDF, diapositivas, un libro electrónico, un sitio web, un blog y un dashboard desde esa fuente. Un agente de programación escribe el código a una velocidad impensable hace poco; tú lo diriges paso a paso y lo revisas con los datos. Dos proyectos reales: una guía de Londres para visitantes, con cifras citadas, mapas y fotos con licencia abierta; y el riesgo del agua potable en Colombia, con datos públicos de cada municipio, explorados y agrupados. No se da por sentado que sepas programar. Ravi Kalia."),
    (">PROMPT, CHECK, PUBLISH<", ">PIDE, REVISA, PUBLICA<"),
    (">Write once.<", ">Escribe una vez.<"), (">Check every step.<", ">Revisa cada paso.<"),
    (">Publish everywhere.<", ">Publica en todas partes.<"),
    (">Change one number in a dataset, and every<", ">Cambia un número en un conjunto de datos, y<"),
    (">document built from it should change too.<", ">cada documento hecho con él debería cambiar<"),
    (">This book shows how: you write prose and<", ">también. Este libro enseña cómo: escribes<"),
    (">code once, in plain text, and Quarto rebuilds<", ">prosa y código una vez, en texto plano, y<"),
    (">a web page, Word, PDF, slides, an e-book,<", ">Quarto reconstruye una página web, Word, PDF,<"),
    (">a website, a blog and a dashboard from that<", ">diapositivas, un libro electrónico, un sitio<"),
    (">one source. A coding agent writes the code<", ">web, un blog y un dashboard desde esa fuente.<"),
    (">at a speed that was out of reach until<", ">Un agente de programación escribe el código<"),
    (">recently; you direct it one small step at<", ">a una velocidad impensable hace poco; tú lo<"),
    (">a time and check its work against the data.<", ">diriges paso a paso y lo revisas con los datos.<"),
    (">TWO REAL PROJECTS<", ">DOS PROYECTOS REALES<"),
    (">A London visitor guide<", ">Una guía de Londres para visitantes<"),
    (">cited figures, maps and openly licensed photographs<", ">cifras citadas, mapas y fotos con licencia abierta<"),
    (">Drinking-water risk in Colombia<", ">El riesgo del agua potable en Colombia<"),
    (">public data for every municipality, explored and clustered<", ">datos públicos de cada municipio, explorados y agrupados<"),
    (">No programming is assumed.<", ">No se da por sentado que sepas programar.<"),
]


def translate(src: Path, dest: Path, pairs) -> None:
    text = src.read_text(encoding="utf-8")
    for pair in pairs:
        old, new, count = (*pair, 1) if len(pair) == 2 else pair
        found = text.count(old)
        if found != count:
            raise SystemExit(f"{src.name}: {old[:50]!r} found {found} times, expected {count}")
        text = text.replace(old, new)
    dest.write_text(text, encoding="utf-8")
    print("es", dest.relative_to(ROOT))


def main() -> None:
    (ES / "diagrams").mkdir(parents=True, exist_ok=True)
    for name, pairs in DIAGRAMS.items():
        translate(EN / "diagrams" / name, ES / "diagrams" / name, pairs)
    translate(EN / "cover.svg", ES / "cover.svg", COVER)
    translate(EN / "back-cover.svg", ES / "back-cover.svg", BACK_COVER)
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "book" / "scripts" / "roadmaps.py"), "--book", "../book-es"],
                   cwd=ROOT / "book", check=True)
    build.BOOK = ROOT / "book-es"   # for rasterise()'s messages
    build.rasterise(sorted([*(ES / "diagrams").glob("*.svg"), *(ES / "roadmaps").glob("*.svg")]), scale=2)
    build.rasterise([ES / "cover.svg", ES / "back-cover.svg"], scale=1, transparent=False)
    import segno
    url = build.LIVE + "es/chapters/06-audiences.html#sec-london-3d"
    (ES / "qr").mkdir(exist_ok=True)
    segno.make(url, error="m").save(ES / "qr" / "london-map.png", scale=8, border=2,
                                   dark="#13202e", light="#ffffff")
    print("qr london-map", url)


if __name__ == "__main__":
    main()
