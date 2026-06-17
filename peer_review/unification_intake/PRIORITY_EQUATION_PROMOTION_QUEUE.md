# Priority Equation Promotion Queue

Generated: 2026-06-11T05:33:42

## Scope

This queue extracts equation-like and theorem-like blocks from the two first-pass unification sources: `Topological Unification of QM and GR` and `Trawin-Enlil Protocol`.  It maps each candidate to nearby or exact master IDs where possible and labels unmapped material for review before any new IDs are minted.

- Candidate blocks extracted: 203
- ID-backed or master-matched candidates: 123
- Unmapped candidates needing review: 80
- Machine-readable queue: `D:\TZPIDProof\peer_review\unification_intake\PRIORITY_EQUATION_PROMOTION_QUEUE.csv`

## Counts By Source

- Topological Unification of QM and GR: 182
- Trawin-Enlil Protocol: 21

## Counts By Promotion Status

- existing_master_equation_exact_or_near_match: 38
- id_backed_equation_context_review: 85
- new_or_unmapped_spine_candidate: 4
- new_theorem_or_definition_candidate: 10
- supporting_math_review: 66

## Counts By Candidate Kind

- align_environment: 3
- corollary_environment: 1
- definition_environment: 3
- display_math: 19
- equation_environment: 26
- inline_math: 145
- theorem_environment: 6

## First Review Slice

