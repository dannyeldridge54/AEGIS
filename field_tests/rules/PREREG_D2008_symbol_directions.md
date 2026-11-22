# PREREG D2008: Symbols as directional points (with letters on the PHOEN points). Locked before code and runs.
**Danny's idea.** The symbols on the page are directions in the framework, not just letters:
- openers point in;
- closers point out;
- separators point sideways;
- terminators end a line of motion;
- quotes toggle;
- a newline resets.

**Directional classes for non-letters (replacing D2007's 6 fixed ones):**
| class | bytes |
|---|---|
| digit | 0–9 |
| step | space |
| reset | newline |
| in (openers) | `( [ { <` |
| out (closers) | `) ] } >` |
| lateral (separators) | `\| = , ; :` |
| end (terminators) | `. ! ?` |
| toggle (quotes) | `' "` |
| other punctuation | everything else printable |
| high byte | ≥ 128 |

**Variants, same engine and node as D2007 (loomz6 class node, LR2 = 1), on the same held-out slice H:**
| variant | letters |
|---|---|
| DIR_PHOEN | the PHOEN classes |
| DIR_RAND1 | the RAND1 partition (null control for the letters) |
| DIR_ONE | all letters in one class (pure direction) |

D2007's results (same slice) are the comparison.

**Verdict.**
- Directions help if DIR_ONE or DIR_PHOEN is smaller than D2007's PHOEN **and** NONE by at least 0.05%.
- Letter ancestry helps (with directions) only if DIR_PHOEN is smaller than DIR_RAND1 by at least 0.05%.
- Each run must round-trip; DIR_PHOEN is checked by decompressing.
