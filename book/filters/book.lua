-- Book conventions (book/PLAN.md §5.2–5.3), for both editions.
--
-- 1. Agent boxes. Consecutive ::: {.prompt}, ::: {.agent} and ::: {.you} divs are
--    wrapped in one ::: {.agent-box} (an explicit .agent-box is kept), and each part gets
--    its label as real text, so the EPUB needs neither CSS content nor JavaScript:
--      .prompt  "Ask your coding agent"  (the exact prompt, in a `default` fence)
--      .agent   "Expect it to run"           (what the agent will probably run)
--      .you     "You do"                     (the few steps only the reader can take)
-- 2. Asides. ::: why, ::: pitfall, ::: practice and ::: tryit become Quarto callouts
--    with fixed titles; the class stays for styling.
-- 3. Exercise lines. ::: done is prefixed "You're done when"; ::: catchup is labelled. A
--    catch-up box stands where its checkpoint's state is reached, so the reader carries on
--    from the box (the checkpoint's README names the workshop slide at the same point). The
--    first box of a chapter says in full what pasting the line does; later ones say it in a
--    line (PLAN-improvement-briefs.md §1, rule 6).
-- 4. Dates. An ISO date in prose (2026-11-12) is wrapped in a .nowrap span, so a narrow
--    screen never breaks it at a hyphen.
-- 5. Chapter openers. ::: opener holds the chapter's objectives (a bullet list, each item
--    starting with a verb) and, for hands-on chapters, a definition list whose terms are
--    "Start from", "You build" and "Checkpoint". It is labelled "In this chapter", and the
--    definition list becomes labelled paragraphs, which every reader lays out the same way.
-- 6. Pause and think. ::: think holds a question (its first block) and the answer (the rest).
--    It is labelled "Pause and think"; the answer goes in a .think-answer div labelled
--    "Answer", set apart so a reader can stop and answer first.
-- 7. Key ideas. ::: keyideas holds a chapter summary's list of takeaways; it only styles them.
-- 11. Stories. ::: story is a short incident a reader could meet in that chapter, labelled
--    "From the build log" (true, with a <!-- source: … --> comment naming where it is recorded),
--    or, with the class .illustration, "An illustration" (a composite scene with no invented
--    numbers or results). PLAN-improvement.md §2, D2.
-- 12. Cards. ::: cards holds a definition list; each term and its definitions become one
--    .card, which the EPUB keeps on one page while the list may break between cards (a table
--    too long for a page, set as cards). A title="…" attribute adds a label kept with the
--    first card; ::: {.cards .ledger title="…"} is Part V's Tunja ledger.
-- 13. Payoff. ::: payoff holds the picture of a chapter's finished output, labelled
--    "What you will build", kept with the picture.

-- 10. Language. Every label above is written in the document's `lang`: English, or the
--    Spanish edition's (book-es/, translation/glossary.md) when `lang` starts "es".
local LABELS = {
  en = {
    prompt = "Ask your coding agent", agent = "Expect it to run", you = "You do",
    why = "Why this works", pitfall = "Common pitfall", practice = "In practice", tryit = "Try it",
    opener = "In this chapter", think = "Pause and think", answer = "Answer",
    done = "You’re done when", stuck = "Stuck for two minutes?",
    catchup = "Paste this into your agent. It backs up your work and brings the project to "
      .. "this point; then carry on from here.",
    catchup_again = "Paste this into your agent, then carry on from here.",
    story = "From the build log", illustration = "An illustration", payoff = "What you will build",
  },
  es = {
    prompt = "Pídele a tu agente", agent = "Probablemente ejecute", you = "Tú haces",
    why = "Por qué funciona", pitfall = "Error frecuente", practice = "En la práctica", tryit = "Pruébalo",
    opener = "En este capítulo", think = "Detente y piensa", answer = "Respuesta",
    done = "Has terminado si", stuck = "¿Dos minutos sin avanzar?",
    catchup = "Pega esto en tu agente, que respalda tu trabajo y lleva el proyecto hasta "
      .. "este punto; luego sigue leyendo desde aquí.",
    catchup_again = "Pega esto en tu agente y luego sigue leyendo desde aquí.",
    story = "De la bitácora del proyecto", illustration = "Una ilustración",
    payoff = "Lo que vas a construir",
  },
}
local L = LABELS.en

