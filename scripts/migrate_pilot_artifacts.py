import os
import shutil
import glob

def migrate():
    src = os.path.join("Nguyen-Tien-Dung-SE190034", "experiment")
    if not os.path.exists(src):
        print(f"ERROR: source dir not found: {src}")
        return

    print("=== Migrating pilot artifacts to root structure (Python) ===")

    # 1. Scripts
    os.makedirs("scripts", exist_ok=True)
    # Copy all python files
    for py_file in glob.glob(os.path.join(src, "scripts", "*.py")):
        dest = os.path.join("scripts", os.path.basename(py_file))
        shutil.copy2(py_file, dest)
        print(f"Copied {py_file} -> {dest}")
        
    # Copy all sh files
    for sh_file in glob.glob(os.path.join(src, "scripts", "*.sh")):
        dest = os.path.join("scripts", os.path.basename(sh_file))
        shutil.copy2(sh_file, dest)
        print(f"Copied {sh_file} -> {dest}")

    # Copy files with RBL-0 standard names
    analyze_src = os.path.join(src, "scripts", "analyze.py")
    if os.path.exists(analyze_src):
        shutil.copy2(analyze_src, os.path.join("scripts", "compute_metric.py"))
        print(f"Copied {analyze_src} -> scripts/compute_metric.py")

    run_mut_src = os.path.join(src, "scripts", "run_mutation.py")
    if os.path.exists(run_mut_src):
        shutil.copy2(run_mut_src, os.path.join("scripts", "run_experiment.py"))
        print(f"Copied {run_mut_src} -> scripts/run_experiment.py")

    # 2. Results
    os.makedirs(os.path.join("results", "raw"), exist_ok=True)
    for root_dir, dirs, files in os.walk(os.path.join(src, "results")):
        # Calculate relative path to results folder
        rel_path = os.path.relpath(root_dir, os.path.join(src, "results"))
        dest_dir = os.path.join("results", rel_path)
        os.makedirs(dest_dir, exist_ok=True)
        for f in files:
            src_file = os.path.join(root_dir, f)
            dest_file = os.path.join(dest_dir, f)
            shutil.copy2(src_file, dest_file)
            print(f"Copied {src_file} -> {dest_file}")

    # 3. Data - faults catalogs
    for sut in ["ncs", "scs", "features"]:
        src_cat = os.path.join(src, "faults", sut, "catalog.json")
        if os.path.exists(src_cat):
            dest_dir = os.path.join("data", "faults", sut)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(src_cat, os.path.join(dest_dir, "catalog.json"))
            print(f"Copied {src_cat} -> {os.path.join(dest_dir, 'catalog.json')}")

    # 4. Figures
    os.makedirs("figures", exist_ok=True)
    for fig_file in glob.glob(os.path.join(src, "results", "figures", "*.png")):
        dest = os.path.join("figures", os.path.basename(fig_file))
        shutil.copy2(fig_file, dest)
        print(f"Copied {fig_file} -> {dest}")

    # 5. LLM prompt template
    os.makedirs(os.path.join("scripts", "llm"), exist_ok=True)
    prompt_src = os.path.join(src, "llm", "prompt_template.md")
    if os.path.exists(prompt_src):
        shutil.copy2(prompt_src, os.path.join("scripts", "llm", "prompt_template.md"))
        print(f"Copied {prompt_src} -> scripts/llm/prompt_template.md")

    print("=== Migration Done ===")

if __name__ == "__main__":
    migrate()
