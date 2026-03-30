# AI-Assisted CAD Design Validation Prototype

This project is a practical final-year prototype for validating simple CAD designs using:

- rule-based engineering checks
- anomaly detection with machine learning
- a CLI-generated compliance report

The prototype is designed to work in two stages:

1. `now`: run with sample extracted CAD features from JSON
2. `next`: connect FreeCAD Python extraction to generate those features from real `.STEP` or `.STL` models

## Project Structure

```text
cad_validator/
  ai.py
  cli.py
  models.py
  report.py
  rules.py
  sample_data.py
  scoring.py
data/
  sample_designs.json
requirements.txt
```

## Features Used

Each design is represented by a compact feature set:

- `length_mm`
- `width_mm`
- `height_mm`
- `thickness_mm`
- `hole_diameter_mm`
- `hole_edge_distance_mm`
- `sharp_edge_count`
- `fillet_radius_mm`

## Engineering Rules

The prototype checks:

- minimum thickness
- hole edge distance
- sharp edges without fillet

## AI Model

The ML component uses `IsolationForest` to flag abnormal designs based on historical "good" samples.

## Quick Start

1. Create and activate a virtual environment
2. Install dependencies
3. Run the validator

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m cad_validator.cli --input data/sample_designs.json
```

## Example Output

```text
Design: thin_plate_bad
Status: NEEDS REVIEW
Design Score: 35/100

Issues:
- WARNING: Thickness too low. Increase thickness to at least 2.0 mm.
- ERROR: Hole too close to edge. Keep edge distance at least 1.5x hole diameter.
- WARNING: Sharp edges detected. Add fillet or chamfer where possible.
- AI FLAG: Design pattern is unusual compared with training samples.
```

## Connecting FreeCAD Later

You can replace the sample JSON input with a FreeCAD extractor that writes the same feature schema.

Example direction:

```python
import FreeCAD
import Part

doc = FreeCAD.open("model.step")
shape = doc.Objects[0].Shape

# Extract geometry and convert it into the JSON schema
```

Once extracted, save the features as JSON and run the CLI validator on that file.

## Suggested Demo Flow

1. Show a normal design passing validation
2. Show a weak design failing rule checks
3. Show the AI anomaly flag
4. Explain how FreeCAD feeds the same pipeline from a real CAD file
