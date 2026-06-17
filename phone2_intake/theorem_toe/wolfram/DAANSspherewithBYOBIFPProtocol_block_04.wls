PrecomputedInteractionMatrices := Association[
  "CollisionMatrix" → SparseArray[
    Table[
      probabilityCollision[n[i], n[j], depth[k]],
      {i, 1, 153600}, {j, 1, 153600}, {k, 0, ∞}
    ]
  ],
  
  "LookupComplexity" → O[Log[153600] + Log[hierarchyLevel]],
  "MemoryFootprint" → O[blobSize/153600] (* Linear in hierarchy levels *)
]