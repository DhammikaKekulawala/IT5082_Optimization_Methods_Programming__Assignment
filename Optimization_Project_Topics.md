# Optimization Methods (IT5082) — Programming Assignment
## Project Topic Options — Full Analysis (4 Projects)

**Group Assignment · 40 Marks · MSc Artificial Intelligence, Semester 02**

This document analyses **four** strong project options for the assignment. Each one:

- picks a **realistic, non-trivial** problem,
- uses **one Exact method** + **one Heuristic/Metaheuristic** (as required),
- uses **real datasets** (or justified synthetic data),
- maps directly to the lectures, so the **viva** goes well.

> **Key idea for top marks:** The rubric rewards a *non-trivial problem*, an understanding of *NP-hardness*, and a *scalability comparison*. The best topics are ones where the exact method solves small instances optimally but becomes too slow on large instances, while the heuristic stays fast. That contrast is the story that earns the highest mark band.

---

## Assignment Requirements (Summary)

| Requirement | Detail |
|---|---|
| Team / Marks | 2 students, 40 marks |
| Pick 1 real problem from | Routing/Logistics · Scheduling · Resource Allocation · Subset Selection |
| Method 1 — **Exact** (required) | ILP / Branch & Bound / Dynamic Programming |
| Method 2 — **Heuristic** (required) | Greedy / Local Search / Simulated Annealing / Genetic Algorithm |
| Compare | solution quality, runtime, scalability, feasibility |
| Data | to **validate** the model (distances, costs, demands) — NOT for training |
| Deliver | GitHub (real commit history) · 15-min YouTube · PDF report · code appendix |

**How the course maps to the two required methods:**

- **L3 Linear Programming, L4 Duality, L5 ILP/MILP** → your **Exact method**
- **L10 Metaheuristics — Hill Climbing, Simulated Annealing, Genetic Algorithms** → your **Heuristic method**
- **L7/L8 KKT & constrained optimization** → useful for the Portfolio option

---

## Quick Comparison of the 4 Topics

| # | Topic | Exact method | Heuristic | Real data | Best for |
|---|---|---|---|---|---|
| ⭐1 | **CVRP** (Vehicle Routing) | MILP | Simulated Annealing | Augerat CVRPLIB | Highest marks, best scalability story |
| 2 | **Nurse/Staff Rostering** | ILP | Genetic Algorithm | INRC / synthetic | Strong formulation marks (constraint-heavy) |
| 3 | **Portfolio Optimization** | MILP | Genetic Algorithm | Stock prices (yfinance) | Elegant, easy real data, finance |
| 4 | **TSP** (Travelling Salesman) | Held-Karp DP | 2-opt + SA | TSPLIB | Easiest to code, clearest NP-hardness demo |

**Recommendation:**
- Want the **highest marks** and don't mind more work → **CVRP** or **Rostering**
- Want the **easiest to code** and clearest NP-hardness demo → **TSP**
- Interested in **finance** with easy real data → **Portfolio**

> **Note:** *Feature Selection* was deliberately avoided — it uses data for **model training**, which the assignment explicitly says to avoid.

---
---

# ⭐ PROJECT 1 — Capacitated Vehicle Routing Problem (CVRP)

**Category:** Routing / Logistics · **Exact:** MILP · **Heuristic:** Simulated Annealing

## 1. The Problem (simple words)
A depot (warehouse) has a fleet of delivery vans. Each van has a **maximum capacity** (e.g. 100 units). There are many **customers**, each needing a certain **demand** (e.g. 15 units). Every customer must be visited **exactly once** by **one** van. Each van starts at the depot and returns to the depot.

**Goal:** Find the set of routes that serves all customers with the **shortest total distance**, without any van exceeding its capacity.

This is **NP-hard** — matches **Lecture 5 (ILP/MILP)** and **Lecture 10 (SA/GA)**.

