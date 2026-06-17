(* Optimal Blob-Sphere Integration *)
OptimalBlobMapping := Function[{blobSize},
  Module[{hierarchyDepth, addressSpace, mappingStrategy},
    hierarchyDepth = Ceiling[Log[4, blobSize/153600]];
    
    addressSpace = Table[
      {level → k, 
       points → 153600, 
       bitRange → {k*153600 + 1, (k+1)*153600},
       depthParameter → k},
      {k, 0, hierarchyDepth}
    ];
    
    mappingStrategy = <|
      "BitToPoint" → Mod[#, 153600] + 1 &,
      "PointToBit" → # + Floor[#2/153600]*153600 &,
      "DepthEncoding" → (# + 0.5)/(10^#2 + 1) &,
      "RadialMapping" → Exp[α*Log[#/(1-#)]] &
    |>;
    
    {addressSpace, mappingStrategy}
  ]
]