# Knight Moves 7 — solving kit

| File | What it is |
|---|---|
| `knight-sandbox.html` | the interactive sandbox — double-click to open |
| `print-grids.html`    | printable blank grids, 4 to a page |
| `PUZZLE.md`           | verbatim rules, the extracted board, the derived move set |

No install, no build. If a yellow "autosave unavailable" strip appears, your browser blocks
storage on `file://` — either use **Export** to save by hand, or serve the folder:

    python3 -m http.server 8731
    # then open http://127.0.0.1:8731/knight-sandbox.html

## Modes

| Mode   | Key | What it does |
|--------|-----|--------------|
| Towers | `t` | Left-click toggles a tower. |
| Path   | `p` | Click a coloured dot to move the knight there. |
| Probe  | `b` | Inspect any square's reach without touching your work. |

**Right-click any square** to cycle it `? maybe` → `✗ no tower` (drawn with a grey hatch) →
clear. The tower tracker then shows how many cells each region has left open.
**Shift-click** fills the pin form with that square.

## Keys

    ⌘Z / ⌘⇧Z    undo / redo (everything, not just moves)
    Backspace   drop the last move off the active segment
    r           flip between Forward and Backward
    t / p / b   switch mode

## Segments — working from a move you already know

The trunk always starts at a1, move 0, score 0. When you work out where the knight lands on
move 6 or 18 without knowing how it got there, **add a segment** anchored at that square and
move number. If the square is a clue cell its entry score is filled in automatically; if not,
leave the entry score blank and moves are still checked for shape and altitude, but ÷ moves
can't be verified and scores show as `?`.

- **Forward** extends the head. **Backward** works back toward earlier moves, inverting each
  operation — a level arrival on move 18 into 138 means move 17 held 120; a ×18 arrival means
  138 must divide by 18. Illegal predecessors are refused with the reason.
- Every segment renders on the board with its own colour stripe and real move numbers.
- Overlaps are flagged: the same square in two segments, or two segments claiming one move.
- Once segments join up, delete the spare and the trunk carries the whole path.

## The rest

- **Legal dots** are coloured by type: grey level (+N), blue up (×N), orange down (÷N). Hover
  one to preview the resulting score. Illegal targets say *why* — "already used",
  "78 is not divisible by 9", "a straight 2-step must change altitude by 1".
- **Lock** freezes a trunk prefix you trust; drop/rewind refuse to cross it until you unlock.
- **Pins** record "cell X is move N" as a pure annotation, and go red when a segment disagrees.
  The **seed** button turns a pin into a segment.
- **Notes** is a free-text box saved with your state and included in Export — handy if you're
  narrating as you go and want the commentary attached to the position it belongs to.
- **Checkpoint checks** (toolbar, off by default) verifies the recording schedule and narrows
  K. It does more of the deduction for you, hence off.
- **Answer** computes the neighbour-sum total from your squares, marked *provisional* until
  you have one unbroken path, 13 towers one per region, all visited.

There is no solver. The tool answers "is this legal, and what does it score" — never "what
should I play next".

## Printing

`print-grids.html` renders blank boards with the pentomino walls and clue numbers. Controls
(hidden when printing): grids per page (4 / 2 / 1), number of sheets, and toggles for clue
numbers, coordinates, a label line, and region shading. 4-up gives ~0.4" cells; drop to 2-up
if you want room to write four-digit scores.

## Self-tests

Open the console and run `kmTests(true)`. 27 checks cover the board extraction, move
generation, altitude rules, the divisibility gate, forward and inverse scoring, segment
anchoring, unknown entry scores, and conflict detection.
