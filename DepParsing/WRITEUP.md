# Dependency Parsing Write-up

## (a)

Target dependencies:

- `ROOT -> attended`
- `attended -> I`
- `attended -> lectures`
- `attended -> class`
- `class -> in`
- `class -> the`
- `class -> NLP`

| Step | Stack | Buffer | New dependency | Transition |
| --- | --- | --- | --- | --- |
| 0 | `[ROOT]` | `[I, attended, lectures, in, the, NLP, class]` | | Initial configuration |
| 1 | `[ROOT, I]` | `[attended, lectures, in, the, NLP, class]` | | SHIFT |
| 2 | `[ROOT, I, attended]` | `[lectures, in, the, NLP, class]` | | SHIFT |
| 3 | `[ROOT, attended]` | `[lectures, in, the, NLP, class]` | `attended -> I` | LEFT-ARC |
| 4 | `[ROOT, attended, lectures]` | `[in, the, NLP, class]` | | SHIFT |
| 5 | `[ROOT, attended]` | `[in, the, NLP, class]` | `attended -> lectures` | RIGHT-ARC |
| 6 | `[ROOT, attended, in]` | `[the, NLP, class]` | | SHIFT |
| 7 | `[ROOT, attended, in, the]` | `[NLP, class]` | | SHIFT |
| 8 | `[ROOT, attended, in, the, NLP]` | `[class]` | | SHIFT |
| 9 | `[ROOT, attended, in, the, NLP, class]` | `[]` | | SHIFT |
| 10 | `[ROOT, attended, in, the, class]` | `[]` | `class -> NLP` | LEFT-ARC |
| 11 | `[ROOT, attended, in, class]` | `[]` | `class -> the` | LEFT-ARC |
| 12 | `[ROOT, attended, class]` | `[]` | `class -> in` | LEFT-ARC |
| 13 | `[ROOT, attended]` | `[]` | `attended -> class` | RIGHT-ARC |
| 14 | `[ROOT]` | `[]` | `ROOT -> attended` | RIGHT-ARC |

## (b)

A sentence with `n` words is parsed in `2n` steps. Each word must be shifted from the buffer to the stack exactly once, giving `n` SHIFT transitions, and the final tree has one head assignment for each word, giving `n` arc transitions including the root attachment.

## (c)

The data is stored in a CoNLL-style format. Each word is on its own line, with the different fields separated by tabs, and blank lines mark the end of a sentence. The important fields for this assignment are the word id, the word itself, its POS tags, its head word, and the dependency label. The sentences are already tokenized and tagged, so the parser can use the given word and tag information directly.

## (g)

Best dev UAS: `88.59`, achieved at epoch 9.

Test UAS: `89.17`.

UAS is useful because dependency parsing primarily needs to recover which token is the syntactic head of each token. For example, in the sentence from part (a), correctly attaching `I`, `lectures`, and `class` to `attended` shows that the parser recovered the main predicate and its core dependents. The dev and test UAS scores are also above the assignment's threshold of 87.

UAS has its limits because it only checks whether each word is attached to the right head. It does not care whether the relation label is correct. For example, the parser would still get credit for attaching `class` to `attended` even if it gave that dependency the wrong label. UAS also treats every wrong attachment the same, even though some mistakes matter more than others. Attaching `I` to the wrong word would usually change the sentence meaning more than misattaching a word like `the`.