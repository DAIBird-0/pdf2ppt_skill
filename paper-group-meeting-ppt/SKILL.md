---
name: paper-group-meeting-ppt
description: Turn an academic paper PDF and optional PPT template or Web-made slide plan into a rigorous, visually clean group-meeting literature-sharing PPT. Use for paper reading, thesis reading, journal club, lab meeting, or recurring paper-to-PPT workflows that require a user-confirmed slide plan before PPT generation, original PDF figures/equations/tables, reusable visual/icon accents, clear Background-Method-Experiments-Conclusion structure, and per-slide speaker notes.
---

# Paper Group Meeting PPT

Use this skill to make a reusable paper-sharing deck from a PDF. The deck must first prove that the paper was understood, then become a clean slide artifact.

This skill orchestrates PDF extraction, literature reading, figure/table screenshot planning, slide specification, PPT generation, and rendered QA. Use the built-in `Presentations` skill/runtime or another available PPT skill for deck authoring; this skill owns the research logic and quality gates.

Default behavior is human-in-the-loop: first produce the paper reading matrix, figure/table mapping, and page-by-page PPT plan; then wait for the user's confirmation or edits before generating the final PPT unless the user explicitly asks for a rough draft in one pass.

This version incorporates lessons from high-recognition open-source skills:

- `anthropics/skills` (`pptx`, `pdf`, about 123k GitHub stars on 2026-04-25): strong PPTX/PDF routing, XML/template workflows, and "render then inspect" QA.
- `openai/skills` (`pdf`, about 17k stars): PDF visual checks by rendering pages to PNG before delivery.
- `MiniMax-AI/skills` (`pptx-generator`, `minimax-pdf`, about 11k stars): tokenized design systems, slide-type planning, and explicit pitfalls.
- `Imbad0202/academic-research-skills` (about 3.5k stars): human-in-the-loop research pipeline, evidence checks, critique/reviewer thinking, and integrity gates.

## Workflow Decision

Use this skill when the request includes at least one of these patterns:

- make a group-meeting PPT from a paper PDF
- make a paper-sharing deck from a paper, arXiv PDF, or conference PDF
- create a reusable paper-to-PPT workflow
- generate speaker notes for a research presentation
- follow a supplied PPT template while turning a paper into slides
- assemble a PPT from a Web-side structured slide plan
- repair bad paper figures by identifying the corresponding PDF figure/table/equation and re-screenshotting it

Do not use this skill for:

- general business decks unrelated to papers
- single-slide design tasks without paper understanding
- document editing tasks better handled by `documents`

## Inputs

Collect or infer these inputs. For PPT-making requests, complete the template/style handshake below before final deck generation.

- source paper PDF
- optional PPT template
- optional Web-side PPT production plan (`JSON` or Markdown)
- optional user-optimized prior deck to learn recurring layout habits
- expected talk length
- audience
- presentation setting
- emphasis preference if given
- output language

If some inputs are missing, assume:

- talk length: `8-10 minutes`
- setting: `group meeting`
- audience: `advisor + labmates`
- structure: `研究背景 -> 研究方法 -> 实验 -> 研究结论与展望`
- no template supplied: use `assets/user-default-paper-group-template.pptx` as the default deck template and follow `references/user-ppt-style-library.md`
- output language: follow the user's language; if Chinese, use professional academic Chinese
- icon accents: enabled by default when useful; use paper-derived icons first and never upload user paper assets

## Mandatory Template/Style Handshake

For every request to make a new PPT with this skill, determine the template route before slide assembly.

If the user has not already answered the template question, ask:

```text
是否提供 PPT 模板？如果提供，请给模板路径；如果不提供，我将使用内置的通用学术默认模板生成。
```

Then follow this decision tree:

- If the user says no template or gives only the paper PDF, use `assets/user-default-paper-group-template.pptx` as the default template. Also follow `references/user-ppt-style-library.md` unless the user explicitly requests another style.
- If the user provides a new template, use that template first. Then ask whether to also follow the personal layout habit library.
- If the user says yes to personal layout habits, read `references/user-ppt-style-library.md` and adapt its layout habits to the supplied template.
- If the user says no to personal layout habits, wait for the user's concrete style/layout instructions before producing the final PPT.
- If the user has already specified both template and style preferences in the same request, do not ask again; proceed with the specified route.

Also clarify icon preference when the user asks about visual style or privacy:

```text
默认会从当前论文图表中提取可复用小图标，加入本地图标库，用于后续 PPT 的卡片/留白增强。你也可以关闭图标增强，或改用 AI 生成图标、PPT 原生图标、手动指定图标。
```

## Beginner Usage Prompts

Simple PDF-only use:

```text
使用 $paper-group-meeting-ppt，根据这篇论文 PDF 制作中文组会文献分享 PPT。
论文：<paper.pdf>
请先做文献阅读矩阵和图表映射，再生成 8-10 分钟 PPT，每页写入 speaker notes。
```

