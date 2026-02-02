# Copilot instructions for this repository

Purpose: Help an AI coding agent be immediately productive editing and extending the force-density example scripts.

- **Big picture**: small collection of single-file Python scripts that implement the force-density method and plotting. Primary scripts are [force-density.py](force-density.py) (hard-coded example) and [force-density-with-files.py](force-density-with-files.py) (CSV-driven, interactive). `main.py` is a light entry point; reusable plotting helpers live in [matplotlib_lines.py](matplotlib_lines.py).

- **Data flow / inputs**:
  - Connectivity and geometry come from CSVs in the repo root: `C.csv`, `Cf.csv`, `Q.csv`, and optional coordinate/force files `xf.csv`, `yf.csv`, `zf.csv`, `fx.csv`, `fy.csv`, `fz.csv`.
  - `force-density-with-files.py` loads `C.csv` and `Cf.csv` with `np.loadtxt` and expects `Q.csv` to be a 1D vector (it's turned into `np.diag(...)`). If `Q.csv` is missing the script falls back to `-I` (negative identity).
  - Shape conventions visible in code: `C.shape[1]` == number of fixed/known nodes; `Cf.shape[1]` == number of unknown nodes; `C.shape[0]` == number of bars.

- **How to run (dev workflow)**:
  - Ensure Python 3.8+ and required packages: `pip install numpy matplotlib`
  - Run the example with the hard-coded case: `python force-density.py`
  - Run the CSV-driven version (prompts for which coordinates/forces to compute): `python force-density-with-files.py` (run from repository root so relative CSV paths resolve)
  - `main.py` is a placeholder; use it to integrate components when building a larger entry point.

- **Important code patterns / gotchas**:
  - Matrix assembly: scripts use NumPy linear algebra: D = C.T @ Q @ C and Df = C.T @ Q @ Cf; solutions use `np.linalg.solve(D, rhs)` — ensure `D` is invertible before calling `solve`.
  - `Q.csv` is expected to be a vector (loaded then placed on the diagonal). If you want to provide a full matrix, adapt the loader accordingly.
  - `force-density-with-files.py` is interactive: the top-level booleans `compute_x/compute_y/compute_z` are obtained via `input(...)`. For non-interactive automation, change these to constants or add CLI args.
  - Files are loaded with `np.loadtxt` and many fallbacks print and use zeros; missing or mis-sized CSVs can lead to shape mismatches — inspect printed shapes (scripts already print matrices) to debug.

- **Where to change behavior**:
  - CSV handling and defaults: edit the `load_coordinate` / `load_force` helpers in [force-density-with-files.py](force-density-with-files.py).
  - Plotting: 3D plotting is implemented inline (scatter + lines). For 2D line plotting reuse [matplotlib_lines.py](matplotlib_lines.py) `plot_arbitrary_lines(lines_data)`.

- **Extension guidance for AI edits**:
  - Prefer small, local edits: add CLI parsing (argparse) to `force-density-with-files.py` rather than rewriting flow.
  - If adding tests or automation, implement a lightweight runner that imports functions (refactor computations into functions first) rather than executing scripts at import time.
  - Keep CSV filenames and shape conventions consistent with existing code; show examples when modifying loaders.

- **Quick examples to include in PRs**:
  - Add an `--auto` flag to skip prompts and accept `--compute x,y,z` list.
  - Add a loader that accepts both a Q vector and a full Q matrix (detect shape and handle both cases).

If any part of the repo's intent is unclear (desired CLI, input file formats, or a canonical example), tell me what you expect and I will update this guidance accordingly.
