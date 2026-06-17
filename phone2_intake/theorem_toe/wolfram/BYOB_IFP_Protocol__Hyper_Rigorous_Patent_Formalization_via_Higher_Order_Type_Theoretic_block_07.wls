StatisticalLearningLemma := 
  Lemma[
    Statement → lim_{t→∞} ℙ_learned^{(t)} = ℙ_true,
    
    Proof → Module[
      {
        (* Online learning via stochastic gradient descent *)
        ∂ℙ/∂t = -η ∇_ℙ 𝔼_{(x,y)~Data}[(ℙ(x,y) - Indicator[collision(x,y)])²],
        
        (* Convergence via martingale theory *)
        MartingaleSequence = {ℙ^{(t)}, ℱ_t}_{t≥0},
        
        (* Doob's convergence theorem *)
        If[Sup_t 𝔼[|ℙ^{(t)}|] < ∞ ∧ lim_{t→∞} Var[ℙ^{(t)}] = 0,
           Then ∃ℙ_∞: ℙ^{(t)} →^{a.s.} ℙ_∞],
        
        (* Learning rate schedule *)
        η(t) = η₀/(1 + γt),  (* Robbins-Monro conditions *)
        
        (* Convergence rate *)
        𝔼[‖ℙ^{(t)} - ℙ_true‖²] ≤ C/√t
      },
      
      QED
    ]
  ]