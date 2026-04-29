# Research Reading Rubric

Use this when the paper is technical, dense, or the user complains that the deck did not read the paper deeply enough.

## Reading Passes

1. Metadata pass: title, venue, year, authors, task, datasets, model family.
2. Problem pass: what real research gap exists, why prior work fails, what assumption changes.
3. Method pass: decompose the method into input, representation, mechanism, objective, output, and inference loop.
4. Evidence pass: map every major claim to the exact figure, table, equation, or experiment that supports it.
5. Critique pass: identify weak assumptions, missing baselines, sensitivity risks, scalability limits, and likely advisor questions.

## Evidence Matrix

Use this table shape in `paper_reading_matrix.md`:

| Claim | Evidence | Figure/Table/Eq | What It Proves | Weakness | Slide Use |
|---|---|---|---|---|---|

Rules:

- Do not treat a claim as slide-worthy until it has evidence.
- If evidence is qualitative only, say so.
- If a result is visually dense, keep the original screenshot but explain the takeaway in one short bullet.
- Mark missing or unclear material as `[MATERIAL GAP]`.

## Talk Thesis

Before slide specs, write one thesis sentence:

```text
This paper matters because [problem] was blocked by [gap], and the authors address it through [core mechanism], supported by [strongest evidence], though [main limitation] remains.
```

## Advisor Question Bank

Prepare 4-8 likely questions:

- Why is this problem important now?
- What does the method add beyond the strongest baseline?
- Which experiment is the strongest proof?
- What is the weakest assumption?
- Does the method scale?
- Could a simpler method explain the same gains?
- What fails under distribution shift?
- What would you change if extending this work?
