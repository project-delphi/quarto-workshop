-- The deck's `description` as a <meta name="description"> tag.
--
-- Quarto (1.10) writes this tag on HTML pages but its Reveal.js template has no place for
-- it, so search engines and scripts/check_site.py would find no description on slides.html.
-- This filter adds the tag to the page head from the document's own `description`.

local function attribute(text)
  return (text:gsub("&", "&amp;"):gsub('"', "&quot;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

function Meta(meta)
  if quarto.doc.is_format("revealjs") and meta.description then
    local text = pandoc.utils.stringify(meta.description)
    quarto.doc.include_text("in-header",
      '<meta name="description" content="' .. attribute(text) .. '">')
  end
end
