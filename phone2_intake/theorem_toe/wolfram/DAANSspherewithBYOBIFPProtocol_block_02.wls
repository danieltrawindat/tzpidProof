InfiniteBlobEncoding := Association[
  "Level0" → spherePoints[153600, bits[0:153599]],
  "Level1" → spherePoints[153600, bits[153600:307199]],
  "LevelK" → spherePoints[153600, bits[k*153600:(k+1)*153600-1]],
  
  (* Depth-Encoded Infinite Extension *)
  "DepthMapping" → Function[{bitIndex},
    Module[{k, i, u, t, r},
      k = Floor[bitIndex/153600];  (* Hierarchy level *)
      i = Mod[bitIndex, 153600];   (* Point index *)
      u = (bitIndex + 0.5)/(10^k + 1);  (* Domain-safe encoding *)
      t = α * Log[u/(1-u)];  (* Logit transformation *)
      r = Exp[t];  (* Radial distance *)
      {spherePoint[i], radius[r], level[k]}
    ]
  ]
]