theory TZPID_TopologyCategory_Carriers
  imports TZPID_Theorem_Semantic_Batch013_Topology_Category_Followup
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 topology/category follow-up batch 013 upgrade.

  This carrier layer turns the follow-up guards into finite categorical and
  topological contracts: antipodal equality, Buckingham-Pi count recovery,
  balanced dipoles, toroidal closure, dimensional access excess, surface/bulk
  recovery, adjoint arrow pairs, encoding-decoding closure, global phase fixed
  points, and field/spectrum object witnesses.
\<close>

section \<open>Topological Reduction Carriers\<close>

definition tc_antipodal_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "tc_antipodal_residual value antipodal_value = value - antipodal_value"

definition tc_pi_count_recovery_residual :: "nat \<Rightarrow> nat \<Rightarrow> int" where
  "tc_pi_count_recovery_residual variable_count base_dimension_count =
     int (buckingham_pi_count variable_count base_dimension_count) +
     int base_dimension_count - int variable_count"

definition tc_dipole_balance_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "tc_dipole_balance_margin north south = - abs (dipole_topology_residual north south)"

definition tc_toroidal_balance_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "tc_toroidal_balance_margin meridian longitude =
     - abs (toroidal_constraint_residual meridian longitude)"

definition tc_dimensional_access_excess :: "nat \<Rightarrow> nat \<Rightarrow> int" where
  "tc_dimensional_access_excess ambient_dim access_dim =
     int ambient_dim - int access_dim"

definition tc_surface_recovery_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "tc_surface_recovery_residual surface bulk =
     surface_dominance_ratio surface bulk * bulk - surface"

section \<open>Finite Category Carriers\<close>

definition tc_identity_arrow :: "category_object \<Rightarrow> category_arrow" where
  "tc_identity_arrow obj = (obj, obj)"

definition tc_arrow_composable :: "category_arrow \<Rightarrow> category_arrow \<Rightarrow> bool" where
  "tc_arrow_composable left right \<longleftrightarrow>
     arrow_codomain left = arrow_domain right"

definition tc_arrow_composition :: "category_arrow \<Rightarrow> category_arrow \<Rightarrow> category_arrow" where
  "tc_arrow_composition left right =
     (arrow_domain left, arrow_codomain right)"

definition tc_roundtrip_residual :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "tc_roundtrip_residual encoded decoded original =
     encoding_decoding_residual decoded original +
     global_phase_symmetry_residual encoded encoded"

definition tc_field_spectrum_pair_guard :: "category_object \<Rightarrow> category_object \<Rightarrow> bool" where
  "tc_field_spectrum_pair_guard field_obj spectrum_obj \<longleftrightarrow>
     categorical_framework_object_guard field_obj \<and>
     categorical_framework_object_guard spectrum_obj \<and>
     adjoint_pair_guard (field_obj, spectrum_obj) (spectrum_obj, field_obj)"

section \<open>Carrier Laws\<close>

theorem tc_antipodal_residual_zero_from_guard:
  assumes "borsuk_ulam_antipodal_guard value antipodal_value"
  shows "tc_antipodal_residual value antipodal_value = 0"
proof -
  have "value = antipodal_value"
    using assms
    unfolding borsuk_ulam_antipodal_guard_def .
  thus ?thesis
    unfolding tc_antipodal_residual_def
    by algebra
qed

theorem tc_pi_count_recovers_variable_count:
  assumes "base_dimension_count \<le> variable_count"
  shows "tc_pi_count_recovery_residual variable_count base_dimension_count = 0"
proof -
  have "buckingham_pi_count variable_count base_dimension_count =
    variable_count - base_dimension_count"
    unfolding buckingham_pi_count_def
    by (rule refl)
  moreover have "int (variable_count - base_dimension_count) +
      int base_dimension_count = int variable_count"
    using assms
    by presburger
  ultimately show ?thesis
    unfolding tc_pi_count_recovery_residual_def
    by linarith
qed

theorem tc_balanced_dipole_margin_zero:
  "tc_dipole_balance_margin mu (- mu) = 0"
proof -
  have "dipole_topology_residual mu (- mu) = 0"
    using id9999_dipole_constraint_topology_balanced .
  thus ?thesis
    unfolding tc_dipole_balance_margin_def
    by algebra
qed

theorem tc_balanced_toroidal_margin_zero:
  "tc_toroidal_balance_margin meridian meridian = 0"
proof -
  have "toroidal_constraint_residual meridian meridian = 0"
    using id9999_universal_toroidal_constraint_balanced .
  thus ?thesis
    unfolding tc_toroidal_balance_margin_def
    by algebra
qed

theorem tc_dimensional_access_excess_nonnegative:
  assumes "dimensional_access_guard ambient_dim access_dim"
  shows "0 \<le> tc_dimensional_access_excess ambient_dim access_dim"
proof -
  have "ambient_dim \<ge> access_dim"
    using assms
    unfolding dimensional_access_guard_def .
  thus ?thesis
    unfolding tc_dimensional_access_excess_def
    by linarith
qed

theorem tc_surface_recovery_residual_zero:
  assumes "bulk \<noteq> 0"
  shows "tc_surface_recovery_residual surface bulk = 0"
proof -
  have "surface_dominance_ratio surface bulk * bulk = surface"
    using assms
    by (rule id9999_surface_dominance_recovers_surface)
  thus ?thesis
    unfolding tc_surface_recovery_residual_def
    by algebra
qed

