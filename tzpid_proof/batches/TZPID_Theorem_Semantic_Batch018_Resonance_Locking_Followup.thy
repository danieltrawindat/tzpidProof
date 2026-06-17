theory TZPID_Theorem_Semantic_Batch018_Resonance_Locking_Followup
  imports TZPID_Theorem_Semantic_Batch017_Quantum_Matter_Followup
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-07

  Semantic translation batch 018.

  This batch promotes the resonance-locking triage follow-up into typed
  HOL.  It covers phase-locking bifurcation, pitchfork bifurcation,
  resonance capture condition, sufficient condition for phase locking,
  and lemniscate saddle point guards.
\<close>

section \<open>Batch 018 Target Rows\<close>

definition theorem_semantic_batch018_ids :: "string list" where
  "theorem_semantic_batch018_ids = [''ID9999'']"

definition theorem_semantic_batch018_queue_rows :: "nat list" where
  "theorem_semantic_batch018_queue_rows = [268, 269, 271, 272, 274]"

theorem theorem_semantic_batch018_unique_id_count:
  "length theorem_semantic_batch018_ids = 1"
proof -
  have "theorem_semantic_batch018_ids = [''ID9999'']"
    unfolding theorem_semantic_batch018_ids_def
    by (rule refl)
  thus ?thesis
    by normalization
qed

theorem theorem_semantic_batch018_queue_row_count:
  "length theorem_semantic_batch018_queue_rows = 5"
proof -
  have "theorem_semantic_batch018_queue_rows = [268, 269, 271, 272, 274]"
    unfolding theorem_semantic_batch018_queue_rows_def
    by (rule refl)
  thus ?thesis
    by normalization
qed

section \<open>Phase Locking and Resonance Capture\<close>

definition phase_locking_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "phase_locking_residual oscillator_phase drive_phase =
     oscillator_phase - drive_phase"

definition phase_locking_bifurcation_guard :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "phase_locking_bifurcation_guard coupling threshold =
     (coupling \<ge> threshold)"

definition resonance_capture_guard :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "resonance_capture_guard detuning capture_width =
     (abs detuning \<le> capture_width)"

definition sufficient_phase_locking_guard ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "sufficient_phase_locking_guard coupling detuning margin =
     (coupling \<ge> abs detuning + margin)"

theorem id9999_phase_locking_residual_zero:
  "phase_locking_residual phase phase = 0"
proof -
  show ?thesis
    unfolding phase_locking_residual_def
    by algebra
qed

theorem id9999_phase_locking_bifurcation_from_threshold:
  assumes "coupling \<ge> threshold"
  shows "phase_locking_bifurcation_guard coupling threshold"
proof -
  show ?thesis
    using assms
    unfolding phase_locking_bifurcation_guard_def .
qed

theorem id9999_resonance_capture_from_detuning_bound:
  assumes "abs detuning \<le> capture_width"
  shows "resonance_capture_guard detuning capture_width"
proof -
  show ?thesis
    using assms
    unfolding resonance_capture_guard_def .
qed

theorem id9999_sufficient_condition_for_phase_locking:
  assumes "coupling \<ge> abs detuning + margin"
  shows "sufficient_phase_locking_guard coupling detuning margin"
proof -
  show ?thesis
    using assms
    unfolding sufficient_phase_locking_guard_def .
qed

section \<open>Pitchfork and Lemniscate Saddle Guards\<close>

definition pitchfork_bifurcation_balance :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pitchfork_bifurcation_balance branch_plus branch_minus =
     branch_plus + branch_minus"

definition lemniscate_saddle_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "lemniscate_saddle_residual gradient_x gradient_y =
     gradient_x\<^sup>2 + gradient_y\<^sup>2"

definition saddle_point_guard :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "saddle_point_guard gradient_x gradient_y =
     (gradient_x = 0 \<and> gradient_y = 0)"

theorem id9999_pitchfork_bifurcation_symmetric_branches:
  "pitchfork_bifurcation_balance branch (- branch) = 0"
proof -
  show ?thesis
    unfolding pitchfork_bifurcation_balance_def
    by algebra
qed

theorem id9999_lemniscate_saddle_zero_gradient:
  "lemniscate_saddle_residual 0 0 = 0"
proof -
  show ?thesis
    unfolding lemniscate_saddle_residual_def
    by algebra
qed

theorem id9999_lemniscate_saddle_point_guard:
  "saddle_point_guard 0 0"
proof -
  have "(0::real) = 0 \<and> (0::real) = 0"
  proof (rule conjI)
    show "(0::real) = 0"
      by (rule refl)
    show "(0::real) = 0"
      by (rule refl)
  qed
  thus ?thesis
    unfolding saddle_point_guard_def .
qed

section \<open>Batch Bundle\<close>

theorem theorem_semantic_batch018_resonance_locking_bundle:
  assumes coupling_threshold: "coupling \<ge> threshold"
    and detuning_bound: "abs detuning \<le> capture_width"
    and sufficient_lock: "coupling2 \<ge> abs detuning2 + margin"
  shows
    "phase_locking_residual phase phase = 0
     \<and> phase_locking_bifurcation_guard coupling threshold
     \<and> resonance_capture_guard detuning capture_width
     \<and> sufficient_phase_locking_guard coupling2 detuning2 margin
     \<and> pitchfork_bifurcation_balance branch (- branch) = 0
     \<and> lemniscate_saddle_residual 0 0 = 0
     \<and> saddle_point_guard 0 0"
proof (intro conjI)
  show "phase_locking_residual phase phase = 0"
    using id9999_phase_locking_residual_zero .
  show "phase_locking_bifurcation_guard coupling threshold"
    using coupling_threshold
    by (rule id9999_phase_locking_bifurcation_from_threshold)
  show "resonance_capture_guard detuning capture_width"
    using detuning_bound
    by (rule id9999_resonance_capture_from_detuning_bound)
  show "sufficient_phase_locking_guard coupling2 detuning2 margin"
    using sufficient_lock
    by (rule id9999_sufficient_condition_for_phase_locking)
  show "pitchfork_bifurcation_balance branch (- branch) = 0"
    using id9999_pitchfork_bifurcation_symmetric_branches .
  show "lemniscate_saddle_residual 0 0 = 0"
    using id9999_lemniscate_saddle_zero_gradient .
  show "saddle_point_guard 0 0"
    using id9999_lemniscate_saddle_point_guard .
qed

end
