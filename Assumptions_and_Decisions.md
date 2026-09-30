# IT5082 Group Assignment: Assumptions and Decisions Log

Companion to `Team_Brief_Traffic_Aware_VRP.md`. This lists every assumption made while planning, how sure we are, and what changes if it turns out wrong.

**Status key:** Confirmed = read directly from the assignment sheet or repo. Assumed = a planning choice nobody has agreed to yet. Unverified = a fact taken from memory or a web page that still needs checking.

---

## A. Assignment and rules

| # | Assumption | Status | If wrong |
|---|---|---|---|
| A1 | Two exact/heuristic methods are required: one exact (ILP, B&B or DP) and one heuristic/metaheuristic | Confirmed (sheet) | n/a |
| A2 | Routing/Logistics is an approved category, so no instructor approval is needed | Confirmed (sheet lists VRP and delivery optimization) | Ask the lecturer before starting |
| A3 | The deadline is unknown | Confirmed missing from the sheet | Check CourseWeb; the phase plan has no dates until then |
| A4 | The sheet's "40 marks" and its per-criterion bands (10-8 / 7-4 / 3-0 across 9 criteria) do not add up | Confirmed (sheet) | Ask the lecturer how marks are scaled; does not change the work |
| A5 | The UI is not a graded criterion | Assumed from the rubric list | If the lecturer values it, move the demo app earlier |
| A6 | Public GitHub repo with commits from both members is required | Confirmed (sheet, README) | n/a |

## B. Topic and model

| # | Assumption | Status | If wrong |
|---|---|---|---|
| B1 | Topic = traffic-aware Capacitated VRP with Time Windows for Colombo same-day delivery | Assumed, partner not yet consulted | Fall back to an alternative (ambulance-station location, cardinality-constrained portfolio) |
| B2 | One depot, identical vehicles (K vehicles, capacity Q) | Assumed | Heterogeneous fleets add variables to the MILP |
| B3 | Objective is total travel cost (distance or time), optionally plus a fixed cost per vehicle | Assumed | Changes only the cost coefficients |
| B4 | Time windows are hard constraints in the exact model and penalised in the heuristics | Assumed | Soft windows would need lateness variables in the MILP |
| B5 | Travel time is piecewise constant by time slot and satisfies the FIFO property (leaving later never arrives earlier) | Assumed | Needed for the time-dependent evaluator to be well-defined |
| B6 | The exact model uses fixed traffic scenarios (off-peak, morning peak, evening peak); only the heuristics use fully time-dependent times | Assumed design choice, marked "please confirm" in the brief | A fully time-dependent MILP is much harder and unlikely to scale |
| B7 | The comparison is made fair by re-evaluating all solutions under the same time-dependent evaluator | Assumed | Without it the methods are judged under different rules |

## C. Methods and tools

| # | Assumption | Status | If wrong |
|---|---|---|---|
| C1 | Exact method = MILP with Miller-Tucker-Zemlin capacity and time constraints, solved by PuLP+CBC, Pyomo or SciPy/HiGHS | Assumed | Other exact options are branch-and-cut in OR-Tools MIP (SCIP) or DP for tiny cases |
| C2 | OR-Tools' routing library is a heuristic (guided local search), so it can be a baseline but not the required exact method | Assumed from how the library works | If it were counted as exact, the report would be criticised |
| C3 | Heuristics = Simulated Annealing and a Genetic Algorithm, using a penalty term for violations (Lecture 8) | Assumed | The sheet only requires one heuristic |
| C4 | Instance sizes N = 10, 25, 50, 100, 250 | Confirmed as the plan in the repo README | Adjust if the exact solver times out earlier than expected |
| C5 | The exact method will be optimal at roughly N = 10 to 25 and reach its time limit beyond that | Assumed (typical for MTZ-style VRP models) | If it solves larger sizes, extend N or tighten the time windows |
| C6 | The libraries (OR-Tools, PuLP, DEAP, folium, OSMnx) are not installed yet | Confirmed on Seyon's machine (Streamlit, Plotly, PyDeck and networkx were present) | Install before starting |

## D. Data

| # | Assumption | Status | If wrong |
|---|---|---|---|
| D1 | CVRPLIB instance A-n32-k5 has known optimum 784 | Unverified (from memory) | Check the instance page; use the value listed there |
| D2 | Benchmarks (CVRPLIB, Solomon) are freely downloadable | The CVRPLIB URL answered with a redirect when tested; not downloaded | Find another mirror |
| D3 | Colombo customer points come from OpenStreetMap places or are synthetic around real landmarks; demands and time windows are synthetic with a written justification | Assumed | The sheet allows synthetic data if justified |
| D4 | The OSRM public demo server can be used lightly; heavy use should go through a local OSRM or OSMnx | Assumed | Rate limiting would break the data pipeline |
| D5 | No free, open, real-time Colombo traffic dataset exists that we know of | Assumed | If one is found, use it instead of calibration |
| D6 | Real traffic data is best used to calibrate time-of-day multipliers from a few API samples | Assumed | Alternative is a documented BPR-style congestion model |
| D7 | Only derived multipliers (peak time divided by free-flow time) are published, not raw API responses, because provider terms may restrict storing and republishing | Assumed, terms not read in full | Read the current terms of whichever provider is used |

## E. Costs (Google Maps Routes API)

| # | Assumption | Status | If wrong |
|---|---|---|---|
| E1 | Traffic-aware Route Matrix is billed at the Pro rate of $10 per 1,000 elements up to 100K | Read on Google's pricing page and usage page, September 2026 | Re-check before spending |
| E2 | Elements = origins x destinations (25 x 25 = 625) | Read on Google's usage page | Re-check |
| E3 | 5,000 free events per month at the Pro rate | Unverified: the pricing page says so, the usage page did not mention a free cap | Cost would be up to about $31 (25 locations) or about $125 (50 locations) |
| E4 | New Google Cloud customers get $300 for 91 days; a card is required | Read via web search, not checked on Google's own page | Ask before entering a card |
| E5 | 5 departure times (7am, 9am, 1pm, 5pm, 8pm) are enough to calibrate multipliers | Assumed | Add slots at the cost of more elements |
| E6 | TomTom and HERE have free tiers and TomTom may not need a card | Unverified | Check the providers' pages |

## F. Team and repo

| # | Assumption | Status | If wrong |
|---|---|---|---|
| F1 | The partner (Kekulawala) agrees to the topic and plan | Assumed, not asked | Revisit the topic choice |
| F2 | The existing repo `Assignment/GIT` (2 commits, `README.md` and `Members.md`) will be the submission repo | Confirmed exists locally; not confirmed that it is pushed to GitHub | Create or push the remote repo |
| F3 | The report must stay under 20% Turnitin similarity | Confirmed (sheet) | Write in our own words, cite sources |

---

## Confirm next
1. **B1** (topic) and **B6** (how traffic enters the exact model).
2. **A3** (deadline), **E3** and **E4** (Google costs and card), and whether to use Google at all (D6).
3. **F1** (partner agreement).
