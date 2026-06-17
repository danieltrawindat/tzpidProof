theory TZPID_PeriodicTable_GravitationalCharge
  imports
    TZPID_Gravity_Focus
    TZPID_HypersphericalBesselResidualBridge_Math_Checks
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Added UTC: 2026-06-10

  HOL carrier for the Paper V periodic-table section.  The paper-facing
  numerical table is a computational certificate; this theory captures the
  formal ledger behind that table: atomic entries have atomic number and
  atomic weight, gravitational charge is mass divided by the Planck mass,
  and isotope-level binding correction subtracts binding energy through
  E = mc^2 before charge normalization.
\<close>

datatype periodic_sample =
    Hydrogen
  | Helium
  | Carbon
  | Oxygen
  | Iron
  | Gold
  | Lead
  | Uranium
  | Oganesson

definition periodic_sample_atomic_number :: "periodic_sample \<Rightarrow> nat" where
  "periodic_sample_atomic_number e =
    (case e of
       Hydrogen \<Rightarrow> 1
     | Helium \<Rightarrow> 2
     | Carbon \<Rightarrow> 6
     | Oxygen \<Rightarrow> 8
     | Iron \<Rightarrow> 26
     | Gold \<Rightarrow> 79
     | Lead \<Rightarrow> 82
     | Uranium \<Rightarrow> 92
     | Oganesson \<Rightarrow> 118)"

definition periodic_sample_atomic_weight :: "periodic_sample \<Rightarrow> real" where
  "periodic_sample_atomic_weight e =
    (case e of
       Hydrogen \<Rightarrow> 1008 / 1000
     | Helium \<Rightarrow> 4002602 / 1000000
     | Carbon \<Rightarrow> 12011 / 1000
     | Oxygen \<Rightarrow> 15999 / 1000
     | Iron \<Rightarrow> 55845 / 1000
     | Gold \<Rightarrow> 19696657 / 100000
     | Lead \<Rightarrow> 2072 / 10
     | Uranium \<Rightarrow> 23802891 / 100000
     | Oganesson \<Rightarrow> 294)"

definition periodic_sample_elements :: "periodic_sample list" where
  "periodic_sample_elements =
    [Hydrogen, Helium, Carbon, Oxygen, Iron, Gold, Lead, Uranium, Oganesson]"

definition atomic_weight_gravitational_charge :: "real \<Rightarrow> real \<Rightarrow> real" where
  "atomic_weight_gravitational_charge charge_unit atomic_weight =
     charge_unit * atomic_weight"

definition binding_corrected_atomic_weight :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "binding_corrected_atomic_weight atomic_weight binding_energy c =
     atomic_weight - binding_energy / c\<^sup>2"

definition binding_corrected_atomic_charge ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "binding_corrected_atomic_charge charge_unit atomic_weight binding_energy c =
     atomic_weight_gravitational_charge charge_unit
       (binding_corrected_atomic_weight atomic_weight binding_energy c)"

definition periodic_table_gravity_source_ids :: "string list" where
  "periodic_table_gravity_source_ids =
    [''Paper-V-periodic-table-section'', ''TAP-009'', ''TAP-010'', ''ID2846'']"

theorem periodic_sample_table_has_nine_entries:
  "length periodic_sample_elements = 9"
proof -
  have "periodic_sample_elements =
    [Hydrogen, Helium, Carbon, Oxygen, Iron, Gold, Lead, Uranium, Oganesson]"
    unfolding periodic_sample_elements_def
    by (rule refl)
  thus ?thesis
    by normalization
qed

theorem periodic_sample_atomic_numbers_match_paper_table:
  "map periodic_sample_atomic_number periodic_sample_elements =
    [1, 2, 6, 8, 26, 79, 82, 92, 118]"
proof -
  have "map periodic_sample_atomic_number periodic_sample_elements =
    map periodic_sample_atomic_number
      [Hydrogen, Helium, Carbon, Oxygen, Iron, Gold, Lead, Uranium, Oganesson]"
    unfolding periodic_sample_elements_def
    by (rule refl)
  thus ?thesis
    unfolding periodic_sample_atomic_number_def
    by normalization
qed

