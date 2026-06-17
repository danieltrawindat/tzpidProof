theory TZPID_MetaFoundation_Carriers
  imports TZPID_Theorem_Semantic_Batch010_Meta_Foundation
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 meta-foundation batch 010 upgrade.

  This carrier layer keeps the meta-foundation rows explicit and bounded:
  base-unit positivity, observer offset recovery, Bayesian factor/posterior
  update, falsifiability margins, threshold and uniformity guards, weak-gravity
  interval bounds, restorative-force sign, reverse-process admissibility,
  creative-threshold margin, and binary split tolerance.
\<close>

section \<open>Foundation and Evidence Carriers\<close>

definition mf_base_unit_margin :: "real \<Rightarrow> real" where
  "mf_base_unit_margin unit = unit"

definition mf_observer_offset_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mf_observer_offset_residual observer_offset state =
     observer_state_relation observer_offset state - state"

definition mf_bayes_recovery_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mf_bayes_recovery_residual likelihood_i likelihood_j =
     bayes_factor likelihood_i likelihood_j * likelihood_j - likelihood_i"

definition mf_posterior_update_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mf_posterior_update_residual prior_odds factor =
     posterior_odds prior_odds factor - prior_odds * factor"

definition mf_falsifiability_margin :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mf_falsifiability_margin prediction alternative threshold =
     falsifiability_gap prediction alternative - threshold"

section \<open>Secondary Proof-Record Carriers\<close>

definition mf_threshold_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mf_threshold_margin capacity pressure = capacity - pressure"

definition mf_weak_gravity_interval_margin :: "real \<Rightarrow> real" where
  "mf_weak_gravity_interval_margin epsilon = min epsilon (1 - epsilon)"

definition mf_reverse_process_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mf_reverse_process_margin entropy_delta mass_channel =
     min (- entropy_delta) mass_channel"

definition mf_creative_pressure_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mf_creative_pressure_margin vacuum_pressure critical_pressure =
     vacuum_pressure - critical_pressure"

definition mf_binary_split_margin :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mf_binary_split_margin omega_one omega_two tolerance =
     tolerance - abs (omega_one - omega_two)"

section \<open>Carrier Laws\<close>

theorem mf_base_unit_guard_from_margin:
  assumes "0 < mf_base_unit_margin unit"
  shows "base_unit_guard unit"
proof -
  have "unit > 0"
    using assms
    unfolding mf_base_unit_margin_def .
  thus ?thesis
    by (rule positive_base_unit_guard)
qed

theorem mf_zero_observer_offset_residual:
  "mf_observer_offset_residual 0 state = 0"
proof -
  have "observer_state_relation 0 state = state"
    using zero_observer_offset_recovers_state .
  thus ?thesis
    unfolding mf_observer_offset_residual_def
    by algebra
qed

theorem mf_bayes_recovery_residual_zero:
  assumes "likelihood_j \<noteq> 0"
  shows "mf_bayes_recovery_residual likelihood_i likelihood_j = 0"
proof -
  have "bayes_factor likelihood_i likelihood_j * likelihood_j = likelihood_i"
    using assms
    by (rule bayes_factor_recovers_likelihood)
  thus ?thesis
    unfolding mf_bayes_recovery_residual_def
    by algebra
qed

theorem mf_posterior_update_residual_zero:
  "mf_posterior_update_residual prior_odds factor = 0"
proof -
  show ?thesis
    unfolding mf_posterior_update_residual_def posterior_odds_def
    by algebra
qed

theorem mf_falsifiability_margin_nonnegative:
  assumes "falsifiability_guard prediction alternative threshold"
  shows "0 \<le> mf_falsifiability_margin prediction alternative threshold"
proof -
  have "falsifiability_gap prediction alternative \<ge> threshold"
    using assms
    unfolding falsifiability_guard_def .
  thus ?thesis
    unfolding mf_falsifiability_margin_def
    by linarith
qed

theorem mf_threshold_margin_nonnegative:
  assumes "stability_threshold_guard capacity pressure"
  shows "0 \<le> mf_threshold_margin capacity pressure"
proof -
  have "capacity \<ge> pressure"
    using assms
    unfolding stability_threshold_guard_def .
  thus ?thesis
    unfolding mf_threshold_margin_def
    by linarith
qed

theorem mf_weak_gravity_interval_margin_positive:
  assumes "weak_gravity_scaling_guard epsilon"
  shows "0 < mf_weak_gravity_interval_margin epsilon"
proof -
  have lower: "0 < epsilon"
    using assms
    unfolding weak_gravity_scaling_guard_def
    by blast
  have upper: "epsilon < 1"
    using assms
    unfolding weak_gravity_scaling_guard_def
    by blast
  have "0 < 1 - epsilon"
    using upper
    by linarith
  thus ?thesis
    unfolding mf_weak_gravity_interval_margin_def
    using lower
    by linarith
