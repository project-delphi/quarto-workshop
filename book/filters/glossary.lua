-- Glossary links (book/README.md, "Conventions").
--
-- A term the book defines is set in italics where it first appears ("*YAML*, a format for
-- settings ..."), and listed in the glossary appendix (appendices/j-glossary.qmd). This filter
-- joins the two:
--
-- 1. In the glossary, each term gets an anchor, `gl-` and the term in lower case with
--    hyphens (`gl-yaml`, `gl-adjusted-rand-index-ari`), so a link can land on it.
-- 2. In every other page, the first italic phrase that is a glossary term, word for word
--    (case aside; a term's bracketed abbreviation may be left out), links to that anchor.
--    Only the first: a page that links every use reads like a web of footnotes. Headings,
--    links and code are left alone.
--
-- The term list is read from the glossary's source when the filter starts, so a new entry
-- links itself everywhere at the next render. English edition only for now: the Spanish
-- edition's glossary has its own terms (translation/PLAN.md, section 8).

local GLOSSARY = "appendices/j-glossary.qmd"

local function slug(text)
  return "gl-" .. text:lower():gsub("[^%w]+", "-"):gsub("^%-+", ""):gsub("%-+$", "")
end

-- A unique anchor for each term, in the glossary's order: two terms that differ only in case
-- ("path" and "PATH") get "gl-path" and "gl-path-2". Used for both the anchors and the links.
local function anchors_for(terms)
  local used, out = {}, {}
  for _, term in ipairs(terms) do
    local id, n = slug(term), 1
    while used[id] do n = n + 1; id = slug(term) .. "-" .. n end
    used[id] = true
    out[#out + 1] = id
  end
  return out
end

-- Terms from the glossary's source: a definition list, each term on its own line followed
-- by a line starting ":   ". Maps each form a reader may write to its anchor: the exact text
-- first, then its lower-case form unless another term has it, then the term without its
-- bracketed abbreviation.
local function read_terms()
  local dir = quarto.project.directory or "."
  local file = io.open(dir .. "/" .. GLOSSARY, "r")
  if not file then return {} end
  local lines = {}
  for line in file:lines() do lines[#lines + 1] = line end
  file:close()
  local list = {}
  for i = 1, #lines - 1 do
    local term = lines[i]
    local nxt = lines[i + 1] == "" and lines[i + 2] or lines[i + 1]
    if term ~= "" and nxt and nxt:match("^:%s%s%s") and not term:match("^[:#]") then
      list[#list + 1] = (term:gsub("`", ""))
    end
  end
  local ids = anchors_for(list)
  local exact, lower = {}, {}
  for i, plain in ipairs(list) do
    exact[plain] = ids[i]
    lower[plain:lower()] = lower[plain:lower()] or ids[i]
    local short = plain:gsub("%s*%b()%s*$", "")
    if short ~= plain then lower[short:lower()] = lower[short:lower()] or ids[i] end
  end
  return exact, lower
end

local function relative_glossary()
  local input = quarto.doc.input_file or ""
  if input:match("/chapters/[^/]+$") then return "../" .. GLOSSARY end
  if input:match("/appendices/[^/]+$") then return "j-glossary.qmd" end
  return GLOSSARY
end

-- The HTML edition renders each page as its own document, the glossary included; the EPUB
-- renders the whole book as one document. So the filter works chapter by chapter, a chapter
-- being everything from one level-1 heading to the next: inside the glossary's chapter it adds
-- the anchors, elsewhere it links each chapter's first use, to the glossary page in HTML and to
-- the anchor itself in the one-document EPUB.
function Pandoc(doc)
  local lang = doc.meta.lang and pandoc.utils.stringify(doc.meta.lang) or "en"
  if lang:match("^es") then return nil end

  local chapters = 0
  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 1 then chapters = chapters + 1 end
  end
  local whole_book = chapters > 1
  local exact, lower = read_terms()
  local target = whole_book and "" or relative_glossary()

  -- Anchors, in the glossary's order (anchors_for gives the same ids as read_terms).
  local names = {}
  local in_glossary = false
  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 1 then in_glossary = b.identifier == "sec-glossary" end
    if in_glossary then
      pandoc.Blocks({ b }):walk({ DefinitionList = function(dl)
        for _, item in ipairs(dl.content) do names[#names + 1] = pandoc.utils.stringify(item[1]) end
      end })
    end
  end
  local ids, k = anchors_for(names), 0

  local seen = {}
  local function skip(el) return el, false end
  local link_terms = {
    traverse = "topdown",
    Header = skip, Link = skip, Code = skip, CodeBlock = skip, Image = skip,
    Emph = function(em)
      local text = pandoc.utils.stringify(em)
      local anchor = exact[text] or lower[text:lower()]
      if not anchor or seen[anchor] then return nil end
      seen[anchor] = true
      return pandoc.Link({ em }, target .. "#" .. anchor, "", { class = "glossary-link" }), false
    end,
  }
  local add_anchors = { DefinitionList = function(dl)
    for _, item in ipairs(dl.content) do
      k = k + 1
      item[1] = { pandoc.Span(item[1], { id = ids[k] }) }
    end
    return dl
  end }

  local out = pandoc.Blocks({})
  in_glossary = false
  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 1 then
      in_glossary = b.identifier == "sec-glossary"
      seen = {}
    end
    local walked = pandoc.Blocks({ b }):walk(in_glossary and add_anchors or link_terms)
    out:extend(walked)
  end
  doc.blocks = out
  return doc
end