With a Web-side plan:

```text
使用 $paper-group-meeting-ppt，按下面的 PPT 制作方案装配组会分享 PPT。
论文：<paper.pdf>
模板：<template.pptx>
要求：所有论文 Fig/Table/Eq 使用 PDF 原始截图；若图被拆成多层素材，用整页截图裁成单一整图。
方案：<paste JSON or Markdown plan>
```

For repairing bad images:

```text
使用 $paper-group-meeting-ppt，检查这个 PPT 的坏图，识别对应论文 Fig/Table/Eq，并从 PDF 重新截图替换。
PPT：<deck.pptx>
论文：<paper.pdf>
```

## Operating Sequence

Follow this order. Do not jump directly from PDF to final PPT unless the user explicitly says a rough draft is acceptable.

1. Extract text, embedded assets, and full-page rendered screenshots from the PDF.
2. Read the paper with a research-quality matrix: problem, gap, method, evidence, limits.
3. Build or validate the deck thesis: one sentence that explains why the paper matters.
4. Map figures/tables/equations to slide jobs. Use original PDF screenshots for paper assets.
5. Write page-by-page outline, specs, and speaker notes.
6. Present the plan to the user and wait for confirmation or edits before final PPT generation, unless the user explicitly asks to skip confirmation.
7. Add icon-accent planning for sparse cards or short-text regions when the personal layout habit library is active and icon accents are not disabled.
8. Generate the PPT using the best available PPT runtime or template workflow.
9. Export PNG previews and inspect every slide for content, figure, icon, and layout defects.
10. Fix bad images by returning to the PDF page and re-screenshotting the whole figure/table/equation.

If the user asks to learn their revised deck, inspect that deck and update the user style library. Prefer stable repeated layout habits over one-off manual adjustments.

## Phase 1. PDF Material Extraction

Use `scripts/extract_pdf_materials.py` when the user only supplies a PDF or when extracted materials are missing.

Preferred command:

```bash
python scripts/extract_pdf_materials.py --pdf paper.pdf --outdir work/paper/extracted --render-pages
```

Expected output folder shape:

```text
<paper-workdir>/
  extracted/
    full_text.txt
    outline.md
    asset_summary.md
    page_manifest.json
    pages/
    page_images/
    figures/
```

Use rendered page images whenever layout fidelity matters. Embedded images may be fragmented by the PDF producer; for figures/tables/equations that appear broken or split, crop from `page_images/` instead of using extracted fragments.

Treat `extracted/figures/` as the primary candidate source for reusable small icons. When a later deck has sparse cards or short text regions, first look through the current paper's `extracted/figures/` and previously approved historical `extracted/figures/` assets before considering any other source.

For manual crops from rendered page images, use `scripts/crop_pdf_region.py` with a recorded pixel bbox and save the bbox in `figure_plan.md`.

## Phase 2. Literature Reading

Before slide writing, create `paper_reading_matrix.md`. See `references/research-reading-rubric.md` when the paper is complex.

The matrix must answer:

- What exact problem is being solved?
- Why do prior methods fail?
- What is the paper's main idea in one sentence?
- What are the minimum method units that must be explained live?
- Which experiments actually prove the claim?
- What are the most likely advisor questions?
- What are the limitations, hidden assumptions, and weak evidence?

If the PDF text is poor, mark `[MATERIAL GAP]` instead of inventing missing details.

## Phase 3. Slide Planning

Create these artifacts in the working directory before generating the PPT:

- `paper_brief.md`
- `paper_reading_matrix.md`
- `figure_plan.md`
- `slide_outline.md`
- `slide_specs.md`
- `speaker_notes.md`
- `icon_plan.md` when icon accents are used

Read `references/output-contract.md` for the expected content of each file.

When the user wants the deck to follow their saved personal PPT habits, read `references/user-ppt-style-library.md` before slide assembly.

If the user supplies a Web-side plan, treat it as the blueprint for slide count, titles, bullets, visual references, and notes. Still validate that the cited figures/tables/equations exist in the PDF and that the plan has a coherent four-section structure.

## Phase 4. Narrative Compression Rules

The deck is not a paper move. It should help the audience answer:

- what problem matters here
- why prior work is insufficient
- what this paper changes
- whether the evidence is convincing
- what the limits are

Default four-section arc:

- `研究背景`: motivation, gap, task definition, why the paper matters.
- `研究方法`: one overview slide plus only the method details needed to understand the contribution.
- `实验`: dataset/setup, main results, ablation/analysis, qualitative case if useful.
- `研究结论与展望`: contribution summary, limitations, discussion questions.

Every non-title slide needs:

- one core message
- one dominant visual or evidence object
- at most 2-4 short bullets
- a speaker-note script that carries the explanation

## Phase 5. Figure/Table/Equation Strategy

