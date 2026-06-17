theory TZPID_PaperXI_SoundBeforeLight
  imports Complex_Main "HOL-Analysis.Analysis"
begin

section \<open>Paper XI: Sound Before Light Carriers\<close>

text \<open>
  Source-truth carrier for missing equations minted from Paper XI,
  Sound Before Light. The theory fixes algebraic definitions and
  diagnostic constants; observational interpretation remains in the
  empirical certificate lane.
\<close>

definition pxi_baryon_loading :: "real => real => real => real" where
  "pxi_baryon_loading Omega_b Omega_gamma a = (3 * Omega_b / (4 * Omega_gamma)) * a"

definition pxi_sound_speed :: "real => real => real" where
  "pxi_sound_speed c Rb = c / sqrt (3 * (1 + Rb))"

definition pxi_precomb_H_sq :: "real => real => real => real => real => real" where
  "pxi_precomb_H_sq H0 Omega_r Omega_m Omega_L z =
     H0^2 * (Omega_r * (1 + z)^4 + Omega_m * (1 + z)^3 + Omega_L)"

definition pxi_neutrino_radiation :: "real => real => real" where
  "pxi_neutrino_radiation Omega_gamma N_eff = Omega_gamma * (1 + 0.2271 * N_eff)"

definition pxi_bao_node :: "real => real => real" where
  "pxi_bao_node k rs = k * rs"

definition pxi_bao_k1 :: "real => real" where
  "pxi_bao_k1 rs = pi / rs"

definition pxi_bao_delta_k :: "real => real" where
  "pxi_bao_delta_k rs = 2 * pi / rs"

definition pxi_registered_ids :: "nat list" where
  "pxi_registered_ids = [
  11536,
  11537,
  11538,
  11539,
  11540,
  11541,
  11542,
  11543,
  11544,
  11545,
  11546,
  11547,
  11548
  ]"

lemma pxi_baryon_loading_unfolds:
  "pxi_baryon_loading Omega_b Omega_gamma a = (3 * Omega_b / (4 * Omega_gamma)) * a"
  by (simp add: pxi_baryon_loading_def)

lemma pxi_sound_speed_unfolds:
  "pxi_sound_speed c Rb = c / sqrt (3 * (1 + Rb))"
  by (simp add: pxi_sound_speed_def)

lemma pxi_neutrino_radiation_unfolds:
  "pxi_neutrino_radiation Omega_gamma N_eff = Omega_gamma * (1 + 0.2271 * N_eff)"
  by (simp add: pxi_neutrino_radiation_def)

lemma pxi_bao_first_node_contract:
  assumes "k = pxi_bao_k1 rs" "rs \<noteq> 0"
  shows "pxi_bao_node k rs = pi"
  using assms by (simp add: pxi_bao_node_def pxi_bao_k1_def)

lemma pxi_delta_k_twice_k1:
  "pxi_bao_delta_k rs = 2 * pxi_bao_k1 rs"
  by (simp add: pxi_bao_delta_k_def pxi_bao_k1_def)

lemma pxi_registered_ids_nonempty:
  "pxi_registered_ids \<noteq> []"
  by (simp add: pxi_registered_ids_def)

end
