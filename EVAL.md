# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

ANSWER:
Dense - uses bge-small, documents are chunked into 300-word chunks that overlap by 50 words and embeds each chunk, dense was not fused, and nothing was changed from the previous lab code
Hybrid - combines both bm25 and dense, where the documents were chunked in a similar manner with dense, but bm25 embedded chunks via term simularity. Hybrid was fused by having both bm25 and dense output their induvidual simularities, and then hybrid ranked answers/documents based on their combined rank. Nothing changed between labs
Rerank - uses hybrid first, then claude to evaluate the top options provided by hybrid, only reading chunks of the articles. The reranker saw the top 20 candidates from hybrid, and nothing was changed from labs 12 and 13.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.592 | 0.471 | 0.444 |
| rerank | 0.758 | 0.800 | 0.769 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.500 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.154 | 0.792 |
| hybrid | nDCG@10 | 0.397 | 0.203 | 0.779 |
| rerank | Recall@10 | 0.714 | 0.595 | 1.000 |
| rerank | MRR@10 | 0.714 | 0.714 | 1.000 |
| rerank | nDCG@10 | 0.714 | 0.626 | 1.000 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.033 | [-0.250, +0.192] | 0.324 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.036 | [-0.178, +0.084] | 0.193 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.075 | [-0.238, +0.075] | 0.228 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.033 | [-0.125, +0.192] | 0.231 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.091 | [-0.305, +0.110] | 0.300 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.036 | [-0.199, +0.113] | 0.227 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.133 | [-0.100, +0.358] | 0.340 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.293 | [+0.043, +0.533] | 0.353 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.251 | [+0.022, +0.466] | 0.323 | rerank higher |
| rerank minus dense | Recall@10 | +0.200 | [+0.050, +0.367] | 0.224 | rerank higher |
| rerank minus dense | MRR@10 | +0.237 | [+0.083, +0.408] | 0.239 | rerank higher |
| rerank minus dense | nDCG@10 | +0.289 | [+0.149, +0.443] | 0.214 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | 0.166 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | 0.246 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.325 | [+0.199, +0.453] | 0.184 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

ANSWER:
It seems that many of the differences between dense, bm25, and hybrid are all not distiguishable, meaning there would not be a huge difference in interchanging the approaches. However, almost every rerank difference is noticable, meaning that using claude to rerank the items had a huge difference. The minimum detectable difference at 20 queries seems to be between rerank and hybrid, and this makes the case that any gap smaller would signify the same approaches being compared. My claim from lecture 12 and 13 about rerank being the best overall is supported by rerank having a significant difference in performance against the other approaches. However, the numbers still signify that bm25 is not nessessarily better than the hybrid or dense approach as I thought it would be.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 12 of 12 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

ANSWER:
It seemed that the rerank system answered due to its clear better performance over the other approaches. I did not change anything in prompts/answer.txt and neither moved.
a01: the quote did support the claim next to it, and i verified it in the cited corpus
a02: the quote did support the claim next to it but it did also provide additional, not nessessarily required details, and i verified it in the cited corpus.
a04: similar story to a02 where the answer was provided and did in fact exist in the corpus, but the answer added additional details

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

ANSWER:
The corpus is a collection of construction regulations and requirements and it came from the us government public database, with roughly 307 documents at around 1000MB. The license basis is public and available for anyone to use. There were two documents that contained published keywords that pointed to other peoples work, but since the documents I downloaded only mentioned where one could learn more and did not actually hold any copyrighted material, I decided to move forward with the documents.
Comes from the eCFR.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

ANSWER:
Total of 30 queries, 20 by claude and 10 by hand. Used identifier, paraphrase, and mixed classes in order to test areas that certain models struggle with/are better at. I decided if a document is relevant if it could directly answer the question. In the case that a question needed multiple documents to find the answer, I gave a document credit if it was part of that list. I found candidates by both using claude to help and by directly reading 10-20 documents myself to also provide test cases that I specifically verified. I chose to continue using binary labels.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 1.000 | 0.772 | 0.829 |
| dense | 0.800 | 0.593 | 0.643 |
| hybrid | 0.900 | 0.738 | 0.778 |
| rerank | 0.967 | 0.888 | 0.908 |

