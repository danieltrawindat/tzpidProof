theory TZPID_QuantumMatter_ProbabilityCarriers
  imports TZPID_Theorem_Semantic_Batch017_Quantum_Matter_Followup
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Quantum/matter probability-carrier upgrade.

  Batch 017 already records scalar guards for vacuum cutoffs, electron
  conservation, discrete dark matter, quantum violation, and Bell helicity
  bounds.  This layer introduces a conservative two-state diagonal density
  carrier.  It is not a full complex Hilbert-space formalization, but it gives
  Phase 2 typed semantics for trace-one normalization, Born probabilities,
  conservation residuals, Bell/CHSH bounds, and discrete matter shells.
\<close>

definition qm_density2_trace :: "real \<Rightarrow> real \<Rightarrow> real" where
  "qm_density2_trace p0 p1 = p0 + p1"

definition qm_density2_positive :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "qm_density2_positive p0 p1 \<longleftrightarrow> 0 \<le> p0 \<and> 0 \<le> p1"

definition qm_density2_normalized :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "qm_density2_normalized p0 p1 \<longleftrightarrow>
    qm_density2_positive p0 p1 \<and> qm_density2_trace p0 p1 = 1"

definition qm_born_probability0 :: "real \<Rightarrow> real \<Rightarrow> real" where
  "qm_born_probability0 p0 p1 = p0"

definition qm_born_probability1 :: "real \<Rightarrow> real \<Rightarrow> real" where
  "qm_born_probability1 p0 p1 = p1"

definition qm_conservation_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "qm_conservation_residual before after = after - before"

definition qm_conservation_law :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "qm_conservation_law before after \<longleftrightarrow>
    qm_conservation_residual before after = 0"

definition qm_chsh_classical_bound :: "real \<Rightarrow> bool" where
  "qm_chsh_classical_bound s \<longleftrightarrow> abs s \<le> 2"

definition qm_chsh_quantum_window :: "real \<Rightarrow> bool" where
  "qm_chsh_quantum_window s \<longleftrightarrow>
    2 < abs s \<and> abs s \<le> 2 * sqrt 2"

definition qm_discrete_matter_shell :: "real \<Rightarrow> real \<Rightarrow> int \<Rightarrow> bool" where
  "qm_discrete_matter_shell mass quantum n \<longleftrightarrow>
    0 \<le> quantum \<and> discrete_dark_matter_distribution mass quantum n"

lemma qm_density2_normalized_from_components:
  assumes "0 \<le> p0"
    and "0 \<le> p1"
    and "p0 + p1 = 1"
  shows "qm_density2_normalized p0 p1"
proof -
  have positive: "qm_density2_positive p0 p1"
    unfolding qm_density2_positive_def
    using assms(1,2)
    by blast
  have trace: "qm_density2_trace p0 p1 = 1"
    unfolding qm_density2_trace_def
    using assms(3) .
  show ?thesis
    unfolding qm_density2_normalized_def
    using positive trace
    by blast
qed

lemma qm_density2_born_probability0_guard:
  assumes "qm_density2_normalized p0 p1"
  shows "normalized_probability_weight (qm_born_probability0 p0 p1)"
proof -
  have positive: "0 \<le> p0"
    using assms
    unfolding qm_density2_normalized_def qm_density2_positive_def
    by blast
  have trace: "p0 + p1 = 1"
    using assms
    unfolding qm_density2_normalized_def qm_density2_trace_def
    by blast
  have p1_nonnegative: "0 \<le> p1"
    using assms
    unfolding qm_density2_normalized_def qm_density2_positive_def
    by blast
  have upper: "p0 \<le> 1"
    using trace p1_nonnegative
    by linarith
  show ?thesis
    unfolding normalized_probability_weight_def qm_born_probability0_def
    using positive upper
    by blast
qed

lemma qm_density2_born_probability1_guard:
  assumes "qm_density2_normalized p0 p1"
  shows "normalized_probability_weight (qm_born_probability1 p0 p1)"
proof -
  have positive: "0 \<le> p1"
    using assms
    unfolding qm_density2_normalized_def qm_density2_positive_def
    by blast
  have trace: "p0 + p1 = 1"
    using assms
    unfolding qm_density2_normalized_def qm_density2_trace_def
    by blast
  have p0_nonnegative: "0 \<le> p0"
    using assms
    unfolding qm_density2_normalized_def qm_density2_positive_def
    by blast
  have upper: "p1 \<le> 1"
    using trace p0_nonnegative
    by linarith
  show ?thesis
    unfolding normalized_probability_weight_def qm_born_probability1_def
    using positive upper
    by blast
qed

lemma qm_conservation_law_from_equality:
  assumes "before = after"
  shows "qm_conservation_law before after"
proof -
  have "qm_conservation_residual before after = 0"
    unfolding qm_conservation_residual_def
    using assms
    by algebra
  then show ?thesis
    unfolding qm_conservation_law_def .
qed

lemma qm_chsh_classical_bound_from_abs:
  assumes "abs s \<le> 2"
  shows "qm_chsh_classical_bound s"
proof -
  show ?thesis
    unfolding qm_chsh_classical_bound_def
    using assms .
qed

lemma qm_chsh_quantum_window_from_bounds:
  assumes "2 < abs s"
    and "abs s \<le> 2 * sqrt 2"
  shows "qm_chsh_quantum_window s"
proof -
  show ?thesis
    unfolding qm_chsh_quantum_window_def
    using assms
    by blast
qed

lemma qm_discrete_shell_from_quantized_mass:
  assumes "0 \<le> quantum"
    and "mass = of_int n * quantum"
  shows "qm_discrete_matter_shell mass quantum n"
proof -
  have distribution: "discrete_dark_matter_distribution mass quantum n"
    unfolding discrete_dark_matter_distribution_def
    using assms(2) .
  show ?thesis
    unfolding qm_discrete_matter_shell_def
    using assms(1) distribution
    by blast
qed

theorem quantum_matter_probability_carrier_contract:
  assumes "0 \<le> p0"
    and "0 \<le> p1"
    and "p0 + p1 = 1"
    and "before = after"
    and "2 < abs s"
    and "abs s \<le> 2 * sqrt 2"
    and "0 \<le> quantum"
    and "mass = of_int n * quantum"
  shows "qm_density2_normalized p0 p1
    \<and> normalized_probability_weight (qm_born_probability0 p0 p1)
    \<and> normalized_probability_weight (qm_born_probability1 p0 p1)
    \<and> qm_conservation_law before after
    \<and> qm_chsh_quantum_window s
    \<and> qm_discrete_matter_shell mass quantum n"
proof (intro conjI)
  have normalized: "qm_density2_normalized p0 p1"
    using assms(1-3)
    by (rule qm_density2_normalized_from_components)
  show "qm_density2_normalized p0 p1"
    using normalized .
  show "normalized_probability_weight (qm_born_probability0 p0 p1)"
    using normalized
    by (rule qm_density2_born_probability0_guard)
  show "normalized_probability_weight (qm_born_probability1 p0 p1)"
    using normalized
    by (rule qm_density2_born_probability1_guard)
  show "qm_conservation_law before after"
    using assms(4)
    by (rule qm_conservation_law_from_equality)
  show "qm_chsh_quantum_window s"
    using assms(5,6)
    by (rule qm_chsh_quantum_window_from_bounds)
  show "qm_discrete_matter_shell mass quantum n"
    using assms(7,8)
    by (rule qm_discrete_shell_from_quantized_mass)
qed

end
