theory TZPID_FifthFlip_CrystalScaleInvariance
  imports
    TZPID_PhaseLockingResonance_Typed_RatioSelection
    TZPID_NestedHypersphere_S3_Spectrum
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  The "Fifth Is the Flip" bridge.  This theory records the algebraic
  core of the spine document:

    * rational phase-locking ratios close under reciprocal flip;
    * the golden ratio is the positive fixed point phi^2 = phi + 1;
    * its reciprocal is phi - 1;
    * the fivefold crystallographic trace lands in the open interval
      (0,1), so it is not one of the integer traces allowed for a
      periodic lattice rotation.

  The full crystallographic restriction theorem and KAM/most-irrational
  interpretation remain cited mathematical physics in the certificate.
  The HOL layer proves the exact algebra used by that interpretation.
\<close>

definition ff_reciprocal_flip :: "real \<Rightarrow> real" where
  "ff_reciprocal_flip r = 1 / r"

definition ff_golden_fixed_point :: "real \<Rightarrow> bool" where
  "ff_golden_fixed_point phi \<longleftrightarrow> 0 < phi \<and> phi\<^sup>2 = phi + 1"

definition ff_golden_trace :: "real \<Rightarrow> real" where
  "ff_golden_trace phi = 1 / phi"

definition ff_crystal_trace_admissible :: "real \<Rightarrow> bool" where
  "ff_crystal_trace_admissible trace \<longleftrightarrow>
    trace \<in> {-2, -1, 0, 1, 2}"

definition ff_rational_lock_ratio :: "real \<Rightarrow> bool" where
  "ff_rational_lock_ratio ratio \<longleftrightarrow>
    (\<exists>p q :: int. q \<noteq> 0 \<and> ratio = of_int p / of_int q)"

definition ff_scale_invariant_flip_hinge :: "real \<Rightarrow> bool" where
  "ff_scale_invariant_flip_hinge phi \<longleftrightarrow>
    ff_golden_fixed_point phi \<and>
    ff_reciprocal_flip phi = phi - 1 \<and>
    \<not> ff_crystal_trace_admissible (ff_golden_trace phi)"

lemma ff_reciprocal_flip_involutive:
  assumes "r \<noteq> 0"
  shows "ff_reciprocal_flip (ff_reciprocal_flip r) = r"
  unfolding ff_reciprocal_flip_def
  using assms
  by field

lemma ff_golden_fixed_point_nonzero:
  assumes "ff_golden_fixed_point phi"
  shows "phi \<noteq> 0"
  using assms
  unfolding ff_golden_fixed_point_def
  by linarith

lemma ff_golden_fixed_point_above_one:
  assumes "ff_golden_fixed_point phi"
  shows "1 < phi"
proof -
  have positive: "0 < phi"
    using assms
    unfolding ff_golden_fixed_point_def
    by blast
  have square_eq: "phi\<^sup>2 = phi + 1"
    using assms
    unfolding ff_golden_fixed_point_def
    by blast
  have "1 < phi\<^sup>2"
    using square_eq positive
    by linarith
  then show ?thesis
    using positive
    by (metis less_le real_le_lsqrt real_sqrt_one real_sqrt_power)
qed

lemma ff_golden_reciprocal_is_minus_one:
  assumes "ff_golden_fixed_point phi"
  shows "ff_reciprocal_flip phi = phi - 1"
proof -
  have nonzero: "phi \<noteq> 0"
    using assms
    by (rule ff_golden_fixed_point_nonzero)
  have square_eq: "phi\<^sup>2 = phi + 1"
    using assms
    unfolding ff_golden_fixed_point_def
    by blast
  show ?thesis
    unfolding ff_reciprocal_flip_def
    using nonzero square_eq
    by field
qed

lemma ff_golden_trace_open_unit_interval:
  assumes "ff_golden_fixed_point phi"
  shows "0 < ff_golden_trace phi \<and> ff_golden_trace phi < 1"
proof -
  have above_one: "1 < phi"
    using assms
    by (rule ff_golden_fixed_point_above_one)
  have positive: "0 < phi"
    using above_one
    by linarith
  have lower: "0 < 1 / phi"
    using positive
    by positivity
  have upper: "1 / phi < 1"
    using above_one positive
    by (metis divide_less_eq_1_pos less_irrefl zero_less_one)
  show ?thesis
    unfolding ff_golden_trace_def
    using lower upper
    by blast
qed

lemma ff_golden_trace_not_crystal_admissible:
  assumes "ff_golden_fixed_point phi"
  shows "\<not> ff_crystal_trace_admissible (ff_golden_trace phi)"
proof -
  have interval: "0 < ff_golden_trace phi \<and> ff_golden_trace phi < 1"
    using assms
    by (rule ff_golden_trace_open_unit_interval)
  show ?thesis
    unfolding ff_crystal_trace_admissible_def
    using interval
    by fastforce
qed

lemma ff_three_two_is_rational_lock_ratio:
  "ff_rational_lock_ratio (3 / 2)"