Sort candidate visuals into:

- main deck must-use
- screenshot from PDF
- simplify/redraw only when user allows it
- appendix only
- discard

Default for academic paper figures:

- Original paper figures, tables, and equations must come from the PDF as screenshots or direct extraction.
- If a figure is split into multiple embedded images, use a single whole screenshot from the rendered PDF page.
- Crop paper visuals tightly enough that the screenshot contains only the figure/table/equation plus its caption/table note/footnote. Do not include surrounding body paragraphs, section headings, page headers, page footers, or adjacent unrelated objects.
- If an image looks broken, white, blurry, clipped, or contains the wrong object, identify its paper label (`Fig. X`, `Table Y`, `Eq. Z`) and re-crop from the page image.
- Dense tables may be shown as original screenshots when the user requires original evidence. Add a short slide takeaway outside the screenshot.
- Redrawing is allowed only for auxiliary explanatory diagrams, not as a substitute for required paper figures/equations/tables.

Read `references/precision-cropping-protocol.md` when the request emphasizes screenshot precision, when repairing bad paper visuals, or when the paper uses multi-layer PDF figures.

## Phase 6. Template and Style Policy

If the user supplies a template:

- study the template's colors, fonts, section dividers, margins, and title hierarchy
- reuse the visual system, not irrelevant content
- keep paper screenshots readable even if the template uses decorative backgrounds

If the user has a saved personal style library and confirms using it, treat it as the default layout preference unless it conflicts with the provided template or a new explicit instruction.

If no template is supplied:

- use `assets/user-default-paper-group-template.pptx` as the template
- follow `references/user-ppt-style-library.md`
- keep the deck minimal and academic, with original paper screenshots and sparse explanatory text

Design rules:

- One slide, one job.
- Titles should be claims or clear topics, not vague labels.
- Screen text should be bullets or short labels, never copied paragraphs.
- Use a consistent margin grid.
- Do not repeat the same "title + bullets + image box" layout for every slide if the story needs variation.
- Render preview PNGs and fix visible defects before delivery.

## Phase 6.5. Icon Accent Layer

Use this phase when the deck follows the saved personal layout habit library or when the user explicitly asks for whitespace reduction with small related icons. Skip this phase when the user disables icon accents.

Source priority for icon accents:

1. the current paper's `extracted/figures/`
2. historically harvested icons from prior `extracted/figures/` directories
3. manually cropped icons from the current paper's rendered page images
4. local PPT-native simple line icons as a fallback
5. AI-generated icons only when the user explicitly requests them

Do not default to network crawling or AI image generation. Use those only if the user explicitly asks for them. Keep all harvested icons local; do not upload the user's paper figures or icon library to external services.

The icon-accent pass should:

- detect sparse layouts such as three-card or four-card concept slides, or short text cards with obvious empty space
- match icon meaning to nearby card titles or bullets
- prefer paper-derived icons that are clean, reusable, and semantically close
- add clean reusable icons from the current paper to the local icon library manifest for future paper decks
- record every chosen icon in `icon_plan.md`
- skip icon insertion entirely when no relevant icon exists

Use `references/icon-usage-policy.md` for the detailed rules and `scripts/harvest_icons_from_figures.py` to build the reusable personal icon library from historical `extracted/figures/` folders. Use `scripts/select_icon_accent.py` to create a deterministic `icon_plan.md` from slide specs and available manifests.

## Phase 7. Speaker Notes Policy

Every main-deck slide must have speaker notes.

When the runtime supports slide notes, write them into the PPT itself. Also save a plain-text or markdown copy as `speaker_notes.md`.

Notes should be:

- oral rather than paper-like
- short enough for live presentation
- aligned with the slide visuals
- appropriate for lab meeting discussion

## Phase 8. Final Deck Generation

For deck generation and export, use the best available PPT workflow in this order:

1. User-supplied PPT template + `Presentations` skill/runtime or PPTX XML/template workflow.
2. Built-in `Presentations` skill/runtime from scratch.
3. Local Office/PowerPoint automation only when headless/export tooling cannot embed images or notes correctly.

Required outputs:

- editable `.pptx`
- PNG previews
- intermediate analysis files
- `speaker_notes.md`

## Quality Gates

Block and revise if any of these are true:

- the deck reads like pasted paper text
- a slide has more than one main message
- the method section does not show input -> mechanism -> output
- the experiment slide lists results without the conclusion
- speaker notes and slide content do not match
- there is no clear background / method / experiment / conclusion structure
- paper figures/tables/equations are replaced by invented text when the user asked for originals
- any paper figure is a fragmented PDF layer instead of one whole screenshot
- preview PNGs show blank placeholders, clipped screenshots, unreadable tables, text overflow, low contrast, or icon accents that are irrelevant / overpowering / misaligned

If the user prioritizes delivery speed, still produce the whole deck first, then record known issues and suggested manual fixes.
