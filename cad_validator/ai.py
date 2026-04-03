import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from cad_validator.models import DesignFeatures
class DesignQualityPredictor:
    def __init__(self, random_state: int = 42) -> None:
        self.model=RandomForestClassifier(n_estimators=100,random_state=random_state,class_weight="balanced")
        self._is_trained=False
        self.feature_names=DesignFeatures.get_feature_names()
    def train(self, designs: list[DesignFeatures]) -> None:
        X = np.array([d.to_feature_vector() for d in designs])
        y = np.array([1 if d.expected_quality == "good" else 0 for d in designs])
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)
        print("\nTraining Random Forest AI Model")
        self.model.fit(X_train, y_train)
        self._is_trained = True
        predictions = self.model.predict(X_test)
        print("\n--- AI Accuracy Report ---")
        print(classification_report(y_test, predictions, target_names=["Bad", "Good"]))
    def predict_with_insights(self, design: DesignFeatures) -> dict:
        if not self._is_trained:
            raise RuntimeError("Model is not trained. Load or train it first.")
        vector=np.array([design.to_feature_vector()])
        probabilities=self.model.predict_proba(vector)[0]
        is_good=probabilities[1] > 0.5 
        confidence=probabilities[1] if is_good else probabilities[0]
        insights=[]
        if not is_good:
            importances=self.model.feature_importances_
            top_indices=np.argsort(importances)[-2:][::-1]
            for idx in top_indices:
                feat_name=self.feature_names[idx]
                feat_val=vector[0][idx]
                insights.append(f"Critical risk factor identified in parameter: {feat_name} ({feat_val}).")
        return {
            "status": "PASS" if is_good else "FAIL",
            "confidence": round(confidence * 100, 2),
            "insights": insights
        }
    def save_model(self, filepath:str="cad_validator/ai_model.pkl") -> None:
        joblib.dump(self.model,filepath)
        print(f"Model saved to {filepath}")
    def load_model(self,filepath:str="cad_validator/ai_model.pkl")->None:
        if Path(filepath).exists():
            self.model=joblib.load(filepath)
            self._is_trained=True
        else:
            raise FileNotFoundError(f"Model file {filepath} not found.Please train first.")
