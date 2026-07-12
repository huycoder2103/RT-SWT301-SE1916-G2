const fs = require('fs');
const path = require('path');

function copyFile(src, dest) {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
    console.log(`Copied ${src} -> ${dest}`);
}

function copyFolderSync(from, to) {
    if (!fs.existsSync(from)) return;
    fs.mkdirSync(to, { recursive: true });
    fs.readdirSync(from).forEach(element => {
        const stat = fs.lstatSync(path.join(from, element));
        if (stat.isFile()) {
            copyFile(path.join(from, element), path.join(to, element));
        } else if (stat.isDirectory()) {
            copyFolderSync(path.join(from, element), path.join(to, element));
        }
    });
}

function migrate() {
    const src = path.join("Nguyen-Tien-Dung-SE190034", "experiment");
    if (!fs.existsSync(src)) {
        console.error(`ERROR: source dir not found: ${src}`);
        process.exit(1);
    }

    console.log("=== Migrating pilot artifacts to root structure (Node.js) ===");

    // 1. Scripts
    fs.mkdirSync("scripts", { recursive: true });
    
    // Copy all .py and .sh files from src/scripts
    const scriptsSrc = path.join(src, "scripts");
    if (fs.existsSync(scriptsSrc)) {
        fs.readdirSync(scriptsSrc).forEach(file => {
            if (file.endsWith('.py') || file.endsWith('.sh')) {
                copyFile(path.join(scriptsSrc, file), path.join("scripts", file));
            }
        });
    }

    // Copy and rename analyze.py -> compute_metric.py
    const analyzeSrc = path.join(src, "scripts", "analyze.py");
    if (fs.existsSync(analyzeSrc)) {
        copyFile(analyzeSrc, path.join("scripts", "compute_metric.py"));
    }

    // Copy and rename run_mutation.py -> run_experiment.py
    const runMutationSrc = path.join(src, "scripts", "run_mutation.py");
    if (fs.existsSync(runMutationSrc)) {
        copyFile(runMutationSrc, path.join("scripts", "run_experiment.py"));
    }

    // 2. Results
    copyFolderSync(path.join(src, "results"), "results");

    // 3. Data - faults catalogs
    const faultSuts = ["ncs", "scs", "features"];
    faultSuts.forEach(sut => {
        const srcCat = path.join(src, "faults", sut, "catalog.json");
        if (fs.existsSync(srcCat)) {
            copyFile(srcCat, path.join("data", "faults", sut, "catalog.json"));
        }
    });

    // 4. Figures
    fs.mkdirSync("figures", { recursive: true });
    const figuresSrc = path.join(src, "results", "figures");
    if (fs.existsSync(figuresSrc)) {
        fs.readdirSync(figuresSrc).forEach(file => {
            if (file.endsWith('.png')) {
                copyFile(path.join(figuresSrc, file), path.join("figures", file));
            }
        });
    }

    // 5. LLM prompt template
    const promptSrc = path.join(src, "llm", "prompt_template.md");
    if (fs.existsSync(promptSrc)) {
        copyFile(promptSrc, path.join("scripts", "llm", "prompt_template.md"));
    }

    console.log("=== Migration Done ===");
}

migrate();
