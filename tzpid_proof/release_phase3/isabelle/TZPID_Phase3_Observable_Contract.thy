theory TZPID_Phase3_Observable_Contract
  imports TZPID_Bessel_External_Certificates
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T03:45:00Z

  Phase3 observable contract for the Delta-alpha HDF5 shell comparison.
  The numerical shell extraction is performed by the Python certificate:

    phase2_checks/delta_alpha_phase3_field_psi_real_slice_0/
      delta_alpha_shell_comparison.json

  Isabelle records the contract boundary: which observable was certified,
  which shell radii were predicted and observed, and that both observed
  radii fall within the declared relative tolerance.
\<close>

definition phase3_hdf5_file :: string where
  "phase3_hdf5_file = ''delta_alpha_phase3.h5''"

definition phase3_shell_dataset :: string where
  "phase3_shell_dataset = ''field/psi_real''"

definition phase3_shell_slice :: nat where
  "phase3_shell_slice = 0"

definition phase3_detected_peak_count :: nat where
  "phase3_detected_peak_count = 75"

definition phase3_predicted_shell_count :: nat where
  "phase3_predicted_shell_count = 2"

definition phase3_relative_tolerance :: real where
  "phase3_relative_tolerance = 11 / 1000"

definition phase3_predicted_shell_1 :: real where
  "phase3_predicted_shell_1 = 6437903504411578 / 10000000000000000"

definition phase3_observed_shell_1 :: real where
  "phase3_observed_shell_1 = 650349046241808 / 1000000000000000"

definition phase3_predicted_shell_2 :: real where
  "phase3_predicted_shell_2 = 12875807008823157 / 10000000000000000"

definition phase3_observed_shell_2 :: real where
  "phase3_observed_shell_2 = 12888735643701286 / 10000000000000000"

definition phase3_max_absolute_error :: real where
  "phase3_max_absolute_error = 65586958006501606 / 10000000000000000000"

definition shell_match_within_relative_tolerance :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "shell_match_within_relative_tolerance predicted observed tolerance =
     (0 < predicted \<and> abs (observed - predicted) / predicted \<le> tolerance)"

definition phase3_hdf5_observable :: "string \<Rightarrow> string \<Rightarrow> nat \<Rightarrow> bool" where
  "phase3_hdf5_observable file dataset slice =
     (file = phase3_hdf5_file
      \<and> dataset = phase3_shell_dataset
      \<and> slice = phase3_shell_slice)"

definition phase3_shell_bearing_observable :: "string \<Rightarrow> string \<Rightarrow> nat \<Rightarrow> bool" where
  "phase3_shell_bearing_observable file dataset slice =
     (phase3_hdf5_observable file dataset slice
      \<and> 0 < phase3_detected_peak_count
      \<and> phase3_predicted_shell_count = 2)"

definition phase3_bessel_shell_prediction_validated :: bool where
  "phase3_bessel_shell_prediction_validated =
     (shell_match_within_relative_tolerance
        phase3_predicted_shell_1 phase3_observed_shell_1 phase3_relative_tolerance
      \<and> shell_match_within_relative_tolerance
        phase3_predicted_shell_2 phase3_observed_shell_2 phase3_relative_tolerance)"

theorem phase3_shell_1_within_relative_tolerance:
  "shell_match_within_relative_tolerance
     phase3_predicted_shell_1 phase3_observed_shell_1 phase3_relative_tolerance"
  unfolding shell_match_within_relative_tolerance_def
    phase3_predicted_shell_1_def phase3_observed_shell_1_def
    phase3_relative_tolerance_def
  by norm_num

theorem phase3_shell_2_within_relative_tolerance:
  "shell_match_within_relative_tolerance
     phase3_predicted_shell_2 phase3_observed_shell_2 phase3_relative_tolerance"
  unfolding shell_match_within_relative_tolerance_def
    phase3_predicted_shell_2_def phase3_observed_shell_2_def
    phase3_relative_tolerance_def
  by norm_num

theorem phase3_hdf5_shell_observable_is_bearing:
  "phase3_shell_bearing_observable
     ''delta_alpha_phase3.h5'' ''field/psi_real'' 0"
  unfolding phase3_shell_bearing_observable_def phase3_hdf5_observable_def
    phase3_hdf5_file_def phase3_shell_dataset_def phase3_shell_slice_def
    phase3_detected_peak_count_def phase3_predicted_shell_count_def
  by norm_num

theorem phase3_bessel_shell_prediction_certificate:
  "phase3_bessel_shell_prediction_validated"
  unfolding phase3_bessel_shell_prediction_validated_def
  using phase3_shell_1_within_relative_tolerance
    phase3_shell_2_within_relative_tolerance
  by blast

theorem phase3_observable_contract_locked:
  "phase3_shell_bearing_observable
      ''delta_alpha_phase3.h5'' ''field/psi_real'' 0
   \<and> phase3_bessel_shell_prediction_validated
   \<and> phase3_max_absolute_error \<le> (7 / 1000 :: real)"
proof (intro conjI)
  show "phase3_shell_bearing_observable
      ''delta_alpha_phase3.h5'' ''field/psi_real'' 0"
    using phase3_hdf5_shell_observable_is_bearing .
  show "phase3_bessel_shell_prediction_validated"
    using phase3_bessel_shell_prediction_certificate .
  show "phase3_max_absolute_error \<le> (7 / 1000 :: real)"
    unfolding phase3_max_absolute_error_def
    by norm_num
qed

end
