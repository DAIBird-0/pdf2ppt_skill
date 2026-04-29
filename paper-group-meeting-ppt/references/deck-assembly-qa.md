# Deck Assembly QA

Use this before final delivery or when repairing bad figures.

## Asset QA

For every slide with a paper visual, check:

- The visual matches the requested paper label (`Fig. X`, `Table Y`, `Eq. Z`).
- It is one whole screenshot when the PDF stores the figure as multiple layers.
- It is not a tiny embedded fragment.
- It is not a blank placeholder.
- Captions/table notes are included when the user wants original paper evidence.
- The crop does not include surrounding body text, section headings, page headers, page footers, or adjacent unrelated objects.
- Equations are sharp and not retyped unless the user permits reconstruction.

When a visual is bad, re-render the PDF page and crop from the page image. Record the fix in `quality_report.md`.

## Layout QA

Inspect rendered PNG previews, not just the editable PPTX.

Check:

- Title is readable at thumbnail size.
- Body text stays within 2-4 bullets.
- No text overlaps images, labels, footers, or page numbers.
- Each slide has one dominant visual or evidence object.
- Screenshots are large enough to read the important part.
- Dense evidence slides have a clear takeaway outside the screenshot.
- Section transitions are visible.
- Colors are consistent with either the user template or a minimal academic palette.

## Icon Accent QA

When icon accents are present, check:

- The icon is semantically related to the nearby card or text block.
- The icon comes from a local paper-derived or approved local source, not an unapproved web grab.
- The icon does not overlap text, figures, equations, navigation, or page counters.
- The icon reduces empty-space awkwardness without becoming the main visual.
- The icon is sharp enough to survive preview rendering.

## Repair Priority

When time is short:

1. Make sure all slides exist and notes are present.
2. Fix blank or wrong figures.
3. Fix clipped or unreadable paper screenshots.
4. Fix text overflow.
5. Polish spacing and visual variety.

## Quality Report Shape

```markdown
# Quality Report

## Rendered Preview
- command/tool:
- preview folder:
- slides checked:

## Asset Mapping
| Slide | Requested Asset | Source Page | Used File | Status |
|---|---|---:|---|---|

## Issues Fixed
- ...

## Remaining Manual Polish
- ...
```