local BOX = {}
local ASIDE = {}
local catchups = 0  -- catch-up boxes seen so far in this chapter (3)
local function set_language(meta)
  local lang = meta.lang and pandoc.utils.stringify(meta.lang) or ""
  L = lang:match("^es") and LABELS.es or LABELS.en
  BOX = { prompt = L.prompt, agent = L.agent, you = L.you }
  ASIDE = {
    why = { "callout-note", L.why },
    pitfall = { "callout-warning", L.pitfall },
    practice = { "callout-tip", L.practice },
    tryit = { "callout-important", L.tryit },
  }
end

-- A part already labelled (inside an .agent-box) carries data-boxed and is not regrouped.
local function box_kind(block)
  if block.t ~= "Div" or block.attributes.boxed then return nil end
  for kind in pairs(BOX) do
    if block.classes:includes(kind) then return kind end
  end
  return nil
end

local function label(kind, block)
  if block.attributes.boxed then return block end
  block.attributes.boxed = "true"
  block.content:insert(1, pandoc.Div({ pandoc.Plain({ pandoc.Strong(BOX[kind]) }) },
    pandoc.Attr("", { "box-label" })))
  return block
end

local function label_children(div)
  for i, child in ipairs(div.content) do
    if child.t == "Div" and not child.attributes.boxed then
      for kind in pairs(BOX) do
        if child.classes:includes(kind) then div.content[i] = label(kind, child) end
      end
    end
  end
  return div
end

-- Group runs of box divs that are not already inside an .agent-box.
local function group_boxes(blocks)
  local out, run = pandoc.Blocks({}), pandoc.Blocks({})
  local function flush()
    if #run > 0 then
      out:insert(label_children(pandoc.Div(run, pandoc.Attr("", { "agent-box" }))))
      run = pandoc.Blocks({})
    end
  end
  for _, block in ipairs(blocks) do
    if box_kind(block) then
      run:insert(block)
    else
      flush()
      out:insert(block)
    end
  end
  flush()
  return out
end

local function labelled(text, class)
  return pandoc.Div({ pandoc.Plain({ pandoc.Strong(text) }) }, pandoc.Attr("", { class or "box-label" }))
end

-- ::: opener: "In this chapter", the objectives, then Start from / You build / Checkpoint.
local function opener(div)
  local out = pandoc.Blocks({ labelled(L.opener) })
  for _, block in ipairs(div.content) do
    if block.t == "DefinitionList" then
      local meta = pandoc.Blocks({})
      for _, item in ipairs(block.content) do
        local term, defs = item[1], item[2]
        -- No space after the label: its fixed width is the gap, so wrapped lines align.
        local para = pandoc.Inlines({ pandoc.Span({ pandoc.Strong(term) }, pandoc.Attr("", { "meta-label" })) })
        for i, def in ipairs(defs) do
          for _, b in ipairs(def) do
            if b.t == "Para" or b.t == "Plain" then
              if i > 1 then para:insert(pandoc.Space()) end
              para:extend(b.content)
            end
          end
        end
        meta:insert(pandoc.Para(para))
      end
      out:insert(pandoc.Div(meta, pandoc.Attr("", { "opener-meta" })))
    else
      out:insert(block)
    end
  end
  div.content = out
  return div
end

-- ::: think: the question, then the answer under its own label.
local function think(div)
  local question, answer = pandoc.Blocks({}), pandoc.Blocks({ labelled(L.answer, "think-answer-label") })
  for i, block in ipairs(div.content) do
    if i == 1 then question:insert(block) else answer:insert(block) end
  end
  local out = pandoc.Blocks({ labelled(L.think) })
  out:insert(pandoc.Div(question, pandoc.Attr("", { "think-question" })))
  if #answer > 1 then out:insert(pandoc.Div(answer, pandoc.Attr("", { "think-answer" }))) end
  div.content = out
  return div
end

-- ::: story: a labelled incident, true or an illustration.
local function story(div)
  div.content:insert(1, labelled(div.classes:includes("illustration") and L.illustration or L.story))
  return div
end

-- ::: cards: each definition-list item becomes a .card (its term, then its definitions).
local function cards(div)
  local out = pandoc.Blocks({})
  if div.attributes.title then
    out:insert(labelled(div.attributes.title))
    div.attributes.title = nil
  end
  for _, block in ipairs(div.content) do
    if block.t == "DefinitionList" then
      for _, item in ipairs(block.content) do
        local card = pandoc.Blocks({ pandoc.Div({ pandoc.Plain(item[1]) }, pandoc.Attr("", { "card-term" })) })
        for _, def in ipairs(item[2]) do card:extend(def) end
        out:insert(pandoc.Div(card, pandoc.Attr("", { "card" })))
      end
    else
      out:insert(block)
    end
  end
  div.content = out
  return div
end

