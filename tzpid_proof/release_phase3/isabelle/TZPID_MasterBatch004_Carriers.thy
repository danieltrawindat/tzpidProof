theory TZPID_MasterBatch004_Carriers
  imports TZPID_Theorem_Semantic_Batch004
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 master batch 004 upgrade.

  This carrier layer turns the batch 004 residual guards into reusable
  algebraic contracts for base-unit scaling, boundary coefficient closure,
  information-capacity margins, dissipative decay, linear dispersion, and
  construction-consistency witnesses.
\<close>

section \<open>Base-Unit and Boundary Carriers\<close>

definition mb004_base_unit_power4 :: "real \<Rightarrow> real" where
  "mb004_base_unit_power4 base_unit = base_unit\<^sup>4"

definition mb004_vacuum_density_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mb004_vacuum_density_residual energy_integral base_unit =
     tzp_vacuum_energy_density energy_integral base_unit *
       mb004_base_unit_power4 base_unit - energy_integral"

definition mb004_boundary_coefficient_residual ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mb004_boundary_coefficient_residual geom top curv =
     boundary_coefficient_decomposition geom top curv - (geom + top + curv)"

definition mb004_mode_mass_increment :: "real \<Rightarrow> real" where
  "mb004_mode_mass_increment mass =
     confined_mode_frequency_square 0 mass"

section \<open>Information, Decay, and Dispersion Carriers\<close>

definition mb004_information_capacity_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mb004_information_capacity_margin k N = 10 powr k - N"

definition mb004_decay_power :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mb004_decay_power eta norm_square =
     - dissipative_energy_derivative eta norm_square"

definition mb004_dispersion_energy :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mb004_dispersion_energy c k mu = c\<^sup>2 * k\<^sup>2 + mu\<^sup>2"

definition mb004_dispersion_energy_residual ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mb004_dispersion_energy_residual Omega c k mu =
     linear_dispersion_residual Omega c k mu"

section \<open>Construction Witness Carrier\<close>

definition mb004_witness_score ::
  "bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> real" where
  "mb004_witness_score geometry wave tzp conservation correspondence resonance energy =
     (if geometry then 1 else 0) +
     (if wave then 1 else 0) +
     (if tzp then 1 else 0) +
     (if conservation then 1 else 0) +
     (if correspondence then 1 else 0) +
     (if resonance then 1 else 0) +
     (if energy then 1 else 0)"

definition mb004_all_witnesses ::
  "bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> bool" where
  "mb004_all_witnesses geometry wave tzp conservation correspondence resonance energy =
     construction_consistency_witness geometry wave tzp conservation correspondence resonance energy"

section \<open>Carrier Laws\<close>

theorem mb004_base_power_matches_batch_definition:
  "mb004_base_unit_power4 base_unit = base_unit\<^sup>4"
proof -
  show ?thesis
    unfolding mb004_base_unit_power4_def
    by (rule refl)
qed

theorem mb004_vacuum_density_residual_zero:
  assumes "base_unit \<noteq> 0"
  shows "mb004_vacuum_density_residual energy_integral base_unit = 0"
proof -
  have recovered:
    "tzp_vacuum_energy_density energy_integral base_unit * base_unit\<^sup>4 =
      energy_integral"
    using assms
    by (rule id0006_vacuum_density_recovers_integral)
  show ?thesis
    unfolding mb004_vacuum_density_residual_def mb004_base_unit_power4_def
    using recovered
    by algebra
qed

theorem mb004_boundary_coefficient_residual_zero:
  "mb004_boundary_coefficient_residual geom top curv = 0"
proof -
  show ?thesis
    unfolding mb004_boundary_coefficient_residual_def
      boundary_coefficient_decomposition_def
    by algebra
qed

theorem mb004_mode_mass_increment_square:
  "mb004_mode_mass_increment mass = mass\<^sup>2"
proof -
  show ?thesis
    unfolding mb004_mode_mass_increment_def confined_mode_frequency_square_def
    by algebra
qed

theorem mb004_information_margin_nonnegative:
  assumes "information_lower_bound_guard k N"
  shows "0 \<le> mb004_information_capacity_margin k N"
proof -
  have "10 powr k \<ge> N"
    using assms
    unfolding information_lower_bound_guard_def .
  thus ?thesis
    unfolding mb004_information_capacity_margin_def
    by linarith
qed

theorem mb004_decay_power_nonnegative:
  assumes "eta \<ge> 0"
    and "norm_square \<ge> 0"
  shows "0 \<le> mb004_decay_power eta norm_square"
