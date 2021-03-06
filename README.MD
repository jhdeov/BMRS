# Overview
Boolean Monadic Recursive Schemas (BMRS) are a logic-based program that simulates subsequential functions. Its halmark is the use of recursive computation. It can be used to model phonological transformations. 


For more information, see:
- Bhaskar et al [2020](https://link.springer.com/chapter/10.1007/978-3-030-40608-0_10) "Boolean monadic recursive schemes as a logical characterization of the subsequential functions"
- Chandlee & Jardine [ms](http://adamjardine.net/files/chandleejardineBMRSms.pdf) "Recursive Schemes for Phonological Analysis"

This is a implementation in progress.

# Running an example
Tutorial follows.
1) **Working formulas**: I have implemented differnet logical transsductions. These include the following working programs:

|Function|File|Source|
|-|-|-|
|even-a with insertion|`Bhaskar_even_a.py`|Bhaskar et al 2020|
|Final obstruent devoicing | `FinalObstrDevoicing.py`|Chandlee & Jardine ms|
|H tone spreading|`HToneSpreadPenult.py`|Chandlee & Jardine ms|
|Intervocalic voicing|`Intervocalic.py`|Personal|
|Iterative stress|`IterStressHixk.py`|Chandlee & Jardine ms|

2) **Pick** a BMRS file that you want to run, e.g., `IterStressHixk.py`in the folder `Formulas`.
3) **Apply** that file:
In the `main.py` file, find the line `bmrs = something`. 
Replace `something` with the location and name of the BMRS file. Separate the location and name with a dot,  `bmrs = 'Formulas.IterStressHixk'`.
4) **Make** an example word. In the `main.py` file, replace `word=something` with your own word that is an acceptable input for the function, e.g., `word="LLLL"`. If the function accepts feature bundles such as for case, then use represent the entire input word as a list, and make the feature bundle a list inside a list, e.g, `word = list('cow') + [  ['nom','sg'] ]`.
5) **Run** the main file
6. The output for now is a long log of prints. The final printed element is a table that shows the input and output alongside all labels, predicates, and functions.

# Writing your own code
For now, my script can only interpret Python code. You have to manually convert your pen-and-paper BMRS system into a file that my script can run. The Python script is very similar to a pen-and-paper BMRS syste. If you want to apply your own BMRS system, do the following:
1) Have your own pen-and-paper BMRS system.
2) Make a copy of the `Template.py` file in the Formulas folder. Rename it anything you want, e.g., `MyBMRS.py'
3) Follow the instructions in your copy of the `Template.py` file. You will need to specify:
   * the set of input labels, e.g. ["a","b",...]
   * the elements of the copy set, e.g. [1] or [1,2,...]
   * if the input string is phonological segments ["t","s"], then specify features for each segment, .e.g, ["labial",...]
   * the set of predicates (if any), e.g., ["final",..]
   * the definition for every output function and predicate in a general template. 

For functions and predicates, my template uses Python if-return-else clauses in a way that (nearly) iconically matches the pen-and-paper BMRS functions.

When converting to my template, if a predicate or output function wants to retrieve value of a label/function/predicate in the input/output, I set up a general function `self.get_value(level, type, name, domain_element)` where:

* `level` can be the string “Input” or a copy index in your copy set, e.g. `self.get_value('input',...)` or `self.get_value(1,...)`. This determines whether the value is found in the input or some copy in the output.
* `type` is either "label","function", or "predicate".
* `name` is the name of the label/function/predicate, such as "voiced". 
* `domain_element` is the domain element.  The generic variable for the current domain element <img src="https://render.githubusercontent.com/render/math?math=x"> is just `domain_element`.

For example,  the Chandlee & Jardine paper has the output function: 

  <img src="https://render.githubusercontent.com/render/math?math=H_o(x)%20=%20\text{if}%20\square'(x)%20\text{then}%20\top%20\text{else}%20 H(x)">

This function's meaning is decomposed into the following paraphrase:
* In copy 1, assign the label "H" to some domain element <img src="https://render.githubusercontent.com/render/math?math=x">...
* If the domain element <img src="https://render.githubusercontent.com/render/math?math=x"> has the label "stressed" in copy 1, ...
* then return true, 
* else return the value of the label "H" in the input for the same domain element <img src="https://render.githubusercontent.com/render/math?math=x">

For my script, the above function is translated as follows:
```
if copy == 1 and label == "H":
         if self.get(1,'label','stressed',domain_element): return True
         else: return self.get("input","label","H",domain_element)`
```