30 judged queries; nDCG uses binary labels; a random ranking of the 307 documents would get recall@10 near 0.033.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | identifier (n=8) | paraphrase (n=13) | mixed (n=9) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 1.000 | 1.000 |
| bm25 | MRR@10 | 0.812 | 0.691 | 0.852 |
| bm25 | nDCG@10 | 0.862 | 0.767 | 0.889 |
| dense | Recall@10 | 0.375 | 1.000 | 0.889 |
| dense | MRR@10 | 0.087 | 0.750 | 0.815 |
| dense | nDCG@10 | 0.154 | 0.811 | 0.833 |
| hybrid | Recall@10 | 0.625 | 1.000 | 1.000 |
| hybrid | MRR@10 | 0.297 | 0.923 | 0.861 |
| hybrid | nDCG@10 | 0.376 | 0.943 | 0.896 |
| rerank | Recall@10 | 0.875 | 1.000 | 1.000 |
| rerank | MRR@10 | 0.875 | 0.819 | 1.000 |
| rerank | nDCG@10 | 0.875 | 0.864 | 1.000 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=10) | claude (n=20) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | not distinguishable |
| bm25 | MRR@10 | 0.870 | 0.723 | +0.147 | [-0.078, +0.353] | not distinguishable |
| bm25 | nDCG@10 | 0.902 | 0.792 | +0.110 | [-0.061, +0.266] | not distinguishable |
| dense | Recall@10 | 0.700 | 0.850 | -0.150 | [-0.500, +0.150] | not distinguishable |
| dense | MRR@10 | 0.492 | 0.643 | -0.151 | [-0.464, +0.178] | not distinguishable |
| dense | nDCG@10 | 0.543 | 0.692 | -0.149 | [-0.450, +0.154] | not distinguishable |
| hybrid | Recall@10 | 0.900 | 0.900 | +0.000 | [-0.250, +0.200] | not distinguishable |
| hybrid | MRR@10 | 0.750 | 0.731 | +0.019 | [-0.275, +0.294] | not distinguishable |
| hybrid | nDCG@10 | 0.786 | 0.774 | +0.013 | [-0.252, +0.254] | not distinguishable |
| rerank | Recall@10 | 1.000 | 0.950 | +0.050 | [+0.000, +0.150] | not distinguishable |
| rerank | MRR@10 | 1.000 | 0.832 | +0.168 | [+0.050, +0.311] | hand higher |
| rerank | nDCG@10 | 1.000 | 0.861 | +0.139 | [+0.037, +0.268] | hand higher |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | +0.150 | +0.300 | -0.150 | [-0.500, +0.150] | not distinguishable |
| MRR@10 | +0.079 | +0.378 | -0.299 | [-0.668, +0.117] | not distinguishable |
| nDCG@10 | +0.100 | +0.359 | -0.259 | [-0.596, +0.104] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.82 (10 queries), claude 0.78 (20 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 10 hand and 20 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.200 | [-0.333, -0.067] | 0.208 | bm25 higher |
| dense minus bm25 | MRR@10 | -0.179 | [-0.368, +0.008] | 0.273 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.186 | [-0.355, -0.024] | 0.242 | bm25 higher |
| hybrid minus bm25 | Recall@10 | -0.100 | [-0.200, +0.000] | 0.156 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.034 | [-0.198, +0.122] | 0.236 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.051 | [-0.196, +0.082] | 0.204 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.100 | [+0.000, +0.233] | 0.156 | not distinguishable |
| hybrid minus dense | MRR@10 | +0.145 | [+0.052, +0.246] | 0.142 | hybrid higher |
| hybrid minus dense | nDCG@10 | +0.135 | [+0.058, +0.216] | 0.116 | hybrid higher |
| rerank minus bm25 | Recall@10 | -0.033 | [-0.100, +0.000] | 0.093 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.116 | [+0.003, +0.236] | 0.169 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.079 | [-0.016, +0.174] | 0.138 | not distinguishable |
| rerank minus dense | Recall@10 | +0.167 | [+0.033, +0.300] | 0.194 | rerank higher |
| rerank minus dense | MRR@10 | +0.296 | [+0.130, +0.466] | 0.242 | rerank higher |
| rerank minus dense | nDCG@10 | +0.265 | [+0.119, +0.421] | 0.219 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.067 | [+0.000, +0.167] | 0.130 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.151 | [+0.010, +0.300] | 0.211 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.130 | [+0.012, +0.258] | 0.180 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

ANSWER:
It seems that dense was notably distinguishable from the rest of the approaches, whereas rerank and bm25 were not very distinguishable(suprising). Overall, it seemed that the models performed better on the hand queries, which was suprising. But models tended to perform very similar on hand vs claude queries on many of them too. My prediction in prompt 1 did not in fact hold, as rerank performed equally to bm25 suprisingly.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
_No ablation runs yet: `uv run p2 run --corpus own --system NAME --ablation` writes one to runs/own/ablation/, then `uv run p2 score` fills this table._
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
_No ablation runs yet: `uv run p2 run --corpus own --system NAME --ablation` writes one to runs/own/ablation/, then `uv run p2 score` fills this table._
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

TODO: write the ablation: the one change, the hypothesis, the result and the claim.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
| --- | ----------------------------- | ----------------- | ----- | ------------------ |

TODO: add one row for each failure you analyzed, and write two or three sentences on the pattern you see across them.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

TODO: write the cross-corpus comparison.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 193,698 | 4,276 | 93.6 | 16,142 | 356 | 7.8 |
| traces/own-own-rerank.jsonl | rerank | 30 | 30 | 2 | 504,746 | 2,730 | 102.2 | 16,825 | 91 | 3.4 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 2 | 283,925 | 2,016 | 68.7 | 14,196 | 101 | 3.4 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 0 | 580,348 | 3,862 | 127.2 | 14,509 | 97 | 3.2 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.293 | [-0.533, -0.043] | 14,196 | 3.4 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.237 | [-0.408, -0.083] | 14,196 | 3.4 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.329 | [-0.504, -0.164] | 14,196 | 3.4 | rerank higher |
| own: bm25 minus rerank | 30 | -0.116 | [-0.236, -0.003] | 16,825 | 3.4 | rerank higher |
| own: dense minus rerank | 30 | -0.296 | [-0.466, -0.130] | 16,825 | 3.4 | rerank higher |
| own: hybrid minus rerank | 30 | -0.151 | [-0.300, -0.010] | 16,825 | 3.4 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 30 | 0.04 | 1.3 |
| traces/retrieval/own-own-dense.jsonl | dense | 30 | 0.27 | 9.1 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 30 | 0.32 | 10.6 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.09 | 4.6 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.30 | 14.9 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.44 | 22.0 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.15 | 3.7 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.65 | 16.1 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.90 | 22.6 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
_No repeated runs or answers files yet (598E: `p2 run ... --repeat 3` and `p2 answer ... --repeat 3`)._
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
