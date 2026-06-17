theory TZPID_QuantumOpenSystem_Carriers
  imports TZPID_Theorem_Semantic_Batch007_Quantum_Open_Systems
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 quantum/open-system upgrade.

  This theory strengthens batch 007 with finite diagonal density and
  channel carriers.  It is still conservative: no claim is made that
  this is a full complex Hilbert-space or complete-positivity proof.
  It does, however, give checked HOL contracts for trace-one diagonal
  states, trace preservation under a two-state column-stochastic channel,
  coherence/decoherence residuals, measurement mixing, commutator
  antisymmetry, noise-denominator positivity, and quantum thermodynamic
  balance.
\<close>

section \<open>Diagonal Density and Channel Carriers\<close>

definition qos_density2_trace :: "real \<Rightarrow> real \<Rightarrow> real" where
  "qos_density2_trace p0 p1 = p0 + p1"

definition qos_density2_positive :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "qos_density2_positive p0 p1 = (0 \<le> p0 \<and> 0 \<le> p1)"

definition qos_density2_normalized :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "qos_density2_normalized p0 p1 =
     (qos_density2_positive p0 p1 \<and> qos_density2_trace p0 p1 = 1)"

definition qos_column_stochastic2 ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "qos_column_stochastic2 a00 a10 a01 a11 =
     (0 \<le> a00 \<and> 0 \<le> a10 \<and> 0 \<le> a01 \<and> 0 \<le> a11
      \<and> a00 + a10 = 1 \<and> a01 + a11 = 1)"

definition qos_channel2_trace ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "qos_channel2_trace p0 p1 a00 a10 a01 a11 =
     (a00 + a10) * p0 + (a01 + a11) * p1"

definition qos_channel2_output0 ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "qos_channel2_output0 p0 p1 a00 a01 = a00 * p0 + a01 * p1"

definition qos_channel2_output1 ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "qos_channel2_output1 p0 p1 a10 a11 = a10 * p0 + a11 * p1"

definition qos_measurement_mix :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "qos_measurement_mix weight prior outcome =
     (1 - weight) * prior + weight * outcome"

definition qos_commutator_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "qos_commutator_residual left right = left - right"

definition qos_noise_denominator :: "real \<Rightarrow> real" where
  "qos_noise_denominator frequency = 1 + frequency\<^sup>2"

definition qos_trace_distance2 :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "qos_trace_distance2 p0 p1 q0 q1 =
     (abs (p0 - q0) + abs (p1 - q1)) / 2"

section \<open>Density and Channel Laws\<close>

theorem qos_density2_normalized_from_components:
  assumes "0 \<le> p0"
    and "0 \<le> p1"
    and "p0 + p1 = 1"
  shows "qos_density2_normalized p0 p1"
proof -
  have positive: "qos_density2_positive p0 p1"
    using assms(1) assms(2)
    unfolding qos_density2_positive_def
    by blast
  have trace: "qos_density2_trace p0 p1 = 1"
    using assms(3)
    unfolding qos_density2_trace_def .
  show ?thesis
    using positive trace
    unfolding qos_density2_normalized_def
    by blast
qed

theorem qos_normalized_probability_weight0:
  assumes "qos_density2_normalized p0 p1"
  shows "normalized_probability_weight p0"
proof -
  have nonnegative: "0 \<le> p0"
    using assms
    unfolding qos_density2_normalized_def qos_density2_positive_def
    by blast
  have trace: "p0 + p1 = 1"
    using assms
    unfolding qos_density2_normalized_def qos_density2_trace_def
    by blast
  have p1_nonnegative: "0 \<le> p1"
    using assms
    unfolding qos_density2_normalized_def qos_density2_positive_def
    by blast
  have "p0 \<le> 1"
    using trace p1_nonnegative
    by linarith
  thus ?thesis
    using nonnegative
    unfolding normalized_probability_weight_def
    by blast
qed

theorem qos_normalized_probability_weight1:
  assumes "qos_density2_normalized p0 p1"
  shows "normalized_probability_weight p1"
