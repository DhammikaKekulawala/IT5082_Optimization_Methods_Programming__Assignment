# IT5082 Optimization Methods — Programming Assignment

**Nurse / Staff Rostering:** an exact method (Integer Linear Programming, Branch & Bound) benchmarked against a
metaheuristic (Genetic Algorithm) on real benchmark instances, comparing solution quality, runtime, scalability and
feasibility.

**Module:** IT5082 – Optimization Methods · MSc in Artificial Intelligence, SLIIT
**Assessment:** Group Programming Assignment (2 members) · 40 marks

## Team

| # | Name | Student ID |
|---|------|------------|
| 1 | Ramalingham Seyon | MS26912516 |
| 2 | Kekulawala Vidanalage Dhammika Kekulawala | MS26902784 |

See [Members.md](Members.md) for the full group information.

## Problem

A hospital ward has a set of nurses and a planning period of 2 to 52 weeks. Each day has one or more shift types with a
required number of nurses. We assign nurses to shifts so that every hard labour rule holds (one shift per day, forbidden
shift sequences, working-time limits, consecutive-work and rest limits, weekend limits, fixed days off) while minimising
the weighted penalty of unmet staffing cover and unmet nurse shift requests. The problem is NP-hard.

## Methods

1. **Exact:** binary ILP solved by Branch & Bound (PuLP with the bundled CBC solver).
2. **Metaheuristic:** Genetic Algorithm (DEAP) with a full roster as the chromosome.

Both minimise the same penalty function, defined by the benchmark, so results are directly comparable.

## Dataset

Nurse Rostering Benchmark Instances 1-24 (Tim Curtois, University of Nottingham),
<https://www.schedulingbenchmarks.org/nrp/>. Real instances from 8 to 150 nurses and 2 to 52 weeks, each with a
best-known lower bound and solution. See [data/README.md](data/README.md).

## Setup

All code in this project runs in the conda environment **`seyon`** (Python 3.10).

```
conda activate seyon
pip install pulp deap            # only the packages this project needs
python src/download_instances.py # fills data/raw/ with the 24 instances
```

`ortools` (CP-SAT) is an optional second exact solver; it is not installed by default because it pins `protobuf`.

## Repository layout

```
data/        benchmark description, best-known table (best_known.csv); raw instances are downloaded, not committed
src/         instance parser, exact ILP, genetic algorithm, experiment runner
notebooks/   experiments and analysis
results/     benchmark outputs and plots
report/      technical PDF report sources
```

## Workflow

- `main` is the shared branch. Seyon works on branch **`seyon`**; changes reach `main` through the shared repository.
- Small, meaningful commits from both members (for example "add instance parser", "add ILP model", "add GA").

## Status

- [x] Topic chosen, plan written (`Rostering_Project_Plan.docx`)
- [x] Repository scaffold, environment, data download script
- [ ] Instance parser
- [ ] ILP model, verified against best-known solutions
- [ ] Genetic Algorithm
- [ ] Experiments, graphs, comparison
- [ ] Report, code appendix, video, submission zip

## Deliverables

- Public GitHub repo with incremental commit history from both members
- 15-minute YouTube demonstration video
- Technical PDF report (IEEE / academic structure)
- Plain-text code appendix
- `Optimization-assignment.zip` bundling `members.txt`, `submission.txt`, report, and code appendix
