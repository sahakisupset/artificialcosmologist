from cosmo_research.assumption_auditor import AssumptionAuditor


def test_auditor_finds_explicit_assumptions():
    text = "The expanding universe began in a Big Bang singularity. The cosmic rest frame is isotropic."
    findings = AssumptionAuditor().audit(text)
    names = {finding.assumption for finding in findings}
    assert "metric_expansion" in names
    assert "big_bang_origin" in names
    assert "preferred_frame" in names
    assert "isotropy" in names


def test_auditor_does_not_invent_finite_age():
    report = AssumptionAuditor().audit_report("A stationary observer studies photon propagation.")
    assert report["core_constraints_check"]["finite_age_not_assumed"]
    assert report["core_constraints_check"]["spatial_boundary_not_assumed"]
