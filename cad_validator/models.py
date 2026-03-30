from dataclasses import dataclass


@dataclass
class DesignFeatures:
    name: str
    length_mm: float
    width_mm: float
    height_mm: float
    thickness_mm: float
    hole_diameter_mm: float
    hole_edge_distance_mm: float
    sharp_edge_count: int
    fillet_radius_mm: float
    expected_quality: str | None = None

    def to_feature_vector(self) -> list[float]:
        return [
            self.length_mm,
            self.width_mm,
            self.height_mm,
            self.thickness_mm,
            self.hole_diameter_mm,
            self.hole_edge_distance_mm,
            float(self.sharp_edge_count),
            self.fillet_radius_mm,
        ]

    @classmethod
    def from_dict(cls, data: dict) -> "DesignFeatures":
        return cls(
            name=data["name"],
            length_mm=float(data["length_mm"]),
            width_mm=float(data["width_mm"]),
            height_mm=float(data["height_mm"]),
            thickness_mm=float(data["thickness_mm"]),
            hole_diameter_mm=float(data["hole_diameter_mm"]),
            hole_edge_distance_mm=float(data["hole_edge_distance_mm"]),
            sharp_edge_count=int(data["sharp_edge_count"]),
            fillet_radius_mm=float(data["fillet_radius_mm"]),
            expected_quality=data.get("expected_quality"),
        )