## 2. Dataset — Augerat CVRPLIB benchmark (Set A)
- **Source:** http://vrp.galgos.inf.puc-rio.br (CVRPLIB — free, official)
- **Inside each `.vrp` file:** node coordinates (x, y), each customer's demand, vehicle capacity, number of vehicles, and the **known optimal solution**.
- **Why it scores well:** real, non-trivial, standard benchmark with **known optima** → you can measure exact quality gap.

| Instance | Customers | Purpose |
|---|---|---|
| A-n32-k5 | 31 | Exact can (almost) solve to optimum |
| A-n44-k6 | 43 | Exact becomes slow |
| A-n60-k9 | 59 | Exact times out → heuristic wins |
| A-n80-k10 | 79 | Only the heuristic works |

*Optional real extra:* one Sri Lankan instance (10–12 real Colombo delivery points via Google Maps / OpenStreetMap distances).

## 3. Mathematical Formulation (MILP)
**Data:** nodes `0..n` (0 = depot); `d(i,j)` distance; `q(i)` demand; `Q` capacity; `K` vehicles.

**Decision variable:** `x(i,j) = 1` if a vehicle goes directly from `i` to `j`, else `0`.

**Objective:** `minimize  SUM over i,j of d(i,j) * x(i,j)`

**Constraints:**
- Each customer entered once: `SUM over i of x(i,j) = 1`
- Each customer left once: `SUM over j of x(i,j) = 1`
- Exactly `K` vehicles leave and return to depot
- Capacity + no sub-tours (MTZ): each route's demand `<= Q`

## 4. The Two Methods
**Exact — MILP:** PuLP + CBC, or Google OR-Tools. Uses Branch & Bound → provably optimal. Works up to ~30–40 customers, then too slow (proves NP-hardness).

**Heuristic — Simulated Annealing (L10):**
- *Representation:* list of routes (customer permutation split by capacity)
- *Neighbour moves:* swap two customers, move a customer to another route, reverse a segment (2-opt)
- *Key idea:* accept worse solutions with probability `exp(-delta/T)`, cool `T` slowly to escape local minima
- Fast even for 80+ customers

*Alternative heuristic:* Genetic Algorithm (DEAP).

## 5. Comparison (Results)
| Metric | Exact (MILP) | Heuristic (SA) |
|---|---|---|
| Total distance | optimal | near-optimal |
| Gap % vs optimum | 0% | ~2–5% |
| Runtime | grows very fast | stays low |
| Solves 80 customers? | No (timeout) | Yes |

**Graphs:** (1) runtime vs size — exact shoots up, heuristic flat; (2) quality gap vs size.

## 6. Tools
```bash
pip install pulp ortools numpy pandas matplotlib
# optional (GA instead of SA):
pip install deap
```

## 7. GitHub Structure
```
cvrp-optimization/
├── data/                     # Augerat .vrp instances
├── notebooks/cvrp_analysis.ipynb
├── src/parser.py             # read .vrp files
├── src/exact_milp.py         # exact method
├── src/heuristic_sa.py       # simulated annealing
├── src/compare.py            # experiments + graphs
├── results/  report.pdf  members.txt  submission.txt  README.md
```

## 8. Division of Work
- **Student A:** parser, MILP exact model, formulation section
- **Student B:** Simulated Annealing, experiments, graphs, results
- **Both:** report, GitHub, 15-min video

---
---

# PROJECT 2 — Nurse / Staff Rostering

**Category:** Scheduling · **Exact:** ILP · **Heuristic:** Genetic Algorithm

## 1. The Problem (simple words)
A hospital ward has a set of nurses and a planning period (e.g. 7 or 14 days). Each day has three shifts: **Morning, Evening, Night**. Each shift needs a required number of nurses. Assign nurses to shifts so all coverage needs are met while respecting labour rules (rest after night shift, max working days, days off).

