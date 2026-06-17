theory TZPID_MatterCreation_ThresholdSpine
  imports TZPID_NewSpines_Computational_Checks
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Matter creation spine upgrade.

  This layer strengthens the Energy-to-Matter Logic focus theory from abstract
  predicates into a real-valued threshold carrier:

    ID10165: regularized vacuum energy is certified finite.
    ID0188: matter onset activates when P_vac >= P_crit.
    ID2846: created energy and mass obey E = m c^2.
    ID1816: created matter density can act as a curvature source.

  The result is still a contract layer, not a first-principles derivation of
  matter creation.  Its job is to make the spine's operational semantics
  explicit enough for later certificates and paper-facing explanation.
\<close>

definition mc_pressure_onset :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "mc_pressure_onset p_vac p_crit \<longleftrightarrow> p_crit \<le> p_vac"

definition mc_density_gain :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mc_density_gain rho_before rho_after = rho_after - rho_before"

definition mc_density_increases :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "mc_density_increases rho_before rho_after \<longleftrightarrow>
    0 < mc_density_gain rho_before rho_after"

definition mc_thresholded_creation ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "mc_thresholded_creation p_vac p_crit rho_before rho_after \<longleftrightarrow>
    mc_pressure_onset p_vac p_crit
    \<and> mc_density_increases rho_before rho_after"

definition mc_mass_energy_residual :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mc_mass_energy_residual energy mass c = energy - mass * c\<^sup>2"

definition mc_mass_energy_locked :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "mc_mass_energy_locked energy mass c \<longleftrightarrow>
    mc_mass_energy_residual energy mass c = 0"

definition mc_curvature_source_strength :: "real \<Rightarrow> real \<Rightarrow> real" where
  "mc_curvature_source_strength g_eff rho_matter = g_eff * rho_matter"

definition mc_created_density_sources_curvature ::
  "real \<Rightarrow> real \<Rightarrow> bool" where
  "mc_created_density_sources_curvature g_eff rho_matter \<longleftrightarrow>
    0 < mc_curvature_source_strength g_eff rho_matter"

lemma mc_pressure_onset_from_threshold:
  assumes "p_crit \<le> p_vac"
  shows "mc_pressure_onset p_vac p_crit"
proof -
  show ?thesis
    using assms
    unfolding mc_pressure_onset_def .
qed

lemma mc_density_gain_positive_from_order:
  assumes "rho_before < rho_after"
  shows "0 < mc_density_gain rho_before rho_after"
proof -
  show ?thesis
    using assms
    unfolding mc_density_gain_def
    by linarith
qed

lemma mc_density_increases_from_order:
  assumes "rho_before < rho_after"
  shows "mc_density_increases rho_before rho_after"
proof -
  have "0 < mc_density_gain rho_before rho_after"
    using assms
    by (rule mc_density_gain_positive_from_order)
  then show ?thesis
    unfolding mc_density_increases_def .
qed

lemma mc_thresholded_creation_from_pressure_and_density:
  assumes "p_crit \<le> p_vac"
    and "rho_before < rho_after"
  shows "mc_thresholded_creation p_vac p_crit rho_before rho_after"
proof -
  have onset: "mc_pressure_onset p_vac p_crit"
    using assms(1)
    by (rule mc_pressure_onset_from_threshold)
  have density: "mc_density_increases rho_before rho_after"
    using assms(2)
    by (rule mc_density_increases_from_order)
  show ?thesis
    unfolding mc_thresholded_creation_def
    using onset density
    by blast
qed

lemma mc_mass_energy_locked_from_identity:
  assumes "energy = mass * c\<^sup>2"
  shows "mc_mass_energy_locked energy mass c"
proof -
  have "mc_mass_energy_residual energy mass c = 0"
    using assms
    unfolding mc_mass_energy_residual_def
    by algebra
  then show ?thesis
    unfolding mc_mass_energy_locked_def .
qed

lemma mc_positive_curvature_source_from_positive_density:
  assumes "0 < g_eff"
    and "0 < rho_matter"
  shows "mc_created_density_sources_curvature g_eff rho_matter"
proof -
  have "0 < g_eff * rho_matter"
    using assms
    by (rule mult_pos_pos)
  then show ?thesis
    unfolding mc_created_density_sources_curvature_def
      mc_curvature_source_strength_def .
qed