proof -
  have nonnegative: "0 \<le> p1"
    using assms
    unfolding qos_density2_normalized_def qos_density2_positive_def
    by blast
  have trace: "p0 + p1 = 1"
    using assms
    unfolding qos_density2_normalized_def qos_density2_trace_def
    by blast
  have p0_nonnegative: "0 \<le> p0"
    using assms
    unfolding qos_density2_normalized_def qos_density2_positive_def
    by blast
  have "p1 \<le> 1"
    using trace p0_nonnegative
    by linarith
  thus ?thesis
    using nonnegative
    unfolding normalized_probability_weight_def
    by blast
qed

theorem qos_column_stochastic_trace_preserving:
  assumes normalized: "qos_density2_normalized p0 p1"
    and channel: "qos_column_stochastic2 a00 a10 a01 a11"
  shows "qos_channel2_trace p0 p1 a00 a10 a01 a11 = 1"
proof -
  have trace: "p0 + p1 = 1"
    using normalized
    unfolding qos_density2_normalized_def qos_density2_trace_def
    by blast
  have col0: "a00 + a10 = 1"
    using channel
    unfolding qos_column_stochastic2_def
    by blast
  have col1: "a01 + a11 = 1"
    using channel
    unfolding qos_column_stochastic2_def
    by blast
  have "qos_channel2_trace p0 p1 a00 a10 a01 a11 =
        (a00 + a10) * p0 + (a01 + a11) * p1"
    unfolding qos_channel2_trace_def
    by (rule refl)
  also have "... = p0 + p1"
    using col0 col1
    by algebra
  also have "... = 1"
    using trace .
  finally show ?thesis .
qed

theorem qos_identity_channel_outputs_state:
  "qos_channel2_output0 p0 p1 1 0 = p0
   \<and> qos_channel2_output1 p0 p1 0 1 = p1"
proof (rule conjI)
  show "qos_channel2_output0 p0 p1 1 0 = p0"
    unfolding qos_channel2_output0_def
    by algebra
  show "qos_channel2_output1 p0 p1 0 1 = p1"
    unfolding qos_channel2_output1_def
    by algebra
qed

section \<open>Open-System Residual Laws\<close>

theorem qos_measurement_mix_zero_weight:
  "qos_measurement_mix 0 prior outcome = prior"
proof -
  show ?thesis
    unfolding qos_measurement_mix_def
    by algebra
qed

theorem qos_measurement_mix_unit_weight:
  "qos_measurement_mix 1 prior outcome = outcome"
proof -
  show ?thesis
    unfolding qos_measurement_mix_def
    by algebra
qed

theorem qos_commutator_antisymmetric:
  "qos_commutator_residual left right = - qos_commutator_residual right left"
proof -
  show ?thesis
    unfolding qos_commutator_residual_def
    by algebra
qed

theorem qos_commutator_equal_terms_zero:
  "qos_commutator_residual term term = zero_point_commutator_residual term term"
proof -
  show ?thesis
    unfolding qos_commutator_residual_def zero_point_commutator_residual_def
    by (rule refl)
qed

theorem qos_noise_denominator_positive:
  "qos_noise_denominator frequency > 0"
proof -
  have square_nonnegative: "frequency\<^sup>2 \<ge> 0"
    by (rule zero_le_power2)
  have "1 + frequency\<^sup>2 > 0"
    using square_nonnegative
    by linarith
  thus ?thesis
    unfolding qos_noise_denominator_def .
qed

theorem qos_noise_spectrum_uses_positive_denominator:
  "quantum_noise_spectrum amplitude frequency =
    amplitude\<^sup>2 / qos_noise_denominator frequency"
proof -
  show ?thesis
    unfolding quantum_noise_spectrum_def qos_noise_denominator_def
    by (rule refl)
qed

theorem qos_trace_distance_identical_zero:
  "qos_trace_distance2 p0 p1 p0 p1 = 0"
