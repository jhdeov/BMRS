# Overview
Boolean Monadic Recursive Schemas (BMRS) are a logic-based program that simulates subsequential functions. Its hallmark is the use of recursive computation. It can be used to model phonological transformations. 


For more information, see:
- Bhaskar et al [2020](https://link.springer.com/chapter/10.1007/978-3-030-40608-0_10) "Boolean monadic recursive schemes as a logical characterization of the subsequential functions"
- Chandlee & Jardine [2021](http://adamjardine.net/files/chandleejardineBMRSms.pdf) "Computational universals in linguistic theory: Using recursive programs for phonological analysis"

This is an implementation of the BMRS notation. The implementation works as a compiler for BMRS programs and for more general logical transductions. We can compile rational functions, concatenated rational functions (see [Dolatian & Heinz 2020](https://jlm.ipipan.waw.pl/index.php/JLM/article/view/245)), and some types of regular non-order-preservng functions. The implementation can thus model any 1-way finite-state transducer, and some types of two-way finite-state transducers. 

This implementations works in the following way:

1) Logical transductions are written in a text file using Lisp syntax. 
2) These text files are converted to Python code. The Python code uses dynamic programming to run the logical transduction.
3) You can apply the transduction on an input word.

# Running a  an example
Tutorial follows.
1) **Working formulas**: I have written different logical transductions in the [TutorialFiles](TutorialFiles) folder.
2) **Pick** a text file that you want to run, e.g., `DeletionOfB.txt`. This text file encodes the logical transduction with Lisp syntax. Move it to the directory that has the `bmrs.py` file.
3) **Run** that text file with an example word `aba`. On the terminal, type:
`python3 bmrs.py run DeletionOfB.txt 'aba'`

The text file is converted to a Python file. And then the Python file is run over the string `aba`. The conversion and run are logged for debugging purposes. A TSV is generated that shows the input and output graphs.

Other commands that you can use:
* Convert the text file without running it:
`python3 bmrs.py convert DeletionOfB.txt`
* Specify a name for the converted the text file without running it:
`python3 bmrs.py convert DeletionOfB.txt DeletionOfB.py`
* Run a pre-existing Python file:
`python3 bmrs.py run DeletionOfB.py 'aba'`

# Writing your own code
For now, the format of the text files is still in development. 

While that YAML system is in development, you can write your own Python files instead. These files can be interpreted by the Python compiler. The Python script is very similar to a pen-and-paper BMRS system. If you want to apply your own BMRS system, do the following:
1) Have your own pen-and-paper BMRS system.
2) Make a copy of the `Template.py` file. Rename it anything you want, e.g., `MyBMRS.py'
3) Follow the instructions in your copy of the `Template.py` file. You will need to specify:
   * the set of input labels, e.g. ["a","b",...]
   * the elements of the copy set, e.g. [1] or [1,2,...]
   * if the input string is phonological segments ["t","s"], then specify features for each segment, e.g., ["labial",...]
   * the set of predicates (if any), e.g., ["final",..]
   * the definition for every output-label formula, output-function formula, and predicate in a general template. 

For output formula and predicates, the template uses Python if-return-else clauses in a way that (nearly) iconically matches the pen-and-paper BMRS functions.

Nodes in the input and output are treated as items with two coordinates: a level _l_ and a domain element <img src="https://render.githubusercontent.com/render/math?math=x">. For example, the node (0,1) is the domain element 1 in the input, while (1,2) is the domain element 2 in copy 1 in the output. 

When converting to the template, information from the input or output nodes is retrieved with the following commands:
* To retrieve the Boolean value of a label or predicate, use the function `self.get_BooleanValue(type,name,node)
* To retrieve a specific input or output node from a function (like successor), use the function `self.get_NodeValue(type,name,node)`
* To retrieve the domain element of a node, use the function `self.get_NodeDomain(node)`
* `type` is either "label", "function", or "predicate".
* `name` is the name of the label/function/predicate, such as "voiced". 
* `node` is an input our output node; it can be written as a tuple (_l_,<img src="https://render.githubusercontent.com/render/math?math=x">). 

For example,  the Chandlee & Jardine paper has the output function: 

  <img src="https://render.githubusercontent.com/render/math?math=H_o(x)%20=%20\text{if}%20\square'(x)%20\text{then}%20\top%20\text{else}%20 H(x)">

This function's meaning is decomposed into the following paraphrase:
* In copy 1, assign the label "H" to some domain element <img src="https://render.githubusercontent.com/render/math?math=x">...
* If the domain element <img src="https://render.githubusercontent.com/render/math?math=x"> has the label "stressed" in copy 1, ...
* then return true, 
* else return the value of the label "H" in the input for the same domain element <img src="https://render.githubusercontent.com/render/math?math=x">

In our Python system, the above function is translated as follows:
```
if copy == 1 and label == "H":
         if self.get_BooleanValue('label','stressed',(1,domain_element)): return True
         else: return self.get_BooleanValue('label','H',(0,domain_element))`
```


