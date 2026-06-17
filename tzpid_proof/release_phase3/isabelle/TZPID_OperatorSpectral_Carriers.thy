theory TZPID_OperatorSpectral_Carriers
  imports TZPID_Theorem_Semantic_Batch006_Operator_Spectral
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 operator/spectral upgrade.

  This theory turns batch 006 from residual-level checks into concrete
  finite spectral carriers: ordered two-mode gaps, harmonic ladders,
  curvature-shifted spectra, Kaluza-Klein access frequencies, beat
  periods, and detuning denominators for transfer rates.  The carriers
  are intentionally small and algebraic, so they can serve as stable
  bridge lemmas for the Bessel/S3-spectrum and phase-locking spines.
\<close>

section \<open>Finite Spectral Carriers\<close>

definition os_two_mode_ordered :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "os_two_mode_ordered lambda0 lambda1 = (lambda0 \<le> lambda1)"

definition os_two_mode_gap :: "real \<Rightarrow> real \<Rightarrow> real" where
  "os_two_mode_gap lambda0 lambda1 = lambda1 - lambda0"

definition os_harmonic_ladder :: "real \<Rightarrow> int \<Rightarrow> real" where
  "os_harmonic_ladder base n = of_int n * base"

definition os_curvature_shift :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "os_curvature_shift base coupling curvature = base + coupling * curvature"

definition os_kk_access_frequency_int :: "int \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "os_kk_access_frequency_int n c radius =
     kk_access_frequency (of_int n) c radius"

definition os_full_beat_period :: "real \<Rightarrow> real" where
  "os_full_beat_period omega_beat = 2 * pi / omega_beat"

definition os_detuning_denominator :: "real \<Rightarrow> real" where
  "os_detuning_denominator detuning = 1 + detuning\<^sup>2"

definition os_transfer_core :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "os_transfer_core coupling amplitude_a amplitude_b =
     coupling * amplitude_a * amplitude_b"

definition os_gap_exceeds_perturbation :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "os_gap_exceeds_perturbation gap perturbation = (0 < gap \<and> perturbation < gap)"

section \<open>Carrier Laws\<close>

theorem os_ordered_two_mode_gap_nonnegative:
  assumes "os_two_mode_ordered lambda0 lambda1"
  shows "os_two_mode_gap lambda0 lambda1 \<ge> 0"
proof -
  have "lambda0 \<le> lambda1"
    using assms
    unfolding os_two_mode_ordered_def .
  thus ?thesis
    unfolding os_two_mode_gap_def
    by algebra
qed

theorem os_harmonic_ladder_adjacent_step:
  "os_harmonic_ladder base (n + 1) - os_harmonic_ladder base n = base"
proof -
  show ?thesis
    unfolding os_harmonic_ladder_def
    by algebra
qed

theorem os_harmonic_ladder_zero_mode:
  "os_harmonic_ladder base 0 = 0"
proof -
  show ?thesis
    unfolding os_harmonic_ladder_def
    by algebra
qed

theorem os_curvature_shift_zero_recovers_base:
  "os_curvature_shift base coupling 0 = base"
proof -
  show ?thesis
    unfolding os_curvature_shift_def
    by algebra
qed

theorem os_curvature_shift_monotone_nonnegative:
  assumes "coupling \<ge> 0"
    and "curvature \<ge> 0"
  shows "os_curvature_shift base coupling curvature \<ge> base"
proof -
  have product_nonnegative: "coupling * curvature \<ge> 0"
    using assms(1) assms(2)
    by (rule mult_nonneg_nonneg)
  show ?thesis
    unfolding os_curvature_shift_def
    using product_nonnegative
    by algebra
qed

theorem os_kk_access_frequency_int_recovers_mode:
  assumes "radius \<noteq> 0"
  shows "os_kk_access_frequency_int n c radius * (2 * pi * radius) = of_int n * c"
proof -
  have "kk_access_frequency (of_int n) c radius * (2 * pi * radius) = of_int n * c"
    using assms
    by (rule kk_access_frequency_recovers_mode)
  thus ?thesis
    unfolding os_kk_access_frequency_int_def .
qed

theorem os_full_beat_period_recovers_full_turn:
  assumes "omega_beat \<noteq> 0"
  shows "os_full_beat_period omega_beat * omega_beat = 2 * pi"
proof -
  have "os_full_beat_period omega_beat * omega_beat =
        (2 * pi / omega_beat) * omega_beat"
    unfolding os_full_beat_period_def
    by (rule refl)
  also have "... = 2 * pi"
    using assms
    by (field)
  finally show ?thesis .
qed

theorem os_semidiurnal_is_half_full_period:
  "semidiurnal_period omega = os_full_beat_period omega / 2"
proof -
  show ?thesis
    unfolding semidiurnal_period_def os_full_beat_period_def
    by algebra
qed

theorem os_detuning_denominator_positive:
  "os_detuning_denominator detuning > 0"
proof -
  have square_nonnegative: "detuning\<^sup>2 \<ge> 0"
    by (rule zero_le_power2)
  have "1 + detuning\<^sup>2 > 0"
    using square_nonnegative
    by linarith
  thus ?thesis
    unfolding os_detuning_denominator_def .
