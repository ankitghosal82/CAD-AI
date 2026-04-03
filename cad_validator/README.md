# 🛠️ Varroc AI Design Copilot

An enterprise-grade, B2B AI Copilot that integrates directly into CAD software to catch Design for Manufacturability (DFM) errors in real-time. Powered by a Random Forest Classifier and Explainable AI (XAI).

## 🚀 The Business Problem
A single manufacturing mistake—like a part being too thin or a hole placed too close to an edge—can cost manufacturing companies tens of thousands of dollars in wasted metal, broken molds, and project delays. 

Currently, engineers rely on manual reviews or slow, post-design simulation software. 

## 💡 The Solution
We didn't build another CAD tool; we built an **invisible AI safety net**. 

The Varroc AI Design Copilot sits seamlessly inside the engineer's existing environment (FreeCAD). With a single click, it extracts 3D geometric features, passes them through a deterministic rule-engine, and feeds them into a trained Machine Learning model to predict manufacturing failure rates with **99% accuracy**.

### ✨ Key Features
* **Real-Time Validation:** Validates 3D models directly inside the FreeCAD environment.
* **Explainable AI (XAI):** Doesn't just say "Pass" or "Fail". It calculates feature importances to provide actionable insights (e.g., *"Critical risk factor identified in parameter: Sharp Edges"*).
* **Hybrid Architecture:** Combines hardcoded deterministic physics rules (DFM) with probabilistic Machine Learning.
* **Smart Scoring:** Generates a 0-100 Confidence Score for every part.

---

## 🧠 Technical Architecture

The backend is completely modular and independent of the CAD software, allowing it to scale as an API for any enterprise tool (SolidWorks, CATIA, etc.).

* `models.py`: Defines the strictly typed `DesignFeatures` blueprint.
* `dataset.py`: Parses enterprise datasets (Excel/CSV) into normalized Python objects using Pandas.
* `ai.py`: The Random Forest classification engine. Handles training, prediction, and XAI feature extraction.
* `rules.py`: The deterministic safety inspector for hardcoded engineering limits.
* `scoring.py` & `report.py`: Calculates final grades and generates human-readable console reports.
* `cli.py`: The command-line orchestrator for headless training and testing.

---

## ⚙️ Installation & Setup

### 1. Install Dependencies
Ensure you have Python 3.10+ installed. Install the required enterprise data science libraries:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Train the AI "Brain"
Before running the live integration, you must train the Random Forest model on the historical manufacturing dataset (`data.xlsx` - 3,000 samples).
\`\`\`bash
python -m cad_validator.cli --train cad_validator/data.xlsx
\`\`\`
*This will output the Precision/Recall/F1 accuracy matrix and generate the `ai_model.pkl` brain file.*

### 3. Test the Engine (Headless Mode)
Verify the AI is working by simulating a live FreeCAD payload:
\`\`\`bash
python -m cad_validator.cli --test
\`\`\`

---

## 🖥️ FreeCAD Live Integration

To see the magic happen live inside CAD:

1. Open **FreeCAD** (v0.21+ recommended).
2. Install the required Python libraries directly into FreeCAD's internal Python environment:
   * Open the FreeCAD Python Console (`View > Panels > Python console`).
   * Run: 
     \`\`\`python
     import subprocess, sys, os
     subprocess.run([os.path.join(os.path.dirname(sys.executable), "python.exe"), "-m", "pip", "install", "joblib", "scikit-learn", "pandas", "openpyxl"])
     \`\`\`
   * Restart FreeCAD.
3. Open a `Part` workbench and generate a 3D geometry (e.g., a Box/Cube).
4. Go to `Macro > Macros... > Create`, name it `Varroc_AI`, and paste the contents of `freecad_ai_copilot.py` (ensure the `PROJECT_PATH` variable points to this repository).
5. Click **Execute**. A popup will instantly deliver the AI validation report.

---

## 📈 Future Roadmap
* **Auto-Correction:** Expanding the FreeCAD macro to automatically apply chamfers or fillets to flagged sharp edges.
* **Cloud API Engine:** Migrating the local `.pkl` model to a FastAPI backend for centralized enterprise deployments.
* **Expanded CAD Support:** Developing native plugins for Autodesk Inventor and SolidWorks.
