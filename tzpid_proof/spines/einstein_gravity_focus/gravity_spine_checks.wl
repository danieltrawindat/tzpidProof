(* Creator: Daniel Alexander Trawin | ORCID: https://orcid.org/0009-0001-4630-3715 *)
(* Wolfram check stub for gold spine: Gravity as an Accumulated Force *)
(* Mirrors wolfram_checks/einstein_focus_checks.wl: each relation is a checkable
   obligation; fill in symbolic verifications and export pass/computed/needs_normalization. *)

spineChecks = {
  <| "name" -> "grav_newtonian_recovery", "relation" -> "a -> a_N as alpha -> 0", "description" -> "accumulated correction vanishes; Newtonian acceleration recovered", "status" -> "obligation" |>,
  <| "name" -> "grav_stress_vanishes", "relation" -> "delta T_ij -> 0 as alpha -> 0  =>  T_ij^eff -> T_ij^N", "description" -> "effective stress reduces to Newtonian stress in far field", "status" -> "obligation" |>,
  <| "name" -> "grav_poisson_dim_balance", "relation" -> "[nabla^2 Phi] == [4 pi G rho]", "description" -> "dimensional balance of the emergent Poisson closure", "status" -> "obligation" |>
};

(* Example: export a results JSON next to the Einstein results *)
(* Export[$ScriptCommandLine[[2]], spineChecks, "JSON"] *)
spineChecks
