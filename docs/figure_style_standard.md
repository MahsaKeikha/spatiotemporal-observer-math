# Block diagram geometry standard

Scientific diagrams in this repository must be readable without requiring the reader to infer where a label belongs or which object an arrow references.

## Required block behavior

Every block diagram should satisfy all of the following before publication:

- Text remains fully inside its block at normal rendering size.
- Long titles, equations, and explanatory labels are wrapped before they approach a block boundary.
- Internal horizontal and vertical padding is visibly generous.
- A block is enlarged when wrapping would make the content crowded.
- Font size is not reduced simply to force excessive content into a small box.
- Equations are split into scientifically meaningful lines when a single line would be too wide.
- Text hierarchy is consistent across title, equation, explanation, and note levels.

## Required connector behavior

Arrows and connectors must communicate topology unambiguously:

- A connector begins at the geometric boundary of its source block.
- Its arrowhead terminates immediately before the boundary of its target block with a consistent clearance.
- Connectors do not begin or end inside text.
- Connector paths do not cross block labels or equations.
- Parallel flows use consistent spacing and alignment.
- Crossing connectors should be avoided. If crossings are unavoidable, the diagram should be reorganized or divided into smaller figures.
- Arrow direction must match the scientific dependency or transformation being described.

## Layout quality

Blocks should align to a visible grid. Related blocks should use consistent dimensions when their content permits it. Unequal dimensions are acceptable when they improve readability. Empty space is preferable to compressed text.

A figure that is technically correct but visually ambiguous is not publication ready.

## Machine-checkable figures

Important pipeline figures should expose block geometry in the SVG source using stable metadata attributes such as `data-qa-block`, `data-x`, `data-y`, `data-width`, and `data-height`. Connector paths should identify their source and target blocks with `data-from` and `data-to`.

For those figures, tests should verify text-safe regions and connector anchoring. Machine checks do not replace visual review. They provide a minimum guard against obvious geometry regressions.

## Typography

Unicode en dash and em dash characters are not used in repository documentation or figures. Use ordinary punctuation or an ASCII hyphen where a hyphen is grammatically appropriate.
