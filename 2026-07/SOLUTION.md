# Knight Moves 7 — solution

**Answer: 33609**

Jane Street, July 2026 — [‘Pent-Up’ Frustration 3 / Knight Moves 7](https://www.janestreet.com/puzzles/pent-up-frustration-3-knight-moves-7-index/).
Rules, board extraction and the derived move set are in [`PUZZLE.md`](PUZZLE.md).

---

## The two facts everything rests on

**1. There are only three kinds of move, and the altitude decides which.**

A move's displacement `(dx, dy, dz)` is a signed permutation of `(0, 1, 2)`. The board is one
cube thick, so a square's standable altitude is 0 (ground) or 1 (tower) — which makes
`dz = ±2` impossible. Only two families survive:

| move | shape | altitude | score on move N |
|---|---|---|---|
| **level** | ordinary knight move | both ends equal | `score + N` |
| **up** | straight 2 orthogonally | ground → tower | `score × N` |
| **down** | straight 2 orthogonally | tower → ground | `score ÷ N`, only if it divides |

Two consequences do most of the work later. A knight standing on a tower can only make an
ordinary knight move **to another tower**. And `×` and `÷` must alternate, with any run of `+`
between them — never two multiplies or two divides in a row.

**2. A square shows a number *if and only if* the knight was on it at a recording moment.**

Recording moments are moves 0, 3, 6, …, 18, then every `K` moves. Twelve clue cells means
7 early records plus **5** late ones, so the path reaches move `18 + 5K`. It visits `M+1 ≤ 64`
distinct squares, so `M ≤ 63`, giving **`4 ≤ K ≤ 9`**. Equally useful in the other direction:
landing on a clue cell at a *non*-recording move is illegal, which kills candidate routes fast.

---

## Opening: moves 1–3 are forced

`g3 = 1` is the smallest clue and the natural first target. Getting from 0 to 1 using moves
1, 2, 3 leaves essentially one option: `0 +1 +2 = 3`, then `÷3 = 1`.

That shape has teeth. Two level moves then a descent means moves 1 and 2 happen **at tower
altitude**, so the start square and the next two are all towers — and since each region holds
exactly one tower, there is only one way to place them:

- `a1` — region **T** (the start)
- `c2` — region **X** (the plus pentomino)
- `e3` — region **F**

Three towers placed and three moves fixed, before anything else.

## Moves 4–18: the deterministic run

Each leg is the only way to hit the next clue in the moves available.

| leg | arithmetic | notes |
|---|---|---|
| #4–#6 → `e4` = 16 | `1 +4 +5 +6` | flat; `×5` and `×4` variants overshoot or miss |
| #7–#9 → `d6` = 23 | `16 ×7 = 112`, `÷8 = 14`, `+9 = 23` | up to `e6` (**P**), back down |
| #10–#12 → `a5` = 528 | `23 +10 +11 = 44`, `×12 = 528` | up onto `a5` (**Y**) |
| #13–#15 → `f8` = 37 | `528 +13 = 541`, `+14 = 555`, `÷15 = 37` | two level moves *at tower altitude* |
| #16–#18 → `d3` = 88 | `37 +16 +17 +18` | see the crux below |

The `#13–#15` leg hides a deduction. Both moves 13 and 14 are level and both endpoints
(`a5`, `d8`) are towers, so the square at move 13 is **also a tower**, knight-adjacent to both.
The intersection of their knight neighbourhoods is exactly `{b7, c6}` — both in region **U**.
So move 13 is region U's tower, and region U is spoken for.

The realisation that reframed everything here was re-reading *"it never visits the same space
twice."* That single constraint collapses most of the branching.

## Finding K

Move 19 begins the non-deterministic stretch. A useful bound came first: with 19 moves used,
5 late records still to place, and only 64 squares, `K` cannot exceed **9** — otherwise the
path would need more squares than the board has.

From 88 on the ground, `88 × 20 = 1760` already exceeds every clue, so any multiply has to be
paired with a divide soon after. Searching multiply-then-divide shapes by hand is tedious, so
this is the point where the [score-paths tool](score-paths.html) got built. It found:

```
88 +19 107 +20 127 ×21 2667 +22 2689 +23 2712 ÷24 113 +25 138
```

Seven moves, landing on `f6 = 138` at move 25. **K = 7** — and 7 turns out to be the *only*
value in 4–9 consistent with the eventual clue placements.

That also demands three towers in a row at moves 21, 22, 23 (`×21` climbs, then two level
moves at tower altitude, then `÷24` descends).

## The remaining legs

With `K = 7` the late checkpoints are fixed at moves 25, 32, 39, 46, 53.

| leg | arithmetic | towers used |
|---|---|---|
| #26–#32 → `f3` = 272 | `138 +26 +27 +28 +29 = 248`, `×30 = 7440`, `÷31 = 240`, `+32 = 272` | 1 |
| #33–#39 → `b4` = 449 | `272 ×33 = 8976`, `÷34 = 264`, `+35 … +38 = 410`, `+39 = 449` | 1 |
| #40–#46 → `b3` = 750 | pure addition: `449 + (40+…+46) = 449 + 301 = 750` | 0 |
| #47–#53 → `h8` = 1100 | pure addition: `750 + (47+…+53) = 750 + 350 = 1100` | 0 |

The last two legs are seven consecutive level moves each, so all fifteen of those squares sit
on the ground — a strong constraint on where they can be.

## The crux: g6 cannot be on the move-16 leg

The 88 → 138 route wanted `g6` at move 16. It can't have it, and the reason is a tower-budget
argument about the far end of the path.

- Move 53 lands on `h8` via `+53`, a **level** move into a ground square. Its predecessor must
  be a ground knight-neighbour of `h8`, and there are exactly two: **`f7` and `g6`**.
- Move 23 is `+23` from `e5`, a tower — so it lands on **another tower**, knight-adjacent to
  `e5`. Eight candidates; `d7` (region P) and `g4` (region F) are out because those regions
  already have towers, and `c4`/`d3`/`f3` are already used. That leaves `f7`, `c6`, `g6`.
- `c6` dies too: move 13 is already region U's tower and `c6` is in region U, so choosing it
  would give U two towers.
- So move 23 ∈ {`f7`, `g6`} — region **Z**'s tower — and move 52 ∈ {`f7`, `g6`} on the ground.
  They are different squares, so **the path consumes both**.

Neither is available at move 16. Enumerating every level-knight route
`f8 →(16) X →(17) Y →(18) d3` with both intermediates on the ground then gives exactly one
survivor:

> **`f8 → d7 → c5 → d3`**, scoring 37 → 53 → 70 → 88.

Without the `g6` ban there were two routes; this deduction is what collapses it to one.

## Endgame

Two bifurcations remained, both resolved by following a branch to contradiction:

1. **Which tower move 33 climbs to** out of `272`. One choice propagated deterministically to
   a contradiction, which settled the other.
2. **How to work backwards from 750 to 449**, where two routes were open. The first choice
   led to a consistent completion through to 1100.

A neat closing check falls out of the finished score chain: count the tower-altitude squares
among moves 0–54 and there are exactly **13**. Since exactly 13 towers exist and no square is
revisited, every tower is visited by move 54, and move 54 lands on one (`h6`). The knight
stops when it has visited all the towers, so **the path ends at move 54** — 55 squares
visited, 9 unvisited. Consistent with `K = 7`: the next record would be move 60, which never
happens.

---

## The solution

### Towers

| region | square | visited at |
|---|---|---|
| T | `a1` | #0 |
| X | `c2` | #1 |
| F | `e3` | #2 |
| P | `e6` | #7 |
| Y | `a5` | #12 |
| U | `b7` | #13 |
| I | `d8` | #14 |
| N | `c4` | #21 |
| O | `e5` | #22 |
| Z | `f7` | #23 |
| W | `e1` | #30 |
| L | `h3` | #33 |
| V | `h6` | #54 |

### The path

| # | sq | op | score | | # | sq | op | score | | # | sq | op | score |
|--:|:--|:--|--:|-|--:|:--|:--|--:|-|--:|:--|:--|--:|
| 0 | `a1`▲ | — | **0** | | 19 | `b2` | `+19` | 107 | | 38 | `c6` | `+38` | 410 |
| 1 | `c2`▲ | `+1` | 1 | | 20 | `a4` | `+20` | 127 | | 39 | `b4` | `+39` | **449** |
| 2 | `e3`▲ | `+2` | 3 | | 21 | `c4`▲ | `×21` | 2667 | | 40 | `a6` | `+40` | 489 |
| 3 | `g3` | `÷3` | **1** | | 22 | `e5`▲ | `+22` | 2689 | | 41 | `c7` | `+41` | 530 |
| 4 | `h1` | `+4` | 5 | | 23 | `f7`▲ | `+23` | 2712 | | 42 | `b5` | `+42` | 572 |
| 5 | `f2` | `+5` | 10 | | 24 | `h7` | `÷24` | 113 | | 43 | `a3` | `+43` | 615 |
| 6 | `e4` | `+6` | **16** | | 25 | `f6` | `+25` | **138** | | 44 | `b1` | `+44` | 659 |
| 7 | `e6`▲ | `×7` | 112 | | 26 | `d5` | `+26` | 164 | | 45 | `d2` | `+45` | 704 |
| 8 | `e8` | `÷8` | 14 | | 27 | `c3` | `+27` | 191 | | 46 | `b3` | `+46` | **750** |
| 9 | `d6` | `+9` | **23** | | 28 | `a2` | `+28` | 219 | | 47 | `d4` | `+47` | 797 |
| 10 | `c8` | `+10` | 33 | | 29 | `c1` | `+29` | 248 | | 48 | `e2` | `+48` | 845 |
| 11 | `a7` | `+11` | 44 | | 30 | `e1`▲ | `×30` | 7440 | | 49 | `f4` | `+49` | 894 |
| 12 | `a5`▲ | `×12` | **528** | | 31 | `g1` | `÷31` | 240 | | 50 | `g2` | `+50` | 944 |
| 13 | `b7`▲ | `+13` | 541 | | 32 | `f3` | `+32` | **272** | | 51 | `h4` | `+51` | 995 |
| 14 | `d8`▲ | `+14` | 555 | | 33 | `h3`▲ | `×33` | 8976 | | 52 | `g6` | `+52` | 1047 |
| 15 | `f8` | `÷15` | **37** | | 34 | `h5` | `÷34` | 264 | | 53 | `h8` | `+53` | **1100** |
| 16 | `d7` | `+16` | 53 | | 35 | `g7` | `+35` | 299 | | 54 | `h6`▲ | `×54` | 59400 |
| 17 | `c5` | `+17` | 70 | | 36 | `f5` | `+36` | 335 | |  |  |  |  |
| 18 | `d3` | `+18` | **88** | | 37 | `e7` | `+37` | 372 | |  |  |  |  |

### Unvisited squares

| square | on-path neighbours | sum |
|---|---|--:|
| `a8` | `a7`=44 | 44 |
| `b8` | `b7`=541 + `c8`=33 | 574 |
| `g8` | `g7`=299 + `f8`=37 + `h8`=1100 | 1436 |
| `b6` | `b7`=541 + `b5`=572 + `a6`=489 + `c6`=410 | 2012 |
| `g5` | `g6`=1047 + `f5`=335 + `h5`=264 | 1646 |
| `g4` | `g3`=1 + `f4`=894 + `h4`=995 | 1890 |
| `h2` | `h3`=8976 + `h1`=5 + `g2`=944 | 9925 |
| `d1` | `d2`=704 + `c1`=248 + `e1`=7440 | 8392 |
| `f1` | `f2`=10 + `e1`=7440 + `g1`=240 | 7690 |
| | **total** | **33609** |

`▲` marks a tower. Bold scores are the twelve printed clues, at moves 0, 3, 6, 9, 12, 15, 18,
25, 32, 39, 46, 53.

## Answer extraction

For each unvisited square, sum the scores of its orthogonally adjacent squares that lie on the
path; add those nine sums.

## **Answer: 33609**

---

## Tools

Built along the way, all self-contained HTML in this directory:

- **[`knight-sandbox.html`](knight-sandbox.html)** — the board. Place and remove towers, mark
  squares `?` / `✗ no tower`, walk the knight with legal moves highlighted and the resulting
  score previewed on hover. Runs can start anywhere, float without a move number until one is
  known, be built forwards *or backwards* (inverting each operation), and join up when they
  meet — sharing out their numbering.
- **[`score-paths.html`](score-paths.html)** — pure score arithmetic, no board. Given a score,
  a move number and an altitude, enumerate what is reachable, connect two scores in a fixed
  number of moves, or chain clue values checkpoint to checkpoint. This is what found `K = 7`.
- **[`print-grids.html`](print-grids.html)** — blank grids, four to a page.

Neither tool solves anything: they answer *"is this legal, and what does it score"*, never
*"what should I play next"*. The deductions above — the forced opening, `K = 7`, the tower
placements, the `g6` elimination — were all made by hand. Once those pinned every score and
altitude, filling in the last 31 squares was a mechanical search with a unique answer.

## Verification

The final path was checked independently of the search that produced it: replaying from score
0, confirming every displacement really is a signed permutation of `(0,1,2)`, doing the
arithmetic in exact rationals to catch any non-integer division, confirming all 13 towers sit
one per region, that all 12 clue cells hit their printed values at the `K = 7` recording
moments and nowhere else, and that the path ends exactly when the last tower is reached.
No errors. The solution is unique given the deductions above.