qed

theorem os_detuning_denominator_zero_detuning:
  "os_detuning_denominator 0 = 1"
proof -
  show ?thesis
    unfolding os_detuning_denominator_def
    by algebra
qed

theorem os_transfer_rate_uses_positive_denominator:
  "intermodal_transfer_rate coupling amplitude_a amplitude_b detuning =
    os_transfer_core coupling amplitude_a amplitude_b /
    os_detuning_denominator detuning"
proof -
  show ?thesis
    unfolding intermodal_transfer_rate_def os_transfer_core_def os_detuning_denominator_def
    by (rule refl)
qed

theorem os_positive_gap_implies_batch006_gap_guard:
  assumes "os_gap_exceeds_perturbation gap perturbation"
  shows "curvature_spectral_gap gap 0 curvature > 0"
proof -
  have gap_positive: "gap > 0"
    using assms
    unfolding os_gap_exceeds_perturbation_def
    by linarith
  have gap_eq: "curvature_spectral_gap gap 0 curvature = gap"
    unfolding curvature_spectral_gap_def
    by algebra
  show ?thesis
    using gap_positive gap_eq
    by linarith
qed

theorem os_gap_guard_with_nonnegative_curvature:
  assumes "os_gap_exceeds_perturbation gap perturbation"
    and "coupling \<ge> 0"
    and "curvature \<ge> 0"
  shows "curvature_spectral_gap gap coupling curvature > 0"
proof -
  have gap_positive: "gap > 0"
    using assms(1)
    unfolding os_gap_exceeds_perturbation_def
    by linarith
  show ?thesis
    using gap_positive assms(2) assms(3)
    by (rule positive_curvature_spectral_gap_guard)
qed

section \<open>Batch 006 Upgrade Contract\<close>

theorem operator_spectral_carrier_contract:
  assumes ordered: "os_two_mode_ordered lambda0 lambda1"
    and radius_nonzero: "radius \<noteq> 0"
    and beat_nonzero: "omega_beat \<noteq> 0"
    and gap_guard: "os_gap_exceeds_perturbation gap perturbation"
    and coupling_nonnegative: "coupling \<ge> 0"
    and curvature_nonnegative: "curvature \<ge> 0"
  shows
    "os_two_mode_gap lambda0 lambda1 \<ge> 0
     \<and> os_harmonic_ladder base (n + 1) - os_harmonic_ladder base n = base
     \<and> os_harmonic_ladder base 0 = 0
     \<and> os_curvature_shift base coupling 0 = base
     \<and> os_curvature_shift base coupling curvature \<ge> base
     \<and> os_kk_access_frequency_int n c radius * (2 * pi * radius) = of_int n * c
     \<and> os_full_beat_period omega_beat * omega_beat = 2 * pi
     \<and> semidiurnal_period omega_beat = os_full_beat_period omega_beat / 2
     \<and> os_detuning_denominator detuning > 0
     \<and> os_detuning_denominator 0 = 1
     \<and> intermodal_transfer_rate transfer_coupling amplitude_a amplitude_b detuning =
       os_transfer_core transfer_coupling amplitude_a amplitude_b /
       os_detuning_denominator detuning
     \<and> curvature_spectral_gap gap coupling curvature > 0"
proof (intro conjI)
  show "os_two_mode_gap lambda0 lambda1 \<ge> 0"
    using ordered
    by (rule os_ordered_two_mode_gap_nonnegative)
  show "os_harmonic_ladder base (n + 1) - os_harmonic_ladder base n = base"
    using os_harmonic_ladder_adjacent_step .
  show "os_harmonic_ladder base 0 = 0"
    using os_harmonic_ladder_zero_mode .
  show "os_curvature_shift base coupling 0 = base"
    using os_curvature_shift_zero_recovers_base .
  show "os_curvature_shift base coupling curvature \<ge> base"
    using coupling_nonnegative curvature_nonnegative
    by (rule os_curvature_shift_monotone_nonnegative)
  show "os_kk_access_frequency_int n c radius * (2 * pi * radius) = of_int n * c"
    using radius_nonzero
    by (rule os_kk_access_frequency_int_recovers_mode)
  show "os_full_beat_period omega_beat * omega_beat = 2 * pi"
    using beat_nonzero
    by (rule os_full_beat_period_recovers_full_turn)
  show "semidiurnal_period omega_beat = os_full_beat_period omega_beat / 2"
    using os_semidiurnal_is_half_full_period .
  show "os_detuning_denominator detuning > 0"
    using os_detuning_denominator_positive .
  show "os_detuning_denominator 0 = 1"
    using os_detuning_denominator_zero_detuning .
  show "intermodal_transfer_rate transfer_coupling amplitude_a amplitude_b detuning =
       os_transfer_core transfer_coupling amplitude_a amplitude_b /
       os_detuning_denominator detuning"
    using os_transfer_rate_uses_positive_denominator .
  show "curvature_spectral_gap gap coupling curvature > 0"
    using gap_guard coupling_nonnegative curvature_nonnegative
    by (rule os_gap_guard_with_nonnegative_curvature)
qed

end
