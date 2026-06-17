theory TZPID_Ripple_LogPeriodic_PhiBridge
  imports
    TZPID_FifthFlip_CrystalScaleInvariance
    TZPID_Phase2_Semantic_Translation
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Ripple/log-periodic phi bridge.

  This checkpoint closes the handoff named in the Phase 2 matrix:
  fifth-flip phi-inflation is lifted into the ripple/log-periodic
  scale-invariance lane.  The formal content is intentionally algebraic:

    * the golden reciprocal alpha = 1 / phi is a valid inward contraction;
    * projected shell radii form a geometric/log-periodic sequence;
    * each successor shell has ratio alpha;
    * the ordinary ripple index wavelength/height is preserved under every
      common projection scale alpha^k.

  The accompanying Python certificate samples the same identities numerically.
\<close>

definition rp_phi_contraction :: "real \<Rightarrow> real" where
  "rp_phi_contraction phi = ff_golden_trace phi"

definition rp_phi_projected_wavelength :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> real" where
  "rp_phi_projected_wavelength phi wavelength k =
    projected_length ((rp_phi_contraction phi) ^ k) wavelength"

definition rp_phi_projected_height :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> real" where
  "rp_phi_projected_height phi height k =
    projected_length ((rp_phi_contraction phi) ^ k) height"

definition rp_phi_log_periodic_bridge :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "rp_phi_log_periodic_bridge phi base_radius wavelength \<longleftrightarrow>
    ff_golden_fixed_point phi
    \<and> hs_inward_hopf_contraction (rp_phi_contraction phi)
    \<and> base_radius \<noteq> 0
    \<and> wavelength \<noteq> 0"

lemma rp_phi_contraction_equals_reciprocal:
  assumes "ff_golden_fixed_point phi"
  shows "rp_phi_contraction phi = 1 / phi"
proof -
  show ?thesis
    unfolding rp_phi_contraction_def ff_golden_trace_def .
qed

lemma rp_phi_contraction_is_inward:
  assumes "ff_golden_fixed_point phi"
  shows "hs_inward_hopf_contraction (rp_phi_contraction phi)"
proof -
  have interval: "0 < ff_golden_trace phi \<and> ff_golden_trace phi < 1"
    using assms
    by (rule ff_golden_trace_open_unit_interval)
  show ?thesis
    unfolding rp_phi_contraction_def hs_inward_hopf_contraction_def
    using interval
    by blast
qed

lemma rp_phi_shell_successor_ratio:
  assumes "ff_golden_fixed_point phi"
    and "base_radius \<noteq> 0"
  shows "hs_projected_log_periodic_shell (rp_phi_contraction phi)
      base_radius (Suc k) /
    hs_projected_log_periodic_shell (rp_phi_contraction phi)
      base_radius k =
    rp_phi_contraction phi"
proof -
  have inward: "hs_inward_hopf_contraction (rp_phi_contraction phi)"
    using assms(1)
    by (rule rp_phi_contraction_is_inward)
  have alpha_nonzero: "rp_phi_contraction phi \<noteq> 0"
    using inward
    unfolding hs_inward_hopf_contraction_def
    by linarith
  show ?thesis
    using assms(2) alpha_nonzero
    by (rule hs_projected_log_periodic_shell_successor_ratio)
qed

lemma rp_phi_projection_scale_nonzero:
  assumes "ff_golden_fixed_point phi"
  shows "(rp_phi_contraction phi) ^ k \<noteq> 0"
proof -
  have inward: "hs_inward_hopf_contraction (rp_phi_contraction phi)"
    using assms
    by (rule rp_phi_contraction_is_inward)
  have alpha_nonzero: "rp_phi_contraction phi \<noteq> 0"
    using inward
    unfolding hs_inward_hopf_contraction_def
    by linarith
  show ?thesis
    using alpha_nonzero
    by (metis power_eq_0_iff)
qed

lemma rp_phi_ripple_index_scale_invariant:
  assumes "ff_golden_fixed_point phi"
  shows "ripple_index
      (rp_phi_projected_wavelength phi wavelength k)
      (rp_phi_projected_height phi height k) =
    ripple_index wavelength height"
proof -
  have nonzero: "(rp_phi_contraction phi) ^ k \<noteq> 0"
    using assms
    by (rule rp_phi_projection_scale_nonzero)
  show ?thesis
    unfolding rp_phi_projected_wavelength_def
      rp_phi_projected_height_def
    using nonzero
    by (rule ripple_projection_semantics_matches_existing_index)
qed

theorem rp_phi_log_periodic_ripple_bridge_contract:
  assumes "ff_golden_fixed_point phi"
    and "base_radius \<noteq> 0"
  shows "hs_inward_hopf_contraction (rp_phi_contraction phi)
    \<and> hs_projected_log_periodic_shell (rp_phi_contraction phi)
        base_radius (Suc k) /
      hs_projected_log_periodic_shell (rp_phi_contraction phi)
        base_radius k =
      rp_phi_contraction phi
    \<and> ripple_index
        (rp_phi_projected_wavelength phi wavelength k)
        (rp_phi_projected_height phi height k) =
      ripple_index wavelength height"
proof (intro conjI)
  show "hs_inward_hopf_contraction (rp_phi_contraction phi)"
    using assms(1)
    by (rule rp_phi_contraction_is_inward)
  show "hs_projected_log_periodic_shell (rp_phi_contraction phi)
      base_radius (Suc k) /
    hs_projected_log_periodic_shell (rp_phi_contraction phi)
      base_radius k =
    rp_phi_contraction phi"
    using assms
    by (rule rp_phi_shell_successor_ratio)
  show "ripple_index
      (rp_phi_projected_wavelength phi wavelength k)
      (rp_phi_projected_height phi height k) =
    ripple_index wavelength height"
    using assms(1)
    by (rule rp_phi_ripple_index_scale_invariant)
qed

end
