# Knight Moves 7 — solving kit

| File | What it is |
|---|---|
| `knight-sandbox.html` | the interactive sandbox — double-click to open |
| `score-paths.html`    | score-arithmetic search: what can this score reach, and how |
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
| Erase  | `e` | Click a placed square to remove it. |

**Right-click any square** to cycle it `? maybe` → `✗ no tower` (drawn with a grey hatch) →
clear. The tower tracker then shows how many cells each region has left open.
**Shift-click** fills the pin form with that square.

## Keys

    ⌘Z / ⌘⇧Z        undo / redo (everything, not just moves)
    Backspace       drop the last move off the active segment
    r               flip between Forward and Backward
    t / p / b / e   switch mode

## Runs — start anywhere, join them up later

The trunk always starts at a1, move 0, score 0. Everything else is a **run** you can start,
extend and merge freely.

**Start one anywhere.** In Path mode, click any empty square. The run begins there with **no
move number** — it floats. Its shape and altitude are still checked, and it still refuses
revisits, but scores stay `?` until it gets a number. Squares in a floating run are labelled
`+0`, `+1`, `+2` rather than `#N`.

**Give it a number when you know one**, via *starts at move* in the Segments card, or unset it
to float again. Numbering a run whose first square is a clue cell picks up that clue as its
entry score automatically.

**Join two runs by pathing into each other.** When the run you're building can reach another
run's endpoint, that target is drawn with a **ring**. Click it and the two merge into one.
Whichever side already has move numbers hands them to the other — so a floating run walked out
from f6 gets real move numbers the moment the trunk reaches it, and every score in it
resolves. Going **Forward** you join onto another run's first square; going **Backward**, onto
its last. If both runs already have numbers they have to line up, otherwise the join isn't
offered.

You can still anchor a run at a known move directly: **add a segment** with a cell and a move
number. The move number is optional now — leave it blank and the run floats.

- **Forward** extends the head. **Backward** works back toward earlier moves, inverting each
  operation — a level arrival on move 18 into 138 means move 17 held 120; a ×18 arrival means
  138 must divide by 18. Illegal predecessors are refused with the reason.
- Every run renders on the board with its own colour stripe.
- Overlaps are flagged: the same square in two runs, or two runs claiming one move. Floating
  runs claim no move slots, so they can't collide on numbering.

## Removing things

- **Erase mode** (`e`) — click any placed square to remove just that one. At either end of a
  run it simply shortens; erase the anchor and the run re-anchors forward, picking up the new
  first square's clue value as its entry score if it has one. Erase from the **middle** and the
  run **splits in two**, with the tail becoming its own segment that keeps its real move
  numbers. To drop everything *after* a move instead, click that row in the move log.
- Squares that sit past a break in their run are drawn with a **red dashed outline and `#N?`**,
  so an orphaned tail is visible and can be erased rather than being invisible.
- **clear** on a segment row resets it to its anchor square, keeping the segment. **✕** deletes
  a segment outright. **Clear all path work** returns to just a1 while keeping towers and marks.
- **clear all** on the pins card drops every pin.
- a1 at move 0 is the fixed start and can't be erased; locked moves are protected until you
  unlock. Both say so rather than failing silently, and every removal is undoable with ⌘Z.

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

## Score paths

Pure arithmetic, no board — it answers "from this score, what can I land on, and by what
sequence of operations". The altitude rule makes the operation order exact rather than a
guess: on **ground** you may only `+N` (stay) or `×N` (rise); on a **tower** only `+N` (stay)
or `÷N` (fall, when it divides evenly). So `×` and `÷` must alternate with any run of `+`
between them — never two multiplies or two divides in a row.

Four modes:

- **Explore** — from a score, the next move number, and an altitude, list everything reachable
  within *n* moves. Runs **forward or backward**: backward inverts each operation, so from 138
  arriving on move 18 it reports that a level arrival came from 120, and a `×18` arrival is
  impossible because 18 doesn't divide 138. Filter to clue values, to checkpoint moves, or to
  paths ending on the ground.
- **Connect** — "can score A at move i become score B at move j?" over a range of move counts.
  A negative answer is a real deduction: it rules the pairing out whatever the board looks
  like. Uses meet-in-the-middle, so wide gaps stay fast.
- **Ladder** — chain clue values checkpoint to checkpoint, each leg a fixed gap, no value
  reused. This is the "moves 1–18 at gap 3" shape of the puzzle.
- **Matrix** — for every ordered pair of clue values, how many `gap`-move sequences join them.

Two constraints beyond the arithmetic are baked in, and both prune hard:

- **Tower budget.** An altitude-1 state means standing on a tower, and there are only 13
  towers, so any path using more than 13 is impossible.
- **K is 4–9.** 12 clue cells = 7 early records (moves 0, 3, …, 18) plus 5 late ones, so the
  path reaches move 18+5K, and M ≤ 63 forces K ≤ 9. That makes "K unknown" a real filter
  rather than a free pass — move 19 can never be a checkpoint, because no K in 4–9 divides 1.
  Results show which K values each checkpoint is consistent with.

Results are candidates, not answers — a route that works arithmetically still has to be
realisable as knight moves. Check it in the sandbox.

## Self-tests

In the sandbox, run `kmTests(true)` in the console — 64 checks covering the board extraction,
move generation, altitude rules, the divisibility gate, forward and inverse scoring, run
anchoring, unknown entry scores, conflict detection, erasing (end, anchor, middle-split, lone
anchor, and the a1 and lock guards), floating runs, and joining in both directions including
the numbering handover and the mismatch refusal.

In score paths, press **run self-tests** (or call `spTests(true)`) — 38 checks. They include
exhaustive sweeps proving backward is the exact inverse of forward and that no backward step
invents an illegal forward move, a replay of every explored path, `connect` cross-checked
against brute-force enumeration, the tower cap, the move-63 ceiling, and the checkpoint
schedule including the unknown-K case.