**Goal:** Build a roster that covers every shift, obeys all rules, and **minimises total cost** (or maximises satisfied nurse preferences). NP-hard scheduling problem.

## 2. Dataset
- **Real option:** First International Nurse Rostering Competition (**INRC-2010**) datasets and **NSPLib** — real nurse numbers, shift demands, contracts.
- **Synthetic option:** generate 10–30 nurses, 7–14 days, 3 shifts, random preferences (allowed if realism is justified).

| Instance | Nurses × Days × Shifts | Purpose |
|---|---|---|
| Small | 8 × 7 × 3 | ILP solves to optimum |
| Medium | 15 × 14 × 3 | ILP becomes slow |
| Large | 30 × 28 × 3 | ILP times out → GA wins |

## 3. Mathematical Formulation (ILP)
**Data:** `i` nurse, `d` day, `s` shift; `R(d,s)` required nurses; `c(i,d,s)` cost/penalty.

**Decision variable:** `x(i,d,s) = 1` if nurse `i` works shift `s` on day `d`, else `0`.

**Objective:** `minimize  SUM over i,d,s of c(i,d,s) * x(i,d,s)`

**Constraints:**
- Coverage: `SUM over i of x(i,d,s) = R(d,s)`
- At most one shift per nurse per day: `SUM over s of x(i,d,s) <= 1`
- Maximum working days per nurse
- Rest rule: a Night shift → cannot work next Morning shift
- Minimum days off per nurse

## 4. The Two Methods
**Exact — ILP:** PuLP + CBC, or OR-Tools CP-SAT. Branch & Bound → provably optimal roster. Slows down on large wards (NP-hardness).

**Heuristic — Genetic Algorithm (L10):**
- *Representation:* a chromosome is a full roster (nurse-to-shift matrix)
- *Fitness:* negative total cost minus penalties for broken constraints
- *Operators:* tournament selection, crossover (mix two rosters), mutation (change one assignment)
- *Tool:* DEAP. Scales to large wards where ILP fails.

*Alternative heuristic:* Simulated Annealing.

## 5. Comparison (Results)
| Metric | Exact (ILP) | Heuristic (GA) |
|---|---|---|
| Roster cost | optimal | near-optimal |
| All hard rules satisfied? | yes | yes (with repair) |
| Runtime | grows very fast | stays moderate |
| Solves 30-nurse ward? | No (timeout) | Yes |

## 6. Tools
```bash
pip install pulp ortools deap numpy pandas matplotlib
```

## 7. GitHub Structure
```
rostering-optimization/
├── data/                       # INRC or synthetic instances
├── notebooks/rostering_analysis.ipynb
├── src/generator.py            # build/load instances
├── src/exact_ilp.py            # exact method
├── src/heuristic_ga.py         # genetic algorithm
├── src/compare.py              # experiments + graphs
├── results/  report.pdf  members.txt  submission.txt  README.md
```

## 8. Division of Work
- **Student A:** instance generator, ILP model, formulation section
- **Student B:** Genetic Algorithm, experiments, graphs, results
- **Both:** report, GitHub, 15-min video

---
---

# PROJECT 3 — Cardinality-Constrained Portfolio Optimization

**Category:** Subset Selection · **Exact:** MILP · **Heuristic:** Genetic Algorithm

## 1. The Problem (simple words)
An investor has a set of candidate stocks (e.g. 30 companies). Managing all of them is costly. The investor wants to pick only a small number of stocks (e.g. at most `K = 8`) and decide how much money (weight) to put in each, so the portfolio has the **lowest risk** while still reaching a **target expected return**.

**Goal:** Choose at most `K` stocks and their weights to minimise risk, subject to reaching a required return and using 100% of the budget. The "at most K stocks" (cardinality) rule needs binary variables → NP-hard.

## 2. Dataset — real stock prices via `yfinance`
- **Universe:** 30 well-known stocks (e.g. S&P 500) or Colombo Stock Exchange (CSE) shares
- **Period:** daily closing prices, 2–3 years
- **Derived:** daily returns, mean return per stock, covariance matrix (risk)

