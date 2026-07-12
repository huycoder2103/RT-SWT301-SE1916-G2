const fs = require('fs');
const path = require('path');

const DATA = path.join(__dirname, "..", "data");
const SUTS = ["ncs", "scs", "features"];

function loadKeptMutants() {
    const rows = [];
    SUTS.forEach(sut => {
        const catPath = path.join(DATA, "faults", sut, "catalog.json");
        if (!fs.existsSync(catPath)) {
            console.error(`Catalog not found: ${catPath}`);
            return;
        }
        const cat = JSON.parse(fs.readFileSync(catPath, 'utf8'));
        cat.mutants.forEach(m => {
            if (m.status === "compiled") {
                rows.push({
                    sut: sut,
                    mutant_id: m.id,
                    file: m.file,
                    line: m.line,
                    operator: m.operator
                });
            }
        });
    });
    return rows;
}

function escapeCsv(val) {
    if (val === null || val === undefined) return '';
    const str = String(val);
    if (str.includes(',') || str.includes('"') || str.includes('\n') || str.includes('\r')) {
        return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
}

function writeCsv(destPath, rows, extraCol = null, extraVal = null) {
    let header = ["sut", "mutant_id", "file", "line", "operator"];
    if (extraCol) {
        header.push(extraCol);
    }
    
    let csvContent = header.map(escapeCsv).join(",") + "\r\n";
    rows.forEach(r => {
        let rowData = [r.sut, r.mutant_id, r.file, r.line, r.operator];
        if (extraCol) {
            rowData.push(extraVal);
        }
        csvContent += rowData.map(escapeCsv).join(",") + "\r\n";
    });
    
    fs.mkdirSync(path.dirname(destPath), { recursive: true });
    fs.writeFileSync(destPath, csvContent, 'utf8');
    console.log(`Wrote ${rows.length} rows to ${destPath}`);
}

function main() {
    const rows = loadKeptMutants();
    console.log(`Loaded ${rows.length} kept mutants.`);
    
    const perSut = {};
    rows.forEach(r => {
        perSut[r.sut] = (perSut[r.sut] || 0) + 1;
    });
    console.log("Kept mutants per SUT:", perSut);
    
    if (rows.length !== 133) {
        console.warn(`WARNING: Expected 133 kept mutants, got ${rows.length}`);
    }
    
    writeCsv(path.join(DATA, "full_ground_truth.csv"), rows);
    writeCsv(path.join(DATA, "pilot_ground_truth.csv"), rows);
    
    const note = "Week-7 pilot ran on the FULL compilable mutant catalog (N=133); no smaller sub-sample was drawn (see notes.md).";
    writeCsv(path.join(DATA, "pilot_sample.csv"), rows, "note", note);
}

main();
