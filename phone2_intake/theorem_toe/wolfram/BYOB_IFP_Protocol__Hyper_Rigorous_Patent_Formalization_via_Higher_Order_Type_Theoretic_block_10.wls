ComplexityAnalysis := Module[
  {
    (* Time complexity analysis *)
    TimeComplexity = Association[
      "DirectCommunication" → 𝒪(1),          (* Constant via DMA *)
      "IFPParsing" → 𝒪(n log n),            (* via Earley parser *)
      "ProbabilityLookup" → 𝒪(1),           (* Precomputed *)
      "ProbabilityPrecompute" → 𝒪(n² log n), (* One-time cost *)
      "SplitCoordination" → 𝒪(log p),       (* p = processors *)
    ],
    
    (* Space complexity analysis *)
    SpaceComplexity = Association[
      "ProbabilityMatrices" → 𝒪(s²),        (* s = state space *)
      "BlobMetadata" → 𝒪(b),                (* b = blob count *)
      "CommandBuffer" → 𝒪(c),               (* c = command queue *)
      "SparseOptimized" → 𝒪(nnz),          (* nnz = nonzeros *)
    ],
    
    (* Parallel speedup analysis *)
    AmdahlSpeedup[p_, f_] := 1/((1-f) + f/p),
    GustafsonsSpeedup[p_, f_] := p - f(p-1),
    
    (* Expected performance *)
    TheoreticalSpeedup = Min[
      AmdahlSpeedup[GPUCores, ParallelizableFraction],
      GustafsonsSpeedup[CPUCores, SerialFraction]
    ]
  },
  
  <|
    "Time" → TimeComplexity,
    "Space" → SpaceComplexity,
    "Speedup" → TheoreticalSpeedup,
    "Efficiency" → TheoreticalSpeedup/TotalCores
  |>
]