# Physical Proof Architecture

Generated: 2026-06-11

## Thesis

Yes: the proof package can use a physical architecture to represent proofs.
The correct formal framing is the Curry-Howard-Lambek correspondence:

| View | Proof-package role | Physical reading |
| --- | --- | --- |
| Logic | propositions and theorem obligations | statements that can be true or false |
| Computer science | types, programs, and carriers | executable/constructive witnesses |
| Category theory | objects, morphisms, monoidal composition | compositional process geometry |
| TQFT / geometry | cobordisms, tangles, boundaries | physical realization of proof flow |

The package should treat this as an architecture layer, not as a shortcut
around proof.  Isabelle/HOL remains the primary formal lane; Lean/Rocq are
secondary portability lanes; Wolfram/Python/HDF5 are computational certificate
lanes.  The physical architecture is the organizing language tying those lanes
together.

## Triangle

```text
       [ LOGIC ] -------- Curry-Howard -------- [ TYPES / PROGRAMS ]
   propositions/proofs                         carriers/programs
            \                                      /
             \                                    /
              \---- Lambek / categorical ---- [ MONOIDAL PROCESS ]
                                                  |
                                                  | TQFT / geometry
                                                  v
                                       [ COBORDISM / TANGLE / FIELD ]
```

## How This Maps To TZPID

| Architecture element | Existing TZPID artifact |
| --- | --- |
| Logic proposition | Isabelle theorem/lemma statement |
| Proof witness | Isar proof term / theorem derivation |
| Type/program | HOL carrier, Lean/Rocq profile mirror |
| Category object | `category_object` in topology/category carriers |
| Category morphism | `category_arrow`, `tc_arrow_composition` |
| Monoidal product | tensor-like product of proof lanes/spines |
| Physical process | vector/MHD/flux/winding carrier |
| TQFT geometry | boundary/flux/circulation/cobordism-style witness |

## Why This Helps

1. It makes proof composition visible.
2. It lets each spine be represented as a process, not just a document.
3. It explains why vector-calculus, category, and proof assistants all belong
   in the same proof package.
4. It gives reviewers a non-handwavy map:
   proposition -> type/program -> morphism/process -> geometric witness.

## Guardrail

This architecture does not say that a metaphor proves a theorem.  It says each
spine should expose:

1. a logical proposition;
2. a typed carrier/program witness;
3. a categorical composition law;
4. a physical/geometric certificate where available.

Only when all relevant carriers are checked should the paper claim the spine is
formally supported.

## Isabelle Artifact

The corresponding HOL carrier theory is:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_PhysicalProofArchitecture.thy`

It records:

- the four architecture nodes;
- the Curry-Howard, Lambek, and TQFT edges;
- monoidal tensor carriers for proof objects and morphisms;
- a physical proof object record;
- composition and tensor-preservation contracts;
- a bridge back into the vector-calculus spine carrier layer.

