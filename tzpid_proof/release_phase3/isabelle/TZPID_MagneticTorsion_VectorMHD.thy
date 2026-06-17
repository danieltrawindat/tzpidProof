theory TZPID_MagneticTorsion_VectorMHD
  imports TZPID_GyromagneticMovement_MHD_Helicity
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Magnetic/torsion vector-MHD upgrade.

  This layer upgrades the magnetic/torsion family from scalar guards to the
  vector-calculus/MHD carriers already locked in the gyromagnetic movement
  spine: helicity density A dot B, uniform helicity integral, ideal-MHD
  dissipation, Elsasser balance, and torsion density.
\<close>

definition mt_vector_helicity_density ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mt_vector_helicity_density ax ay az bx by bz =
    gm_helicity_density ax ay az bx by bz"

definition mt_uniform_helicity_integral :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mt_uniform_helicity_integral volume density =
    gm_uniform_helicity_integral volume density"

definition mt_torsion_density :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mt_torsion_density curvature twist =
    pattern_torsion_functional curvature twist"

definition mt_ideal_mhd_helicity_conserved ::
  "real \<Rightarrow> real \<Rightarrow> bool" where
  "mt_ideal_mhd_helicity_conserved eta helicity_rate \<longleftrightarrow>
    gm_ideal_mhd eta \<and> helicity_rate = 0"

definition mt_elsasser_balance :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "mt_elsasser_balance magnetic_force coriolis_force \<longleftrightarrow>
    gm_mhd_elsasser_balance magnetic_force coriolis_force"

lemma mt_vector_helicity_density_zero_when_b_zero:
  shows "mt_vector_helicity_density ax ay az 0 0 0 = 0"
proof -
  have "gm_helicity_density ax ay az 0 0 0 = 0"
    by (rule gm_helicity_density_zero_when_magnetic_field_zero)
  then show ?thesis
    unfolding mt_vector_helicity_density_def .
qed

lemma mt_uniform_helicity_integral_zero_density:
  shows "mt_uniform_helicity_integral volume 0 = 0"
proof -
  have "gm_uniform_helicity_integral volume 0 = 0"
    by (rule gm_uniform_helicity_integral_zero_density)
  then show ?thesis
    unfolding mt_uniform_helicity_integral_def .
qed

lemma mt_ideal_mhd_conservation_from_zero_eta:
  assumes "eta = 0"
  shows "mt_ideal_mhd_helicity_conserved eta 0"
proof -
  have ideal: "gm_ideal_mhd eta"
    using assms
    unfolding gm_ideal_mhd_def .
  show ?thesis
    unfolding mt_ideal_mhd_helicity_conserved_def
    using ideal
    by blast
qed

lemma mt_ideal_mhd_zero_resistive_dissipation:
  assumes "mt_ideal_mhd_helicity_conserved eta helicity_rate"
  shows "gm_resistive_helicity_dissipation eta current_norm_sq = 0"
proof -
  have ideal: "gm_ideal_mhd eta"
    using assms
    unfolding mt_ideal_mhd_helicity_conserved_def
    by blast
  show ?thesis
    using ideal
    by (rule gm_ideal_mhd_zero_resistive_helicity_dissipation)
qed

lemma mt_elsasser_balance_unit_number:
  assumes "mt_elsasser_balance magnetic_force coriolis_force"
  shows "elsasser_number magnetic_force coriolis_force = 1"
proof -
  have balance: "gm_mhd_elsasser_balance magnetic_force coriolis_force"
    using assms
    unfolding mt_elsasser_balance_def .
  show ?thesis
    using balance
    by (rule gm_mhd_elsasser_balance_gives_unit_elsasser)
qed

lemma mt_torsion_density_zero_for_opposite_twist:
  shows "mt_torsion_density curvature (- curvature) = 0"
proof -
  have "pattern_torsion_functional curvature (- curvature) = 0"
    by (rule opposite_twist_zeroes_pattern_torsion_functional)
  then show ?thesis
    unfolding mt_torsion_density_def .
qed

theorem magnetic_torsion_vector_mhd_contract:
  assumes "eta = 0"
    and "mt_elsasser_balance magnetic_force coriolis_force"
  shows "mt_vector_helicity_density ax ay az 0 0 0 = 0
    \<and> mt_uniform_helicity_integral volume 0 = 0
    \<and> mt_ideal_mhd_helicity_conserved eta 0
    \<and> gm_resistive_helicity_dissipation eta current_norm_sq = 0
    \<and> elsasser_number magnetic_force coriolis_force = 1
    \<and> mt_torsion_density curvature (- curvature) = 0"
proof (intro conjI)
  show "mt_vector_helicity_density ax ay az 0 0 0 = 0"
    by (rule mt_vector_helicity_density_zero_when_b_zero)
  show "mt_uniform_helicity_integral volume 0 = 0"
    by (rule mt_uniform_helicity_integral_zero_density)
  show conserved: "mt_ideal_mhd_helicity_conserved eta 0"
    using assms(1)
    by (rule mt_ideal_mhd_conservation_from_zero_eta)
  show "gm_resistive_helicity_dissipation eta current_norm_sq = 0"
    using conserved
    by (rule mt_ideal_mhd_zero_resistive_dissipation)
  show "elsasser_number magnetic_force coriolis_force = 1"
    using assms(2)
    by (rule mt_elsasser_balance_unit_number)
  show "mt_torsion_density curvature (- curvature) = 0"
    by (rule mt_torsion_density_zero_for_opposite_twist)
qed

end
