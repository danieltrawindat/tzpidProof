theory TZPID_SpartanStandingWave_Expansion
  imports Complex_Main "HOL-Analysis.Analysis"
begin

section \<open>Spartan Standing-Wave Expansion Carriers\<close>

text \<open>
  Source-truth carrier for equations minted from standing_wave_expaansion.txt
  and TZPID_SPARTAN_DAWN_CMB_BAO_SNE_TEST.md. These definitions formalize
  algebraic and semantic proof obligations; empirical fit claims remain in
  the computational certificate lane.
\<close>

definition sse_H :: "real => real => real" where
  "sse_H Rdot R = Rdot / R"

definition sse_distance :: "real => real => real" where
  "sse_distance R chi = R * chi"

definition sse_superluminal_metric :: "real => real => real => bool" where
  "sse_superluminal_metric D c H = (D > c / H)"

definition sse_bessel_node :: "real => real => real => real" where
  "sse_bessel_node a x01 k = a * x01 / k"

definition sse_scale_jump :: "real => real => real" where
  "sse_scale_jump N a1 = N * a1"

definition sse_inflation_scale :: "real => real => real => real => real" where
  "sse_inflation_scale ai Hinf t ti = ai * exp (Hinf * (t - ti))"

definition sse_efolds :: "real => real => real" where
  "sse_efolds af ai = ln (af / ai)"

definition sse_sound_speed :: "real => real => real" where
  "sse_sound_speed c Rb = c / sqrt (3 * (1 + Rb))"

definition sse_baryon_loading :: "real => real => real" where
  "sse_baryon_loading rho_b rho_gamma = 3 * rho_b / (4 * rho_gamma)"

definition sse_node_velocity :: "real => real => real" where
  "sse_node_velocity H r = H * r"

definition sse_sn_breathing_rate :: "nat => real => real" where
  "sse_sn_breathing_rate n H = real n * H"

definition sse_sn_mode_freq :: "nat => nat => real => real => real" where
  "sse_sn_mode_freq n ell cs R = cs / R * sqrt (real ell * (real ell + real n - 1))"

definition sse_dimensional_bessel_order :: "real => real" where
  "sse_dimensional_bessel_order n = n / 2 - 1"

definition sse_s4_visible_radius :: "real => real => real" where
  "sse_s4_visible_radius R4 alpha = R4 * sin alpha"

definition sse_s4_observed_H :: "real => real => real => real" where
  "sse_s4_observed_H H4 alpha_dot alpha = H4 + alpha_dot * cot alpha"

definition sse_s5_visible_radius :: "real => real => real => real" where
  "sse_s5_visible_radius R5 beta alpha = R5 * sin beta * sin alpha"

definition sse_s5_observed_H :: "real => real => real => real => real => real" where
  "sse_s5_observed_H H5 beta_dot beta alpha_dot alpha = H5 + beta_dot * cot beta + alpha_dot * cot alpha"

definition sse_hidden_dispersion :: "real => real => real => real => real" where
  "sse_hidden_dispersion cs k3 kalpha kbeta = cs^2 * (k3^2 + kalpha^2 + kbeta^2)"

definition sse_visible_wavelength :: "real => real" where
  "sse_visible_wavelength k3 = 2 * pi / k3"

definition sse_projected_phase_speed :: "real => real => real => real => real" where
  "sse_projected_phase_speed cs kalpha kbeta k3 = cs * sqrt (1 + (kalpha^2 + kbeta^2) / k3^2)"

definition sse_projected_node_radius :: "real => real => real => real => real => real" where
  "sse_projected_node_radius R5 beta alpha jnu m = R5 * sin beta * sin alpha * jnu / sqrt (m * (m + 2))"

definition sse_closed_curvature_radius :: "real => real => real => real" where
  "sse_closed_curvature_radius c H0 OmegaK = c / (H0 * sqrt (abs OmegaK))"

definition sse_cpl_w :: "real => real => real => real" where
  "sse_cpl_w w0 wa a = w0 + wa * (1 - a)"

definition sse_redshift_drift :: "real => real => real => real" where
  "sse_redshift_drift z H0 Hz = (1 + z) * H0 - Hz"

definition sse_neutrino_corrected_radiation :: "real => real => real" where
  "sse_neutrino_corrected_radiation Omega_gamma N_eff = Omega_gamma * (1 + 0.2271 * N_eff)"

definition sse_registered_ids :: "nat list" where
  "sse_registered_ids = [
  11433,
  11434,
  11435,
  11436,
  11437,
  11438,
  11439,
  11440,
  11441,
  11442,
  11443,
  11444,
  11445,
  11446,
  11447,
  11448,
  11449,
  11450,
  11451,
  11452,
  11453,
  11454,
  11455,
  11456,
  11457,
  11458,
  11459,
  11460,
  11461,
  11462,
  11463,
  11464,
  11465,
  11466,
  11467,
  11468,
  11469,
  11470,
  11471,
  11472,
  11473,
  11474,
  11475,
  11476,
  11477,
  11478,
  11479,
  11480,
  11481,
  11482,
  11483,
  11484,
  11485,
  11486,
  11487,
  11488,
  11489,
  11490,
  11491,
  11492,
  11493,
  11494,
  11495,
  11496,
  11497,
  11498,
  11499,
  11500,
  11501,
  11502,
  11503,
  11504,
  11505,
  11506,
  11507,
  11508,
  11509,
  11510,
  11511,
  11512,
  11513,
  11514,
  11515,
  11516,
  11517,
  11518,
  11519,
  11520,
  11521,
  11522,
  11523,
  11524,
  11525,
  11526,
  11527,
  11528,
  11529,
  11530,
  11531,
  11532,
  11533,
  11534,
  11535
  ]"

lemma sse_hubble_breathing_unfolds:
  "sse_H Rdot R = Rdot / R"
  by (simp add: sse_H_def)

lemma sse_distance_unfolds:
  "sse_distance R chi = R * chi"
  by (simp add: sse_distance_def)

lemma sse_node_scale_jump:
  "sse_bessel_node (sse_scale_jump N a1) x01 k = N * sse_bessel_node a1 x01 k"
  by (simp add: sse_bessel_node_def sse_scale_jump_def algebra_simps)

lemma sse_sn_breathing_rate_345:
  "sse_sn_breathing_rate 3 H = 3 * H \<and> sse_sn_breathing_rate 4 H = 4 * H \<and> sse_sn_breathing_rate 5 H = 5 * H"
  by (simp add: sse_sn_breathing_rate_def)

lemma sse_bessel_order_examples:
  "sse_dimensional_bessel_order 3 = 1/2 \<and> sse_dimensional_bessel_order 4 = 1 \<and> sse_dimensional_bessel_order 5 = 3/2"
  by (simp add: sse_dimensional_bessel_order_def)

lemma sse_hidden_dispersion_unfolds:
  "sse_hidden_dispersion cs k3 kalpha kbeta = cs^2 * (k3^2 + kalpha^2 + kbeta^2)"
  by (simp add: sse_hidden_dispersion_def)

lemma sse_s5_observed_H_unfolds:
  "sse_s5_observed_H H5 beta_dot beta alpha_dot alpha = H5 + beta_dot * cot beta + alpha_dot * cot alpha"
  by (simp add: sse_s5_observed_H_def)

lemma sse_redshift_drift_unfolds:
  "sse_redshift_drift z H0 Hz = (1 + z) * H0 - Hz"
  by (simp add: sse_redshift_drift_def)

lemma sse_registered_ids_nonempty:
  "sse_registered_ids \<noteq> []"
  by (simp add: sse_registered_ids_def)

end

