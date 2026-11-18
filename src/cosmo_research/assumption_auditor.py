import re
from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass(frozen=True)
class AssumptionFinding:
    assumption: str
    category: str
    evidence: str
    severity: str
    recommendation: str


class AssumptionAuditor:
    """Surfaces common hidden cosmological assumptions without declaring them false."""

    RULES: ClassVar[dict[str, tuple[str, str, str, str]]] = {
        "finite_universe_age": (r"\b(universe|cosmos)\b.{0,35}\b(beginning|born|age of the universe|13\.8 billion|finite age)\b", "age", "High", "Make model age explicit or eliminate a finite-age boundary condition."),
        "spatial_boundary": (r"\b(edge|boundary|outside the universe|spatial limit|finite (?:spatial )?(?:size|volume))\b", "boundary", "Medium", "Specify topology and whether boundaries are physical or observational."),
        "metric_expansion": (r"\b(expanding universe|cosmic expansion|metric expansion|scale factor|Hubble expansion)\b", "expansion", "High", "State the metric-expansion axiom explicitly and provide a non-expansion alternative."),
        "homogeneity": (r"\b(homogeneous|homogeneity|cosmological principle)\b", "geometry", "Medium", "Test homogeneity assumptions against scale and observational selection."),
        "isotropy": (r"\b(isotropic|isotropy)\b", "geometry", "Medium", "State whether isotropy is spatial, temporal, or observer-dependent."),
        "preferred_frame": (r"\b(preferred frame|cosmic rest frame|ether|aether|absolute frame)\b", "symmetry", "High", "Identify the frame, its observational signature, and Lorentz covariance."),
        "big_bang_origin": (r"\b(big bang|initial singularity|singularity)\b", "origin", "High", "Avoid equating the hot dense phase with an origin unless separately derived."),
    }

    def audit(self, text: str) -> list[AssumptionFinding]:
        findings: list[AssumptionFinding] = []
        for assumption, (pattern, category, severity, recommendation) in self.RULES.items():
            match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
            if match:
                start = max(0, match.start() - 45)
                end = min(len(text), match.end() + 45)
                evidence = " ".join(text[start:end].split())
                findings.append(AssumptionFinding(assumption, category, evidence, severity, recommendation))
        return findings

    def audit_report(self, text: str) -> dict:
        findings = self.audit(text)
        return {
            "finding_count": len(findings),
            "assumptions": [asdict(finding) for finding in findings],
            "core_constraints_check": {
                "finite_age_not_assumed": not any(f.assumption == "finite_universe_age" for f in findings),
                "spatial_boundary_not_assumed": not any(f.assumption == "spatial_boundary" for f in findings),
                "metric_expansion_explicit": any(f.assumption == "metric_expansion" for f in findings),
            },
        }
