IFPCompositionalityTheorem := 
  Theorem[
    Statement → ∀ cmd₁, cmd₂ ∈ IFPCommands:
      ⟦cmd₁ ∘ cmd₂⟧ = ⟦cmd₁⟧ ∘ ⟦cmd₂⟧,
    
    Proof → Module[
      {
        (* Denotational semantics *)
        ⟦·⟧ : IFPCommands → (BlobState → BlobState),
        
        (* Church encoding of commands *)
        ChurchEncoding[cmd_] := cmd Match {
          Approach[obj] :> λs. s ⊕ {position → Lerp[s.position, obj.position, 0.1]},
          Examine[obj] :> λs. s ⊕ {knowledge → s.knowledge ∪ Properties[obj]},
          Interact[obj, action] :> λs. ProbabilityMatrix[s, obj, action],
          Move[direction] :> λs. s ⊕ {position → s.position + direction}
        },
        
        (* Composition preserves semantics *)
        ⟦cmd₁ ∘ cmd₂⟧[s] = ⟦cmd₁⟧[⟦cmd₂⟧[s]]
                        = (ChurchEncoding[cmd₁] ∘ ChurchEncoding[cmd₂])[s]
                        = ChurchEncoding[cmd₁][ChurchEncoding[cmd₂][s]]
      },
      
      (* By structural induction on cmd₁, cmd₂ *)
      InductionBase → ⟦Identity⟧ = λs.s,
      InductionStep → If[⟦cmd₁⟧ ∘ ⟦cmd₂⟧ = ⟦cmd₁ ∘ cmd₂⟧,
                        Then ⟦cmd₁ ∘ (cmd₂ ∘ cmd₃)⟧ = ⟦(cmd₁ ∘ cmd₂) ∘ cmd₃⟧],
      
      QED
    ]
  ]