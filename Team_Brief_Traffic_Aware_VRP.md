# IT5082 Optimization Methods: Group Assignment Team Brief

**Module:** IT5082 Optimization Methods, MSc in Artificial Intelligence, SLIIT
**Assessment:** Group Programming Assignment, 2 members, 40 marks
**Members:** Ramalingham Seyon (MS26912516) and Kekulawala Vidanalage Dhammika Kekulawala (MS26902784)
**Status of this document:** proposal for discussion. The topic is NOT final until both members agree (see section 9).

_____

---

## 1. What the assignment requires (from `Optimization_Assignment.pdf`)

- Pick a realistic decision problem, formulate it mathematically (decision variables, objective, constraints), solve it with **two methods**, and compare them.
- **Required methods:** (1) one **exact** method (ILP, Branch & Bound or Dynamic Programming) and (2) one **heuristic / metaheuristic** (Greedy, Local Search, Simulated Annealing or Genetic Algorithm).
- **Compare:** solution quality, runtime, scalability, feasibility.
- **Data:** used to instantiate and validate the model (distances, costs, demands), not to train ML models. Real data preferred; synthetic data is allowed with a realism justification.
- **Allowed problem categories:** Routing/Logistics, Scheduling, Resource Allocation, Subset Selection. Anything else needs instructor approval.
- **Environment:** Python, Jupyter preferred. Suggested libraries: OR-Tools, PuLP, Pyomo, SciPy, DEAP, PyGAD, Inspyred, Nevergrad.

### Submission (single upload: `Optimization-assignment.zip`)
1. `members.txt`
2. `submission.txt` (dataset link + GitHub link + YouTube link)
3. GitHub repository with a **commit history and meaningful commit messages**
4. 15-minute YouTube video
5. PDF report
6. Code appendix (plain text)

### Rules that cost marks
- A missing component = zero. Turnitin similarity above 20% is penalized. Only one upload is allowed. Late resubmission is capped at 45%. A GitHub repo without meaningful commit history is penalized.
- The deadline is not printed on the brief. **Confirm it on CourseWeb.**

### Marking rubric (9 criteria; the sheet prints bands of 10-8 good / 7-4 average / 3-0 poor per criterion but states a 40-mark total, so ask the lecturer how the marks are scaled)
1. Problem selection: realistic, non-trivial
2. Problem and data description: clear context and constraints
3. Mathematical formulation: correct and complete
4. Optimization methods: two justified methods
5. Implementation and GitHub: clean code plus commits
6. Results: clear comparison
7. Discussion: insightful, with future work
8. Individual contribution: clearly shown
9. Viva: strong understanding

Note: the interface/UI is **not** a graded criterion. It is a demo layer for the video (see section 8).

---

## 2. Proposed topic

**Traffic-aware Capacitated Vehicle Routing Problem with Time Windows (CVRPTW) for same-day delivery in Colombo.**

A fleet of vehicles leaves one depot, serves customers with known demands and delivery time windows, and returns. We minimise total travel cost while respecting vehicle capacity and time windows. Travel times depend on the hour of day (congestion).

### Why this topic
- **Non-trivial (Criterion 1):** a plain GPS shortest path (one origin to one destination) is solvable by Dijkstra and would be marked "trivial". Multi-stop routing with capacity and time windows is **NP-hard**, so an exact-versus-metaheuristic comparison is justified.
- **Explicitly allowed:** "Routing / Logistics (TSP, Vehicle Routing, Delivery Optimization)" is on the brief's list, so no instructor approval is needed.
- **Defendable in the viva:** public benchmark instances with known optimal costs let us prove our solvers are correct before using our own data.
- **Naturally shows the trade-off the rubric asks for:** the exact method should be optimal at small sizes and hit its time limit at larger ones. The metaheuristic should keep producing good feasible solutions at large sizes.
- **Real story:** Colombo road times, congestion by time of day, and estimated distance, time and fuel savings against a naive plan.

### Tie to the lectures
| Topic | Lecture |
|---|---|
| NP-hardness, exact vs heuristic, TSP | Lecture 1 |
| ILP / MILP, LP relaxation, Branch & Bound, cutting planes | Lecture 5 |
| Duality and gap (relaxation bound as a certificate) | Lectures 4 and 7 |
| Penalty methods for constraint violation (used in the heuristics) | Lecture 8 |
| Simulated Annealing, Genetic Algorithms, exploration vs exploitation, permutation encoding, the TSP+SA worked example | Lecture 10 |

