HemisphereAntipodalPartition[spherePoints_] := Module[
  {northHemisphere, southHemisphere, antipodals},
  
  (* Hemisphere Separation *)
  northHemisphere = Select[spherePoints, #[[3]] > 0 &];
  southHemisphere = Select[spherePoints, #[[3]] ≤ 0 &];
  
  (* Antipodal Pairing Function *)
  antipodals = Table[
    {spherePoints[[i]], -spherePoints[[i]]},
    {i, 1, Length[spherePoints]/2}
  ];
  
  (* Entanglement Assignment *)
  EntanglementAssignment = AssociationThread[
    antipodals → Table[
      MaximallyEntangledState[2, "Bell"],
      Length[antipodals]
    ]
  ];
  
  Return[Association[
    "NorthernMetaBits" → Length[northHemisphere],
    "SouthernMetaBits" → Length[southHemisphere],
    "AntipodalPairs" → antipodals,
    "EntanglementMap" → EntanglementAssignment,
    "FiberAllocation" → 153600
  ]]
]