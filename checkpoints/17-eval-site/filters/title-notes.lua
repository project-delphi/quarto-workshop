-- Speaker notes for the title slide, written once for both slide formats.
--
-- A `::: {.notes}` div placed before the first slide heading is the title slide's notes.
-- PowerPoint (pandoc's pptx writer) already attaches it to the title slide. Reveal.js would
-- make a blank slide of it, so for revealjs this filter removes the div and passes its text
-- to the title slide as Reveal's `data-notes` attribute (plain text, no formatting).

function Pandoc(doc)
  if not quarto.doc.is_format("revealjs") then
    return nil
  end
  for i, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      return nil -- no notes before the first slide
    end
    if block.t == "Div" and block.classes:includes("notes") then
      local attributes = doc.meta["title-slide-attributes"] or pandoc.MetaMap({})
      attributes["data-notes"] = pandoc.utils.stringify(block)
      doc.meta["title-slide-attributes"] = attributes
      doc.blocks:remove(i)
      return doc
    end
  end
end
