// Acme's house template for white papers (Quarto 1.10.20, Typst).
//
// This file replaces one of Quarto's Typst template partials, `typst-show.typ`, the one that
// applies the page style to the document; whitepaper.qmd names it under `template-partials`.
// Quarto writes it after `_brand.yml`'s definitions (`brand-color`, `brand-logo`), so it can
// use them, and before the body, so the body can call `whitepaper-abstract`. Names between
// dollar signs are Pandoc template variables, filled from the YAML (write $$ for a dollar).
//
// It gives the PDF a title block (logo, a "Technical white paper" label, title, subtitle,
// company and date), a running header from page 2 and a footer with page numbers, in the
// brand's colours. Fonts, section numbers and heading colours still come from Quarto's own
// `article` function and _brand.yml.

// The brand's colours, by role (_brand.yml).
#let house-accent = brand-color.primary   // navy: label, title and rules
#let house-muted = brand-color.secondary  // slate: subtitle, header and footer
#let house-rule = brand-color.stone       // hairlines

// The abstract, set apart from the body. whitepaper.qmd opens it in one raw Typst block,
// `#whitepaper-abstract[`, and closes it in another, `]`, so the text between them can
// hold inline Python.
#let whitepaper-abstract(body) = block(
  width: 100%, inset: (x: 1.2em, y: 1em), above: 0em, below: 1.6em,
  fill: brand-color-background.stone, radius: 2pt,
)[
  #set par(justify: true)
  #text(weight: 700, fill: house-accent)[Abstract] #h(0.6em) #body
]

#let whitepaper(
  title: none, subtitle: none, date: none,
  company: none, label: [Technical white paper],
  logo: none, logo-alt: none,
  doc,
) = {
  set document(title: title)  // the PDF's title (article sets it only when it draws one)
  // The header names the paper from page 2 on; every footer carries the page number.
  set page(
    background: none,  // Quarto's page.typ puts the brand logo on every page; here it is in the title block
    header: context if counter(page).get().first() > 1 {
      set text(size: 0.8em, fill: house-muted)
      grid(columns: (1fr, auto), title, company)
      v(-0.4em)
      line(length: 100%, stroke: 0.5pt + house-rule)
    },
    footer: context {
      set text(size: 0.8em, fill: house-muted)
      line(length: 100%, stroke: 0.5pt + house-rule)
      v(-0.4em)
      grid(columns: (1fr, auto), [#label · #company],
           // "page" stays outside the numbering pattern: Typst would read its letters
           // (the "a") as a counter.
           [page #counter(page).display("1 of 1", both: true)])
    },
  )
  // Tables: smaller type, and no justified stretching inside cells.
  show table: set text(size: 0.9em)
  show table: set par(justify: false)
  // The title block, on page 1 only.
  block(width: 100%, below: 1.8em)[
    #grid(columns: (1fr, auto), align: (left + horizon, right + horizon),
      if logo != none { image(logo, height: 1.1cm, alt: logo-alt) },
      text(size: 0.8em, weight: 700, fill: house-accent, tracking: 0.08em, upper(label)))
    #v(0.8em)
    #line(length: 100%, stroke: 1.2pt + house-accent)
    #v(0.6em)
    #set par(justify: false, leading: 0.5em)
    #text(size: 1.9em, weight: 700, fill: house-accent, hyphenate: false, title)
    #if subtitle != none { v(0.3em); text(size: 1.1em, fill: house-muted, subtitle) }
    #v(0.6em)
    #text(size: 0.9em)[#company #h(0.5em) · #h(0.5em) #date]
  ]
  doc
}

// Quarto's own article function sets the language, fonts and section numbers; it gets no
// title, so it draws no title block of its own.
#show: doc => article(
$if(lang)$
  lang: "$lang$",
$endif$
$if(region)$
  region: "$region$",
$endif$
$if(brand.typography.base.family)$
  font: $brand.typography.base.family$,
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
$if(section-numbering)$
  sectionnumbering: "$section-numbering$",
$endif$
  doc,
)

#show: doc => whitepaper(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(date)$
  date: [$date$],
$endif$
$if(company)$
  company: [$company$],  // the document's `company`: _brand.yml's meta does not reach templates
$endif$
  logo: "/" + brand-logo.medium.path,
  logo-alt: brand-logo.medium.alt,
  doc,
)
