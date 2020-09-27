# Overview
Boolean Monadic Recursive Schemas (BMRS) are a logic-based program that simulates subsequential functions. Its halmark is the use of recursive computation. It can be used to model phonological transformations. 


For more information, see:
- Bhaskar et al [2020](https://link.springer.com/chapter/10.1007/978-3-030-40608-0_10) "Boolean monadic recursive schemes as a logical characterization of the subsequential functions"
- Chandlee & Jardine [ms](http://adamjardine.net/files/chandleejardineBMRSms.pdf) "Recursive Schemes for Phonological Analysis"

This is a implementation in progress.

# Running an example
Tutorial follows.
1) **Working formulas**: I have implemented the following working programs:

|Function|File|Source|
|-|-|-|
|even-a with insertion|`Bhaskar_even_a.py`|Bhaskar et al 2020|
|Final obstruent devoicing | `FinalObstrDevoicing.py`|Chandlee & Jardine ms|
|H tone spreading|`HToneSpreadPenult.py`|Chandlee & Jardine ms|
|Intervocalic voicing|`Intervocalic.py`|Personal|
|Iterative stress|`IterStressHixk.py`|Chandlee & Jardine ms|

2) **Pick** a file that you want to run, e.g., `IterStressHixk.py`
3) **Apply** that file:
In the `Input.py` file, the top line is `from Formulas.something import *`
Replace `something` with the name of the file you want, e.g. `from Formulas.IterStressHixk import *`
4) **Make** an example word
In the `main.py` file, replace `word=something` with your own word that is an acceptable input for the function, e.g., `word="LLLL"` if you want iterative stress
5) **Run** the main file
6. The output for now is a long log of prints. The final printed element is a table that shows the input and output alongside all labels, predicates, and functions
# Writing your own code
For now, if you want to write your own code then do the following
1) From the `Formulas` folder, copy the `Template.py` file and give it a unique name
2) Modify it based on the instructions there. 
3) Apply the steps from "Running an example"

