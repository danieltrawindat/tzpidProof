theory TZPID_OperatorSpectral_FollowupCarriers
  imports TZPID_Theorem_Semantic_Batch012_Operator_Spectral_Followup
          TZPID_OperatorSpectral_Carriers
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 operator/spectral follow-up upgrade.

  Batch 012 is the follow-up lane for closed-path wavelength locks,
  Kaluza-Klein effective modes, spectral inversion, Alfvén mode
  quantization, Hamiltonian flow, and gap stability.  This layer binds
  those residual guards to explicit reusable carriers and to the finite
  spectral carrier layer from batch 006.
\<close>

section \<open>Closed Path and Modal Carriers\<close>

definition osf_closed_path_wavenumber :: "real \<Rightarrow> real \<Rightarrow> real" where
  "osf_closed_path_wavenumber winding path_length =
     2 * pi * winding / path_length"

definition osf_tidal_mode_wavelength :: "real \<Rightarrow> real \<Rightarrow> real" where
  "osf_tidal_mode_wavelength mode radius =
     tidal_wavelength_quantization mode radius"

definition osf_effective_mass_squared :: "real \<Rightarrow> real \<Rightarrow> real" where
  "osf_effective_mass_squared mode radius =
     (four_d_effective_mode_mass mode radius)\<^sup>2"

definition osf_coupled_mode_observed :: "real \<Rightarrow> real \<Rightarrow> real" where
  "osf_coupled_mode_observed base coupling = base * coupling"

definition osf_alfven_frequency :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "osf_alfven_frequency mode length velocity =
     alfven_mode_quantization mode length * velocity"

definition osf_hamiltonian_flow_residual ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "osf_hamiltonian_flow_residual qdot dHdp pdot dHdq external_force scale =
     scale * ((qdot - dHdp) + (pdot - (- dHdq + external_force)))"

definition osf_spectral_inverse_pair :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "osf_spectral_inverse_pair observed reconstructed =
     (observed = reconstructed)"

section \<open>Follow-Up Laws\<close>

theorem osf_closed_path_wavenumber_zeroes_residual:
  assumes "path_length \<noteq> 0"
  shows "closed_path_wavelength_quantization_residual
          (osf_closed_path_wavenumber winding path_length)
          path_length winding = 0"
proof -
  have "osf_closed_path_wavenumber winding path_length * path_length =
        2 * pi * winding"
  proof -
    have denominator_nonzero: "path_length \<noteq> 0"
      using assms .
    have "(2 * pi * winding / path_length) * path_length =
          2 * pi * winding"
      using denominator_nonzero
      by (field)
    thus ?thesis
      unfolding osf_closed_path_wavenumber_def .
  qed
  thus ?thesis
    by (rule id9999_wavelength_quantization_residual_zero)
qed

theorem osf_tidal_mode_wavelength_recovers_circumference:
  assumes "mode \<noteq> 0"
  shows "osf_tidal_mode_wavelength mode radius * mode = 2 * pi * radius"
proof -
  show ?thesis
    using assms
    unfolding osf_tidal_mode_wavelength_def
    by (rule id8520_tidal_wavelength_recovers_circumference)
qed

theorem osf_effective_mass_squared_nonnegative:
  "osf_effective_mass_squared mode radius \<ge> 0"
proof -
  show ?thesis
    unfolding osf_effective_mass_squared_def
    by (rule zero_le_power2)
qed

theorem osf_effective_mode_mass_recovers_mode:
  assumes "radius \<noteq> 0"
  shows "four_d_effective_mode_mass mode radius * radius = mode"
proof -
  show ?thesis
    using assms
    by (rule id9595_effective_mode_mass_recovers_mode)
qed

theorem osf_coupled_mode_residual_zero:
  "kk_mode_coupling_residual
     (osf_coupled_mode_observed base coupling) base coupling = 0"
proof -
  have "osf_coupled_mode_observed base coupling = base * coupling"
    unfolding osf_coupled_mode_observed_def
    by (rule refl)
  thus ?thesis
    by (rule id9999_kk_mode_coupling_residual_zero)
qed

theorem osf_alfven_frequency_recovers_velocity_scaled_mode:
  assumes "length \<noteq> 0"
  shows "osf_alfven_frequency mode length velocity * length =
         mode * pi * velocity"
proof -
  have base: "alfven_mode_quantization mode length * length = mode * pi"
    using assms
    by (rule id9999_alfven_mode_quantization_recovers_mode)
  have "osf_alfven_frequency mode length velocity * length =
        (alfven_mode_quantization mode length * velocity) * length"
    unfolding osf_alfven_frequency_def
    by (rule refl)
  also have "... = (alfven_mode_quantization mode length * length) * velocity"
    by algebra
  also have "... = mode * pi * velocity"
    using base
    by algebra
  finally show ?thesis .