| Source | Kind | Line | Role | Matched IDs | Status | Candidate |
| --- | --- | ---: | --- | --- | --- | --- |
| Trawin-Enlil Protocol | equation_environment | 55 | map_or_limit_relation | ID0449; ID1871; ID3584; ID3708; ID5092; ID6489; ID9859 | id_backed_equation_context_review | `\begin{gathered} \text{ID0449} \to \text{ID3584} \to \text{ID5092} \to \text{ID1871} \\ \to \text{ID6489} \to \text{ID9859} \to \text{ID3708}. \end{gathered}` |
| Topological Unification of QM and GR | inline_math | 36 | symbolic_expression | ID0469; ID4218; ID4226; ID4227; ID8493; ID9523; ID9525 | id_backed_equation_context_review | `\infty` |
| Topological Unification of QM and GR | inline_math | 36 | map_or_limit_relation | ID0469; ID4218; ID4226; ID4227; ID8493; ID9523; ID9525 | id_backed_equation_context_review | `\eta: \mathrm{id} \Rightarrow F \circ G` |
| Topological Unification of QM and GR | inline_math | 36 | series_or_spectral_expansion | ID0469; ID4218; ID4226; ID4227; ID8493; ID9523; ID9525 | id_backed_equation_context_review | `\rho_{\mathrm{vac}}(r) \sim \sum_n (-1)^n \Gamma(n + \cdots)` |
| Topological Unification of QM and GR | inline_math | 38 | symbolic_expression | ID0469; ID4218; ID4226; ID4227; ID8493; ID9523; ID9525 | id_backed_equation_context_review | `\infty` |
| Topological Unification of QM and GR | equation_environment | 55 | map_or_limit_relation | ID0469; ID4218; ID4226; ID4227; ID8493; ID9523; ID9525 | id_backed_equation_context_review | `\begin{gathered} \text{ID9525} \to \text{ID4218} \to \text{ID0469} \to \text{ID4227} \\ \to \text{ID4226} \to \text{ID9523} \to \text{ID8493}. \end{gathered}` |
| Topological Unification of QM and GR | inline_math | 117 | symbolic_expression | ID0400; ID1392; ID5773; ID9176 | id_backed_equation_context_review | `h_{\mu\nu}` |
| Topological Unification of QM and GR | inline_math | 117 | symbolic_expression | ID0400; ID1392; ID5773; ID9176 | id_backed_equation_context_review | `\psi` |
| Topological Unification of QM and GR | inline_math | 117 | symbolic_expression | ID0400; ID1392; ID5773 | id_backed_equation_context_review | `\Sigma_{\mathrm{half}} \propto (\nabla_\mu \nabla_\nu - g_{\mu\nu}\Box)\Delta S` |
| Topological Unification of QM and GR | inline_math | 119 | symbolic_expression | ID0400; ID1392; ID5773 | id_backed_equation_context_review | `H_0` |
| Topological Unification of QM and GR | inline_math | 119 | symbolic_expression | ID0400; ID1392; ID5773 | id_backed_equation_context_review | `\Lambda` |
| Topological Unification of QM and GR | inline_math | 122 | symbolic_expression | ID0400; ID1392; ID5773 | id_backed_equation_context_review | `H_0` |
| Topological Unification of QM and GR | inline_math | 124 | symbolic_expression | ID0400; ID1392; ID5773 | id_backed_equation_context_review | `S^3` |
| Topological Unification of QM and GR | inline_math | 124 | definition_or_identity | ID0400; ID1392; ID5773 | id_backed_equation_context_review | `R(t) = a(t)` |
| Topological Unification of QM and GR | equation_environment | 125 | map_or_limit_relation | ID0400; ID1392; ID5773 | id_backed_equation_context_review | `H(t) = \frac{\dot{R}(t)}{R(t)}, \qquad V_{S^3} = 2\pi^2 R^3 \;\Longrightarrow\; \frac{\dot{V}}{V} = 3\frac{\dot{R}}{R} = 3H, \label{eq:breathing}` |
| Topological Unification of QM and GR | inline_math | 129 | symbolic_expression | ID0400; ID1392 | id_backed_equation_context_review | `S^3` |
| Topological Unification of QM and GR | inline_math | 129 | symbolic_expression | ID0400; ID1392 | id_backed_equation_context_review | `H_0 \approx 0.069` |
| Topological Unification of QM and GR | inline_math | 129 | ratio_or_fractional_relation | ID0400; ID1392 | id_backed_equation_context_review | `\dot{V}/V = 3H_0 \approx 0.21` |
| Topological Unification of QM and GR | inline_math | 131 | symbolic_expression | ID0400; ID1392 | id_backed_equation_context_review | `\Lambda` |
| Topological Unification of QM and GR | equation_environment | 134 | ratio_or_fractional_relation | ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\rho_\Lambda = \frac{\hbar c}{R^4}\, \frac{\Phi_0}{\Phi_{\mathrm{total}}} \;\sim\; H_0^2 \;\approx\; 6 \times 10^{-10}\ \mathrm{J\,m^{-3}}, \label{eq:lambdamaster}` |
| Topological Unification of QM and GR | inline_math | 138 | symbolic_expression | ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\rho_\Lambda \sim H_0^2` |
| Topological Unification of QM and GR | equation_environment | 139 | ratio_or_fractional_relation | ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\Lambda = \frac{3\, \Omega_\Lambda H_0^2}{c^2} = \begin{cases} 1.09 \times 10^{-52}\ \mathrm{m^{-2}}, & \rho_\Lambda = 5.3 \times 10^{-10}\ \mathrm{J\,m^{-3}} \quad (\text{Planc...` |
| Topological Unification of QM and GR | inline_math | 146 | symbolic_expression | ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `6 \times 10^{-10}` |
| Topological Unification of QM and GR | inline_math | 146 | symbolic_expression | ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `^{-3}` |
| Topological Unification of QM and GR | inline_math | 146 | symbolic_expression | ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\Lambda` |
| Topological Unification of QM and GR | equation_environment | 147 | ratio_or_fractional_relation | ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\lambda_\Lambda = \left( \frac{\hbar c}{\rho_\Lambda} \right)^{1/4} \approx 85\text{--}88\ \mu\mathrm{m}, \label{eq:delength}` |
| Topological Unification of QM and GR | inline_math | 151 | symbolic_expression | ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\Lambda` |
| Topological Unification of QM and GR | inline_math | 151 | symbolic_expression | ID0187; ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `H_0` |
| Topological Unification of QM and GR | inline_math | 153 | symbolic_expression | ID0187; ID0188; ID0400; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `10^{123}` |
| Topological Unification of QM and GR | equation_environment | 156 | ratio_or_fractional_relation | ID0187; ID0188; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\frac{\hbar c}{\ell_P^4} \approx 4 \times 10^{113}\ \mathrm{J\,m^{-3}} \quad (\text{ID2462}), \qquad \frac{\hbar c}{R_H^4} \approx 9 \times 10^{-131}\ \mathrm{J\,m^{-3}} \quad (...` |
| Topological Unification of QM and GR | inline_math | 160 | symbolic_expression | ID0187; ID0188; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `^{-3}` |
| Topological Unification of QM and GR | inline_math | 160 | ratio_or_fractional_relation | ID0187; ID0188; ID0388; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\hbar c/\ell_P^4 : \rho_\Lambda \approx 10^{123}` |
| Topological Unification of QM and GR | inline_math | 160 | ratio_or_fractional_relation | ID0187; ID0188; ID0388; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\rho_\Lambda = \hbar c/R^4` |
| Topological Unification of QM and GR | inline_math | 160 | symbolic_expression | ID0187; ID0188; ID0388; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `; $H_0` |
| Topological Unification of QM and GR | inline_math | 160 | ratio_or_fractional_relation | ID0187; ID0188; ID0388; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\dot{R}/R` |
| Topological Unification of QM and GR | inline_math | 160 | ratio_or_fractional_relation | ID0187; ID0188; ID0388; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `\hbar c/R^4` |
| Topological Unification of QM and GR | inline_math | 160 | symbolic_expression | ID0187; ID0188; ID0388; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `10^{123}` |
| Topological Unification of QM and GR | inline_math | 160 | ratio_or_fractional_relation | ID0187; ID0188; ID0388; ID1392; ID2453; ID2462 | id_backed_equation_context_review | `(R_\Lambda/\ell_P)^4` |
| Topological Unification of QM and GR | inline_math | 164 | definition_or_identity | ID0187; ID0188; ID0388; ID2453; ID2462 | id_backed_equation_context_review | `P_\Lambda = -\rho_\Lambda c^2` |
| Topological Unification of QM and GR | inline_math | 164 | symbolic_expression | ID0187; ID0188; ID0388; ID2453; ID2462 | id_backed_equation_context_review | `\rho_\Lambda V \propto V` |

## Operating Rule

Use this queue as a review layer, not as automatic registry mutation.  Existing IDs should be reused whenever the candidate is semantically equivalent.  New IDs should be minted only for clean formal statements that are absent from the master and useful for a paper-facing spine.
