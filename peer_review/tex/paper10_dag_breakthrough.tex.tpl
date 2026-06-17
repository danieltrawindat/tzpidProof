\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{mathptmx}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{float}
\usepackage{microtype}
\usepackage[colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black,filecolor=black,menucolor=black,anchorcolor=black,pdfauthor={Daniel Alexander Trawin},pdfcreator={Trawin, Daniel Alexander},pdftitle={A Formally Verified Acyclic Derivation Order for a 10,271-Node Unification Registry},pdfsubject={TZPID Proof Pipeline, Paper X, DOI: 10.5281/zenodo.20632000},pdfkeywords={TZPID, derivation order, directed acyclic graph, dependency topology, Isabelle/HOL, Sledgehammer, proof ladder, DOI 10.5281/zenodo.20632000}]{hyperref}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{axiom}[theorem]{Axiom}
\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}

\title{A Formally Verified Acyclic Derivation Order for a 10,271-Node Unification Registry:\\ Dependency Topology, Depth Metrics, and an Isabelle/HOL Certification Pathway\\[0.6em]
\large TZPID Proof Pipeline Series, Paper X}
\author{Daniel Alexander Trawin\\
\small ORCID: \href{https://orcid.org/0009-0001-4630-3715}{0009-0001-4630-3715}\\
\small DOI: \href{https://doi.org/10.5281/zenodo.20632000}{10.5281/zenodo.20632000}\\
\small \href{mailto:danielalexandertrawin@gmail.com}{danielalexandertrawin@gmail.com}}
\date{June 2026}

\begin{document}
\maketitle

\begin{abstract}
This paper reports the dependency-order breakthrough in the TZPID proof pipeline. The canonical registry contains {{TOTAL_NODES}} entries, but the proof burden is not a single opaque chain. By reassembling the master registry into a dependency-respecting proof ladder, extracting {{EDGE_COUNT}} concrete materialized edge cases, and checking the generated ordering invariant in Isabelle/HOL, the package establishes a reproducible acyclic derivation order for the registry. The graph topology contains {{ISOLATED_COUNT}} isolated entries, {{NONISOLATED_COUNT}} non-isolated entries, {{NONTRIVIAL_COMPONENTS}} nontrivial connected clusters, and a maximum dependency depth of {{MAX_DEPTH_EDGES}} edges, or {{MAX_DEPTH_NODES}} sequential layers. This bounded depth is the Occam-style result: a registry with more than ten thousand entries reduces to a finite, shallow, explicitly checkable dependency architecture. The reassembled proof ladder is therefore the derivation-order authority for the proof package, and the Isabelle theory \texttt{TZPID\_DerivationOrder.thy} provides the formal order certificate.
\end{abstract}

\section{The problem: a registry is not yet a derivation}
\label{sec:problem}

The TZPID corpus is deliberately broad: foundational definitions, formal equations, spine obligations, computational certificates, source-truth metadata, and paper-facing interpretations all live in one registry. Scale creates a problem. A flat master list records entries, but it does not tell a reviewer which entries must be accepted before which other entries can be read as derived.

The solution developed here is to turn the registry into a directed acyclic derivation infrastructure. The file \texttt{TZPID\_ALL\_IDS\_REASSEMBLED\_PROOF\_LADDER.md} reorders all {{TOTAL_NODES}} canonical entries into a proof ladder. Its order is induced by explicit ID citations, curated spine chains, companion-spine chains, and canonical ID order only where no dependency constrains two entries.

\begin{definition}[Proof ladder]
A proof ladder is a total registry order in which every materialized prerequisite appears above every entry that depends on it.
\end{definition}

\begin{definition}[Materialized edge case]
A materialized edge case is a concrete pair $(d,r)$, where rung $r$ depends on rung $d$. The derivation-order condition is $d < r$.
\end{definition}

\section{The core theorem}
\label{sec:core-theorem}

\begin{theorem}[DAG non-circularity and derivation-order invariant]
For the reassembled TZPID proof ladder, every one of the {{EDGE_COUNT}} concrete materialized rung-to-rung edge cases satisfies the strict upward-rung condition
\[
d < r.
\]
Consequently, the materialized dependency graph is acyclic with respect to the reassembled ladder order.
\end{theorem}

\begin{proof}
The edge list is exported as \texttt{graph\_topology/materialized\_edges.csv}. The generated Isabelle/HOL theory \texttt{TZPID\_DerivationOrder.thy} defines
\[
\texttt{edge\_points\_upward}\,(d,r) \equiv d < r
\]
and checks the complete list \texttt{explicit\_ladder\_edges} by evaluation. Since each materialized edge satisfies the strict order predicate, no checked edge can point to itself, point downward, or participate in a directed cycle under the ladder ranking. The Isabelle build is therefore a machine-checkable certificate that the reassembled list is a valid derivation order for the materialized edge set.
\end{proof}

\section{What was counted}
\label{sec:counts}

The audit separates prose dependencies, table tokens, and formal edge cases because they serve different review roles.

\begin{table}[H]
\centering
\small
\caption{Dependency counts used in the DAG audit.}
\label{tab:counts}
\begin{tabularx}{\textwidth}{rL{10.4cm}}
\toprule
Count & Meaning \\
\midrule
{{EDGE_COUNT}} & Concrete materialized rung-to-rung edges encoded in Isabelle/HOL. \\
{{NUMERIC_TOKEN_COUNT}} & Numeric table tokens if the single parenthetical \texttt{(+1)} summary marker is counted as a number. \\
{{PROSE_EDGE_COUNT}} & Prose-level dependency edges before cycle handling. \\
{{CUT_EDGE_COUNT}} & Cycle-partner prose edges cut to linearize the proof ladder and retained for refinement. \\
\bottomrule
\end{tabularx}
\end{table}

The formal theorem is intentionally stated over the {{EDGE_COUNT}} concrete materialized edge cases. The remaining prose-level and parenthetical material is preserved as audit evidence rather than silently forced into the formal graph.

\section{Topology of the registry graph}
\label{sec:topology}

\begin{table}[H]
\centering
\small
\caption{Connected-component topology of the reassembled registry graph.}
\label{tab:topology}
\begin{tabular}{lr}
\toprule
Metric & Value \\
\midrule
Total ladder nodes & {{TOTAL_NODES}} \\
Materialized dependency edges & {{EDGE_COUNT}} \\
Isolated nodes & {{ISOLATED_COUNT}} \\
Non-isolated nodes & {{NONISOLATED_COUNT}} \\
Connected components & {{COMPONENT_COUNT}} \\
Nontrivial connected clusters & {{NONTRIVIAL_COMPONENTS}} \\
Largest connected cluster & {{LARGEST_COMPONENT_NODES}} nodes / {{LARGEST_COMPONENT_EDGES}} edges \\
Maximum dependency depth & {{MAX_DEPTH_EDGES}} edges / {{MAX_DEPTH_NODES}} layers \\
\bottomrule
\end{tabular}
\end{table}

\begin{center}
\fbox{\begin{minipage}{0.88\textwidth}
\centering
\textbf{Occam-depth claim.} The registry has {{TOTAL_NODES}} entries, but the present dependency graph has a maximum sequential depth of only {{MAX_DEPTH_EDGES}} edges. With parallel processing by layer, the materialized proof order has {{MAX_DEPTH_NODES}} required sequential layers rather than {{TOTAL_NODES}} serial steps.
\end{minipage}}
\end{center}

\section{Depth histogram}
\label{sec:histogram}

The following histogram records how many entries land at each dependency depth. Depth 0 contains foundational or isolated entries; higher depths mark entries that inherit longer chains of prerequisites.

\begin{table}[H]
\centering
\small
\caption{Parallel layer counts by maximum prerequisite depth.}
\label{tab:depthhist}
\begin{tabular}{rr}
\toprule
Layer & Node count \\
\midrule
{{DEPTH_HISTOGRAM_ROWS}}
\bottomrule
\end{tabular}
\end{table}

\section{The deepest chain}
\label{sec:deepest}

The deepest materialized chain is the current critical path. It is the most order-sensitive corridor in the proof package, and a change near its top should trigger a downstream rebuild of the affected layer.

\begin{table}[H]
\centering
\scriptsize
\caption{Longest dependency chain in the materialized graph.}
\label{tab:longest}
\begin{tabularx}{\textwidth}{rrrrL{7.2cm}}
\toprule
Step & Layer & Rung & ID & Title \\
\midrule
{{LONGEST_CHAIN_ROWS}}
\bottomrule
\end{tabularx}
\end{table}

\section{The causal self-consistency argument}
\label{sec:causal}

The most important conceptual consequence is not merely that the full graph is ordered. It is that the major physical chains can coexist without circularity. Matter creation, gravity as accumulated force, gyromagnetic movement, phase locking, topological unification, and nested-hyperspherical enclosure claims are all indexed against the same upward-rung invariant. A physical chain may be speculative in interpretation, but it is not allowed to be circular in derivation order.

This gives the proof package a clear causal posture. The registry can discuss feedback, recursion, breathing, resonance, and self-organization at the model level while keeping the formal dependency order acyclic at the proof-infrastructure level. The universe described by the spines may contain loops; the derivation of the claims about those loops does not.

\section{Hub and sink priorities}
\label{sec:hubs}

The graph also exposes where peer review should focus first.

\begin{table}[H]
\centering
\scriptsize
\caption{Top prerequisite super-nodes by direct dependents.}
\label{tab:hubs}
\begin{tabularx}{\textwidth}{rrrL{8.4cm}}
\toprule
Rung & ID & Degree & Title \\
\midrule
{{TOP_PREREQ_ROWS}}
\bottomrule
\end{tabularx}
\end{table}

\begin{table}[H]
\centering
\scriptsize
\caption{Top dependent nodes by direct prerequisites.}
\label{tab:sinks}
\begin{tabularx}{\textwidth}{rrrL{8.4cm}}
\toprule
Rung & ID & Degree & Title \\
\midrule
{{TOP_DEPENDENT_ROWS}}
\bottomrule
\end{tabularx}
\end{table}

High prerequisite-degree nodes should be reviewed as load-bearing definitions. High dependent-degree nodes should be reviewed as audit sinks: they are places where many independent assumptions converge.

\section{Isabelle/HOL certification pathway}
\label{sec:isabelle}

The generated Isabelle theory is intentionally narrow. It does not try to prove every physical statement in the registry. It proves the build-order invariant that the physical theories rely on:

\begin{verbatim}
definition edge_points_upward :: "(nat * nat) => bool"
  where "edge_points_upward e == fst e < snd e"

definition explicit_ladder_edges :: "(nat * nat) list"
  where "explicit_ladder_edges == [...]"

lemma derivation_order_strictly_upward:
  "list_all edge_points_upward explicit_ladder_edges"
  by eval
\end{verbatim}

This is the correct scope for the DAG layer. Spine-specific semantic claims belong in the individual Isabelle/HOL theories and computational certificate lanes; the DAG theory certifies that those claims can be assembled in a non-circular derivation order.

\section{Artifacts}
\label{sec:artifacts}

The reproducible artifact set is:

\begin{itemize}
  \item \texttt{peer\_review/tex/paper10\_dag\_breakthrough.tex.tpl}: this template.
  \item \texttt{peer\_review/tex/paper10\_dag\_breakthrough.tex}: the filled paper.
  \item \texttt{fill\_dag\_paper.py}: metric computation and paper/theory generator.
  \item \texttt{TZPID\_ALL\_IDS\_REASSEMBLED\_PROOF\_LADDER.md}: derivation-order authority.
  \item \texttt{graph\_topology/materialized\_edges.csv}: {{EDGE_COUNT}} checked edge cases.
  \item \texttt{graph\_topology/GRAPH\_TOPOLOGY\_REPORT.md}: topology, critical path, and prose-gap audit.
  \item \texttt{graph\_topology/dependency\_heatmap\_nonisolated.svg}: reviewer-facing graph visualization.
  \item \texttt{tzpid\_proof/isabelle\_tzpid/TZPID\_DerivationOrder.thy}: generated Isabelle/HOL order certificate.
\end{itemize}

\section{Conclusion}
\label{sec:conclusion}

The DAG breakthrough converts the TZPID registry from a large catalog into a proof pipeline. It supplies a derivation-order authority for all {{TOTAL_NODES}} canonical entries, separates isolated parallelizable material from connected risk zones, identifies the deepest dependency chain, and proves the strict upward-rung invariant for all {{EDGE_COUNT}} concrete materialized edge cases. The result is not a claim that every physics interpretation has already been proven. It is the stronger infrastructure claim that the registry now has a reproducible, acyclic, machine-checkable order in which such proofs and certificates can be built.

\begin{thebibliography}{9}

\bibitem{tzpid-ladder}
Daniel Alexander Trawin,
\emph{TZPID Reassembled Proof Ladder---All IDs in Derivation Order},
TZPIDProof archive, 2026.
DOI: \href{https://doi.org/10.5281/zenodo.20632000}{10.5281/zenodo.20632000}.

\bibitem{tzpid-sledgehammer}
Daniel Alexander Trawin,
\emph{TZPID Proof Ladder Sledgehammer Report},
TZPIDProof archive, 2026.
DOI: \href{https://doi.org/10.5281/zenodo.20632000}{10.5281/zenodo.20632000}.

\bibitem{isabelle}
Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel,
\emph{Isabelle/HOL: A Proof Assistant for Higher-Order Logic},
Springer, 2002.

\end{thebibliography}

\end{document}