proof -
  have decay: "dissipative_energy_derivative eta norm_square \<le> 0"
    using assms
    by (rule dissipative_energy_decay_nonpositive)
  show ?thesis
    unfolding mb004_decay_power_def
    using decay
    by linarith
qed

theorem mb004_dispersion_residual_zero_from_energy:
  assumes "Omega\<^sup>2 = mb004_dispersion_energy c k mu"
  shows "mb004_dispersion_energy_residual Omega c k mu = 0"
proof -
  have "Omega\<^sup>2 = c\<^sup>2 * k\<^sup>2 + mu\<^sup>2"
    using assms
    unfolding mb004_dispersion_energy_def .
  thus ?thesis
    unfolding mb004_dispersion_energy_residual_def
    by (rule linear_dispersion_relation_zero_residual)
qed

theorem mb004_witness_score_all_true:
  assumes "geometry"
    and "wave"
    and "tzp"
    and "conservation"
    and "correspondence"
    and "resonance"
    and "energy"
  shows "mb004_witness_score geometry wave tzp conservation correspondence resonance energy = 7"
proof -
  show ?thesis
    unfolding mb004_witness_score_def
    using assms
    by norm_num
qed

theorem mb004_all_witnesses_from_assumptions:
  assumes "geometry"
    and "wave"
    and "tzp"
    and "conservation"
    and "correspondence"
    and "resonance"
    and "energy"
  shows "mb004_all_witnesses geometry wave tzp conservation correspondence resonance energy"
proof -
  have witness:
    "construction_consistency_witness geometry wave tzp conservation correspondence resonance energy"
    using assms
    by (rule construction_consistency_from_all_witnesses)
  show ?thesis
    unfolding mb004_all_witnesses_def
    using witness .
qed

section \<open>Batch 004 Upgrade Contract\<close>

theorem master_batch004_carrier_contract:
  assumes base_unit_nonzero: "base_unit \<noteq> 0"
    and info_guard: "information_lower_bound_guard k_index N"
    and eta_nonnegative: "eta \<ge> 0"
    and norm_nonnegative: "norm_square \<ge> 0"
    and dispersion: "Omega\<^sup>2 = mb004_dispersion_energy c k_wave mu"
    and geometry: "geometry"
    and wave: "wave"
    and tzp: "tzp"
    and conservation: "conservation"
    and correspondence: "correspondence"
    and resonance: "resonance"
    and energy: "energy"
  shows
    "mb004_vacuum_density_residual energy_integral base_unit = 0
     \<and> mb004_boundary_coefficient_residual geom top curv = 0
     \<and> mb004_mode_mass_increment mass = mass\<^sup>2
     \<and> 0 \<le> mb004_information_capacity_margin k_index N
     \<and> 0 \<le> mb004_decay_power eta norm_square
     \<and> mb004_dispersion_energy_residual Omega c k_wave mu = 0
     \<and> mb004_witness_score geometry wave tzp conservation correspondence resonance energy = 7
     \<and> mb004_all_witnesses geometry wave tzp conservation correspondence resonance energy"
proof (intro conjI)
  show "mb004_vacuum_density_residual energy_integral base_unit = 0"
    using base_unit_nonzero
    by (rule mb004_vacuum_density_residual_zero)
  show "mb004_boundary_coefficient_residual geom top curv = 0"
    using mb004_boundary_coefficient_residual_zero .
  show "mb004_mode_mass_increment mass = mass\<^sup>2"
    using mb004_mode_mass_increment_square .
  show "0 \<le> mb004_information_capacity_margin k_index N"
    using info_guard
    by (rule mb004_information_margin_nonnegative)
  show "0 \<le> mb004_decay_power eta norm_square"
    using eta_nonnegative norm_nonnegative
    by (rule mb004_decay_power_nonnegative)
  show "mb004_dispersion_energy_residual Omega c k_wave mu = 0"
    using dispersion
    by (rule mb004_dispersion_residual_zero_from_energy)
  show "mb004_witness_score geometry wave tzp conservation correspondence resonance energy = 7"
    using geometry wave tzp conservation correspondence resonance energy
    by (rule mb004_witness_score_all_true)
  show "mb004_all_witnesses geometry wave tzp conservation correspondence resonance energy"
    using geometry wave tzp conservation correspondence resonance energy
    by (rule mb004_all_witnesses_from_assumptions)
qed

end