---

## 3. Mathematical formulation (draft)

**Sets and parameters**
- Nodes 0..N, where 0 is the depot and 1..N are customers. K vehicles, capacity Q.
- Customer i has demand q_i, service time s_i and time window [e_i, l_i].
- t_ij = travel time from i to j, d_ij = distance from i to j.

**Decision variables**
- x_ij in {0,1}: 1 if a vehicle drives directly from i to j.
- T_i >= 0: arrival (service start) time at node i.
- u_i: cumulative load on the vehicle after serving i.

**Objective:** minimise total travel cost, sum over i,j of c_ij * x_ij, where c_ij is distance or travel time (optionally plus a fixed cost per vehicle used).

**Constraints**
1. Each customer is entered exactly once and left exactly once.
2. At most K routes leave the depot, and flow is conserved at every node.
3. Capacity (Miller-Tucker-Zemlin style): u_j >= u_i + q_j - Q(1 - x_ij), with q_i <= u_i <= Q.
4. Time propagation: T_j >= T_i + s_i + t_ij - M(1 - x_ij).
5. Time windows: e_i <= T_i <= l_i.
6. x_ij in {0,1}.

### Key design decision: how to handle traffic (please confirm)
Travel time that changes continuously with the hour is hard to put in a linear model. Proposed approach:
- **Exact method:** solve the MILP on a **fixed traffic scenario** (for example off-peak, morning peak, evening peak), each using its own static time matrix.
- **Heuristics:** evaluate routes with the **time-dependent** travel times (piecewise constant by time slot), which is easy inside a search algorithm.
- **Fair comparison:** re-evaluate every solution (exact and heuristic) under the same time-dependent evaluator, and report how well the exact solution for one scenario holds up under real time-varying traffic. This is itself a useful, defendable finding.

---

## 4. Methods

### Exact (required)
- MILP as above, solved with **PuLP + CBC**, **Pyomo**, or **SciPy `milp` (HiGHS)**. Report solver status, optimality gap, root LP-relaxation bound and runtime, with a time limit.
- Note: OR-Tools' routing library is itself a heuristic (guided local search). It can serve as an extra reference baseline but does **not** count as the exact method.
- Expected: optimal at roughly N = 10 to 25, time limit or large gap beyond that. This is the scalability story.

### Metaheuristics (at least one required; two is stronger)
- **Simulated Annealing:** neighbourhoods relocate, swap, 2-opt* and or-opt; infeasibility handled with a penalty term (Lecture 8); exponential cooling.
- **Genetic Algorithm:** giant-tour permutation encoding decoded into routes, order crossover, swap mutation, tournament selection with elitism (Lecture 10). Library option: DEAP.
- Optional: a hybrid (GA followed by SA/local-search refinement).
- Run metaheuristics over multiple random seeds and report mean, standard deviation and best.

---

## 5. Data plan

### 5a. Benchmarks for correctness (free, public)
- **CVRPLIB** instances (for example A-n32-k5, known optimum reported as 784; verify on the site) and **Solomon** VRPTW instances. Check our exact solver and heuristics reproduce known optimal or best-known values before applying them to Colombo.

### 5b. Colombo instance
- Depot and customer locations: real points of interest (supermarkets, pharmacies) from OpenStreetMap, or synthetic customers around real Colombo landmarks with a realism justification. Demands and time windows are generated from a documented distribution (allowed by the brief if justified).
- Road times: OpenStreetMap-based routing (free-flow). The public OSRM demo server answered a test Colombo route, but it is a demo server, so avoid heavy use or run it locally.

### 5c. Traffic data (options)
| Option | Notes |
|---|---|
| Google Maps Routes API (Route Matrix, traffic-aware) | Gives travel times by departure time from live and historical traffic; cannot return past traffic. Billing account and card required. |
| TomTom or HERE routing/traffic APIs | Free tiers exist; reportedly no card needed for TomTom. **Not verified, check current terms.** |
| Mapbox `driving-traffic` profile | Typical traffic by time of day; free tier. **Not verified.** |
| Open datasets from other cities (METR-LA, PEMS-BAY, NYC taxi trips) | Free downloads, useful to build a rush-hour congestion profile; not Colombo, so needs a justification. |
| OSRM public server | Free-flow times only, no traffic. |
| Documented congestion model (for example BPR-style multipliers on free-flow times) | Allowed as synthetic data if justified; calibrate against a few real samples. |

