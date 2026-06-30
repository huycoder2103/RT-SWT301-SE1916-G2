#!/usr/bin/env bash
# Download the 13 included arXiv PDFs and extract page-numbered text for citation mining.
set -u
cd "$(dirname "$0")/papers" || exit 1

# map: <slug>=<arxiv_id>  (order matches evidence-table.md #1..#13)
declare -A P=(
  ["01_RESTGPT"]="2312.00894"
  ["02_KAT"]="2407.10227"
  ["03_RESTSpecIT"]="2402.05102"
  ["04_APITestGenie"]="2409.03838"
  ["05_RestTSLLM"]="2509.05540"
  ["06_AutoRestTest"]="2411.07098"
  ["07_LlamaRestTest"]="2501.08598"
  ["08_LogiAgent"]="2503.15079"
  ["09_RESTifAI"]="2512.08706"
  ["10_EvoMaster"]="1901.01538"
  ["11_NoTimeToRest"]="2204.08348"
  ["12_Morest"]="2204.12148"
  ["13_DeepREST"]="2408.08594"
)

for slug in "${!P[@]}"; do
  id="${P[$slug]}"
  pdf="${slug}_${id}.pdf"
  if [ ! -s "$pdf" ]; then
    echo ">> downloading $slug ($id)"
    curl -L -s -A "Mozilla/5.0" -o "$pdf" "https://arxiv.org/pdf/${id}"
    sleep 1
  fi
  # validate it is a real PDF
  if head -c 5 "$pdf" | grep -q "%PDF"; then
    sz=$(wc -c < "$pdf")
    echo "OK  $pdf  (${sz} bytes)"
  else
    echo "BAD $pdf  (not a PDF)"
  fi
done

echo "===== EXTRACTING TEXT (page-numbered) ====="
mkdir -p ../paper_text
for slug in "${!P[@]}"; do
  id="${P[$slug]}"
  pdf="${slug}_${id}.pdf"
  txt="../paper_text/${slug}.txt"
  if head -c 5 "$pdf" | grep -q "%PDF"; then
    pdftotext "$pdf" - 2>/dev/null | \
      awk 'BEGIN{RS="\f"; n=0} {n++; printf "\n===== PAGE %d =====\n%s", n, $0}' > "$txt"
    pages=$(grep -c "===== PAGE" "$txt")
    lines=$(wc -l < "$txt")
    echo "TXT $txt  ($pages pages, $lines lines)"
  fi
done
echo "DONE"
