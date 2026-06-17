MarkdownToLaTeX[md_String] := Module[{
  headerMap = {"#" -> "\\section", "##" -> "\\subsection", "###" -> "\\subsubsection"},
  mathMap = {"$...$" -> "\\(...\\)", "$$...$$" -> "\\[...\\]"},
  listMap = {"*" -> "\\item", "1." -> "\\item"}
},
  StringReplace[md, Join[headerMap, mathMap, listMap]]
]