```python
import yfinance as yf
data = yf.download(['AAPL','MSFT','GOOG', ...], start='2022-01-01', end='2024-12-31')
```
Real data used only to **instantiate** the model — exactly as the brief asks.

## 3. Mathematical Formulation (MILP)
Risk as variance is quadratic (MIQP). To keep the exact method a **linear MILP** (Lecture 5), measure risk with **Mean Absolute Deviation (MAD)**, which is linear.

**Data:** `i` stock, `t` day; `r(i,t)` return; `mu(i)` mean return; `R` target return; `K` max stocks.

**Decision variables:** `w(i)` = budget fraction in stock `i` (continuous 0–1); `y(i) = 1` if stock chosen (binary).

**Objective (MAD):** `minimize (1/T) * SUM over t of | SUM over i of (r(i,t) - mu(i)) * w(i) |`
(the absolute value is linearised with helper variables → stays a MILP.)

**Constraints:**
- Budget: `SUM over i of w(i) = 1`
- Target return: `SUM over i of mu(i)*w(i) >= R`
- Link: `w(i) <= y(i)` (no weight unless chosen)
- Cardinality: `SUM over i of y(i) <= K`
- No short selling: `w(i) >= 0`

## 4. The Two Methods
**Exact — MILP:** PuLP + CBC, or OR-Tools. Branch & Bound → provably optimal portfolio. Slows as candidate stocks grow (NP-hardness).

**Heuristic — Genetic Algorithm (L10):**
- *Representation:* chosen stocks + their weights
- *Fitness:* negative risk, penalty if return target or cardinality broken
- *Operators:* tournament selection, crossover of two portfolios, mutation of a weight/stock
- *Tool:* DEAP. Handles a large universe quickly.

## 5. Comparison (Results)
| Metric | Exact (MILP) | Heuristic (GA) |
|---|---|---|
| Portfolio risk | optimal (lowest) | near-optimal |
| Meets return target? | yes | yes |
| Runtime | grows fast | stays low |
| Handles 100+ stocks? | slow/timeout | Yes |

**Graphs:** runtime vs number of stocks; risk gap vs optimum; optional risk-return **efficient frontier**.

## 6. Tools
```bash
pip install yfinance pulp deap numpy pandas matplotlib
```

## 7. GitHub Structure
```
portfolio-optimization/
├── data/                        # downloaded price CSVs
├── notebooks/portfolio_analysis.ipynb
├── src/data_loader.py           # yfinance + returns/cov
├── src/exact_milp.py            # exact method
├── src/heuristic_ga.py          # genetic algorithm
├── src/compare.py               # experiments + graphs
├── results/  report.pdf  members.txt  submission.txt  README.md
```

## 8. Division of Work
- **Student A:** data loader, MILP model, formulation section
- **Student B:** Genetic Algorithm, experiments, graphs, results
- **Both:** report, GitHub, 15-min video

---
---

# PROJECT 4 — Travelling Salesman Problem (TSP)

**Category:** Routing / Logistics · **Exact:** Held-Karp Dynamic Programming · **Heuristic:** 2-opt + Simulated Annealing

## 1. The Problem (simple words)
A salesman must visit `N` cities. He starts at a home city, visits every city **exactly once**, and returns home. Travelling between cities has a distance.

**Goal:** Find the visiting order giving the **shortest total tour distance**. The classic NP-hard problem — number of tours grows as `(N-1)!/2`.

## 2. Dataset — TSPLIB benchmark
- **Source:** http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/ (free, official)
- **Inside:** instances like `burma14`, `ulysses16`, `berlin52`, each with city coordinates and **known optimal** tour length.
- **Local option:** build a real Sri Lankan instance from town coordinates (Colombo, Kandy, Galle, Jaffna, …).

