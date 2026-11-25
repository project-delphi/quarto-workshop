# Code string literals changed in the Spanish edition

Written by `translation/compare.py`: every string literal in an executable cell that
differs between `book/` and `book-es/` (decision D3 in `PLAN.md`). Everything else
in the cells is identical. Review that each one only reaches the page.

| File | Cell | English | Spanish |
|---|--:|---|---|
| `appendices/e-checkpoints.qmd` | 2 | `"zeroth"` | `"cero"` |
| `appendices/e-checkpoints.qmd` | 2 | `"first"` | `"primer"` |
| `appendices/e-checkpoints.qmd` | 2 | `"second"` | `"segundo"` |
| `appendices/e-checkpoints.qmd` | 2 | `"third"` | `"tercer"` |
| `appendices/e-checkpoints.qmd` | 2 | `"fourth"` | `"cuarto"` |
| `appendices/e-checkpoints.qmd` | 2 | `"fifth"` | `"quinto"` |
| `appendices/e-checkpoints.qmd` | 2 | `"sixth"` | `"sexto"` |
| `appendices/e-checkpoints.qmd` | 2 | `"seventh"` | `"séptimo"` |
| `appendices/e-checkpoints.qmd` | 2 | `"eighth"` | `"octavo"` |
| `appendices/e-checkpoints.qmd` | 2 | `"ninth"` | `"noveno"` |
| `appendices/e-checkpoints.qmd` | 2 | `"tenth"` | `"décimo"` |
| `appendices/k-facts.qmd` | 1 | `"sources "` | `"fuentes "` |
| `appendices/k-facts.qmd` | 1 | `g · .2f · [source]( · ) · [ · ]( · )` | `g · .2f · [fuente]( · ) · [ · ]( · )` |
| `appendices/k-facts.qmd` | 2 | `##  ·  { · .unnumbered} · \n · ** · .**  · . Checked  · ,  · .\n` | `##  ·  { · .unnumbered} · \n · ** · .**  · . Consultado el  · ,  · .\n` |
| `appendices/k-facts.qmd` | 3 | `"\| Model \| Input / output, \\$ per million tokens \|"` | `"\| Modelo \| Entrada / salida (\\$) \|"` |
| `appendices/k-facts.qmd` | 3 | `\|  ·  \|  ·  /  ·  \| · \n:  · , checked  · . { · #tbl-prices} · \n · \n\nWhat each vendor says its model is for:\n\n::: cards · \n:   \" · \"\n · \nSources: Anthropic's [pricing]( · ) and [models]( · )  · pages and OpenAI's [models]( · ) pages.` | `\|  ·  \|  ·  /  ·  \| · \n:  · , consultados el  · . { · #tbl-prices} · \n · \n\nPara qué sirve cada modelo, según su proveedor:\n\n::: cards · \n:    · \n · \nFuentes: las páginas de [precios]( · ) y de [modelos]( · )  · de Anthropic, y la de [modelos]( · ) de OpenAI.` |
| `appendices/k-facts.qmd` | 4 | `"\| Host \| Free plan \|"` | `"\| Servicio de alojamiento \| Plan gratuito \|"` |
| `appendices/k-facts.qmd` | 4 | `\| [ · ]( · ) \|  ·  \| · \n: Free plans of six static hosts, checked on their official pages on  · . { · #tbl-hosts-free}` | `\| [ · ]( · ) \|  ·  \| · \n: Planes gratuitos de seis servicios de alojamiento estático, consultados en su web oficial el  · . { · #tbl-hosts-free}` |
| `chapters/04-markdown.qmd` | 1 | `"first"` | `"primero"` |
| `chapters/04-markdown.qmd` | 1 | `"second"` | `"segundo"` |
| `chapters/04-markdown.qmd` | 1 | `"third"` | `"tercero"` |
| `chapters/04-markdown.qmd` | 1 | `"fourth"` | `"cuarto"` |
| `chapters/04-markdown.qmd` | 1 | `"fifth"` | `"quinto"` |
| `chapters/04-markdown.qmd` | 1 | `"sixth"` | `"sexto"` |
| `chapters/04-markdown.qmd` | 1 | `"seventh"` | `"séptimo"` |
| `chapters/04-markdown.qmd` | 1 | `"eighth"` | `"octavo"` |
| `chapters/04-markdown.qmd` | 1 | `"ninth"` | `"noveno"` |
| `chapters/04-markdown.qmd` | 1 | `"tenth"` | `"décimo"` |
| `chapters/04-markdown.qmd` | 1 | `" and "` | `" y "` |
| `chapters/05-compute.qmd` | 12 | `"Visits in 2025"` | `"Visitas en 2025"` |
| `chapters/06-audiences.qmd` | 1 | `" and the "` | `" y el "` |
| `chapters/06-audiences.qmd` | 10 | `"Map"` | `"Mapa"` |
| `chapters/06-audiences.qmd` | 10 | `"Tilt: height is visits"` | `"Inclinado: la altura son las visitas"` |
| `chapters/06-audiences.qmd` | 10 | `"Up close: the five sights"` | `"De cerca: las cinco atracciones"` |
| `chapters/07-publish.qmd` | 1 | `"zeroth"` | `"cero"` |
| `chapters/07-publish.qmd` | 1 | `"first"` | `"primer"` |
| `chapters/07-publish.qmd` | 1 | `"second"` | `"segundo"` |
| `chapters/07-publish.qmd` | 1 | `"third"` | `"tercer"` |
| `chapters/07-publish.qmd` | 1 | `"fourth"` | `"cuarto"` |
| `chapters/07-publish.qmd` | 1 | `"fifth"` | `"quinto"` |
| `chapters/07-publish.qmd` | 1 | `"sixth"` | `"sexto"` |
| `chapters/07-publish.qmd` | 1 | `"seventh"` | `"séptimo"` |
| `chapters/07-publish.qmd` | 1 | `"eighth"` | `"octavo"` |
| `chapters/07-publish.qmd` | 1 | `"ninth"` | `"noveno"` |
| `chapters/07-publish.qmd` | 1 | `"tenth"` | `"décimo"` |
| `chapters/07-publish.qmd` | 8 | `"\| Page \| attrac­tions \| visits \| churches \| sights \|"` | `"\| Página \| attrac­tions \| visits \| churches \| sights \|"` |
| `chapters/07-publish.qmd` | 9 | `"slides"` | `"diapositivas"` |
| `chapters/07-publish.qmd` | 9 | `" and "` | `" y "` |
| `chapters/08-water-question.qmd` | 1 | `"zone"` | `"zona"` |
| `chapters/08-water-question.qmd` | 1 | `"municipality"` | `"municipio"` |
| `chapters/08-water-question.qmd` | 1 | `"water-risk index, utility-supplied (0–100); INS"` | `"índice de riesgo del agua, de prestadores (0–100); INS"` |
| `chapters/08-water-question.qmd` | 1 | `"Piped water"` | `"Acueducto"` |
| `chapters/08-water-question.qmd` | 1 | `"aqueduct coverage (%); TerriData"` | `"cobertura de acueducto (%); TerriData"` |
| `chapters/08-water-question.qmd` | 1 | `"Sewer"` | `"Alcantarillado"` |
| `chapters/08-water-question.qmd` | 1 | `"sewerage coverage (%); TerriData"` | `"cobertura de alcantarillado (%); TerriData"` |
| `chapters/08-water-question.qmd` | 1 | `"Poverty"` | `"Pobreza"` |
| `chapters/08-water-question.qmd` | 1 | `"people multidimensionally poor (%); 2018 census"` | `"personas en pobreza multidimensional (%); censo de 2018"` |
| `chapters/08-water-question.qmd` | 1 | `"Rural share"` | `"Proporción rural"` |
| `chapters/08-water-question.qmd` | 1 | `"rural share of the population (0–1); DANE"` | `"proporción rural de la población (0–1); DANE"` |
| `chapters/08-water-question.qmd` | 1 | `"Altitude"` | `"Altitud"` |
| `chapters/08-water-question.qmd` | 1 | `"the head town's height (m); SRTM"` | `"la altura de la cabecera (m); SRTM"` |
| `chapters/08-water-question.qmd` | 1 | `"Rainfall"` | `"Precipitación"` |
| `chapters/08-water-question.qmd` | 1 | `"rain over the municipality (mm a year); CHIRPS"` | `"lluvia sobre el municipio (mm al año); CHIRPS"` |
| `chapters/08-water-question.qmd` | 1 | `"municipal performance score (0–100); TerriData"` | `"puntaje de desempeño municipal (0–100); TerriData"` |
| `chapters/08-water-question.qmd` | 1 | `"water transfers (nominal pesos per person, logged); TerriData, DANE"` | `"transferencias para agua (pesos corrientes por persona, en logaritmo); TerriData, DANE"` |
| `chapters/08-water-question.qmd` | 1 | `"Infant mortality"` | `"Mortalidad infantil"` |
| `chapters/08-water-question.qmd` | 1 | `"deaths under one year per 1,000 live births; TerriData"` | `"muertes de menores de un año por cada 1,000 nacidos vivos; TerriData"` |
| `chapters/08-water-question.qmd` | 1 | `"mean exam score of the zone's schools (0–500); ICFES"` | `"puntaje medio del examen en los colegios de la zona (0–500); ICFES"` |
| `chapters/08-water-question.qmd` | 1 | `"School dropout"` | `"Deserción escolar"` |
| `chapters/08-water-question.qmd` | 1 | `"public-school pupils who leave during the year (%); MEN"` | `"estudiantes de colegios públicos que se retiran durante el año (%); MEN"` |
| `chapters/08-water-question.qmd` | 1 | `"municipality"` | `"municipio"` |
| `chapters/08-water-question.qmd` | 1 | `"zone"` | `"zona"` |
| `chapters/08-water-question.qmd` | 1 | `"municipality"` | `"municipio"` |
| `chapters/08-water-question.qmd` | 1 | `; one value · ; ` | `; un solo valor · ; ` |
| `chapters/08-water-question.qmd` | 2 | `"\| Variable \| Measures (unit); source \| Level; years \|"` | `"\| Variable \| Mide (unidad); fuente \| Nivel; años \|"` |
| `chapters/10-prepare.qmd` | 3 | `"\| Feature \| Difference \| Share, raw \| Share, z \|"` | `"\| Característica \| Diferencia \| Proporción, original \| Proporción, z \|"` |
| `chapters/11-cluster.qmd` | 1 | `"first"` | `"primer"` |
| `chapters/11-cluster.qmd` | 1 | `"second"` | `"segundo"` |
| `chapters/11-cluster.qmd` | 1 | `"third"` | `"tercer"` |
| `chapters/11-cluster.qmd` | 1 | `"fourth"` | `"cuarto"` |
| `chapters/11-cluster.qmd` | 1 | `"fifth"` | `"quinto"` |
| `chapters/11-cluster.qmd` | 1 | `"sixth"` | `"sexto"` |
| `chapters/11-cluster.qmd` | 1 | `"seventh"` | `"séptimo"` |
| `chapters/11-cluster.qmd` | 1 | `"eighth"` | `"octavo"` |
| `chapters/11-cluster.qmd` | 1 | `"ninth"` | `"noveno"` |
| `chapters/11-cluster.qmd` | 1 | `"tenth"` | `"décimo"` |
| `chapters/11-cluster.qmd` | 1 | `"rules out nothing here"` | `"no descarta nada aquí"` |
| `chapters/11-cluster.qmd` | 1 | `"rules out only k = "` | `"aquí solo descarta k = "` |
| `chapters/11-cluster.qmd` | 1 | `" and "` | `" y "` |
| `chapters/11-cluster.qmd` | 1 | `" here"` | `""` |
| `chapters/11-cluster.qmd` | 1 | `"clusters "` | `"los clústeres "` |
| `chapters/11-cluster.qmd` | 1 | `"excluded: the urban–rural split"` | `"excluido: la separación urbana–rural"` |
| `chapters/11-cluster.qmd` | 1 | `"silhouette too far below the best"` | `"silueta demasiado por debajo de la mejor"` |
| `chapters/11-cluster.qmd` | 1 | `"chosen: the smallest that passes"` | `"elegido: el más pequeño que pasa"` |
| `chapters/11-cluster.qmd` | 1 | `"passes, but larger"` | `"pasa, pero es más grande"` |
| `chapters/11-cluster.qmd` | 1 | `"chosen: the smallest that passes"` | `"elegido: el más pequeño que pasa"` |
| `chapters/11-cluster.qmd` | 1 | `"chosen"` | `"elegido"` |
| `chapters/11-cluster.qmd` | 1 | `"IRCA"` | `"el IRCA"` |
| `chapters/11-cluster.qmd` | 1 | `"piped-water coverage"` | `"la cobertura de acueducto"` |
| `chapters/11-cluster.qmd` | 1 | `"sewer coverage"` | `"la cobertura de alcantarillado"` |
| `chapters/11-cluster.qmd` | 1 | `"poverty"` | `"la pobreza"` |
| `chapters/11-cluster.qmd` | 1 | `"rural share"` | `"la proporción rural"` |
| `chapters/11-cluster.qmd` | 1 | `"altitude"` | `"la altitud"` |
| `chapters/11-cluster.qmd` | 1 | `"rainfall"` | `"la precipitación"` |
| `chapters/11-cluster.qmd` | 1 | `"MDM"` | `"la MDM"` |
| `chapters/11-cluster.qmd` | 1 | `"SGP"` | `"el SGP"` |
| `chapters/11-cluster.qmd` | 1 | `" and "` | `" y "` |
| `chapters/11-cluster.qmd` | 1 | `'rises'` | `'sube'` |
| `chapters/11-cluster.qmd` | 1 | `'falls'` | `'baja'` |
| `chapters/11-cluster.qmd` | 1 | `"sits below the others"` | `"queda por debajo de los demás"` |
| `chapters/11-cluster.qmd` | 1 | `cluster  ·  and  · all  ·  of its zone-years, urban and rural, fall in  · its urban zone-years fall in  ·  and its rural ones in  · one more still cuts  · .0% ·  or more ·  with ` | `el clúster  ·  y  · sus  ·  zonas-año, urbanas y rurales, caen todas en  · sus zonas-año urbanas caen en  ·  y las rurales en  · uno más todavía recorta un  · .0% ·  o más ·  con ` |
| `chapters/11-cluster.qmd` | 2 | `"The four steps are listed above."` | `"Los cuatro pasos se enumeran arriba."` |
| `chapters/11-cluster.qmd` | 5 | `"\| k \| One more cluster cuts \| Silhouette \| Verdict \|"` | `"\| k \| Un clúster más recorta \| Silueta \| Veredicto \|"` |
| `chapters/11-cluster.qmd` | 7 | `"The 2-D picture is the figure above."` | `"La imagen 2-D es la figura de arriba."` |
| `chapters/11-cluster.qmd` | 7 | `"Face on: the 2-D picture"` | `"De frente: la imagen 2-D"` |
| `chapters/11-cluster.qmd` | 7 | `"Turn: PC3 comes forward"` | `"Girar: PC3 viene al frente"` |
| `chapters/11-cluster.qmd` | 7 | `"PC3 upright"` | `"PC3 en vertical"` |
| `chapters/11-cluster.qmd` | 8 | `"Map"` | `"Mapa"` |
| `chapters/11-cluster.qmd` | 8 | `"Tilt: height is altitude"` | `"Inclinado: la altura es la altitud"` |
| `chapters/11-cluster.qmd` | 8 | `"Into the highlands"` | `"Hacia las tierras altas"` |
| `chapters/12-interpret.qmd` | 1 | `"piped-water coverage"` | `"cobertura de acueducto"` |
| `chapters/12-interpret.qmd` | 1 | `"sewer coverage"` | `"cobertura de alcantarillado"` |
| `chapters/12-interpret.qmd` | 1 | `"poverty"` | `"pobreza"` |
| `chapters/12-interpret.qmd` | 1 | `"rural share"` | `"proporción rural"` |
| `chapters/12-interpret.qmd` | 1 | `"altitude"` | `"altitud"` |
| `chapters/12-interpret.qmd` | 1 | `"rainfall"` | `"precipitación"` |
| `chapters/12-interpret.qmd` | 1 | `"municipal performance"` | `"desempeño municipal"` |
| `chapters/12-interpret.qmd` | 1 | `"water transfers"` | `"transferencias para agua"` |
| `chapters/12-interpret.qmd` | 1 | `z_ ·  ·  ·  ( · +.1f ·  SD) · _mean · cluster  ·  ( · )` | `z_ ·  ·  ·  ( · +.1f ·  DE) · _mean · clúster  ·  ( · )` |
| `chapters/12-interpret.qmd` | 2 | `"infant mortality"` | `"la mortalidad infantil"` |
| `chapters/12-interpret.qmd` | 2 | `"exam scores"` | `"los puntajes del examen"` |
| `chapters/12-interpret.qmd` | 2 | `"dropout"` | `"la deserción"` |
| `chapters/12-interpret.qmd` | 2 | `" and "` | `" y "` |
| `chapters/12-interpret.qmd` | 2 | `"low-coverage"` | `"baja cobertura"` |
| `chapters/12-interpret.qmd` | 2 | `"poverty"` | `"pobreza"` |
| `chapters/12-interpret.qmd` | 2 | `"2017–2019 and 2021–2023"` | `"2017–2019 y 2021–2023"` |
| `chapters/12-interpret.qmd` | 2 | `"Cities and large towns"` | `"Ciudades y pueblos grandes"` |
| `chapters/12-interpret.qmd` | 2 | `"Highland towns"` | `"Pueblos de tierras altas"` |
| `chapters/12-interpret.qmd` | 2 | `"Lowland towns"` | `"Pueblos de tierras bajas"` |
| `chapters/12-interpret.qmd` | 4 | `"\| \| Kind \| Zone-years \| Municipalities \| Median IRCA (0–100) \|"` | `"\| \| Tipo \| Zonas-año \| Municipios \| Mediana del IRCA (0–100) \|"` |
| `chapters/12-interpret.qmd` | 5 | `" (filled)"` | `" (llenada)"` |
| `chapters/12-interpret.qmd` | 5 | `+.1f · _imputed · \| Feature \| Tunja, rural \| Centre  ·  \| Centre  ·  \| · its own  · the shared  · \|  ·  \|  ·  \|  ·  \|  ·  \| · \| *Squared distance,  · * \| \| * · .1f · * \| * · .1f · * \| · \| **Squared distance, all  · ** \| \| ** · .1f · ** \| ** · .1f · ** \|` | `+.1f · _imputed · \| Característica \| Tunja, rural \| Centro  ·  \| Centro  ·  \| · sus  ·  propias · las  ·  compartidas · \|  ·  \|  ·  \|  ·  \|  ·  \| · \| *Distancia al cuadrado,  · * \| \| * · .1f · * \| * · .1f · * \| · \| **Distancia al cuadrado, las  · ** \| \| ** · .1f · ** \| ** · .1f · ** \|` |
| `chapters/12-interpret.qmd` | 6 | `"Infant mortality\nper 1,000 births"` | `"Mortalidad infantil\npor 1,000 nacidos vivos"` |
| `chapters/12-interpret.qmd` | 6 | `"Saber 11\nmean score"` | `"Saber 11\npuntaje medio"` |
| `chapters/12-interpret.qmd` | 6 | `"School dropout\n(%)"` | `"Deserción escolar\n(%)"` |
| `chapters/12-interpret.qmd` | 7 | `"Infant mortality\nper 1,000 (lower is better)"` | `"Mortalidad infantil\npor 1,000 (menos es mejor)"` |
| `chapters/12-interpret.qmd` | 7 | `"Saber 11 score\n(higher is better)"` | `"Puntaje Saber 11\n(más es mejor)"` |
| `chapters/12-interpret.qmd` | 7 | `"Dropout %\n(lower is better)"` | `"Deserción %\n(menos es mejor)"` |
| `chapters/12-interpret.qmd` | 8 | `Box plots of  · , one per cluster. Medians:  · cluster  ·  ( · )  · .1f · cluster  ·  no data` | `Diagramas de caja de  · , uno por clúster. Medianas:  · clúster  ·  ( · )  · .1f · clúster  ·  sin datos` |
| `chapters/13-causation.qmd` | 2 | `"2017–2019 and 2021–2023"` | `"2017–2019 y 2021–2023"` |
| `chapters/13-causation.qmd` | 2 | `"Poverty"` | `"Pobreza"` |
| `chapters/13-causation.qmd` | 2 | `"Rural share"` | `"Proporción rural"` |
| `chapters/13-causation.qmd` | 2 | `"Piped-water coverage"` | `"Cobertura de acueducto"` |
| `chapters/13-causation.qmd` | 2 | `"Altitude"` | `"Altitud"` |
| `chapters/13-causation.qmd` | 2 | `"clusters "` | `"los clústeres "` |
| `chapters/13-causation.qmd` | 2 | `cluster  ·  and  · .1f` | `el clúster  ·  y  · .1f` |
| `chapters/13-causation.qmd` | 4 | `"\| Feature \| "` | `"\| Característica \| "` |
| `chapters/13-causation.qmd` | 5 | `"N"` | `"S"` |
| `chapters/13-causation.qmd` | 5 | `"L"` | `"B"` |
| `chapters/13-causation.qmd` | 5 | `"H"` | `"A"` |
| `chapters/13-causation.qmd` | 5 | `"U"` | `"I"` |
| `chapters/13-causation.qmd` | 5 | `"IRCA band: N no risk · L low · M medium · H high · U unfit"` | `"Nivel del IRCA: S sin riesgo · B bajo · M medio · A alto · I inviable"` |
| `chapters/13-causation.qmd` | 5 | `"IRCA band: N no risk · L low · M medium\nH high · U unfit"` | `"Nivel del IRCA: S sin riesgo · B bajo · M medio\nA alto · I inviable"` |
| `chapters/13-causation.qmd` | 6 | `"\| \| n \| ρ \| 95% interval \| SD of IRCA \|"` | `"\| \| n \| ρ \| Intervalo del 95% \| DE del IRCA \|"` |
| `chapters/13-causation.qmd` | 6 | ` to  · \| All places \|  ·  \|  ·  \|  ·  \|  · .1f ·  \| · \| Cluster  ·  \|  ·  \|  ·   · \|  ·  \|  · .1f ·  \|` | ` a  · \| Todos los lugares \|  ·  \|  ·  \|  ·  \|  · .1f ·  \| · \| Clúster  ·  \|  ·  \|  ·   · \|  ·  \|  · .1f ·  \|` |
| `chapters/14-publish-many.qmd` | 14 | `"none"` | `"ninguno"` |
| `chapters/14-publish-many.qmd` | 14 | `"\| Page \| Reads `outputs/` \| Reads `data/` \| Writes \|"` | `"\| Página \| Lee `outputs/` \| Lee `data/` \| Escribe \|"` |
| `chapters/14-publish-many.qmd` | 14 | `"the post"` | `"la entrada"` |
| `chapters/14-publish-many.qmd` | 14 | `"none"` | `"ninguno"` |
| `chapters/14-publish-many.qmd` | 14 | ` file · ` · ` · \|  ·  \|  ·  \|  ·  \|  ·  \|` | ` archivo · ` · ` · \|  ·  \|  ·  \|  ·  \|  ·  \|` |
| `chapters/exercises-london.qmd` | 2 | `\| Attraction \| Visits in  ·  \| · \|  ·  \|  · , ·  \| · \n: Visits in  ·  to five ALVA member attractions. One cell is wrong.` | `\| Atracción \| Visitas en  ·  \| · \|  ·  \|  · , ·  \| · \n: Visitas en  ·  a cinco atracciones miembro de ALVA. Una celda está mal.` |
| `chapters/exercises-water.qmd` | 1 | `"no-risk water"` | `"agua sin riesgo"` |
| `chapters/results.qmd` | 4 | `"\| Age band \| Test contacts \| Called \| Subscription rate \| Recall \|"` | `"\| Franja de edad \| Contactos de prueba \| Llamados \| Tasa de suscripción \| Recall \|"` |
| `chapters/results.qmd` | 6 | `"Mean predicted probability"` | `"Probabilidad predicha media"` |
| `chapters/results.qmd` | 6 | `"Observed subscription rate"` | `"Tasa de suscripción observada"` |
| `chapters/slides.qmd` | 1 | `"body"` | `"cuerpo"` |
| `chapters/slides.qmd` | 1 | `"headings"` | `"títulos"` |
| `chapters/slides.qmd` | 1 | `"links"` | `"enlaces"` |
| `chapters/slides.qmd` | 1 | `"captions, footer"` | `"pies de figura, pie de página"` |
| `chapters/slides.qmd` | 1 | `"\u2019"` | `"’"` |
| `chapters/slides.qmd` | 2 | `. ` | `. [ · ]{ · lang=en translate=no}` |
| `chapters/slides.qmd` | 5 | `"\| Text \| Colour \| Contrast on the background \|"` | `"\| Texto \| Color \| Contraste sobre el fondo \|"` |
| `chapters/slides.qmd` | 5 | `\|  ·  \| ` · ` \|  · .1f · :1 \| · \n: The finished theme's text colours on its background, ` · `, computed with the WCAG 2.2 formula, from the variables its test checks. { · #tbl-slides-contrast}` | `\|  ·  \| ` · ` \|  · .1f · :1 \| · \n: Los colores de texto del tema terminado sobre su fondo, ` · `, calculados con la fórmula de WCAG 2.2, a partir de las variables que comprueba su prueba. { · #tbl-slides-contrast}` |
| `chapters/team.qmd` | 1 | `" and "` | `" y "` |
| `chapters/team.qmd` | 6 | `\| `version` \| `value` \| `low`, `high` (the  ·  interval) \|\n\|---\|--:\|--:\| · \|  ·  \|  ·  \|  · ,  ·  \|` | `\| `version` \| `value` \| `low`, `high` (el intervalo del  · ) \|\n\|---\|--:\|--:\| · \|  ·  \|  ·  \|  · ,  ·  \|` |
| `chapters/white-papers.qmd` | 1 | `"all of them"` | `"todos"` |
| `chapters/white-papers.qmd` | 1 | `@ · -[\w-]+ ·   · @ · @ ·  of them` | `@ · -[\w-]+ ·   · @ · @ ·  de ellos` |
| `chapters/white-papers.qmd` | 5 | `"\| Key \| Year \| Cited by \|"` | `"\| Clave \| Año \| Lo citan \|"` |
| `chapters/white-papers.qmd` | 5 | `"card"` | `"ficha"` |
| `chapters/white-papers.qmd` | 5 | `"\n: The project's references, from the finished `references.bib`, and the documents that cite each. {#tbl-wp-refs}"` | `"\n: Las referencias del `references.bib` terminado, y los documentos que citan cada una. {#tbl-wp-refs}"` |
