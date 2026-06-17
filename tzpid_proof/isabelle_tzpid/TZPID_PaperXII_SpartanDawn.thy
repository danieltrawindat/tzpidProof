theory TZPID_PaperXII_SpartanDawn
  imports Complex_Main "HOL-Analysis.Analysis"
begin

section \<open>Paper XII: Spartan Dawn Test Carriers\<close>

text \<open>
  Source-truth carrier for missing model-comparison equations minted from
  Paper XII, The Spartan Dawn Test. The definitions formalize the data-trial
  algebra and diagnostics; empirical interpretation remains paper-facing.
\<close>

definition pxii_E2 :: "real => real => real => real => real => real => real" where
  "pxii_E2 z Omega_r Omega_m Omega_K Omega_X F =
    Omega_r * (1 + z)^4 + Omega_m * (1 + z)^3 + Omega_K * (1 + z)^2 + Omega_X * F"

definition pxii_Fz :: "real => real => real => real" where
  "pxii_Fz z w0 wa = (1 + z) powr (3 * (1 + w0 + wa)) * exp (-3 * wa * z / (1 + z))"

definition pxii_w_a :: "real => real => real => real" where
  "pxii_w_a w0 wa a = w0 + wa * (1 - a)"

definition pxii_closed_DM :: "real => real => real => real => real" where
  "pxii_closed_DM c H0 Omega_K DC = c / (H0 * sqrt (abs Omega_K)) * sin (sqrt (abs Omega_K) * H0 * DC / c)"

definition pxii_DH :: "real => real => real" where
  "pxii_DH c Hz = c / Hz"

definition pxii_DV_cubed :: "real => real => real => real => real" where
  "pxii_DV_cubed z DM DH = z * DM^2 * DH"

definition pxii_AIC :: "real => real => real" where
  "pxii_AIC chi2 k = chi2 + 2 * k"

definition pxii_redshift_drift :: "real => real => real => real" where
  "pxii_redshift_drift z H0 Hz = (1 + z) * H0 - Hz"

definition pxii_registered_ids :: "nat list" where
  "pxii_registered_ids = [
  11549,
  11550,
  11551,
  11552,
  11553,
  11554,
  11555,
  11556,
  11557,
  11558,
  11559,
  11560,
  11561,
  11562,
  11563,
  11564,
  11565,
  11566,
  11567,
  11568,
  11569,
  11570,
  11571,
  11572,
  11573,
  11574,
  11575
  ]"

lemma pxii_E2_unfolds:
  "pxii_E2 z Or Om Ok Ox F = Or * (1 + z)^4 + Om * (1 + z)^3 + Ok * (1 + z)^2 + Ox * F"
  by (simp add: pxii_E2_def)

lemma pxii_w_a_unfolds:
  "pxii_w_a w0 wa a = w0 + wa * (1 - a)"
  by (simp add: pxii_w_a_def)

lemma pxii_DH_unfolds:
  "pxii_DH c Hz = c / Hz"
  by (simp add: pxii_DH_def)

lemma pxii_DV_cubed_unfolds:
  "pxii_DV_cubed z DM DH = z * DM^2 * DH"
  by (simp add: pxii_DV_cubed_def)

lemma pxii_AIC_unfolds:
  "pxii_AIC chi2 k = chi2 + 2 * k"
  by (simp add: pxii_AIC_def)

lemma pxii_redshift_drift_unfolds:
  "pxii_redshift_drift z H0 Hz = (1 + z) * H0 - Hz"
  by (simp add: pxii_redshift_drift_def)

lemma pxii_AIC_flat_model_value:
  "pxii_AIC 16.13 2 = 20.13"
  by (simp add: pxii_AIC_def)

lemma pxii_registered_ids_nonempty:
  "pxii_registered_ids \<noteq> []"
  by (simp add: pxii_registered_ids_def)

end
