# Batch-Molecular-Docking-and-Score-Extraction-Pipeline-Using-Autodock-Vina
Automated molecular docking pipeline built with AutoDock Vina. It docks a batch of ligand PDBQT files against a target receptor, saves docking outputs and logs, and extracts binding affinities into a CSV file for easy analysis.

## Overview

This Python script automates **molecular docking** using **AutoDock Vina**. It docks multiple ligand molecules against a target protein receptor and extracts binding affinity scores to a CSV file for easy analysis.

### What It Does

1. **Loads ligands** from a folder (PDBQT format)
2. **Docks each ligand** against a protein receptor using AutoDock Vina
3. **Generates output files** with docking results and logs
4. **Extracts scores** from Vina log files and saves them to `vina_scores.csv`

---

## Requirements

### Software
- **Python 3.7+** (Windows)
- **AutoDock Vina** installed at: `C:\Program Files (x86)\The Scripps Research Institute\Vina\`
- **Vina Split tool** (included with AutoDock Vina)

### File Formats
- **Ligands**: PDBQT format files
- **Receptor (target protein)**: Single PDBQT file

### Paths (Customizable)
Edit these lines in the script to match your file locations:

```python
LIGANDS_DIR = Path(r"C:\path\to\your\ligands\folder")  # Your ligands directory
TARGET_FILE = Path(r"C:\path\to\your\protein.pdbqt")  # Your receptor protein file
```

---

## Setup

### 1. Install Python
Download from [python.org](https://www.python.org/) and install Python 3.8+.

### 2. Install AutoDock Vina
- Download from [Scripps Research](http://vina.scripps.edu/)
- Extract to: `C:\Program Files (x86)\The Scripps Research Institute\Vina\`
- Verify `vina.exe` and `vina_split.exe` are in this folder

### 3. Prepare Your Data

Create the following folder structure:

```
C:\path\to\your\project\
│
├── docking (1).py          (this script)
├── grid_box.txt            (configuration file)
├── vina_scores.csv         (output - generated)
│
└── input data:
    ├── out/                (created automatically - docking output)
    └── Log/                (created automatically - log files)
```

### 4. Configure Grid Box

Create a `grid_box.txt` file in the same folder as the script. This defines the docking search box:

```
dummy line
dummy line
size_x 20 20 20
center_x 0 0 0
```

**Explanation:**
- `size_x, size_y, size_z`: Width, height, depth of search box (in Ångströms)
- `center_x, center_y, center_z`: Center coordinates of the box (x, y, z)

**Example for a larger search area:**
```
dummy line
dummy line
size_x 30 30 30
center_x 10 5 -2
```

**To find the correct center coordinates:**
- Open your protein in a molecular viewer (PyMOL, Chimera)
- Identify the binding site
- Get the center coordinates of your target binding pocket

---

## Running the Script

### Option 1: Command Line

Open PowerShell or Command Prompt and run:

```powershell
cd C:\path\to\your\project
python "docking (1).py"
```

### Option 2: Double-Click
Right-click the script → "Open with Python"

### Option 3: From Python IDE
- Open in VS Code, PyCharm, or Spyder
- Click "Run"

---

## Output Files

After running, the script generates:

### 1. **vina_scores.csv** (Main Results)
CSV file with docking scores:

```
ligand,score
cpds-mini1.pdbqt,-4.3
cpds-mini2.pdbqt,-1.8
cpds-mini3.pdbqt,-5.8
...
```

**Interpretation:**
- **Ligand**: Name of the docked compound
- **Score**: Binding affinity (kcal/mol)
  - **Negative = Better binding** (more stable complex)
  - Example: -5.0 is better than -3.0

### 2. **out/ folder**
Contains Vina docking output files:
- `vina_cpds-mini1.pdbqt.pdbqt` — Full docking result
- `vina_cpds-mini1.pdbqt_ligand_1.pdbqt` — Lowest energy pose

### 3. **Log/ folder**
Contains detailed logs for each docking run:
- `vina_cpds-mini1.pdbqt.txt` — Vina output log

Example log snippet:
```
mode |   affinity | dist from best mode
     | (kcal/mol) | rmsd l.b.| rmsd u.b.
-----+------------+----------+----------
   1         -4.3      0.000      0.000
   2         -3.9      3.184      8.185
```

---

## Script Workflow

```
START
  ↓
Load ligands from folder
  ↓
Load receptor PDBQT file
  ↓
Read grid_box.txt (docking box parameters)
  ↓
FOR EACH LIGAND:
  ├─ Run AutoDock Vina docking
  ├─ Save output to out/ folder
  └─ Save log to Log/ folder
  ↓
Parse ALL log files
  ↓
Extract best binding score from each log
  ↓
Write results to vina_scores.csv
  ↓
