# Knight Moves 7 — reference

Source: https://www.janestreet.com/puzzles/pent-up-frustration-3-knight-moves-7-index/
Image:  https://www.janestreet.com/puzzles/pent-3-knight-7.png  (855x855)

## Rules (verbatim)

The board above has been tiled with the 12 pentominoes (plus a 2-by-2 tetromino) into 13
regions. Think of each of these 13 regions as constructed out of 1-by-1-by-1 cubes. We need
to add a tower to each region. A tower is an additional size-1 cube placed on one of a
region's squares.

After adding these towers, place a knight at the bottom-left square. It then proceeds to
make knight's moves until it has visited all the towers. It never visits the same space
twice. (A move on this board involves travelling 0 units in one dimension, 1 in another,
and 2 in the third. The knight is allowed to "pass through" towers as it moves.)

But there's a catch: As you can see, the knight starts with a score of 0. On its Nth move,
its score increases by N if the move is to a location at the same altitude as the square it
moved from. If, instead, it moves up, the score is multiplied by N. And finally, if it moves
down, the score is divided by N. This last type of move is only allowed if the score is
evenly divisible by N.

Every three moves, up until move #18, the knight wrote down its score upon arriving at a
given square. From then on it only wrote down its score every K moves, for some larger value
K. Using this information, can you reconstruct the knight's path?

After filling all the remaining visited squares with the missing score values, find the
unvisited squares. For each of these squares, compute the sum of the scores in any
orthogonally adjacent squares that were part of the knight's path. The answer to this puzzle
is the sum of these "neighbor sums" from the unvisited squares.

## Board (a1 = bottom-left = the "0" start square)

Letters are the pentomino name of each region; O is the 2x2 tetromino.

```
      a  b  c  d  e  f  g  h
  8   I  I  I  I  I  V  V  V     8
  7   U  U  U  P  P  Z  Z  V     7
  6   U  N  U  P  P  P  Z  V     6
  5   Y  N  N  O  O  F  Z  Z     5
  4   Y  Y  N  O  O  F  F  L     4
  3   Y  T  N  X  F  F  W  L     3
  2   Y  T  X  X  X  W  W  L     2
  1   T  T  T  X  W  W  L  L     1
      a  b  c  d  e  f  g  h
```

Given scores (12 cells):

    a1 = 0 (start)   a5 = 528   b4 = 449   b3 = 750
    d6 = 23          f6 = 138   d3 = 88    e4 = 16
    f8 = 37          h8 = 1100  g3 = 1     f3 = 272

### How this was extracted

Rendered the PNG to a canvas and measured pixels rather than eyeballing:

- Grid lines at 48.5, 143.5, ..., 808.5 -> 8x8, cell size exactly 95px.
- Every interior edge measured: thin = 2px, thick = 7px, no ambiguous values.
- Flood fill with those walls -> 13 regions, sizes 5x12 + 4, total 64.
- Shape check: the 13 regions are exactly the 12 distinct free pentominoes
  (I V U P Z N Y F L T X W) plus one 2x2 tetromino. A single mis-read wall would
  almost certainly have produced a duplicate shape or a non-pentomino, so this is
  strong independent confirmation.
- Scanned each cell interior for ink -> exactly 12 cells contain numbers.

## Derived move set

The board is one cube thick, so a square's standable altitude is 0 (plain) or 1 (tower).
A move's displacement (dx, dy, dz) is a signed permutation of (0, 1, 2). Since |dz| <= 1,
the dz = +/-2 case is impossible. That leaves exactly two families:

| Family | Displacement                    | Altitude        | Score on move N         |
|--------|---------------------------------|-----------------|-------------------------|
| Level  | ordinary knight move, dz = 0    | both ends equal | score += N              |
| Up     | straight 2 squares orthogonally | plain -> tower  | score *= N              |
| Down   | straight 2 squares orthogonally | tower -> plain  | score /= N if divisible |

Consequences:

- A knight on a tower can make an ordinary knight move only to another tower.
- Up/down moves are rook-like two-steppers, not knight moves.
- Score starts at 0, and 0 is divisible by everything, so early down-moves are legal
  and leave the score at 0.
- Each square has exactly one standable altitude, so "never visits the same space twice"
  reduces to never revisiting a square.

## Derived checkpoint structure (tool has this OFF by default)

A square shows a number iff the knight was on it at a recording moment. Recording moments
are moves 0, 3, 6, 9, 12, 15, 18, then 18+K, 18+2K, ... for some K > 3.

12 clue cells = 7 early records (including move 0) + 5 late records, so the path reaches at
least move 18+5K. The path visits M+1 <= 64 distinct squares, so M <= 63, giving K <= 9.

| K | total moves M must be in |
|---|--------------------------|
| 4 | 38-41 |
| 5 | 43-47 |
| 6 | 48-53 |
| 7 | 53-59 |
| 8 | 58-63 |
| 9 | 63 exactly |

The first clue cell hit after move 18 pins K, after which every remaining checkpoint move
number is fixed.