qed

theorem mf_reverse_process_margin_nonnegative:
  assumes "reverse_process_guard entropy_delta mass_channel"
  shows "0 \<le> mf_reverse_process_margin entropy_delta mass_channel"
proof -
  have entropy: "entropy_delta \<le> 0"
    using assms
    unfolding reverse_process_guard_def
    by blast
  have mass: "mass_channel \<ge> 0"
    using assms
    unfolding reverse_process_guard_def
    by blast
  have "0 \<le> - entropy_delta"
    using entropy
    by linarith
  thus ?thesis
    unfolding mf_reverse_process_margin_def
    using mass
    by linarith
qed

theorem mf_creative_pressure_margin_positive:
  assumes "creative_singularity_guard vacuum_pressure critical_pressure"
  shows "0 < mf_creative_pressure_margin vacuum_pressure critical_pressure"
proof -
  have "vacuum_pressure > critical_pressure"
    using assms
    unfolding creative_singularity_guard_def .
  thus ?thesis
    unfolding mf_creative_pressure_margin_def
    by linarith
qed

theorem mf_binary_split_margin_nonnegative:
  assumes "binary_split_guard omega_one omega_two tolerance"
  shows "0 \<le> mf_binary_split_margin omega_one omega_two tolerance"
proof -
  have "abs (omega_one - omega_two) \<le> tolerance"
    using assms
    unfolding binary_split_guard_def .
  thus ?thesis
    unfolding mf_binary_split_margin_def
    by linarith
qed

section \<open>Batch 010 Upgrade Contract\<close>

theorem meta_foundation_carrier_contract:
  assumes unit_margin: "0 < mf_base_unit_margin unit"
    and likelihood_nonzero: "likelihood_j \<noteq> 0"
    and falsifiable: "falsifiability_guard prediction alternative threshold"
    and threshold_guard: "stability_threshold_guard capacity pressure"
    and weak_gravity: "weak_gravity_scaling_guard epsilon"
    and reverse: "reverse_process_guard entropy_delta mass_channel"
    and creative: "creative_singularity_guard vacuum_pressure critical_pressure"
    and split: "binary_split_guard omega_one omega_two tolerance"
  shows
    "base_unit_guard unit
     \<and> mf_observer_offset_residual 0 state = 0
     \<and> mf_bayes_recovery_residual likelihood_i likelihood_j = 0
     \<and> mf_posterior_update_residual prior_odds factor = 0
     \<and> 0 \<le> mf_falsifiability_margin prediction alternative threshold
     \<and> 0 \<le> mf_threshold_margin capacity pressure
     \<and> particle_uniformity_guard charge charge
     \<and> charge_spin_quantization_guard charge_index spin_index
     \<and> 0 < mf_weak_gravity_interval_margin epsilon
     \<and> restorative_force_guard gradient (- gradient)
     \<and> 0 \<le> mf_reverse_process_margin entropy_delta mass_channel
     \<and> 0 < mf_creative_pressure_margin vacuum_pressure critical_pressure
     \<and> 0 \<le> mf_binary_split_margin omega_one omega_two tolerance"
proof (intro conjI)
  show "base_unit_guard unit"
    using unit_margin
    by (rule mf_base_unit_guard_from_margin)
  show "mf_observer_offset_residual 0 state = 0"
    using mf_zero_observer_offset_residual .
  show "mf_bayes_recovery_residual likelihood_i likelihood_j = 0"
    using likelihood_nonzero
    by (rule mf_bayes_recovery_residual_zero)
  show "mf_posterior_update_residual prior_odds factor = 0"
    using mf_posterior_update_residual_zero .
  show "0 \<le> mf_falsifiability_margin prediction alternative threshold"
    using falsifiable
    by (rule mf_falsifiability_margin_nonnegative)
  show "0 \<le> mf_threshold_margin capacity pressure"
    using threshold_guard
    by (rule mf_threshold_margin_nonnegative)
  show "particle_uniformity_guard charge charge"
    using particle_uniformity_reflexive .
  show "charge_spin_quantization_guard charge_index spin_index"
    using charge_spin_quantization_typed_guard .
  show "0 < mf_weak_gravity_interval_margin epsilon"
    using weak_gravity
    by (rule mf_weak_gravity_interval_margin_positive)
  show "restorative_force_guard gradient (- gradient)"
    using restorative_force_definition_guard .
  show "0 \<le> mf_reverse_process_margin entropy_delta mass_channel"
    using reverse
    by (rule mf_reverse_process_margin_nonnegative)
  show "0 < mf_creative_pressure_margin vacuum_pressure critical_pressure"
    using creative
    by (rule mf_creative_pressure_margin_positive)
  show "0 \<le> mf_binary_split_margin omega_one omega_two tolerance"
    using split
    by (rule mf_binary_split_margin_nonnegative)
qed

end