END - Success!
```

---

## Analyzing Results

### Using Excel or Pandas

**Open CSV in Excel:**
1. Open `vina_scores.csv` with Excel
2. Sort by "score" column (ascending = best binders first)

**Using Python (Pandas):**
```python
import pandas as pd

df = pd.read_csv('vina_scores.csv')
df_sorted = df.sort_values('score')
print(df_sorted)
```

### Interpreting Scores

| Score | Interpretation |
|-------|-----------------|
| < -8.0 | Very strong binder |
| -6 to -8 | Strong binder |
| -4 to -6 | Moderate binder |
| -2 to -4 | Weak binder |
| > -2 | Very weak / No binding |

---

## Troubleshooting

### Error: "FileNotFoundError: grid_box.txt"
**Solution:** Create `grid_box.txt` in the script folder with proper format (see Setup section).

### Error: "Target receptor must be a .pdbqt file"
**Solution:** 
- Check `TARGET_FILE` path in script
- Ensure protein file ends in `.pdbqt`
- Verify the file exists at that path

### Error: "Cannot find Vina executable"
**Solution:**
- Verify AutoDock Vina is installed at: `C:\Program Files (x86)\The Scripps Research Institute\Vina\`
- Check that `vina.exe` and `vina_split.exe` exist in that folder
- Update the paths in the script if installed elsewhere:
  ```python
  VINA_EXE = r"C:\your\custom\path\vina.exe"
  ```

### Script runs but CSV is empty
**Solution:**
- Check that log files were created in `Log/` folder
- Verify ligand files are in PDBQT format
- Ensure docking actually completed (check console output)

### Slow performance
**Note:** Docking is computationally intensive. With 49 ligands, expect:
- ~5-10 minutes on modern hardware (12 CPUs)
- Longer on older systems

---

## Customization

### Change Docking Parameters

Edit these lines to modify paths:

```python
# Ligand folder - change to your ligands directory
LIGANDS_DIR = Path(r"C:\Users\YourUsername\Documents\Ligands")

# Receptor protein - change to your receptor file
TARGET_FILE = Path(r"C:\Users\YourUsername\Documents\Receptor\protein.pdbqt")

# Output locations
OUT_DIR = BASE_DIR / "out"      # Docking output
LOG_DIR = BASE_DIR / "Log"      # Log files
CSV_OUT = BASE_DIR / "vina_scores.csv"  # Results
```

### Modify Grid Box Size

Edit `grid_box.txt`:
```
dummy line
dummy line
size_x 25 25 25        # Larger search box (was 20)
center_x 0 0 0         # Center coordinates
```

---

## File Structure

```
C:\path\to\your\project\
│
├── docking (1).py              ← Main script
├── README.md                   ← This file
├── grid_box.txt                ← Docking parameters
├── vina_scores.csv             ← Results (generated)
│
├── out/                        ← Docking outputs (generated)
│   ├── vina_compound1.pdbqt.pdbqt
│   ├── vina_compound1.pdbqt_ligand_1.pdbqt
│   └── ... (one set per ligand)
│
└── Log/                        ← Log files (generated)
    ├── vina_compound1.pdbqt.txt
    ├── vina_compound2.pdbqt.txt
    └── ... (one log per ligand)
```

---

## Script Code Breakdown

### 1. **Imports & Setup**
```python
from pathlib import Path
import subprocess, re, csv

BASE_DIR = Path(__file__).resolve().parent  # Script folder
LIGANDS_DIR = Path(...)                     # Ligand folder
TARGET_FILE = Path(...)                     # Receptor protein
```

### 2. **Load Configuration**
Reads `grid_box.txt` to get docking box size and center coordinates.

### 3. **Run Docking**
Loops through each ligand and calls AutoDock Vina:
```python
subprocess.run([VINA_EXE, "--receptor", ..., "--ligand", ...])
```

### 4. **Extract Scores**
Parses log files with regex to find binding affinity:
```python
pattern = re.compile(r'^\s*\d+\s+(-?\d+\.\d+)', re.MULTILINE)
```

### 5. **Write CSV**
Saves results:
```python
writer.writerow(['ligand', 'score'])
writer.writerows(rows)
```

---

## References

- **AutoDock Vina**: http://vina.scripps.edu/
- **PDBQT Format**: https://autodock-vina.readthedocs.io/en/latest/
- **Molecular Docking**: https://en.wikipedia.org/wiki/Docking_(molecular)

---

## Support

If you encounter issues:
1. Check that all paths are correct
2. Verify AutoDock Vina is installed
3. Ensure ligand/receptor files are in PDBQT format
4. Check file permissions (read/write access)
5. Look at log files in `Log/` folder for Vina errors

---

**Created:** May 2026  
**Script:** Automated Molecular Docking Pipeline  
**Tool:** AutoDock Vina

