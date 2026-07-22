#!/usr/bin/env python3
r"""
Pre-compile sanity check for paper/ -- catches the errors LaTeX would only reveal at build
time, so the paper can be validated on a machine with no TeX installed.

Checks:
  1. every \Macro used in main.tex/sections/* is defined in paper/generated/numbers.tex
     (i.e. no undefined control sequence, and no number silently missing)
  2. every macro defined in numbers.tex is actually used (dead macro -> drift risk)
  3. every \input'ed file exists
  4. every \includegraphics target resolves via \graphicspath
  5. every \cite key exists in references.bib
  6. no hand-typed statistic: flags suspicious bare decimals/p-values in prose

Exit code 0 = clean, 1 = problems found.
Usage: python scripts/check_paper.py
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "paper")
NUMBERS = os.path.join(PAPER, "generated", "numbers.tex")
BIB = os.path.join(PAPER, "references.bib")

# LaTeX built-ins / package commands we must not report as undefined.
KNOWN = {
    "documentclass", "IEEEoverridecommandlockouts", "usepackage", "graphicspath",
    "input", "begin", "end", "title", "author", "IEEEauthorblockN", "IEEEauthorblockA",
    "IEEEauthorrefmark", "maketitle", "bibliographystyle", "bibliography", "section",
    "subsection", "subsubsection", "label", "ref", "cite", "textbf", "textit", "emph",
    "texttt", "includegraphics", "caption", "centering", "columnwidth", "toprule",
    "midrule", "bottomrule", "multicolumn", "small", "quad", "chi", "delta", "mu",
    "alpha", "leq", "geq", "approx", "times", "newcommand", "item", "enumerate",
    "url", "hidelinks", "textwidth", "linewidth", "center", "frac", "max", "min",
    "text", "mathrm", "left", "right", "hline", "footnotesize", "scriptsize",
    "vspace", "hspace", "noindent", "par", "and", "thanks", "IEEEkeywords",
    "bfseries", "itshape", "color", "textcolor", "verb", "S", "%", "&", "_", "#",
    "$", "{", "}", "\\", ",", ";", ":", "!", "@", "-", "/", "'", "`", '"', "~",
    "sim", "pm", "cdot", "ldots", "dots", "gg", "ll", "neq", "in", "subset",
    "rightarrow", "leftarrow", "Rightarrow", "Leftarrow", "to", "mapsto",
    "abstract", "keywords", "tabular", "table", "figure", "equation", "align",
    "IEEEtran", "textrm", "textsc", "underline", "sout", "footnote", "appendix",
    # Springer LNCS (llncs.cls) -- target format for EAI FISAT 2026.
    "titlerunning", "authorrunning", "institute", "email", "inst", "orcidID",
    "setlength", "tabcolsep", "arraystretch", "href", "subtitle", "spnewtheorem",
    # url package: \path{} is verbatim and breakable -- used for long file paths
    # that would otherwise overflow the LNCS text block as \texttt{}.
    "path", "urlstyle", "Urlmuskip",
    # llncs: credits environment + its mandatory run-in heading macros
    "credits", "discintname", "ackname",
}

# Sections that report OUR measurements -- a bare decimal here must come from numbers.tex.
# Related-work / intro / method quote figures from cited papers, which are legitimately
# literal (they are not our results and must not drift with our data).
OWN_RESULTS = {"00_abstract.tex", "04_results.tex", "05_discussion.tex", "07_conclusion.tex",
               "06_threats.tex"}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def strip_comments(s):
    return re.sub(r"(?<!\\)%.*", "", s)


def main():
    problems = []
    notes = []

    if not os.path.exists(NUMBERS):
        print("FAIL: paper/generated/numbers.tex missing -- run: python scripts/gen_paper_macros.py")
        return 1

    defined = set(re.findall(r"\\newcommand\{\\(\w+)\}", read(NUMBERS)))

    tex_files = [os.path.join(PAPER, "main.tex")] + sorted(
        glob.glob(os.path.join(PAPER, "sections", "*.tex")))

    used, cited, inputs, graphics = set(), set(), set(), set()
    for p in tex_files:
        body = strip_comments(read(p))
        for m in re.findall(r"\\([A-Za-z]+)", body):
            used.add(m)
        for m in re.findall(r"\\cite\{([^}]+)\}", body):
            cited.update(k.strip() for k in m.split(","))
        for m in re.findall(r"\\input\{([^}]+)\}", body):
            inputs.add(m)
        for m in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", body):
            graphics.add(m)

        # 6. hand-typed statistic detector -- only for sections reporting our own results.
        if os.path.basename(p) in OWN_RESULTS:
            for line in body.splitlines():
                if line.strip().startswith("%") or "\\newcommand" in line:
                    continue
                # Layout lengths (0.85\textwidth, \setlength{...}{1.2pt}) are not statistics.
                if "\\includegraphics" in line or "\\setlength" in line:
                    continue
                for lit in re.findall(r"(?<![\w.\\-])(\d+\.\d+)(?![\w.}-])", line):
                    if lit in {"0.90", "4.6"}:   # pre-registered threshold / model name
                        continue
                    problems.append(
                        f"{os.path.relpath(p, ROOT)}: hand-typed statistic '{lit}' in a "
                        f"results section -- must be a macro from numbers.tex")

    # 1. undefined macros
    unknown = {u for u in used if u not in defined and u not in KNOWN}
    for u in sorted(unknown):
        problems.append(f"UNDEFINED macro \\{u} -- not in numbers.tex and not a known LaTeX command")

    # 2. dead macros
    for d in sorted(defined - used):
        notes.append(f"unused macro \\{d} (defined but never printed)")

    # 3. inputs exist
    for i in sorted(inputs):
        cand = os.path.join(PAPER, i if i.endswith(".tex") else i + ".tex")
        if not os.path.exists(cand):
            problems.append(f"MISSING \\input target: {i}")

    # 4. graphics resolve
    searchdirs = [os.path.join(PAPER, "figures"), os.path.join(ROOT, "figures")]
    for g in sorted(graphics):
        if not any(os.path.exists(os.path.join(d, g)) for d in searchdirs):
            problems.append(f"MISSING figure: {g} (searched {', '.join(os.path.relpath(d, ROOT) for d in searchdirs)})")

    # 5. cite keys exist
    if os.path.exists(BIB):
        keys = set(re.findall(r"@\w+\{([^,]+),", read(BIB)))
        for c in sorted(cited):
            if c not in keys:
                problems.append(f"MISSING bib key: {c}")
        for k in sorted(keys - cited):
            notes.append(f"uncited bib entry: {k}")
    else:
        problems.append("references.bib missing")

    print(f"macros defined : {len(defined)}")
    print(f"macros used    : {len(defined & used)}")
    print(f"figures        : {len(graphics)}")
    print(f"cite keys      : {len(cited)}")
    print()
    for n in notes:
        print(f"  note: {n}")
    if notes:
        print()
    if problems:
        for p in problems:
            print(f"  PROBLEM: {p}")
        print(f"\nFAIL -- {len(problems)} problem(s)")
        return 1
    print("PASS -- no undefined macros, all inputs/figures/citations resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