qed

theorem osf_hamiltonian_flow_zero_from_guard:
  assumes "hamilton_equations_guard qdot dHdp pdot dHdq external_force"
  shows "osf_hamiltonian_flow_residual qdot dHdp pdot dHdq external_force scale = 0"
proof -
  have q: "qdot = dHdp"
    using assms
    unfolding hamilton_equations_guard_def
    by blast
  have p: "pdot = - dHdq + external_force"
    using assms
    unfolding hamilton_equations_guard_def
    by blast
  show ?thesis
    unfolding osf_hamiltonian_flow_residual_def
    using q p
    by algebra
qed

theorem osf_spectral_inverse_zero_residual:
  assumes "osf_spectral_inverse_pair observed reconstructed"
  shows "spectral_inversion_residual observed reconstructed = 0"
proof -
  have "observed = reconstructed"
    using assms
    unfolding osf_spectral_inverse_pair_def .
  thus ?thesis
    unfolding spectral_inversion_residual_def
    by algebra
qed

theorem osf_gap_guard_uses_spectral_carrier:
  assumes "os_gap_exceeds_perturbation gap perturbation"
    and "coupling \<ge> 0"
    and "curvature \<ge> 0"
  shows "curvature_spectral_gap gap coupling curvature > 0"
proof -
  show ?thesis
    using assms
    by (rule os_gap_guard_with_nonnegative_curvature)
qed

section \<open>Batch 012 Upgrade Contract\<close>

theorem operator_spectral_followup_carrier_contract:
  assumes path_nonzero: "path_length \<noteq> 0"
    and mode_nonzero: "mode \<noteq> 0"
    and radius_nonzero: "radius \<noteq> 0"
    and length_nonzero: "length \<noteq> 0"
    and hamilton_guard: "hamilton_equations_guard qdot dHdp pdot dHdq external_force"
    and inverse_pair: "osf_spectral_inverse_pair observed reconstructed"
    and gap_guard: "os_gap_exceeds_perturbation gap perturbation"
    and coupling_nonnegative: "coupling_gap \<ge> 0"
    and curvature_nonnegative: "curvature \<ge> 0"
  shows
    "closed_path_wavelength_quantization_residual
       (osf_closed_path_wavenumber winding path_length)
       path_length winding = 0
     \<and> osf_tidal_mode_wavelength mode radius * mode = 2 * pi * radius
     \<and> osf_effective_mass_squared kk_mode radius \<ge> 0
     \<and> four_d_effective_mode_mass kk_mode radius * radius = kk_mode
     \<and> kk_mode_coupling_residual
       (osf_coupled_mode_observed base coupling) base coupling = 0
     \<and> osf_alfven_frequency alfven_mode length velocity * length =
       alfven_mode * pi * velocity
     \<and> osf_hamiltonian_flow_residual qdot dHdp pdot dHdq external_force scale = 0
     \<and> spectral_inversion_residual observed reconstructed = 0
     \<and> curvature_spectral_gap gap coupling_gap curvature > 0"
proof (intro conjI)
  show "closed_path_wavelength_quantization_residual
       (osf_closed_path_wavenumber winding path_length)
       path_length winding = 0"
    using path_nonzero
    by (rule osf_closed_path_wavenumber_zeroes_residual)
  show "osf_tidal_mode_wavelength mode radius * mode = 2 * pi * radius"
    using mode_nonzero
    by (rule osf_tidal_mode_wavelength_recovers_circumference)
  show "osf_effective_mass_squared kk_mode radius \<ge> 0"
    using osf_effective_mass_squared_nonnegative .
  show "four_d_effective_mode_mass kk_mode radius * radius = kk_mode"
    using radius_nonzero
    by (rule osf_effective_mode_mass_recovers_mode)
  show "kk_mode_coupling_residual
       (osf_coupled_mode_observed base coupling) base coupling = 0"
    using osf_coupled_mode_residual_zero .
  show "osf_alfven_frequency alfven_mode length velocity * length =
       alfven_mode * pi * velocity"
    using length_nonzero
    by (rule osf_alfven_frequency_recovers_velocity_scaled_mode)
  show "osf_hamiltonian_flow_residual qdot dHdp pdot dHdq external_force scale = 0"
    using hamilton_guard
    by (rule osf_hamiltonian_flow_zero_from_guard)
  show "spectral_inversion_residual observed reconstructed = 0"
    using inverse_pair
    by (rule osf_spectral_inverse_zero_residual)
  show "curvature_spectral_gap gap coupling_gap curvature > 0"
    using gap_guard coupling_nonnegative curvature_nonnegative
    by (rule osf_gap_guard_uses_spectral_carrier)
qed

end