**Recommended approach:** take a small set of real API samples for Colombo at a few departure times (for example 7am, 9am, 1pm, 5pm, 8pm) to calibrate time-of-day congestion multipliers, then apply those multipliers to the larger OpenStreetMap-based instances. This gives real Colombo evidence in the model and lets us test all sizes.

**Terms of service warning:** Google (and some other providers) restrict storing and republishing their data, but the assignment needs a public dataset link and a reproducible pipeline. Prefer publishing only **derived multipliers** (peak travel time divided by free-flow time), not raw API responses. Read each provider's current terms before storing anything.

### 5d. Google Maps cost estimate (from Google's pages, September 2026; re-check before spending)
- Route Matrix with traffic-aware routing is billed at the **Pro** rate of **$10 per 1,000 elements** (up to 100K). Elements = origins x destinations.
- The pricing page lists **5,000 free events per month** for that rate, but the usage-and-billing page did not mention a free cap. Treat the free cap as unconfirmed.
- New Google Cloud customers get a **$300 credit for 91 days**; a card is required and the account must never have been a paying Google Cloud or Maps customer.

| Plan (5 departure times) | Elements | If the free cap applies | If no free cap |
|---|---|---|---|
| 25 locations | 3,125 | $0 | about $31 |
| 50 locations | 12,500 | about $75 | about $125 |

**Safety steps:** set a budget alert and a daily quota cap in the Cloud console before any calls. Who enters a card, if anyone, is an open decision (section 9).

---

## 6. Experiments and metrics

- Instance sizes (from the repo README): **N = 10, 25, 50, 100, 250**.
- Metrics per method and size: total cost, **optimality gap %** (against the exact bound or best-known value), runtime, memory, feasibility (capacity and time-window violations), and for metaheuristics the spread over seeds.
- Scenarios: off-peak vs peak traffic; time-window tightness; fleet size.
- Deliver plots: gap vs size, runtime vs size (log scale), convergence curves, cost under time-dependent re-evaluation.

---

## 7. Repository (`Assignment/GIT`)

Current state: a local git repo with 2 commits ("Initial Commit", "Convert README to UTF-8"), containing `README.md` and `Members.md`.

Planned layout (from the README): `data/`, `src/`, `notebooks/`, `results/`, `report/`.

Commit rules to protect the GitHub marks:
- Small, frequent commits with descriptive messages (for example "Add MTZ capacity constraints to MILP model"), from **both** members.
- Do not commit everything in one go at the end.
- Keep API keys out of the repo (use environment variables and `.gitignore`).

---

## 8. Optional demo interface (for the video)

A Streamlit app (Streamlit, Plotly and PyDeck are already installed on Seyon's machine): interactive Colombo map with colour-coded routes, sidebar for customer count / fleet size / capacity / time windows / solver choice, live convergence chart, benchmark panel (gap and runtime), and headline savings versus naive routing. Build this **after** the solvers and benchmarks work. It supports the 15-minute video but earns no rubric marks by itself.

Packages still to install: OR-Tools, PuLP (or Pyomo), DEAP, folium, OSMnx.

---

## 9. Open decisions (need your input)

1. **Topic:** agree on traffic-aware CVRPTW in Colombo, or choose an alternative (for example ambulance-station location or a cardinality-constrained portfolio).
2. **Deadline:** not stated on the brief; confirm on CourseWeb.
3. **Traffic data source:** Google (needs a card, about $0 to $125 for the plan above), TomTom/HERE, or the documented congestion model only. Who sets up the account?
4. **Traffic handling in the exact model:** fixed scenarios (proposed) versus something more complex.
5. **Exact solver:** CBC via PuLP, Pyomo, or SciPy/HiGHS.
6. **Which heuristics:** Simulated Annealing, Genetic Algorithm, or both.
7. **Repository visibility** and where the dataset and video links will be hosted.

---

## Sources for the pricing information
- Routes API pricing: https://developers.google.com/maps/billing-and-pricing/pricing
- Routes API usage and billing: https://developers.google.com/maps/documentation/routes/usage-and-billing
- Getting started with Google Maps Platform: https://developers.google.com/maps/get-started
