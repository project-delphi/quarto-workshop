-- Book conventions (book/PLAN.md §5.2–5.3), for both editions.
--
-- 1. Assistant boxes. Consecutive ::: {.prompt}, ::: {.agent} and ::: {.you} divs are
--    wrapped in one ::: {.agent-box} (an explicit .agent-box is kept), and each part gets
--    its label as real text, so the EPUB needs neither CSS content nor JavaScript:
--      .prompt  "Ask your coding assistant"  (the exact prompt, in a `default` fence)
--      .agent   "Expect it to run"           (what the assistant will probably run)
--      .you     "You do"                     (the few steps only the reader can take)
-- 2. Asides. ::: why, ::: pitfall, ::: practice and ::: tryit become Quarto callouts
--    with fixed titles; the class stays for styling.
-- 3. Exercise lines. ::: done is prefixed "You're done when"; ::: catchup is labelled.

local BOX = {
  prompt = "Ask your coding assistant",
  agent = "Expect it to run",
  you = "You do",
}

local ASIDE = {
  why = { "callout-note", "Why this works" },
  pitfall = { "callout-warning", "Common pitfall" },
  practice = { "callout-tip", "In practice" },
  tryit = { "callout-important", "Try it" },
}

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

local function aside(div)
  for name, spec in pairs(ASIDE) do
    if div.classes:includes(name) then
      div.classes:insert(1, spec[1])
      if not div.attributes.title then div.attributes.title = spec[2] end
      return div
    end
  end
  if div.classes:includes("done") then
    local first = div.content[1]
    if first and (first.t == "Para" or first.t == "Plain") then
      first.content:insert(1, pandoc.Space())
      first.content:insert(1, pandoc.Strong("You're done when"))
    end
    return div
  end
  if div.classes:includes("catchup") then
    div.content:insert(1, pandoc.Para({ pandoc.Strong("Stuck for two minutes?"), pandoc.Space(),
      pandoc.Str("Paste this into your assistant, then rejoin at the next exercise:") }))
    return div
  end
  return nil
end

return {
  { Div = function(div)
      if div.classes:includes("agent-box") then return label_children(div) end
      return aside(div)
    end },
  { Blocks = group_boxes },
}
