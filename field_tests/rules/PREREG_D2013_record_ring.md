# PREREG D2013: A record/2D ring, the most general node for non-text data. Locked before scoring.
**Danny: "if it can be stored on a computer, add rings or nodes to collect it".**
- One node covers many data families, because tables, images (rows of pixels), binary records and audio frames all repeat at their own natural period.
- The ring detects that period automatically: the same byte recurring at the same spacing three times sets rlen.
- It then predicts from the byte "above" (one period back), and from the column (position modulo the period).

**Engine.** loomz12 = loomz11 plus nodes 16 (above, above-right, two periods back) and 17 (above + last byte, column).

**Base.** The same binary with nodes 16 and 17 masked off.

**Corpus (1 MB each, or the whole file if smaller), mixed types:**
| file | content |
|---|---|
| txt | enwik8 slice F, the first 1 MB |
| exe | libc.so.6, the first 1 MB |
| img | a 24-bit RGB screenshot, raw, 1 MB |
| csv | targets.sqlite exported as CSV, 15.8 kB |
| db | the targets.sqlite binary, 49 kB |

xz -9e is the reference.

**Pass.**
- The record ring is ≥ 1% smaller on at least 2 of the 3 non-text binary/table files (img, csv, db).
- It costs ≤ 0.05% on txt.
- Round-trip OK on img.
