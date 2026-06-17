theory TZPID_PortalEquilibrium_Laws
  imports TZPID_PortalBreathing_OccupancyInterface
begin

text \<open>
  Portal-equilibrium law extraction from the saved force-vector and phi-ratio
  sections of the_portal_equation.txt. These are conservative carriers and
  algebraic checks, not empirical validation of the stronger transcript claims.
\<close>

definition pe_gravity_force :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pe_gravity_force m g = m * g"

definition pe_surface_force :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pe_surface_force gamma R1 R2 = gamma * (1 / R1 + 1 / R2)"

definition pe_inertial_force :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pe_inertial_force m a = m * a"

definition pe_acoustic_force :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pe_acoustic_force P A = P * A"

definition pe_drag_force :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pe_drag_force rho v C_d A = (1 / 2) * rho * v\<^sup>2 * C_d * A"

definition pe_five_force_balance :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "pe_five_force_balance F_g F_s F_i F_a F_r \<longleftrightarrow>
    F_g + F_s + F_i + F_a + F_r = 0"

definition pe_phi_ratio :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pe_phi_ratio F_s F_i = F_s / F_i"

definition pe_portal_state :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pe_portal_state F_s F_i F_a phi = F_s * phi / (F_i + F_a)"

definition pe_predicted_acoustic_force :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pe_predicted_acoustic_force F_s F_i phi = F_s * phi - F_i"

definition pe_golden_ratio :: real where
  "pe_golden_ratio = (1 + sqrt 5) / 2"

lemma pe_five_force_balance_by_counterterm:
  shows "pe_five_force_balance F_g F_s F_i F_a (-(F_g + F_s + F_i + F_a))"
  unfolding pe_five_force_balance_def
  by algebra

lemma pe_portal_state_one_from_predicted_acoustic_force:
  assumes "F_s * phi \<noteq> 0"
  shows "pe_portal_state F_s F_i
    (pe_predicted_acoustic_force F_s F_i phi) phi = 1"
proof -
  show ?thesis
    unfolding pe_portal_state_def pe_predicted_acoustic_force_def
    using assms
    by field
qed

lemma pe_phi_ratio_positive:
  assumes "0 < F_s"
    and "0 < F_i"
  shows "0 < pe_phi_ratio F_s F_i"
  unfolding pe_phi_ratio_def
  using assms
  by positivity

lemma pe_golden_ratio_positive:
  shows "0 < pe_golden_ratio"
proof -
  have "0 < sqrt 5"
    by simp
  then show ?thesis
    unfolding pe_golden_ratio_def
    by linarith
qed

theorem pe_portal_equilibrium_law_contract:
  assumes "F_s * phi \<noteq> 0"
  shows "pe_five_force_balance F_g F_s F_i F_a (-(F_g + F_s + F_i + F_a))
    \<and> pe_portal_state F_s F_i
      (pe_predicted_acoustic_force F_s F_i phi) phi = 1"
proof (intro conjI)
  show "pe_five_force_balance F_g F_s F_i F_a (-(F_g + F_s + F_i + F_a))"
    by (rule pe_five_force_balance_by_counterterm)
  show "pe_portal_state F_s F_i
      (pe_predicted_acoustic_force F_s F_i phi) phi = 1"
    using assms
    by (rule pe_portal_state_one_from_predicted_acoustic_force)
qed

end
