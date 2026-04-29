# Output Contract

When this skill is used, the working directory should usually end up with these artifacts:

## Required Intermediate Files

### `paper_brief.md`

Must include:

- core problem
- why prior work fails
- key contributions
- minimum explainable method units
- best experiments to show
- likely questions and limitations

### `paper_reading_matrix.md`

Must include:

- paper metadata: title, venue, year, authors if available
- one-sentence thesis: what the paper proves or contributes
- problem/gap/evidence table
- method decomposition: input, representation, mechanism, output, loss/objective if relevant
- experiment evidence matrix: claim, figure/table, metric, result, confidence
- limitations and likely advisor questions
- `[MATERIAL GAP]` markers where the PDF does not provide enough evidence

### `figure_plan.md`

Split candidate visuals into:

- main deck must-use
- PDF screenshot
- optional redraw/simplify
- appendix only
- discard

For each visual, include:

- paper label (`Fig. X`, `Table Y`, `Eq. Z`)
- source page
- target slide
- pixel crop bbox when using a rendered page screenshot
- extraction mode: embedded image, full-page crop, whole-page screenshot, or redraw
- quality status: ok, too dense, blurry, fragmented, wrong crop, missing

### `slide_outline.md`

For each slide, specify:

- slide number
- title
- one-sentence job of the slide
- whether it is main deck or appendix

### `slide_specs.md`

For each slide, specify:

- title
- single core message
- visual asset or redraw plan
- layout plan
- talk transition
- section: `研究背景`, `研究方法`, `实验`, or `研究结论与展望`
- expected reading load: light, medium, or dense
- screenshot crop path if using original paper visual
- screenshot crop bbox and source page image path if using a manual crop

### `speaker_notes.md`

For each slide, include:

- slide title
- short oral script
- timing hint if useful

### `icon_plan.md`

Create this file whenever icon accents are used.

For each icon, include:

- target slide
- nearby card title or text region
- semantic reason for the icon
- source class: current `extracted/figures/`, historical harvested icon, manual crop, or PPT-native fallback
- source file path if one exists
- placement note
- status: planned, inserted, skipped, or rejected

## Required Final Files

- editable `.pptx`
- preview PNGs
- `speaker_notes.md`
- `quality_report.md` describing preview inspection and unresolved issues
- `icon_plan.md` when icon accents are used

## Default Slide Structure

Unless the user overrides it, keep the main story inside:

1. `研究背景`
2. `研究方法`
3. `实验`
4. `研究结论与展望`

## Beginner-Friendly Usage Pattern

If the user gives only a PDF and says “make a group meeting PPT”, assume:

- 8-10 minute talk
- advisor + labmates
- minimal academic design
- speaker notes required
- original PDF figures/tables/equations as screenshots unless user permits redraw
- icon accents only when the page has meaningful empty space and the personal style library is active
