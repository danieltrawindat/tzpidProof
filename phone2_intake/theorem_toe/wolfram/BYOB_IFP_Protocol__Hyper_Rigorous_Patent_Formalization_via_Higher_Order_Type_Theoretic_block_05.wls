ParserCorrectnessLemma := 
  Lemma[
    Statement → Parse ∘ Unparse = Identity,
    
    Proof → Module[
      {
        (* Parsing combinator monad *)
        ParserMonad = StateMonad[TokenStream],
        
        (* Monadic parser *)
        parseCommand = Do[
          verb ← parseVerb,
          object ← parseObject,
          modifiers ← many(parseModifier),
          Return[Command[verb, object, modifiers]]
        ],
        
        (* Unparsing via pretty-printing *)
        unparseCommand[Command[v, o, ms]] := 
          StringJoin[v, " ", o, " ", StringRiffle[ms, " "]],
        
        (* Round-trip property *)
        ∀cmd: parseCommand[unparseCommand[cmd]] = Success[cmd]
      },
      
      QED
    ]
  ]