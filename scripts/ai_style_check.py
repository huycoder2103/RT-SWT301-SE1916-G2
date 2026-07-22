#!/usr/bin/env python3
r"""
Writing-style audit for paper/sections/*.tex.

WHAT THIS IS. A checklist of prose patterns that LLM drafting tends to produce and
that human academic writing tends not to: uniform rhythm, formulaic connectives,
rhetorical symmetry, self-referential commentary. Each is also, independently, a
writing-quality defect, which is why they are worth fixing on their own terms.

WHAT THIS IS NOT. It is not an AI detector and does not estimate one's output.
A low score here does not mean a detector will pass the text, and chasing these
numbers does not make LLM-drafted prose author-original. The tool's real use is to
point at the specific sentences worth rewriting in your own voice; see the
"REVISE FIRST" list it prints at the end.

Usage:
    python scripts/ai_style_check.py            # summary + flagged lines
    python scripts/ai_style_check.py --verbose  # every flagged occurrence
"""
import glob
import os
import re
import statistics
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS = os.path.join(ROOT, "paper", "sections")

VERBOSE = "--verbose" in sys.argv

# ---------------------------------------------------------------- patterns

# Connectives that read as mechanical when they open a sentence.
TRANSITIONS = r"However|Moreover|Furthermore|Therefore|Indeed|Notably|Importantly|" \
              r"Additionally|Consequently|Nevertheless|Nonetheless|Crucially"

# Antithesis / balanced-clause frames.
ANTITHESIS = [
    (r"\b(is|was|are|were|does|do)\s+not\s+[^.;:]{3,80}[;,]\s*(it|they|that|this)\s+"
     r"(is|are|was|were)\b", "not-X-it-is-Y"),
    (r"\bnot\s+only\b[^.]{0,80}\bbut\b", "not-only-but"),
    (r"\brather\s+than\b[^.]{0,60}\b(is|are|was|were|it)\b", "rather-than pivot"),
    (r"\bWhere\b[^.,;]{3,60},[^.]{3,60}\.\s*Where\b", "Where X. Where Y."),
]

# Commentary about the paper rather than about the subject matter.
META = [
    r"we would rather", r"the (contribution|point) is", r"this is the practical case",
    r"we report this rather than", r"is not cosmetic", r"we read (this|it) as",
    r"is less \w+ than it (first )?appears", r"which is (why|what) we",
    r"it is worth (noting|stressing)", r"the honest reading",
]

# Stacked hedges: a hedge immediately qualified by another.
HEDGE_STACK = [
    r"we would expect[^.]{0,120}\bbut\b[^.]{0,80}\b(prediction|not a result)\b",
    r"(may|might|could) (plausibly|conceivably)",
    r"(suggest|indicate)s? that[^.]{0,80}(may|might|could)",
]

# Rule-of-three: "A, B, and C" / "A, B and C" in running prose.
TRICOLON = re.compile(r"\b\w[\w'-]*(?:\s+[\w'-]+){0,3},\s+\w[\w'-]*(?:\s+[\w'-]+){0,3},"
                      r"\s+(?:and|or)\s+\w")

SHOWY = (r"\b(precisely|decisively|comfortably|pointedly|actively|structurally|tautolog\w+|"
         r"inconvenient|quirk|paradox|cleverer|bites|crucially|fundamentally|profound\w*|"
         r"nuanced|underscore\w*|delve\w*|realm|landscape|testament|pivotal|multifaceted)\b")


# ---------------------------------------------------------------- helpers

def strip_tex(text):
    """Reduce LaTeX to running prose. Drops floats, math, macros, and markup."""
    t = re.sub(r"(?<!\\)%.*", "", text)
    t = re.sub(r"\\begin\{(tabular|table|figure|center|equation|align)\*?\}.*?"
               r"\\end\{\1\*?\}", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " NUM ", t)
    t = re.sub(r"\\(cite|ref|label|includegraphics|path|input)\{[^}]*\}", " ", t)
    t = re.sub(r"\\(textbf|textit|emph|texttt|textrm)\{([^{}]*)\}", r"\2", t)
    t = re.sub(r"\\[A-Za-z]+\*?(\[[^\]]*\])?", " ", t)
    t = re.sub(r"[{}$&~^_\\]", " ", t)
    return re.sub(r"[ \t]+", " ", t)


def paragraphs(prose):
    return [p.strip() for p in re.split(r"\n\s*\n", prose) if len(p.split()) >= 15]


def sentences(prose):
    flat = re.sub(r"\s+", " ", prose)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(])", flat)
            if len(s.split()) >= 3]


def line_of(source, needle):
    idx = source.find(needle[:45])
    return source[:idx].count("\n") + 1 if idx > 0 else 0


def flag(store, sect, source, quote, kind):
    store.append((sect, line_of(source, quote), kind, " ".join(quote.split())[:105]))


# ---------------------------------------------------------------- analysis

