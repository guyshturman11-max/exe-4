# Files and Graphs Exercise

**Course:** Programming for Mechatronics, Dr. Tal Alon
**Author:** Guy Shturman

## Contents

| Folder | Description |
|---|---|
| `q1` | **Grades Corrector**: loads a students CSV file into a table, adds bonus points (max 100), and saves the updated grades back to the file |
| `q2` | **Ice Cream Revenue Analyzer**: plots revenue vs. outside temperature as a scatter plot with a linear trend line (`np.polyfit`) |

## Requirements

- Python 3.12+
- PySide6, matplotlib, numpy

## How to run

From the project folder:

```bash
uv sync
uv run q1/main.py
uv run q2/main.py
```

## Built with

- **PySide6**: GUI (windows, table, buttons)
- **matplotlib**: graphs embedded in the window
- **numpy**: trend line calculation
- **QSS**: styling, in a separate `style.qss` file for each exercise