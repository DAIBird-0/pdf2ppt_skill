# Precision Cropping Protocol

Use this reference whenever paper figures, tables, equations, or prompts are inserted into a PPT as screenshots.

## Crop Boundary Rule

Default crop content:

- Include the whole figure, table, equation, or prompt block.
- Include the figure caption, table caption, table notes, and equation number when present.
- Preserve footnotes that define symbols, metrics, or abbreviations.

Default exclusions:

- Exclude surrounding body paragraphs.
- Exclude section headings such as `5 Methodology` or `6 Experiments`.
- Exclude page headers, page footers, page numbers, margins, and unrelated adjacent figures/tables.
- Exclude neighboring columns unless the requested asset spans both columns.

If a caption is extremely long and makes the visual unreadable, keep the figure/table readable and add a short external source label only if the user permits that tradeoff. Otherwise, preserve the full caption and enlarge the screenshot region in the slide layout.

## Required Workflow

1. Locate the requested label (`Fig. X`, `Table Y`, `Eq. Z`) in the PDF text or page manifest.
2. Render the PDF page to a high-resolution page image; use at least 2x scale or about 300 DPI.
3. Inspect the rendered page visually before cropping.
4. Crop from the rendered page image, not from embedded PDF image fragments, when the asset is layered, split, clipped, or uncertain.
5. Record each crop in `figure_plan.md`: paper label, source page, pixel bbox, output path, and QA status.
6. Insert the crop as one single image object in the PPT.
7. Export slide previews and inspect the final slide, not just the raw crop.

## Crop QA Checklist

Mark a crop as bad and redo it if:

- It contains body text outside the caption/table note.
- It cuts off any part of the figure, table border, legend, axis label, caption, or table note.
- It includes unrelated adjacent objects.
- The visible label does not match the requested label.
- The screenshot is a fragmented layer rather than one whole asset.
- The screenshot has too much blank margin, making the content unnecessarily small.
- The image becomes unreadable after being placed on the slide.

## Practical Guidance

- For two-column papers, check whether the caption belongs above or below the visual before setting the bbox.
- For tables, include the top caption and bottom explanatory notes when they define metrics or symbols.
- For equations, include nearby equation numbers and any immediately attached line breaks, but not the full explanatory paragraph unless requested.
- For prompt-template figures in appendices, crop the whole prompt block and its figure caption as a single object.
- Use a short source chip outside the screenshot, such as `Figure 3: Overall Framework`, so the screenshot itself can stay clean.
- When uncertain, make a slightly larger first crop, inspect it, then tighten. Do not proceed to final PPT with known over-crops that include body paragraphs.
