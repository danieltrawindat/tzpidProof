theory TZPID_EmergenceBifurcation_NormalForms
  imports TZPID_Theorem_Semantic_Batch015_Emergence_Bifurcation_Followup
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Emergence/bifurcation normal-form upgrade.

  Batch 015 already contains residual guards for infinite-order transition,
  symmetry-fixed bifurcation, and emergence thresholds.  This layer promotes
  those guards into reusable normal-form carriers:

    * pitchfork residual: mu*x - x^3;
    * saddle-node residual: mu + x^2;
    * transition-boundary residual: control - critical;
    * asymptotic emergence profile: exp(-scale/t) for t > 0.

  The purpose is to lock exact threshold semantics for Phase 2, while leaving
  domain-specific identification of the physical control parameter to later
  paper-facing certificates.
\<close>

definition eb_pitchfork_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "eb_pitchfork_residual mu x = mu * x - x\<^sup>3"

definition eb_pitchfork_equilibrium :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "eb_pitchfork_equilibrium mu x \<longleftrightarrow>
    eb_pitchfork_residual mu x = 0"

definition eb_pitchfork_nonzero_branch :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "eb_pitchfork_nonzero_branch mu x \<longleftrightarrow>
    x \<noteq> 0 \<and> x\<^sup>2 = mu"

definition eb_saddle_node_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "eb_saddle_node_residual mu x = mu + x\<^sup>2"

definition eb_transition_boundary_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "eb_transition_boundary_residual control critical = control - critical"

definition eb_transition_boundary :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "eb_transition_boundary control critical \<longleftrightarrow>
    eb_transition_boundary_residual control critical = 0"

definition eb_asymptotic_emergence_profile ::
  "real \<Rightarrow> real \<Rightarrow> real" where
  "eb_asymptotic_emergence_profile scale t =
    (if 0 < t then exp (-(scale / t)) else 0)"

lemma eb_pitchfork_zero_branch_equilibrium:
  shows "eb_pitchfork_equilibrium mu 0"
proof -
  have "eb_pitchfork_residual mu 0 = 0"
    unfolding eb_pitchfork_residual_def
    by algebra
  then show ?thesis
    unfolding eb_pitchfork_equilibrium_def .
qed

lemma eb_pitchfork_nonzero_branch_equilibrium:
  assumes "eb_pitchfork_nonzero_branch mu x"
  shows "eb_pitchfork_equilibrium mu x"
proof -
  have branch: "x\<^sup>2 = mu"
    using assms
    unfolding eb_pitchfork_nonzero_branch_def
    by blast
  have "eb_pitchfork_residual mu x = x * (mu - x\<^sup>2)"
    unfolding eb_pitchfork_residual_def
    by algebra
  also have "... = 0"
    using branch
    by algebra
  finally have "eb_pitchfork_residual mu x = 0" .
  then show ?thesis
    unfolding eb_pitchfork_equilibrium_def .
qed

lemma eb_saddle_node_cusp_equilibrium:
  shows "eb_saddle_node_residual 0 0 = 0"
proof -
  show ?thesis
    unfolding eb_saddle_node_residual_def
    by algebra
qed

lemma eb_transition_boundary_from_equality:
  assumes "control = critical"
  shows "eb_transition_boundary control critical"
proof -
  have "eb_transition_boundary_residual control critical = 0"
    using assms
    unfolding eb_transition_boundary_residual_def
    by algebra
  then show ?thesis
    unfolding eb_transition_boundary_def .
qed

lemma eb_asymptotic_profile_positive_after_onset:
  assumes "0 < t"
  shows "0 < eb_asymptotic_emergence_profile scale t"
proof -
  have "0 < exp (-(scale / t))"
    by (rule exp_pos)
  then show ?thesis
    unfolding eb_asymptotic_emergence_profile_def
    using assms
    by presburger
qed

lemma eb_asymptotic_profile_zero_before_onset:
  assumes "\<not> 0 < t"
  shows "eb_asymptotic_emergence_profile scale t = 0"
proof -
  show ?thesis
    unfolding eb_asymptotic_emergence_profile_def
    using assms
    by presburger
qed

theorem emergence_bifurcation_normal_form_contract:
  assumes "control = critical"
    and "eb_pitchfork_nonzero_branch mu x"
    and "0 < t"
  shows "eb_pitchfork_equilibrium mu 0
    \<and> eb_pitchfork_equilibrium mu x
    \<and> eb_saddle_node_residual 0 0 = 0
    \<and> eb_transition_boundary control critical
    \<and> 0 < eb_asymptotic_emergence_profile scale t"
proof (intro conjI)
  show "eb_pitchfork_equilibrium mu 0"
    by (rule eb_pitchfork_zero_branch_equilibrium)
  show "eb_pitchfork_equilibrium mu x"
    using assms(2)
    by (rule eb_pitchfork_nonzero_branch_equilibrium)
  show "eb_saddle_node_residual 0 0 = 0"
    by (rule eb_saddle_node_cusp_equilibrium)
  show "eb_transition_boundary control critical"
    using assms(1)
    by (rule eb_transition_boundary_from_equality)
  show "0 < eb_asymptotic_emergence_profile scale t"
    using assms(3)
    by (rule eb_asymptotic_profile_positive_after_onset)
qed

end