| Instance | Cities | Purpose |
|---|---|---|
| burma14 | 14 | DP solves to optimum in seconds |
| ulysses16 | 16 | DP still solvable, getting slow |
| ~18–20 cities | 18–20 | DP becomes impossible (time/memory) |
| berlin52 | 52 | Only the heuristic can solve it |

## 3. Mathematical Formulation
**Exact — Held-Karp DP recurrence:** Let `g(S, j)` = length of shortest path starting at city 1, visiting every city in set `S` once, ending at `j`.

```
g(S, j) = min over k in S, k != j  of  [ g(S \ {j}, k) + d(k, j) ]
answer  = min over j  of  [ g(all cities, j) + d(j, 1) ]
```
Cost: `O(2^n * n^2)` time, `O(2^n * n)` memory → explodes around 18–20 cities.

**Equivalent ILP (optional):** `minimize SUM d(i,j) x(i,j)`, `x` binary, each city entered/left once, plus MTZ sub-tour elimination (Lecture 5).

## 4. The Two Methods
**Exact — Held-Karp DP:** implemented in Python with a bitmask over set `S`. Provably shortest tour. Works up to ~15–17 cities, then out of time/memory — the **clearest NP-hardness demo**.

**Heuristic — 2-opt Local Search + Simulated Annealing (L10):**
- *Representation:* a permutation (ordering) of cities
- *Move (2-opt):* remove two edges and reconnect the tour the other way to remove crossings
- *Escape:* wrap 2-opt inside Simulated Annealing to accept some worse moves
- Solves 52+ cities in under a second, very close to optimum

## 5. Comparison (Results)
| Metric | Exact (Held-Karp DP) | Heuristic (2-opt + SA) |
|---|---|---|
| Tour length | optimal | near-optimal (1–3% gap) |
| Gap vs optimum | 0% | small |
| Runtime | doubles with each city | stays very low |
| Solves 52 cities? | No (impossible) | Yes |

**Graphs:** runtime vs cities on a **log scale** (DP explodes); tour quality gap vs city count; draw the best tour on the city map.

## 6. Tools
```bash
pip install numpy pandas matplotlib
# tsplib95 helps read the benchmark files:
pip install tsplib95
```

## 7. GitHub Structure
```
tsp-optimization/
├── data/                     # TSPLIB instances
├── notebooks/tsp_analysis.ipynb
├── src/parser.py             # read TSPLIB files
├── src/exact_heldkarp.py     # exact dynamic programming
├── src/heuristic_sa.py       # 2-opt + simulated annealing
├── src/compare.py            # experiments + graphs
├── results/  report.pdf  members.txt  submission.txt  README.md
```

## 8. Division of Work
- **Student A:** TSPLIB parser, Held-Karp DP, formulation section
- **Student B:** 2-opt + Simulated Annealing, experiments, graphs, results
- **Both:** report, GitHub, 15-min video

---
---

## How Each Project Maps to the Marking Rubric (40 Marks)

| Rubric criterion | How every project above earns it |
|---|---|
| Problem Selection | Realistic, non-trivial problem in an allowed category |
| Problem & Data Description | Clear context + real benchmark/market data |
| Mathematical Formulation | Complete model (variables, objective, constraints) |
| Optimization Methods | Two justified methods (one exact + one heuristic) |
| Implementation & GitHub | Clean code + many meaningful commits |
| Results | Quality, runtime, scalability, feasibility comparison + graphs |
| Discussion | NP-hardness trade-offs + future work |
| Individual Contribution | One student owns exact, one owns heuristic |
| Viva | Clear alignment with Lectures 3, 4, 5, 7, 10 |

> **Reminder:** Make **many small, meaningful commits** on GitHub. Repos without a real commit history are penalised. Missing components = zero. Turnitin > 20% is penalised.

---

*Prepared as a study/planning aid for the IT5082 Optimization Methods assignment.*
