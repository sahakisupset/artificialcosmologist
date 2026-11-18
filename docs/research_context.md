# Cosmology Research Agent - Research Context

## Objective
Investigate alternative explanations for cosmological redshift.

## Core Constraints
- Do not assume a Big Bang origin.
- Do not assume a finite age of the universe.
- Do not assume spatial boundaries.
- Do not assume metric expansion as an axiom.
- Treat Lambda-CDM as one competing explanatory model.
- Prefer falsifiable mathematical models.

## Research Questions
1. Can observed redshift arise from photon propagation effects?
2. Can vacuum structure induce frequency evolution?
3. Are there observer-dependent geometric explanations?
4. What observational constraints eliminate candidate theories?

## Agent Architecture
Observation Database
 -> Literature Retrieval (NASA ADS, arXiv)
 -> Theory Generator
 -> Assumption Auditor
 -> Adversarial Critic
 -> Symbolic Derivation Engine
 -> Observable Generator
 -> Data Fitting Pipeline
 -> Theory Evolution Engine

## External Sources
- NASA ADS
- arXiv
- Planck
- DESI
- Pantheon+
- SDSS
- Euclid
- Rubin LSST

## Technology Stack
- Python
- DeepSeek-R1
- SymPy
- SciPy
- ChromaDB or Qdrant
- Pandas
- NumPy

## Key Design Principle
All hidden assumptions regarding beginnings, endings, boundaries, homogeneity, isotropy, expansion, and preferred frames should be surfaced and evaluated rather than silently accepted.
