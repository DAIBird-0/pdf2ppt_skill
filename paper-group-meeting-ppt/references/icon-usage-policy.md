# Icon Usage Policy

Use this reference when the deck contains card layouts, short explanatory blocks, or other regions with visually awkward empty space.

Icon accents are optional. If the user disables them, skip this layer entirely. If the user asks for another source, use the requested source while preserving the deck's visual system.

## Goal

Add small, relevant icon accents that:

- reduce the feeling of large blank areas
- support reading by reinforcing the nearby concept
- stay visually secondary to the real paper evidence

## Allowed Icon Sources

Default source priority:

1. current paper `extracted/figures/`
2. approved historical icons harvested from prior `extracted/figures/`
3. manually cropped icons from current paper page renders
4. local PPT-native simple line icons
5. AI-generated icons only when explicitly requested by the user

Do not default to:

- web crawling
- online icon packs
- AI image generation

Those routes are only allowed when the user explicitly asks for them.

Keep harvested icons local. Do not upload the user's paper, extracted figures, or icon library to external services unless the user explicitly asks for a workflow that requires it.

## Placement Rules

- Add icons only when a card or short-text region has obvious empty space after layout.
- A good default trigger is when roughly `35%-45%` of the card remains visually empty.
- Use one icon per card at most.
- Use `3-4` icons per slide at most.
- Prefer placing the icon near the lower-right or lower-middle of the card.
- Keep a clear gap from the text block and card edges.
- Do not place icons on top of paper screenshots, equations, dense tables, page counters, or the navigation bar.

## Style Rules

- Keep icons visually light and secondary.
- Prefer a single-color or low-detail icon.
- Follow the local accent color, muted navy, grey, or the card's cue color.
- Use moderate transparency when needed so the icon does not compete with text.
- If the icon source is raster, avoid blurry or jagged assets.
- Add only reusable, clean, semantically meaningful icons to the local icon library manifest so later decks can inherit a gradually personalized visual vocabulary.

## Semantic Mapping

Default mapping examples:

- dataset / mobility record / trajectory: database, map, phone, route marker
- metric / utility / performance: chart, target, gauge
- privacy / DP / PATE / noise: lock, shield, anonymized user
- method / pipeline / framework: nodes, arrows, flow, server
- experiment / benchmark / ablation: table, bar chart, comparison
- conclusion / future work / limitation: flag, arrow, discussion bubble

If no strong semantic match exists, leave the space empty rather than forcing decoration.
