# Can U Dig It? — solving kit

| File | What it is |
|---|---|
| **`SOLUTION.md`** | **the write-up — a living document; the answer goes at the top once there is one** |
| `grid-search.html` | the tool — double-click to open. Search the grid, auto-find dictionary words, mark what you've found, read the leftovers |
| `PUZZLE.md` | the one-sentence rules verbatim, the transcribed grid, the coordinate convention |
| `grid.txt` | the grid as 14 plain lines, for scripts |
| `can-u-dig-it.jpg` | the puzzle image as published |

No install, no build. Found words and notes autosave in the browser. If a red "autosave unavailable"
strip appears, your browser blocks storage on `file://` — either use **export** to keep your list by
hand, or serve the folder:

    python3 -m http.server 8731
    # then open http://127.0.0.1:8731/grid-search.html

## grid-search.html

### The grid

- **Click** a cell, then click another in the same row, column or diagonal — the line between them
  becomes the selection and its word appears in the Selection card.
- **Shift-click** appends one adjacent cell at a time, for a path that bends.
- **Double-click** a cell to correct its letter (the image is the authority; the transcription was
  checked but not by a human). Edited cells get a red dot; **reset letters** drops all edits.
- `Esc` clears the selection. **add to found** records the selection; **search this word** looks for
  other copies of it; **reverse** flips the reading direction.
- Colours: blue = selection, amber = search hits, green = cells inside a found word, purple = letter
  highlight. **show the source image** at the bottom left opens the original for comparison.

### Search

Type a pattern and press Enter.

| Pattern | Means |
|---|---|
| `dig` | that word, exactly |
| `d.g` or `d?g` | any one letter in that spot |
| `di*` | `di` then any run of letters, to the end of the line (straight mode only) |
| `/t.n.*y/` | a JavaScript regex, anchored at the starting cell |
| `-` | the hyphen in row 14 — it's a real character |

Two modes:

- **straight lines** — reads from every cell in every ticked direction (E W S N and the four
  diagonals). **wrap around edges** treats the grid as a torus, so a word can run off the right edge
  and continue from the left.
- **bent path** — the word is spelled by adjacent cells, turning as it likes, never reusing a cell.
  Untick **bends may be diagonal** to allow only orthogonal steps. Plain words and `.`/`?` wildcards
  only; capped at 500 paths, so use it for words, not for `....`.

Click any hit to select it on the grid; **+ found** records it directly.

### Auto-find

Scans every straight line (same direction and wrap settings as Search) for dictionary words at
least **min length** long, longest first. Two dictionaries:

- **common English** — ~19k words, embedded. Fast to read through, but it's a web-frequency list, so
  it has junk in it and is missing plenty of real words.
- **loaded / pasted list** — pick a file with one word per line, e.g. `/usr/share/dict/words`
  (235k words; `⌘⇧G` in the file dialog lets you type the path), or paste a list of your own —
  say, a themed set you suspect the puzzle is built from.

The **filter** box narrows the results by substring. Results are candidates, not answers.

### Found words and leftovers

Everything you record lands here with its coordinates. Click a row to select it again; ✕ removes
it. Underneath, the tool reads out every letter that is **not** in any found word — row by row,
column by column, and as a grid with `·` for used cells. **export** turns the list, the leftovers
and your notes into markdown and puts it on the clipboard (and in a box below, in case the clipboard
is blocked on `file://`) — paste it straight into `SOLUTION.md`.

### Letters, strings, notes

- **Letters** — every character with its count. Click one to light up all its copies on the grid.
- **Rows, columns, diagonals** — the grid as plain strings in each reading direction, with a
  **reversed** toggle, for eyeballing.
- **Notes** — free text, saved with the found list, included in export.

There is no solver. The tool finds and records; the deduction is yours.

### Self-tests

Open the browser console and run `gsTests(true)` — 30 checks covering the transcription's shape,
straight and wrapped search, wildcards and regex, bent-path search, dictionary scanning, found-word
coverage and leftovers, export, and cell edits.
