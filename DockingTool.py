from pathlib import Path
import subprocess
import re
import csv

BASE_DIR = Path(__file__).resolve().parent
LIGANDS_DIR = Path(r"C:\path\to\your\ligands\folder")  # Change to your ligands directory
TARGET_FILE = Path(r"C:\path\to\your\protein.pdbqt")  # Change to your receptor protein file
OUT_DIR = BASE_DIR / "out"
LOG_DIR = BASE_DIR / "Log"
CSV_OUT = BASE_DIR / "vina_scores.csv"




VINA_EXE = r"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe"  # Standard Vina installation
VINA_SPLIT_EXE = r"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina_split.exe"  # Standard Vina installation
OBABEL_EXE = r"C:\Program Files (x86)\MGLTools-1.5.7\OpenBabel-2.3.2\obabel.exe"  # Standard MGLTools installation

OUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

Ligands = [item.name for item in LIGANDS_DIR.iterdir() if item.is_file()]

print("""molecular docking using AutoDock Vina

Ligands:""")

print(Ligands)

print("Receptors:")

if TARGET_FILE.is_file() and TARGET_FILE.suffix.lower() == ".pdbqt":
    print(TARGET_FILE.name)
try:
    with open(BASE_DIR / "grid_box.txt", "r") as sdf:
        lines = sdf.readlines()

    temp = lines[2].split()

    x_size = temp[1]
    y_size = temp[2]
    z_size = temp[3]

    temp = lines[3].split()

    x_value = temp[1]
    y_value = temp[2]
    z_value = temp[3]

    print("parameters in your grid_box.txt: x,y,z size search: ")
    print(x_size, y_size, z_size)
    print("Also your x,y,z values are:")
    print(x_value,y_value,z_value)


except:

    x_value = input("X coordinate of the center: ")
    y_value = input("Y coordinate of the center: ")
    z_value = input("Z coordinate of the center: ")
    x_size = input("Size in the X dimension: ")
    y_size = input("Size in the Y dimension: ")
    z_size = input("Size in the Z dimension: ")

if not TARGET_FILE.is_file() or TARGET_FILE.suffix.lower() != ".pdbqt":
    raise FileNotFoundError(f"Target receptor must be a .pdbqt file: {TARGET_FILE}")

for lig in Ligands:
    subprocess.run(
        [
            VINA_EXE,
            "--receptor",
            str(TARGET_FILE),
            "--ligand",
            str(LIGANDS_DIR / lig),
            "--center_x",
            str(x_value),
            "--center_y",
            str(y_value),
            "--center_z",
            str(z_value),
            "--size_x",
            str(x_size),
            "--size_y",
            str(y_size),
            "--size_z",
            str(z_size),
            "--out",
            str(OUT_DIR / f"vina_{lig}.pdbqt"),
            "--log",
            str(LOG_DIR / f"vina_{lig}.txt"),
        ],
        check=True,
    )



pattern = re.compile(r'^\s*\d+\s+(-?\d+\.\d+)', re.MULTILINE)

rows = []
for f in sorted(LOG_DIR.iterdir()):
    if f.is_file() and f.suffix == '.txt':
        text = f.read_text(errors='ignore')
        m = pattern.search(text)
        score = ''
        if m:
            score = m.group(1)
        ligand = f.name.replace('vina_','').replace('.txt','')
        rows.append((ligand, score))

with CSV_OUT.open('w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ligand', 'score'])
    writer.writerows(rows)

print(f"\n✓ Docking complete! Wrote {len(rows)} results to {CSV_OUT}")
print(f"  Output folder: {OUT_DIR}")
print(f"  Log folder: {LOG_DIR}")