theorem atomic_weight_charge_is_planck_normalized_mass:
  assumes "mP \<noteq> 0"
    and "charge_unit = 1 / mP"
  shows
    "atomic_weight_gravitational_charge charge_unit atomic_weight =
     gravitational_charge atomic_weight mP"
proof -
  have "atomic_weight_gravitational_charge charge_unit atomic_weight =
        charge_unit * atomic_weight"
    unfolding atomic_weight_gravitational_charge_def
    by (rule refl)
  also have "... = atomic_weight / mP"
    using assms
    by (field)
  also have "... = gravitational_charge atomic_weight mP"
    unfolding gravitational_charge_def
    by (rule refl)
  finally show ?thesis .
qed

theorem atomic_weight_charge_positive:
  assumes "charge_unit > 0"
    and "atomic_weight > 0"
  shows "atomic_weight_gravitational_charge charge_unit atomic_weight > 0"
proof -
  have "charge_unit * atomic_weight > 0"
    using assms
    by (rule mult_pos_pos)
  thus ?thesis
    unfolding atomic_weight_gravitational_charge_def .
qed

theorem atomic_weight_charge_monotone:
  assumes "charge_unit > 0"
    and "w1 \<le> w2"
  shows
    "atomic_weight_gravitational_charge charge_unit w1
      \<le> atomic_weight_gravitational_charge charge_unit w2"
proof -
  have "charge_unit * w1 \<le> charge_unit * w2"
    using assms
    by (rule mult_left_mono)
  thus ?thesis
    unfolding atomic_weight_gravitational_charge_def .
qed

theorem binding_corrected_weight_recovers_uncorrected_at_zero_binding:
  "binding_corrected_atomic_weight atomic_weight 0 c = atomic_weight"
proof -
  have "binding_corrected_atomic_weight atomic_weight 0 c =
        atomic_weight - 0 / c\<^sup>2"
    unfolding binding_corrected_atomic_weight_def
    by (rule refl)
  also have "... = atomic_weight"
    by algebra
  finally show ?thesis .
qed

theorem binding_correction_never_increases_mass:
  assumes "binding_energy \<ge> 0"
    and "c \<noteq> 0"
  shows "binding_corrected_atomic_weight atomic_weight binding_energy c \<le> atomic_weight"
proof -
  have c_square_pos: "c\<^sup>2 > 0"
    using assms(2)
    by (simp add: zero_less_power2)
  have "binding_energy / c\<^sup>2 \<ge> 0"
    using assms(1) c_square_pos
    by (rule divide_nonneg_pos)
  hence "atomic_weight - binding_energy / c\<^sup>2 \<le> atomic_weight"
    by linarith
  thus ?thesis
    unfolding binding_corrected_atomic_weight_def .
qed

theorem binding_corrected_charge_recovers_mass_charge_at_zero_binding:
  "binding_corrected_atomic_charge charge_unit atomic_weight 0 c =
   atomic_weight_gravitational_charge charge_unit atomic_weight"
proof -
  have "binding_corrected_atomic_charge charge_unit atomic_weight 0 c =
        atomic_weight_gravitational_charge charge_unit
          (binding_corrected_atomic_weight atomic_weight 0 c)"
    unfolding binding_corrected_atomic_charge_def
    by (rule refl)
  also have "... =
        atomic_weight_gravitational_charge charge_unit atomic_weight"
    using binding_corrected_weight_recovers_uncorrected_at_zero_binding
    by presburger
  finally show ?thesis .
qed

theorem isotope_binding_ledger_connects_to_existing_TAP010:
  assumes "mP \<noteq> 0"
  shows
    "mP * isotope_gravitational_charge Z N mp mn me Ebind c mP =
     isotope_mass Z N mp mn me Ebind c"
proof -
  show ?thesis
    using assms
    by (rule isotope_charge_recovers_isotope_mass)
qed

theorem periodic_table_section_source_count:
  "length periodic_table_gravity_source_ids = 4"
proof -
  have "periodic_table_gravity_source_ids =
    [''Paper-V-periodic-table-section'', ''TAP-009'', ''TAP-010'', ''ID2846'']"
    unfolding periodic_table_gravity_source_ids_def
    by (rule refl)
  thus ?thesis
    by normalization
qed

end
