# User PPT Style Library

Use this reference when the user asks to follow a clean academic paper-sharing PPT style or to preserve their prior paper-sharing PPT habits.

Default reusable template: `assets/user-default-paper-group-template.pptx`.

When no external PPT template is provided, use that file as the deck template and treat the rules below as the default personal style. When an external template is provided, apply these habits only after the user confirms they want the personal layout habit library layered onto the new template.

## Overall Visual System

- Use 16:9 widescreen, typically `960 x 540` PowerPoint points.
- Prefer a clean academic style: deep-blue navigation, light background, large readable Chinese text, and original paper evidence as cropped screenshots.
- Use `#003366` as the primary navigation blue.
- Use `#F5F8FB` or white for the background.
- Use `#1F2937` for main text, `#596575` for footer text, `#BFBFBF` for page counters, and `#DCE7F3` for small source-label chips.
- Use restrained accents for concept cards: `#003366`, `#2E6F95`, `#B34545`, `#C28B2C`.

## Fixed Slide Chrome

- Add a top navigation bar on most slides: full width, height about `72 pt`, fill `#003366`.
- Put the section label inside the nav bar, left aligned. Typical position: `x=16-44`, `y=15`, `w=160-335`, `h=43-82`, font about `32 pt`, white.
- Put the page counter at top right. Typical position: `x=846`, `y=29`, `w=70`, `h=15`, font about `9 pt`, grey.
- Add a small footer on normal slides: `Paper Reading | Group Meeting` or the paper short name, `x=50`, `y=505`, font about `8 pt`, muted grey.

## Text Hierarchy

- Main slide title: `23 pt`, dark text, usually `x=50`, `y=80-115`, `w=700`.
- Body bullets: `18-20 pt`, concise, usually 2-4 bullets.
- Full-width explanatory bullets above a large figure: `14 pt`, one or two lines only.
- Card headings: `15-20 pt`, colored to match the card accent bar.
- Card body: `13-20 pt`, short explanatory phrases, not paragraphs.
- Source labels above paper screenshots: small rounded chip, `9 pt`, deep-blue text on pale-blue fill.
- Prefer claim-like titles over generic labels. A title should tell the audience what to notice.

## Preferred Layout Families

### Title Slide

- Left vertical blue block about `308 pt` wide.
- Main English paper title on the blue block, white, large. Chinese translation can sit below as secondary text.
- Right side: one large visual or abstract cover graphic inside a white frame, around `x=349`, `y=71`, `w=550`, `h=350`.
- Bottom-right or lower-right: one sentence that states the deck's main story.

### Two-Column Evidence Slide

- Left: explanation bullets, around `x=50-60`, `y=155-180`, `w=330-340`.
- Right: original paper figure/table screenshot, around `x=418-430`, `y=130-155`, `w=450-540`, `h=290-330`.
- Place a source chip directly above the screenshot.
- Keep one takeaway card or summary box only when it clarifies the evidence.

### Full-Width Framework Slide

- Use for large method diagrams.
- Main title high on the page, around `y=80`.
- One short bullet strip below the title, around `x=60`, `y=125`, `w=820`, font about `14 pt`.
- Put the figure in a wide white frame, around `x=57`, `y=226`, `w=847`, `h=278`; center the screenshot inside it.

### Three-Card Concept Slide

- Use three aligned cards, around `x=58`, `350`, `642`; `y=145-180`; width `250-260`; height `145-250`.
- Each card has a narrow colored vertical accent bar on the left.
- Use card body text to explain ideas, and optionally a one-line synthesis at the bottom around `y=432-457`.

### Four-Card Schema Slide

- Use four compact cards, around `x=66`, `282`, `498`, `714`; `y=180`; width `185`; height `180`.
- Add small icons or mini visual cues only if they are clean and do not compete with the text.

## Sparse Card Icon Rule

- When a three-card, four-card, or short-text card layout leaves a large blank area, add one small related icon to reduce emptiness and support reading.
- Prefer icons harvested from `extracted/figures/` of the current or previously approved paper tasks. Use the global icon library only after checking those paper-derived sources.
- Put the icon near the lower-right or lower-middle of the card, with a clear gap from nearby text.
- Keep icons visually secondary: small, clean, low-detail, and color-aligned with the card accent or page palette.
- If no semantically relevant icon exists, do not force decoration.

### Conclusion Slide

- Use three large cards across the page, around `x=58`, `350`, `642`; `y=178`; width `260`; height `245`.
- Card headings should make contributions or discussion points explicit.

## Content Habits

- Explain the paper's contribution logic before showing dense evidence.
- Keep screen text sparse; carry detailed explanation in speaker notes.
- For background slides, explicitly name the generalization gap the paper addresses.
- For experiment slides, state the conclusion of the evidence, not just the metric names.
- Do not let screenshots become decoration. Each screenshot needs an external takeaway or a clear verbal role.
