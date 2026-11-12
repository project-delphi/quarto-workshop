-- Animated figures (book/PLAN.md §4). Write a GIF as
--   ![Caption.](../media/gifs/name.gif){#fig-name .anim fig-alt="..."}
-- The EPUB keeps the GIF: readers that animate play it, the others show its first frame,
-- which each GIF is designed to make a usable still. In HTML the image becomes a <picture>
-- whose reduced-motion source is the still (media/stills/name.png, from `make media`), so
-- readers who ask their system for less motion get the still. Runs after Quarto has built
-- the figure, so numbering and captions are unchanged.

if not quarto.doc.is_format("html:js") then return {} end

local function escape(s)
  return (s:gsub("&", "&amp;"):gsub('"', "&quot;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

return {
  Image = function(img)
    if not img.classes:includes("anim") then return nil end
    local still = img.src:gsub("/gifs/", "/stills/"):gsub("%.gif$", ".png")
    local alt = img.attributes["fig-alt"] or pandoc.utils.stringify(img.caption)
    return pandoc.RawInline("html", string.format(
      '<picture><source srcset="%s" media="(prefers-reduced-motion: reduce)">' ..
      '<img src="%s" alt="%s" class="anim img-fluid" loading="lazy"></picture>',
      still, img.src, escape(alt)))
  end,
}
