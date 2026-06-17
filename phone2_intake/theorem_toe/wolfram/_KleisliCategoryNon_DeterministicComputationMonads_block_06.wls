ParallelPerformanceMetrics := Module[
  {
    (* Amdahl's Law with Overhead *)
    SpeedupAmdahl[p_, f_, κ_] := 
      1/((1-f) + f/p + κ*Log[p]),  (* κ = communication overhead *)
    
    (* Gustafson's Law *)
    SpeedupGustafson[p_, f_] := 
      p - f*(p - 1),
    
    (* Karp-Flatt Metric *)
    ExperimentalSerialFraction[p_, Ψ_p_] := 
      (1/Ψ_p - 1/p)/(1 - 1/p),
    
    (* Isoefficiency Function *)
    Isoefficiency[p_, W_] := Module[
      {
        T_serial = W,
        T_parallel[p] = W/p + T_overhead[p],
        T_overhead[p] = α*p*Log[p] + β*p²,  (* Example overhead *)
        
        (* Efficiency *)
        E[p] = T_serial/(p * T_parallel[p]),
        
        (* Isoefficiency: W(p) such that E = constant *)
        W[p] = Solve[E[p] == E_target, W][[1]]
      },
      
      W[p] = Θ[p² Log p]  (* Typical for many algorithms *)
    ],
    
    (* Statistical Performance Model *)
    PerformanceRegression = LinearModelFit[
      PerformanceData,
      {1, 1/p, Log[p], p, p*Log[p]},  (* Basis functions *)
      p,
      Weights → 1/VarianceEstimate,
      ConfidenceLevel → 0.95
    ],
    
    (* Roofline Model *)
    RooflineModel = Module[
      {
        PeakPerformance = FLOPS_peak,
        PeakBandwidth = Bandwidth_peak,
        
        ArithmeticIntensity = FLOPS/BytesTransferred,
        
        AttainablePerformance[I_] := Min[
          PeakPerformance,
          PeakBandwidth * I
        ],
        
        (* Ridge point *)
        I_ridge = PeakPerformance/PeakBandwidth
      },
      
      Plot[AttainablePerformance[I], {I, 0.01, 100},
        LogScale → {True, True},
        Epilog → {
          Red, PointSize[Large],
          Point[{ArithmeticIntensity, MeasuredPerformance}]
        }
      ]
    ]
  },
  
  (* Energy Efficiency *)
  EnergyModel = Module[
    {
      (* Dynamic power *)
      P_dynamic = α * C * V² * f,
      
      (* Static power *)
      P_static = V * I_leak,
      
      (* Energy-Delay Product *)
      EDP = Energy * ExecutionTime,
      
      (* Race-to-idle vs. DVFS *)
      OptimalFrequency = ArgMin[
        EDP[f],
        {f, f_min, f_max}
      ]
    },
    
    EnergyPerOperation = (P_dynamic + P_static) * ExecutionTime / Operations
  ]
]