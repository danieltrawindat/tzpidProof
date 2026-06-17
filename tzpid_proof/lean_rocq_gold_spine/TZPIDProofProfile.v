(*
Project: TZPID Proof Pipeline
Creator: Daniel Alexander Trawin
ORCID: https://orcid.org/0009-0001-4630-3715
Generated UTC: 2026-06-11T00:00:00Z

Rocq/Coq proof-profile lane.

This file is a portability mirror for the Isabelle/HOL spine contracts in:

* TZPID_VectorCalculus_IsarSpineLayer.thy
* TZPID_VectorCalculus_IntegralCarriers.thy
* TZPID_TopologicalUnification_MintedCarriers.thy
* TZPID_TopologicalUnification_SpineMerges.thy

It intentionally stays finite and algebraic so it can be checked by the
installed Rocq/Coq toolchain without extra libraries.  Isabelle/HOL remains
the primary proof-development lane; Rocq is used here as an independent
profile/check lane for the carrier shape.
*)

From Stdlib Require Import List ZArith Lia.
Import ListNotations.
Open Scope Z_scope.

Inductive vector_calculus_spine : Type :=
  | VC_DeltaAlpha_Gradient
  | VC_Gyromagnetic_Lz
  | VC_Magnetic_Helicity
  | VC_Elsasser_MHD
  | VC_Torsion_Cancellation
  | VC_Flux_Quantization
  | VC_Topological_Boundary
  | VC_Winding_Update.

Definition spine_backbone : list vector_calculus_spine :=
  [ VC_DeltaAlpha_Gradient
  ; VC_Gyromagnetic_Lz
  ; VC_Magnetic_Helicity
  ; VC_Elsasser_MHD
  ; VC_Torsion_Cancellation
  ; VC_Flux_Quantization
  ; VC_Topological_Boundary
  ; VC_Winding_Update
  ].

Theorem spine_backbone_count :
  List.length spine_backbone = 8%nat.
Proof.
  reflexivity.
Qed.

Definition curl_z (partial_x_grad_y partial_y_grad_x : Z) : Z :=
  partial_x_grad_y - partial_y_grad_x.

Theorem mixed_partials_zero_curl :
  forall partial_x_grad_y partial_y_grad_x : Z,
    partial_x_grad_y = partial_y_grad_x ->
    curl_z partial_x_grad_y partial_y_grad_x = 0.
Proof.
  intros partial_x_grad_y partial_y_grad_x H.
  unfold curl_z.
  lia.
Qed.

Definition rect_area (width height : Z) : Z :=
  width * height.

Definition rect_boundary_circulation
    (curl_strength width height : Z) : Z :=
  curl_strength * width * height.

Definition rect_surface_flux
    (curl_strength width height : Z) : Z :=
  curl_strength * rect_area width height.

Theorem green_rectangle_constant_curl :
  forall curl_strength width height : Z,
    rect_boundary_circulation curl_strength width height =
    rect_surface_flux curl_strength width height.
Proof.
  intros.
  unfold rect_boundary_circulation, rect_surface_flux, rect_area.
  lia.
Qed.

Definition divergence (partial_x_Fx partial_y_Fy : Z) : Z :=
  partial_x_Fx + partial_y_Fy.

Definition incompressible (partial_x_Fx partial_y_Fy : Z) : Prop :=
  divergence partial_x_Fx partial_y_Fy = 0.

Theorem incompressible_from_opposite_partials :
  forall partial_x_Fx partial_y_Fy : Z,
    partial_y_Fy = - partial_x_Fx ->
    incompressible partial_x_Fx partial_y_Fy.
Proof.
  intros partial_x_Fx partial_y_Fy H.
  unfold incompressible, divergence.
  lia.
Qed.

Definition dot3
    (ax ay az bx_comp by_comp bz : Z) : Z :=
  ax * bx_comp + ay * by_comp + az * bz.

Definition helicity_density
    (ax ay az bx_comp by_comp bz : Z) : Z :=
  dot3 ax ay az bx_comp by_comp bz.

Theorem helicity_density_zero_when_b_zero :
  forall ax ay az : Z,
    helicity_density ax ay az 0 0 0 = 0.
Proof.
  intros.
  unfold helicity_density, dot3.
  lia.
Qed.

Definition uniform_helicity_integral (volume density : Z) : Z :=
  volume * density.

Theorem uniform_helicity_integral_zero_density :
  forall volume : Z,
    uniform_helicity_integral volume 0 = 0.
Proof.
  intros.
  unfold uniform_helicity_integral.
  lia.
Qed.

Definition elsasser_number_unit
    (magnetic_force coriolis_force : Z) : Prop :=
  magnetic_force = coriolis_force /\ coriolis_force <> 0.

Theorem elsasser_balance_consumed :
  forall magnetic_force coriolis_force : Z,
    elsasser_number_unit magnetic_force coriolis_force ->
    magnetic_force = coriolis_force.
Proof.
  intros magnetic_force coriolis_force H.
  destruct H as [H _].
  exact H.
Qed.

Definition torsion_density (curvature twist : Z) : Z :=
  curvature + twist.

Theorem opposite_twist_torsion_zero :
  forall curvature : Z,
    torsion_density curvature (- curvature) = 0.
Proof.
  intros.
  unfold torsion_density.
  lia.
Qed.

Definition flux_multiple (flux_quantum n : Z) : Z :=
  n * flux_quantum.

Definition flux_quantized (flux flux_quantum n : Z) : Prop :=
  flux = n * flux_quantum.

Theorem flux_multiple_is_quantized :
  forall flux_quantum n : Z,
    flux_quantized (flux_multiple flux_quantum n) flux_quantum n.
Proof.
  intros.
  unfold flux_quantized, flux_multiple.
  reflexivity.
Qed.

Definition winding_phase (turns : Z) : Z :=
  turns.

Definition winding_index (phase turns : Z) : Prop :=
  phase = turns.

Theorem quantized_circulation_is_winding_index :
  forall turns : Z,
    winding_index (winding_phase turns) turns.
Proof.
  intros.
  unfold winding_index, winding_phase.
  reflexivity.
Qed.

Record proof_profile : Type := {
  spine_count : nat;
  vector_calculus_layer : bool;
  integral_carrier_layer : bool;
  lean_lane_expected : bool;
  rocq_lane_checked : bool
}.

Definition tzpid_proof_profile : proof_profile := {|
  spine_count := 8%nat;
  vector_calculus_layer := true;
  integral_carrier_layer := true;
  lean_lane_expected := true;
  rocq_lane_checked := true
|}.

Theorem proof_profile_spine_count :
  spine_count tzpid_proof_profile = 8%nat.
Proof.
  reflexivity.
Qed.

Theorem proof_profile_has_secondary_lanes :
  lean_lane_expected tzpid_proof_profile = true /\
  rocq_lane_checked tzpid_proof_profile = true.
Proof.
  split; reflexivity.
Qed.
