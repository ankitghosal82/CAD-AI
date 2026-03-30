import numpy as np
from sklearn.ensemble import IsolationForest

from cad_validator.models import DesignFeatures


class DesignAnomalyDetector:
    def __init__(self, random_state: int = 42) -> None:
        self.model = IsolationForest(
            n_estimators=200,
            contamination=0.25,
            random_state=random_state,
        )
        self._is_trained = False

    def fit(self, designs: list[DesignFeatures]) -> None:
        good_designs = [
            design for design in designs if design.expected_quality in (None, "good")
        ]
        if not good_designs:
            raise ValueError("At least one normal design is required for training.")

        feature_matrix = np.array([design.to_feature_vector() for design in good_designs])
        self.model.fit(feature_matrix)
        self._is_trained = True

    def predict(self, design: DesignFeatures) -> int:
        if not self._is_trained:
            raise RuntimeError("Model must be trained before prediction.")

        vector = np.array([design.to_feature_vector()])
        return int(self.model.predict(vector)[0])