theorem tc_identity_left_composition:
  "tc_arrow_composition (tc_identity_arrow obj) (obj, target) = (obj, target)"
proof -
  show ?thesis
    unfolding tc_arrow_composition_def tc_identity_arrow_def arrow_domain_def arrow_codomain_def
    by (rule refl)
qed

theorem tc_identity_right_composition:
  "tc_arrow_composition (source, obj) (tc_identity_arrow obj) = (source, obj)"
proof -
  show ?thesis
    unfolding tc_arrow_composition_def tc_identity_arrow_def arrow_domain_def arrow_codomain_def
    by (rule refl)
qed

theorem tc_adjoint_pair_roundtrip:
  "tc_arrow_composable (field_obj, spectrum_obj) (spectrum_obj, field_obj)
    \<and> tc_arrow_composition (field_obj, spectrum_obj) (spectrum_obj, field_obj) =
      (field_obj, field_obj)"
proof (intro conjI)
  show "tc_arrow_composable (field_obj, spectrum_obj) (spectrum_obj, field_obj)"
    unfolding tc_arrow_composable_def arrow_domain_def arrow_codomain_def
    by (rule refl)
  show "tc_arrow_composition (field_obj, spectrum_obj) (spectrum_obj, field_obj) =
      (field_obj, field_obj)"
    unfolding tc_arrow_composition_def arrow_domain_def arrow_codomain_def
    by (rule refl)
qed

theorem tc_roundtrip_residual_zero:
  "tc_roundtrip_residual original original original = 0"
proof -
  show ?thesis
    unfolding tc_roundtrip_residual_def
      encoding_decoding_residual_def global_phase_symmetry_residual_def
    by algebra
qed

theorem tc_field_spectrum_pair_guard_intro:
  "tc_field_spectrum_pair_guard field_obj spectrum_obj"
proof -
  have field: "categorical_framework_object_guard field_obj"
    using id10098_field_category_object_guard .
  have spectrum: "categorical_framework_object_guard spectrum_obj"
    using id10099_spectral_category_object_guard .
  have adjoint:
    "adjoint_pair_guard (field_obj, spectrum_obj) (spectrum_obj, field_obj)"
    using id9579_adjoint_functor_correspondence_guard .
  show ?thesis
    unfolding tc_field_spectrum_pair_guard_def
    using field spectrum adjoint
    by blast
qed

section \<open>Batch 013 Upgrade Contract\<close>

theorem topology_category_carrier_contract:
  assumes antipodal: "borsuk_ulam_antipodal_guard value antipodal_value"
    and pi_count: "base_dimension_count \<le> variable_count"
    and access: "dimensional_access_guard ambient_dim access_dim"
    and bulk_nonzero: "bulk \<noteq> 0"
  shows
    "tc_antipodal_residual value antipodal_value = 0
     \<and> tc_pi_count_recovery_residual variable_count base_dimension_count = 0
     \<and> tc_dipole_balance_margin mu (- mu) = 0
     \<and> tc_toroidal_balance_margin meridian meridian = 0
     \<and> 0 \<le> tc_dimensional_access_excess ambient_dim access_dim
     \<and> tc_surface_recovery_residual surface bulk = 0
     \<and> tc_arrow_composition (tc_identity_arrow obj) (obj, target) = (obj, target)
     \<and> tc_arrow_composition (source, obj) (tc_identity_arrow obj) = (source, obj)
     \<and> tc_arrow_composable (field_obj, spectrum_obj) (spectrum_obj, field_obj)
     \<and> tc_arrow_composition (field_obj, spectrum_obj) (spectrum_obj, field_obj) =
       (field_obj, field_obj)
     \<and> tc_roundtrip_residual original original original = 0
     \<and> tc_field_spectrum_pair_guard field_obj spectrum_obj"
proof (intro conjI)
  show "tc_antipodal_residual value antipodal_value = 0"
    using antipodal
    by (rule tc_antipodal_residual_zero_from_guard)
  show "tc_pi_count_recovery_residual variable_count base_dimension_count = 0"
    using pi_count
    by (rule tc_pi_count_recovers_variable_count)
  show "tc_dipole_balance_margin mu (- mu) = 0"
    using tc_balanced_dipole_margin_zero .
  show "tc_toroidal_balance_margin meridian meridian = 0"
    using tc_balanced_toroidal_margin_zero .
  show "0 \<le> tc_dimensional_access_excess ambient_dim access_dim"
    using access
    by (rule tc_dimensional_access_excess_nonnegative)
  show "tc_surface_recovery_residual surface bulk = 0"
    using bulk_nonzero
    by (rule tc_surface_recovery_residual_zero)
  show "tc_arrow_composition (tc_identity_arrow obj) (obj, target) = (obj, target)"
    using tc_identity_left_composition .
  show "tc_arrow_composition (source, obj) (tc_identity_arrow obj) = (source, obj)"
    using tc_identity_right_composition .
  show "tc_arrow_composable (field_obj, spectrum_obj) (spectrum_obj, field_obj)"
    using tc_adjoint_pair_roundtrip
    by blast
  show "tc_arrow_composition (field_obj, spectrum_obj) (spectrum_obj, field_obj) =
      (field_obj, field_obj)"
    using tc_adjoint_pair_roundtrip
    by blast
  show "tc_roundtrip_residual original original original = 0"
    using tc_roundtrip_residual_zero .
  show "tc_field_spectrum_pair_guard field_obj spectrum_obj"
    using tc_field_spectrum_pair_guard_intro .
qed

end