proof -
  have first_zero: "abs (p0 - p0) = 0"
  proof -
    have "p0 - p0 = 0"
      by algebra
    hence "abs (p0 - p0) = abs 0"
      by (rule arg_cong)
    also have "... = 0"
      by (rule abs_zero)
    finally show ?thesis .
  qed
  have second_zero: "abs (p1 - p1) = 0"
  proof -
    have "p1 - p1 = 0"
      by algebra
    hence "abs (p1 - p1) = abs 0"
      by (rule arg_cong)
    also have "... = 0"
      by (rule abs_zero)
    finally show ?thesis .
  qed
  have "qos_trace_distance2 p0 p1 p0 p1 =
        (abs (p0 - p0) + abs (p1 - p1)) / 2"
    unfolding qos_trace_distance2_def
    by (rule refl)
  also have "... = 0"
    using first_zero second_zero
    by algebra
  finally show ?thesis .
qed

theorem qos_thermo_balance_matches_batch007:
  "quantum_thermo_balance heat work (heat - work) = 0"
proof -
  show ?thesis
    using quantum_thermo_balanced_zero .
qed

section \<open>Batch 007 Upgrade Contract\<close>

theorem quantum_open_system_carrier_contract:
  assumes p0_nonnegative: "0 \<le> p0"
    and p1_nonnegative: "0 \<le> p1"
    and trace_one: "p0 + p1 = 1"
    and channel: "qos_column_stochastic2 a00 a10 a01 a11"
  shows
    "qos_density2_normalized p0 p1
     \<and> normalized_probability_weight p0
     \<and> normalized_probability_weight p1
     \<and> qos_channel2_trace p0 p1 a00 a10 a01 a11 = 1
     \<and> qos_channel2_output0 p0 p1 1 0 = p0
     \<and> qos_channel2_output1 p0 p1 0 1 = p1
     \<and> qos_measurement_mix 0 prior outcome = prior
     \<and> qos_measurement_mix 1 prior outcome = outcome
     \<and> qos_commutator_residual left right = - qos_commutator_residual right left
     \<and> qos_commutator_residual term term = zero_point_commutator_residual term term
     \<and> qos_noise_denominator frequency > 0
     \<and> quantum_noise_spectrum amplitude frequency =
       amplitude\<^sup>2 / qos_noise_denominator frequency
     \<and> qos_trace_distance2 p0 p1 p0 p1 = 0
     \<and> quantum_thermo_balance heat work (heat - work) = 0"
proof (intro conjI)
  have normalized: "qos_density2_normalized p0 p1"
    using p0_nonnegative p1_nonnegative trace_one
    by (rule qos_density2_normalized_from_components)
  show "qos_density2_normalized p0 p1"
    using normalized .
  show "normalized_probability_weight p0"
    using normalized
    by (rule qos_normalized_probability_weight0)
  show "normalized_probability_weight p1"
    using normalized
    by (rule qos_normalized_probability_weight1)
  show "qos_channel2_trace p0 p1 a00 a10 a01 a11 = 1"
    using normalized channel
    by (rule qos_column_stochastic_trace_preserving)
  show "qos_channel2_output0 p0 p1 1 0 = p0"
    using qos_identity_channel_outputs_state
    by blast
  show "qos_channel2_output1 p0 p1 0 1 = p1"
    using qos_identity_channel_outputs_state
    by blast
  show "qos_measurement_mix 0 prior outcome = prior"
    using qos_measurement_mix_zero_weight .
  show "qos_measurement_mix 1 prior outcome = outcome"
    using qos_measurement_mix_unit_weight .
  show "qos_commutator_residual left right = - qos_commutator_residual right left"
    using qos_commutator_antisymmetric .
  show "qos_commutator_residual term term = zero_point_commutator_residual term term"
    using qos_commutator_equal_terms_zero .
  show "qos_noise_denominator frequency > 0"
    using qos_noise_denominator_positive .
  show "quantum_noise_spectrum amplitude frequency =
       amplitude\<^sup>2 / qos_noise_denominator frequency"
    using qos_noise_spectrum_uses_positive_denominator .
  show "qos_trace_distance2 p0 p1 p0 p1 = 0"
    using qos_trace_distance_identical_zero .
  show "quantum_thermo_balance heat work (heat - work) = 0"
    using qos_thermo_balance_matches_batch007 .
qed

end