local function aside(div)
  if div.classes:includes("opener") then return opener(div) end
  if div.classes:includes("think") then return think(div) end
  if div.classes:includes("story") then return story(div) end
  if div.classes:includes("cards") then return cards(div) end
  if div.classes:includes("payoff") then
    div.content:insert(1, labelled(L.payoff))
    return div
  end
  for name, spec in pairs(ASIDE) do
    if div.classes:includes(name) then
      div.classes:insert(1, spec[1])
      if not div.attributes.title then div.attributes.title = spec[2] end
      if name == "tryit" then div.attributes.icon = "false" end
      return div
    end
  end
  if div.classes:includes("done") then
    local first = div.content[1]
    if first and (first.t == "Para" or first.t == "Plain") then
      first.content:insert(1, pandoc.Space())
      first.content:insert(1, pandoc.Strong(L.done))
    end
    return div
  end
  if div.classes:includes("catchup") then
    div.content:insert(1, pandoc.Para({ pandoc.Strong(L.stuck), pandoc.Space(),
      pandoc.Str(catchups == 0 and L.catchup or L.catchup_again) }))
    catchups = catchups + 1
    return div
  end
  return nil
end

-- 8. Headings: a hyphenated word ("k-Means") is kept on one line, so a narrow screen never
--    breaks a title at its hyphen. A date the first pass wrapped is already whole: the walk
--    is top-down so it can stop at that span instead of wrapping its text a second time, and
--    it never enters a span it has just made (false), which would wrap the word forever.
local function heading_words(header)
  header.content = header.content:walk({ traverse = "topdown",
    Span = function(span)
      if span.classes:includes("nowrap") then return span, false end
    end,
    Str = function(str)
      if str.text:find("%w%-%w") then
        return pandoc.Span({ pandoc.Str(str.text) }, pandoc.Attr("", { "nowrap" })), false
      end
    end })
  return header
end

-- 9. Wide pictures. An image given a width above 40% (a screenshot, a page of a PDF, a
--    drawing) gets the class "scaled", which the EPUB stylesheet widens on a phone; smaller
--    ones (photos set beside the text) keep their width.
--    A picture of a rendered output (media/figures/) not on a light panel is a screenshot:
--    it gets a thin frame, so it does not read as the book's own page.
local function scaled(img)
  local changed = false
  local pct = tonumber((img.attributes.width or ""):match("^(%d+%.?%d*)%%$"))
  if pct and pct > 40 then
    img.classes:insert("scaled")
    changed = true
  end
  if img.src:find("/media/figures/") and not img.classes:includes("on-light") then
    img.classes:insert("screenshot")
    changed = true
  end
  if changed then return img end
end

local DATE = "%d%d%d%d%-%d%d%-%d%d"

local function keep_dates(str)
  local text, out, pos = str.text, pandoc.Inlines({}), 1
  if not text:find(DATE) then return nil end
  while true do
    local s, e = text:find(DATE, pos)
    if not s then break end
    if s > pos then out:insert(pandoc.Str(text:sub(pos, s - 1))) end
    out:insert(pandoc.Span({ pandoc.Str(text:sub(s, e)) }, pandoc.Attr("", { "nowrap" })))
    pos = e + 1
  end
  if pos <= #text then out:insert(pandoc.Str(text:sub(pos))) end
  return out
end

return {
  -- The labels' language first: Pandoc runs a filter's Meta function after its blocks.
  { Meta = set_language },
  -- Every date in a Str, but none inside a link: a URL's own dates must stay breakable. The
  -- walk is bottom-up, so a link's text has been wrapped by the time its Link is seen.
  { Str = keep_dates,
    Link = function(link)
      link.content = link.content:walk({ Span = function(span)
        if span.classes:includes("nowrap") then return span.content end
      end })
      return link
    end },
  { Div = function(div)
      if div.classes:includes("agent-box") then return label_children(div) end
      -- A picture on a light panel is not framed as a screenshot (9), whether the class is
      -- on the image or on a div around it. Images are seen before the div that holds them.
      local walked = nil
      if div.classes:includes("on-light") then
        div = div:walk({ Image = function(img)
          if img.classes:includes("screenshot") then
            img.classes = img.classes:filter(function(c) return c ~= "screenshot" end)
            return img
          end
        end })
        walked = div
      end
      return aside(div) or walked
    end,
    -- The EPUB is rendered as one document, so the catch-up count (3) starts again at each
    -- chapter's title; Header and Div are visited in document order in this pass.
    Header = function(header)
      if header.level == 1 then catchups = 0 end
      return heading_words(header)
    end,
    Image = scaled },
  { Blocks = group_boxes },
}
