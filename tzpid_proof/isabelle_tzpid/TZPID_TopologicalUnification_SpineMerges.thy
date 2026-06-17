theory TZPID_TopologicalUnification_SpineMerges
  imports
    TZPID_TopologicalUnification_MintedCarriers
    TZPID_MagneticTorsion_VectorMHD
    TZPID_TopologyVector_Invariants
begin

section ‹Topological Unification Spine Merges›

text ‹
  This theory discharges the two `Merge_With_Existing_Spine` review decisions
  from the Topological Unification priority queue.  Elsasser universality is
  merged into the gyromagnetic/magnetic-torsion MHD lane, and topological
  locking is merged into the topology/vector flux-quantization lane.
›

datatype merge_target =
    Merge_Elsasser_Universality
  | Merge_Topological_Locking

definition topological_unification_merge_targets :: "merge_target list" where
  "topological_unification_merge_targets =
    [Merge_Elsasser_Universality, Merge_Topological_Locking]"

fun merge_candidate :: "merge_target ⇒ priority_candidate" where
  "merge_candidate Merge_Elsasser_Universality = Elsasser_Universality" |
  "merge_candidate Merge_Topological_Locking = Topological_Locking"

fun merge_target_existing_ids :: "merge_target ⇒ string list" where
  "merge_target_existing_ids Merge_Elsasser_Universality =
     [''ID0038'', ''ID0040'', ''ID8826'', ''ID9081'', ''ID9525'']" |
  "merge_target_existing_ids Merge_Topological_Locking =
     [''ID3386'', ''ID8523'', ''ID9723'', ''ID4218'']"

definition within_tolerance :: "real ⇒ real ⇒ real ⇒ bool" where
  "within_tolerance value center tolerance ⟷ abs (value - center) ≤ tolerance"

definition topological_locking_flux :: "real ⇒ int ⇒ real" where
  "topological_locking_flux flux_quantum n = tv_flux_multiple flux_quantum n"

definition flux_quantum_h_over_2e :: "real ⇒ real ⇒ real" where
  "flux_quantum_h_over_2e h e = h / (2 * e)"

theorem merge_target_count:
  "length topological_unification_merge_targets = 2"
  by (eval)

theorem merge_targets_trace_to_priority_candidates:
  "m ∈ set topological_unification_merge_targets ⟹
   review_action (merge_candidate m) = Merge_With_Existing_Spine"
  by (cases m; eval)

theorem elsasser_merge_gives_unit_and_half_tolerance:
  assumes "mt_elsasser_balance magnetic_force coriolis_force"
  shows "elsasser_number magnetic_force coriolis_force = 1 ∧
         within_tolerance (elsasser_number magnetic_force coriolis_force) 1 (1/2)"
proof -
  have unit: "elsasser_number magnetic_force coriolis_force = 1"
    using assms
    by (rule mt_elsasser_balance_unit_number)
  have tol: "within_tolerance (elsasser_number magnetic_force coriolis_force) 1 (1/2)"
    unfolding within_tolerance_def
    using unit
    by simp
  show ?thesis
    using unit tol
    by blast
qed

theorem topological_locking_flux_is_quantized:
  "flux_quantized (topological_locking_flux flux_quantum n) flux_quantum n"
proof -
  have "flux_quantized (tv_flux_multiple flux_quantum n) flux_quantum n"
    by (rule tv_flux_multiple_is_quantized)
  then show ?thesis
    unfolding topological_locking_flux_def .
qed

theorem topological_locking_recovers_registered_flux_multiple:
  "topological_locking_flux flux_quantum n =
   macroscopic_flux_multiple (of_int n) flux_quantum"
proof -
  have "tv_flux_multiple flux_quantum n =
        macroscopic_flux_multiple (of_int n) flux_quantum"
    by (rule tv_flux_multiple_recovers_registered_form)
  then show ?thesis
    unfolding topological_locking_flux_def .
qed

theorem topological_locking_h_over_2e_form:
  assumes "e ≠ 0"
  shows "topological_locking_flux (flux_quantum_h_over_2e h e) n =
         of_int n * (h / (2 * e))"
proof -
  have "topological_locking_flux (flux_quantum_h_over_2e h e) n =
        of_int n * flux_quantum_h_over_2e h e"
    unfolding topological_locking_flux_def tv_flux_multiple_def
    by (rule refl)
  then show ?thesis
    unfolding flux_quantum_h_over_2e_def .
qed

theorem topological_unification_merge_contract:
  assumes "mt_elsasser_balance magnetic_force coriolis_force"
  shows "review_action Elsasser_Universality = Merge_With_Existing_Spine ∧
         review_action Topological_Locking = Merge_With_Existing_Spine ∧
         within_tolerance (elsasser_number magnetic_force coriolis_force) 1 (1/2) ∧
         flux_quantized (topological_locking_flux flux_quantum n) flux_quantum n"
proof (intro conjI)
  show "review_action Elsasser_Universality = Merge_With_Existing_Spine"
    by simp
  show "review_action Topological_Locking = Merge_With_Existing_Spine"
    by simp
  show "within_tolerance (elsasser_number magnetic_force coriolis_force) 1 (1/2)"
    using assms elsasser_merge_gives_unit_and_half_tolerance
    by blast
  show "flux_quantized (topological_locking_flux flux_quantum n) flux_quantum n"
    by (rule topological_locking_flux_is_quantized)
qed

text ‹
  Paper-facing meaning: the Topological Unification source strengthens existing
  lanes.  Elsasser universality is consumed by the MHD balance carrier, while
  topological locking is consumed by the flux-quantization carrier.  Neither
  merge requires a duplicate registry equation.
›

end