def main():
    files = sorted(glob.glob(os.path.join(SECTIONS, "*.tex")))
    if not files:
        print("no section files found under paper/sections/")
        return 1

    findings, rows = [], []
    all_lens, all_openers, all_words = [], [], Counter()

    for path in files:
        name = os.path.basename(path)
        raw = open(path, encoding="utf-8").read()
        prose = strip_tex(raw)
        sents = sentences(prose)
        paras = paragraphs(prose)
        if len(sents) < 4:
            continue

        lens = [len(s.split()) for s in sents]
        all_lens += lens

        for s in sents:
            first = s.split()[0].strip("(,.")
            all_openers.append(first)
            for w in re.findall(r"[a-z][a-z'-]{5,}", s.lower()):
                all_words[w] += 1

        # --- pattern sweeps
        for pat, kind in ANTITHESIS:
            for m in re.finditer(pat, prose, re.I):
                flag(findings, name, raw, m.group(0), kind)
        for pat in META:
            for m in re.finditer(pat, prose, re.I):
                seg = next((s for s in sents if m.group(0) in s), m.group(0))
                flag(findings, name, raw, seg, "meta-commentary")
        for pat in HEDGE_STACK:
            for m in re.finditer(pat, prose, re.I):
                flag(findings, name, raw, m.group(0), "stacked hedge")
        for m in re.finditer(SHOWY, prose, re.I):
            seg = next((s for s in sents if m.group(0) in s), m.group(0))
            flag(findings, name, raw, seg, f"showy: {m.group(0)}")

        tricolons = [s for s in sents if TRICOLON.search(s)]
        for s in tricolons:
            flag(findings, name, raw, s, "tricolon")

        opens = Counter(s.split()[0].strip("(,.") for s in sents)
        for word, n in opens.items():
            if n >= 4 and word.lower() not in {"the", "a", "an"}:
                findings.append((name, 0, f"repeated opener x{n}", f'"{word} ..."'))

        trans = sum(1 for s in sents if re.match(rf"^({TRANSITIONS})\b", s))

        rows.append({
            "file": name,
            "sent": len(sents),
            "mean": statistics.mean(lens),
            "sd": statistics.stdev(lens) if len(lens) > 1 else 0.0,
            "short": sum(1 for x in lens if x <= 10),
            "long": sum(1 for x in lens if x >= 30),
            "para_sd": (statistics.stdev([len(p.split()) for p in paras])
                        if len(paras) > 1 else 0.0),
            "trans": trans,
            "tri": len(tricolons),
        })

    # ------------------------------------------------------------ report
    print("=" * 78)
    print("WRITING-STYLE AUDIT  --  not an AI detector; see module docstring")
    print("=" * 78)

    print(f"\n{'section':22s}{'sent':>5}{'mean':>7}{'sd':>6}{'<=10':>6}{'>=30':>6}"
          f"{'para sd':>9}{'trans':>7}{'tri':>5}")
    print("-" * 78)
    for r in rows:
        print(f"{r['file']:22s}{r['sent']:5d}{r['mean']:7.1f}{r['sd']:6.1f}"
              f"{r['short']:6d}{r['long']:6d}{r['para_sd']:9.1f}{r['trans']:7d}{r['tri']:5d}")

    sd = statistics.stdev(all_lens)
    mean = statistics.mean(all_lens)
    ttr = len(all_words) / max(sum(all_words.values()), 1)
    print("-" * 78)
    print(f"{'OVERALL':22s}{len(all_lens):5d}{mean:7.1f}{sd:6.1f}"
          f"{sum(1 for x in all_lens if x <= 10):6d}"
          f"{sum(1 for x in all_lens if x >= 30):6d}")

    print(f"\nsentence-length variance : sd={sd:.1f} on mean={mean:.1f}")
    print("  Human academic prose typically lands sd 9-14. Below ~8 reads mechanical:")
    print("  vary rhythm by merging two short related sentences, or splitting a long one.")
    print(f"lexical variety (TTR)    : {ttr:.3f} over content words >5 chars")

    top = [f"{w} x{n}" for w, n in all_words.most_common(60)
           if n >= 7 and w not in {
               "manual", "faults", "mutants", "status", "oracle", "oracles", "suite",
               "suites", "paper", "section", "results", "testing", "generator",
               "generators", "coverage", "metric", "metrics", "evomaster", "specification",
               "operations", "endpoint", "scenarios", "population", "comparison"}][:12]
    if top:
        print(f"\nnon-domain words repeated 7+ times (check for tic usage):")
        print("  " + ", ".join(top))

    openers = [f"{w} x{n}" for w, n in Counter(all_openers).most_common(8) if n >= 8]
    if openers:
        print(f"\nmost common sentence openers: {', '.join(openers)}")

    print(f"\n{'-' * 78}\nFLAGGED PASSAGES ({len(findings)})\n{'-' * 78}")
    by_kind = Counter(k.split(":")[0] for _, _, k, _ in findings)
    for kind, n in by_kind.most_common():
        print(f"  {kind:24s} {n}")

    shown = findings if VERBOSE else findings[:20]
    print()
    for sect, line, kind, quote in shown:
        loc = f"{sect}:{line}" if line else sect
        print(f"  [{kind}] {loc}\n      {quote}")
    if not VERBOSE and len(findings) > len(shown):
        print(f"\n  ... {len(findings) - len(shown)} more; run with --verbose")

    print(f"\n{'=' * 78}")
    print("REVISE FIRST")
    print("=" * 78)
    worst = sorted(rows, key=lambda r: r["sd"])[:3]
    for r in worst:
        print(f"  {r['file']:22s} sd={r['sd']:.1f}  "
              f"({r['short']} short / {r['long']} long sentences)")
    print("\n  These sections have the most uniform rhythm, so they are where reading")
    print("  aloud and rewriting in your own voice will change the text most. That")
    print("  revision, not this script, is what makes the writing yours.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
