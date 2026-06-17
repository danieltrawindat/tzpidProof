theory TZPID_PapersXI_XV_VerificationSuite
  imports
    TZPID_PaperXI_SoundBeforeLight
    TZPID_PaperXII_SpartanDawn
    TZPID_PaperXIII_S3_S4_S5_Geometry
    TZPID_PaperXIV_NestedShell_BAO
    TZPID_PaperXV_TRAWIN_Closure
begin

section \<open>Papers XI-XV Verification Suite\<close>

text \<open>
  Consolidated certificate layer for Papers XI-XV.  The individual paper
  theories provide source-truth carriers.  This suite checks cross-paper
  compatibility: BAO definitions, nested-shell mode ratios, S3/S4/S5
  degeneracies, breathing/continuity closure, and registry-ID coverage.
\<close>

definition p11_p15_registered_ids :: "nat list" where
  "p11_p15_registered_ids =
    pxi_registered_ids @
    pxii_registered_ids @
    p13_registered_ids @
    p14_registered_ids @
    p15_registered_ids"

lemma p11_p15_registered_count:
  "length p11_p15_registered_ids = 135"
  unfolding p11_p15_registered_ids_def
    pxi_registered_ids_def pxii_registered_ids_def p13_registered_ids_def
    p14_registered_ids_def p15_registered_ids_def
  by eval

lemma p11_p15_registered_first_last:
  "hd p11_p15_registered_ids = 11536 \<and> last p11_p15_registered_ids = 11670"
  unfolding p11_p15_registered_ids_def
    pxi_registered_ids_def pxii_registered_ids_def p13_registered_ids_def
    p14_registered_ids_def p15_registered_ids_def
  by eval

theorem p11_p14_bao_period_alignment:
  "pxi_bao_delta_k rs = p14_bao_period rs"
proof -
  have xi: "pxi_bao_delta_k rs = 2 * pi / rs"
    by (simp add: pxi_bao_delta_k_def)
  have xiv: "p14_bao_period rs = 2 * pi / rs"
    by (simp add: p14_bao_period_def)
  from xi xiv show ?thesis
    by simp
qed

theorem p11_p14_modes_per_wiggle_alignment:
  assumes "rs \<noteq> 0" and "Rc \<noteq> 0"
  shows "pxi_bao_delta_k rs / p14_mode_spacing Rc = p14_modes_per_wiggle Rc rs"
proof -
  have period: "pxi_bao_delta_k rs = p14_bao_period rs"
    by (rule p11_p14_bao_period_alignment)
  have ratio: "p14_bao_period rs / p14_mode_spacing Rc = p14_modes_per_wiggle Rc rs"
    using assms by (rule p14_bao_over_mode_spacing)
  from period ratio show ?thesis
    by simp
qed

theorem p13_p14_s3_degeneracy_alignment:
  "p14_s3_degeneracy ell = p13_s3_degeneracy ell"
proof -
  have a: "p14_s3_degeneracy ell = (ell + 1)^2"
    by (simp add: p14_s3_degeneracy_def)
  have b: "p13_s3_degeneracy ell = (ell + 1)^2"
    by (simp add: p13_s3_degeneracy_def)
  from a b show ?thesis
    by simp
qed

theorem p13_p14_s4_degeneracy_alignment:
  "p14_s4_degeneracy ell = p13_s4_degeneracy ell"
proof -
  have a: "p14_s4_degeneracy ell = ((ell + 1) * (ell + 2) * (2 * ell + 3)) / 6"
    by (simp add: p14_s4_degeneracy_def)
  have b: "p13_s4_degeneracy ell = ((ell + 1) * (ell + 2) * (2 * ell + 3)) / 6"
    by (simp add: p13_s4_degeneracy_def)
  from a b show ?thesis
    by simp
qed

theorem p13_p14_s5_degeneracy_alignment:
  "p14_s5_degeneracy ell = p13_s5_degeneracy ell"
proof -
  have a: "p14_s5_degeneracy ell = ((ell + 1) * (ell + 2)^2 * (ell + 3)) / 12"
    by (simp add: p14_s5_degeneracy_def)
  have b: "p13_s5_degeneracy ell = ((ell + 1) * (ell + 2)^2 * (ell + 3)) / 12"
    by (simp add: p13_s5_degeneracy_def)
  from a b show ?thesis
    by simp
qed

theorem p13_p15_breathing_closure_alignment:
  assumes "R \<noteq> 0" and "Rdot = H * R"
  shows "p15_volume_log_rate R Rdot = p13_volume_rate 3 H"
proof -
  have xv: "p15_volume_log_rate R Rdot = 3 * H"
    using assms by (rule p15_breathing_volume_closure)
  have xiii: "p13_volume_rate 3 H = 3 * H"
    by (simp add: p13_volume_rate_def)
  from xv xiii show ?thesis
    by simp
qed

theorem p13_p15_vacuum_continuity_alignment:
  assumes "c \<noteq> 0" and "p = - rho * c^2"
  shows "p13_continuity_balance rhodot 3 H rho p c =
         p15_continuity_balance rhodot H rho p c"
proof -
  have xiii: "p13_continuity_balance rhodot 3 H rho p c = rhodot"
    using assms by (simp add: p13_continuity_balance_def)
  have xv: "p15_continuity_balance rhodot H rho p c = rhodot"
    using assms by (rule p15_vacuum_continuity_fixed_point)
  from xiii xv show ?thesis
    by simp
qed

theorem p12_aic_is_closed_arithmetic:
  "pxii_AIC chi2 k = chi2 + 2 * k"
proof -
  have defn: "pxii_AIC chi2 k = chi2 + 2 * k"
    by (simp add: pxii_AIC_def)
  from defn show ?thesis .
qed

theorem p15_operator_layer_is_sixfold:
  "card p15_operator_alphabet = 6"
proof -
  show ?thesis
    by (rule p15_operator_alphabet_card)
qed

theorem p11_p15_suite_nonempty_and_ordered:
  "p11_p15_registered_ids \<noteq> [] \<and>
   length p11_p15_registered_ids = 135 \<and>
   hd p11_p15_registered_ids = 11536 \<and>
   last p11_p15_registered_ids = 11670"
  using p11_p15_registered_count p11_p15_registered_first_last
  by auto

end