proof -
  have witness: "(3 / 2 :: real) = of_int 3 / of_int 2"
    by norm_num
  show ?thesis
    unfolding ff_rational_lock_ratio_def
    using witness
    by blast
qed

lemma ff_two_one_is_rational_lock_ratio:
  "ff_rational_lock_ratio 2"
proof -
  have witness: "(2 :: real) = of_int 2 / of_int 1"
    by norm_num
  show ?thesis
    unfolding ff_rational_lock_ratio_def
    using witness
    by blast
qed

lemma ff_rational_lock_closed_by_nonzero_flip:
  assumes "ff_rational_lock_ratio ratio"
    and "ratio \<noteq> 0"
  shows "ff_rational_lock_ratio (ff_reciprocal_flip ratio)"
proof -
  obtain p q :: int where q_nonzero: "q \<noteq> 0"
    and ratio_eq: "ratio = of_int p / of_int q"
    using assms(1)
    unfolding ff_rational_lock_ratio_def
    by blast
  have p_nonzero: "p \<noteq> 0"
    using assms(2) ratio_eq
    by force
  have flip_eq: "ff_reciprocal_flip ratio = of_int q / of_int p"
    unfolding ff_reciprocal_flip_def
    using ratio_eq p_nonzero q_nonzero
    by field
  show ?thesis
    unfolding ff_rational_lock_ratio_def
    using flip_eq p_nonzero
    by blast
qed

lemma ff_crystal_integer_traces_admissible:
  "ff_crystal_trace_admissible (-2)
    \<and> ff_crystal_trace_admissible (-1)
    \<and> ff_crystal_trace_admissible 0
    \<and> ff_crystal_trace_admissible 1
    \<and> ff_crystal_trace_admissible 2"
  unfolding ff_crystal_trace_admissible_def
  by blast

lemma ff_musical_fifth_flip_exact:
  "ff_reciprocal_flip (3 / 2) = 2 / 3"
  unfolding ff_reciprocal_flip_def
  by norm_num

theorem ff_golden_flip_hinge_contract:
  assumes "ff_golden_fixed_point phi"
  shows "ff_scale_invariant_flip_hinge phi
    \<and> ff_reciprocal_flip phi = phi - 1
    \<and> 0 < ff_golden_trace phi
    \<and> ff_golden_trace phi < 1
    \<and> \<not> ff_crystal_trace_admissible (ff_golden_trace phi)"
proof (intro conjI)
  show "ff_scale_invariant_flip_hinge phi"
    unfolding ff_scale_invariant_flip_hinge_def
    using assms ff_golden_reciprocal_is_minus_one
      ff_golden_trace_not_crystal_admissible
    by blast
  show "ff_reciprocal_flip phi = phi - 1"
    using assms
    by (rule ff_golden_reciprocal_is_minus_one)
  show "0 < ff_golden_trace phi"
    using assms ff_golden_trace_open_unit_interval
    by blast
  show "ff_golden_trace phi < 1"
    using assms ff_golden_trace_open_unit_interval
    by blast
  show "\<not> ff_crystal_trace_admissible (ff_golden_trace phi)"
    using assms
    by (rule ff_golden_trace_not_crystal_admissible)
qed

theorem ff_locking_and_golden_flip_bridge:
  assumes "ff_golden_fixed_point phi"
  shows "ff_rational_lock_ratio (3 / 2)
    \<and> ff_reciprocal_flip (3 / 2) = 2 / 3
    \<and> ff_rational_lock_ratio (ff_reciprocal_flip (3 / 2))
    \<and> ff_scale_invariant_flip_hinge phi"
proof (intro conjI)
  show "ff_rational_lock_ratio (3 / 2)"
    using ff_three_two_is_rational_lock_ratio .
  show "ff_reciprocal_flip (3 / 2) = 2 / 3"
    using ff_musical_fifth_flip_exact .
  show "ff_rational_lock_ratio (ff_reciprocal_flip (3 / 2))"
    using ff_three_two_is_rational_lock_ratio
    by (metis ff_rational_lock_closed_by_nonzero_flip nonzero_eq_divide_eq one_neq_zero zero_neq_numeral)
  show "ff_scale_invariant_flip_hinge phi"
    using assms ff_golden_flip_hinge_contract
    by blast
qed

context TZPID_NestedHypersphere_Focus
begin

theorem fifth_flip_extends_nested_hypersphere_spine:
  assumes "ff_golden_fixed_point phi"
  shows "nested_hypersphere_unifying_chain
    \<and> ff_rational_lock_ratio (3 / 2)
    \<and> ff_reciprocal_flip (3 / 2) = 2 / 3
    \<and> ff_scale_invariant_flip_hinge phi"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  show "ff_rational_lock_ratio (3 / 2)"
    using ff_three_two_is_rational_lock_ratio .
  show "ff_reciprocal_flip (3 / 2) = 2 / 3"
    using ff_musical_fifth_flip_exact .
  show "ff_scale_invariant_flip_hinge phi"
    using assms ff_golden_flip_hinge_contract
    by blast
qed

end

end