lemma mc_wolfram_regularization_certificate_passed:
  "new_spine_verified_check EnergyMatter_Regularization_Finite"
proof -
  show ?thesis
    using energy_matter_regularization_finite_passed .
qed

lemma mc_wolfram_threshold_certificate_passed:
  "new_spine_verified_check EnergyMatter_Creation_Threshold"
proof -
  show ?thesis
    using energy_matter_creation_threshold_passed .
qed

lemma mc_wolfram_mass_energy_certificate_passed:
  "new_spine_verified_check EnergyMatter_Mass_Energy_Identity"
proof -
  show ?thesis
    using energy_matter_mass_energy_identity_passed .
qed

theorem matter_creation_threshold_spine_contract:
  assumes pressure_threshold: "p_crit \<le> p_vac"
    and density_order: "rho_before < rho_after"
    and mass_energy: "energy = mass * c\<^sup>2"
    and positive_g: "0 < g_eff"
    and positive_created_density: "0 < rho_after"
  shows "new_spine_verified_check EnergyMatter_Regularization_Finite
    \<and> new_spine_verified_check EnergyMatter_Creation_Threshold
    \<and> new_spine_verified_check EnergyMatter_Mass_Energy_Identity
    \<and> mc_thresholded_creation p_vac p_crit rho_before rho_after
    \<and> 0 < mc_density_gain rho_before rho_after
    \<and> mc_mass_energy_locked energy mass c
    \<and> mc_created_density_sources_curvature g_eff rho_after"
proof (intro conjI)
  show "new_spine_verified_check EnergyMatter_Regularization_Finite"
    by (rule mc_wolfram_regularization_certificate_passed)
  show "new_spine_verified_check EnergyMatter_Creation_Threshold"
    by (rule mc_wolfram_threshold_certificate_passed)
  show "new_spine_verified_check EnergyMatter_Mass_Energy_Identity"
    by (rule mc_wolfram_mass_energy_certificate_passed)
  show "mc_thresholded_creation p_vac p_crit rho_before rho_after"
    using pressure_threshold density_order
    by (rule mc_thresholded_creation_from_pressure_and_density)
  show "0 < mc_density_gain rho_before rho_after"
    using density_order
    by (rule mc_density_gain_positive_from_order)
  show "mc_mass_energy_locked energy mass c"
    using mass_energy
    by (rule mc_mass_energy_locked_from_identity)
  show "mc_created_density_sources_curvature g_eff rho_after"
    using positive_g positive_created_density
    by (rule mc_positive_curvature_source_from_positive_density)
qed

context TZPID_EnergyMatter_Focus
begin

theorem matter_creation_threshold_extends_energy_matter_spine:
  assumes pressure_threshold: "p_crit \<le> p_vac"
    and density_order: "rho_before < rho_after"
    and mass_energy: "energy = mass * c\<^sup>2"
    and positive_g: "0 < g_eff"
    and positive_created_density: "0 < rho_after"
  shows "energy_to_matter_spine_chain
    \<and> matter_creation_pressure_threshold EM_P_vac EM_P_crit
    \<and> mass_energy_equivalence EM_energy EM_mass
    \<and> created_matter_curvature_source EM_Phi EM_G_eff EM_rho_matter
    \<and> mc_thresholded_creation p_vac p_crit rho_before rho_after
    \<and> mc_mass_energy_locked energy mass c
    \<and> mc_created_density_sources_curvature g_eff rho_after"
proof (intro conjI)
  show "energy_to_matter_spine_chain"
    using energy_to_matter_chain .
  show "matter_creation_pressure_threshold EM_P_vac EM_P_crit"
    using id0188_creation_threshold .
  show "mass_energy_equivalence EM_energy EM_mass"
    using id2846_mass_energy .
  show "created_matter_curvature_source EM_Phi EM_G_eff EM_rho_matter"
    using id1816_curvature_source .
  show "mc_thresholded_creation p_vac p_crit rho_before rho_after"
    using pressure_threshold density_order
    by (rule mc_thresholded_creation_from_pressure_and_density)
  show "mc_mass_energy_locked energy mass c"
    using mass_energy
    by (rule mc_mass_energy_locked_from_identity)
  show "mc_created_density_sources_curvature g_eff rho_after"
    using positive_g positive_created_density
    by (rule mc_positive_curvature_source_from_positive_density)
qed

end

end
