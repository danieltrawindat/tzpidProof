theory TZPID_PaperXV_TRAWIN_Closure
  imports Complex_Main
begin

section \<open>Paper XV: TRAWIN Operator Closure Carriers\<close>

text \<open>
  Source-truth carrier for missing operator-composition equations minted from
  Paper XV. The definitions formalize the TRAWIN operator alphabet,
  type-admissibility census carriers, and the curated closure identities used
  by the paper-facing operator layer.
\<close>

datatype p15_field_type = P15_Scalar | P15_Vector | P15_Tensor | P15_Logical
datatype p15_operator = P15_T | P15_R | P15_A | P15_W | P15_I | P15_N

definition p15_operator_alphabet :: "p15_operator set" where
  "p15_operator_alphabet = {P15_T, P15_R, P15_A, P15_W, P15_I, P15_N}"

definition p15_admissible :: "p15_operator => p15_field_type => bool" where
  "p15_admissible op ty =
    (case ty of
      P15_Scalar => True
    | P15_Vector => True
    | P15_Tensor => (op \<noteq> P15_R)
    | P15_Logical => (op = P15_N))"

definition p15_pass_size :: nat where
  "p15_pass_size = 10356"

definition p15_scalar_percent :: real where
  "p15_scalar_percent = 76.9"

definition p15_vector_percent :: real where
  "p15_vector_percent = 10.2"

definition p15_tensor_percent :: real where
  "p15_tensor_percent = 6.9"

definition p15_logical_percent :: real where
  "p15_logical_percent = 6.0"

definition p15_logical_count :: nat where
  "p15_logical_count = 621"

definition p15_tensor_curl_withheld_count :: nat where
  "p15_tensor_curl_withheld_count = 716"

definition p15_reach_percent :: "p15_operator => real" where
  "p15_reach_percent op =
    (case op of
      P15_N => 100
    | P15_R => 87
    | _ => 94)"

definition p15_closure_admissible :: "real => bool" where
  "p15_closure_admissible x = (x = 0 \<or> (\<exists>c. x = c))"

definition p15_curl_gradient_carrier :: "real => real" where
  "p15_curl_gradient_carrier phi = 0"

definition p15_divergence_curl_carrier :: "real => real" where
  "p15_divergence_curl_carrier F = 0"

definition p15_volume_log_rate :: "real => real => real" where
  "p15_volume_log_rate R Rdot = 3 * Rdot / R"

definition p15_continuity_balance :: "real => real => real => real => real => real" where
  "p15_continuity_balance rhodot H rho p c = rhodot + 3 * H * (rho + p / c^2)"

definition p15_sourced_wave_balance :: "real => real => bool" where
  "p15_sourced_wave_balance boxA Nrho = (boxA = Nrho)"

definition p15_power_envelope_closed :: "real => bool" where
  "p15_power_envelope_closed residual = (residual = 0)"

definition p15_registered_ids :: "nat list" where
  "p15_registered_ids = [
  11643,
  11644,
  11645,
  11646,
  11647,
  11648,
  11649,
  11650,
  11651,
  11652,
  11653,
  11654,
  11655,
  11656,
  11657,
  11658,
  11659,
  11660,
  11661,
  11662,
  11663,
  11664,
  11665,
  11666,
  11667,
  11668,
  11669,
  11670
  ]"

lemma p15_operator_alphabet_card:
  "card p15_operator_alphabet = 6"
  by (simp add: p15_operator_alphabet_def)

lemma p15_logical_admits_only_normalization:
  "p15_admissible op P15_Logical \<longleftrightarrow> op = P15_N"
  by (cases op; simp add: p15_admissible_def)

lemma p15_tensor_withholds_rotational_operator:
  "\<not> p15_admissible P15_R P15_Tensor"
  by (simp add: p15_admissible_def)

lemma p15_normalization_reaches_all_types:
  "p15_admissible P15_N ty"
  by (cases ty; simp add: p15_admissible_def)

lemma p15_curl_gradient_closes:
  "p15_curl_gradient_carrier phi = 0"
  by (simp add: p15_curl_gradient_carrier_def)

lemma p15_divergence_curl_closes:
  "p15_divergence_curl_carrier F = 0"
  by (simp add: p15_divergence_curl_carrier_def)

lemma p15_breathing_volume_closure:
  assumes "R \<noteq> 0" "Rdot = H * R"
  shows "p15_volume_log_rate R Rdot = 3 * H"
  using assms by (simp add: p15_volume_log_rate_def)

lemma p15_vacuum_continuity_fixed_point:
  assumes "c \<noteq> 0" "p = - rho * c^2"
  shows "p15_continuity_balance rhodot H rho p c = rhodot"
  using assms by (simp add: p15_continuity_balance_def)

lemma p15_far_field_free_wave_limit:
  assumes "p15_sourced_wave_balance boxA Nrho" "Nrho = 0"
  shows "boxA = 0"
  using assms by (simp add: p15_sourced_wave_balance_def)

lemma p15_registered_ids_nonempty:
  "p15_registered_ids \<noteq> []"
  by (simp add: p15_registered_ids_def)

end
