# Jane Street puzzles — working notes

My solutions, tools, and notes for [Jane Street's monthly puzzles](https://www.janestreet.com/puzzles/).
One directory per puzzle, named `YYYY-MM` after the month the puzzle was published.

## Code style: readability first, always

**All code in this repo is written to be read by a human who is still learning the language.**
Comprehension beats brevity, cleverness, and idiom. Prefer more lines that are obvious over
fewer lines that need decoding.

If a convention is standard but not self-explanatory, using it is fine — **but add a comment
explaining what it does and why it's there.** Never leave an unexplained idiom in the code.

Concretely:

| Avoid | Prefer |
|---|---|
| `if value % k:` | `if value % k != 0:` |
| `if not problems:` | `if len(problems) == 0:` |
| `sum(map(sum, grid))` | a named helper with an explicit loop |
| `check(g) or "legal"` | an explicit `if` / `else` |
| nested list comprehensions | named intermediate variables, or plain loops |
| `status in (A, B)` | `status == A or status == B` |
| single-letter names (`d`, `k`, `q`) | `cells`, `divisor`, `quotient` |

Also:

- Give every function a docstring saying what it returns, not how it works.
- Comment the **why**, never the syntax. `# the objective becomes a constraint, since an
  objective silently disables enumeration` is useful; `# loop over rows` is noise.
- Name things after the problem domain (`row_digit_sum_expression`), not the implementation.
- Two names that look alike but mean different things is a bug in the writing. Rename one.

This costs nothing that matters here — see the performance note below.

## Before editing any existing file

**Commit the current state to git first.** Always, before modifying a file that already exists.
This makes every change recoverable from the Source Control panel, even if there are unsaved
edits in the editor that would otherwise be lost when the file is rewritten.

Then say what file is about to change, so it can be saved (`Cmd+S`) beforehand — VS Code
auto-reloads a file from disk only when the buffer has no unsaved changes. If a reload is needed
anyway: Command Palette -> **File: Revert File**, or close and reopen the tab for `.ipynb`.

Unsaved VS Code buffers are written to a hot-exit backup under
`~/Library/Application Support/Code/Backups/` every few seconds, and can be recovered from there
if something is overwritten. This is a last resort, not the plan.

## Solver work

Puzzles are solved with **OR-Tools CP-SAT** in Jupyter notebooks. Use the modern `snake_case`
API (`model.new_int_var`, `model.add`), not the legacy `CamelCase` aliases.

Environment is a single `uv` venv at the repo root, shared by every puzzle folder and gitignored:

```bash
uv venv
uv pip install ortools ipykernel
```

VS Code auto-detects `.venv` as a notebook kernel. There is no `pyproject.toml` and no Jupyter
server.

**Performance note.** The explicit style above applies to *model construction*, which runs once
and takes microseconds. The actual search happens in OR-Tools' C++ core, which never sees your
Python. A comprehension and an equivalent `for` loop produce a byte-identical model. Write for
clarity and lose nothing.

The one place to think about efficiency is the **model itself** — tight variable domains, linear
rather than modulo encodings, implied constraints. That is where orders of magnitude live, and
it is unrelated to Python style.

## Method for a new puzzle

1. Write `check(solution)` in plain Python **before** the model.
2. Validate it against a known-good instance (Jane Street usually supplies an example).
3. Encode the rules; solve; confirm `OPTIMAL` with a zero gap.
4. Add your own deductions as *implied* constraints, then assert the objective did not move.
5. Drop the objective, constrain `total == best`, and enumerate.
6. Run `check()` on everything before submitting.

[`2014-01/sum-of-squares.ipynb`](2014-01/sum-of-squares.ipynb) is the worked reference for this
method and doubles as a CP-SAT tutorial.

## Puzzles I want to solve unaided

Some puzzles are being solved without help. **Never read or fetch the published solution page
for these**, and don't reveal the answer in chat — leave notebook outputs cleared so I see it
first when I run them.

- `2026-04` — Can U Dig It?
- `2014-01` — Sum of Squares
