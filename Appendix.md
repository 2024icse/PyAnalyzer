# Appendix

This appendix contains supplemental materials for clarifying details in study setup.

In general, our work collected two micro-benchmarks (45+233=**278** small programs), one macro-benchmarks (**54** real-world applications), and **191** real-world projects of **10MSLOC** for comprehensive comparisons with 7 advanced techniques (i.e., Understand, Sourcetrail, Depends, ENRE, PySonar2, PyCG, and Type4Py). *To the best of our knowledge, the size of benchmarks and the number of baselines we collected are the largest when compared to those used in existing work*.

## Setup(Section 4)


### Collection of Three Benchmarks(Section 4.2)

In this section, we provide a detailed description of the data collection process for the three benchmarks used in our paper.

#### Micro-BenchmarkA for RQ1(Section 4.2.1)

This section provides a detailed description of the process used to collect Benchmark A and presents a comprehensive introduction to the contents of Benchmark A.

##### Collection process

To verify the effectiveness of PyAnalyzer on common entities and dependencies identification, we constructed a benchmark that covers diverse kinds of entities dependencies in Python. We collected a micro-benchmark A for evaluating the accuracy of deterministic dependencies along with entities generated by different methods. The detailed collection process is as follows.

1. We referred to the language specification and divided the spec into several excerpts, where each one focusing on an individual language feature. This division enables us to design tests to cover fine-grained language features as possible.

   The following shows an example of Python language specification namely global declaration and nonlocal declaration.

   ```yaml
   // Syntax Production Rules
   global_stmt ::= "global" identifier ("," identifier)*
   nonlocal_stmt ::= "nonlocal" identifier ("," identifier)*
   
   // Semantic Instructions
   global :
       In Python, the global keyword allows us to modify the variable outside of the current scope. It is used to create a global variable and make changes to the variable in a local context.
   nonglobal :
       The nonlocal keyword is used to work with variables inside nested functions, where the variable should not belong to the inner function. Use the keyword nonlocal to declare that the variable is not local.
   ```

2. We then manually constructed code snippets to apply language features by following the related specification excerpts. Taking the following code snippet as example.

   ```python
   // file0.py
   
    1 a = 1
    2 
    3 def outer():
    4     a = 2
    5   
    6     def inner():
    7         nonlocal a
    8         a = 3
    9         global b
   10         b = 4
   11 
   12     inner()
   13     print(f"{a}")     # 3
   14  
   15 outer()
   16 print(f"{b}")         # 4
   ```

   In this code, the variable "a" is defined and assigned a value of 1 in line 1. Inside the "outer" function (lines 3-15), a new local variable "a" is defined and assigned a value of 2 in line 4. 

   Then, the "inner" function is defined (lines 6-10). Inside the "inner" function, the "nonlocal" keyword is used in line 7 to indicate that we are referring to the variable "a" from the nearest enclosing scope (the "outer" function scope) rather than creating a new local variable. So, the value of "a" is changed to 3 in line 8.

   Next, the "global" keyword is used in line 9 to indicate that we are referring to the global variable "b" rather than creating a new local variable. So, the value of the global variable "b" is changed to 4 in line 10.

   Finally, the "outer" function is called in line 15, and it calls the "inner" function in line 12. The value of the variable "a" inside the "outer" function is printed in line 13, and the value of the global variable "b" is printed in line 16.

3. For every code snippet, we manually write an assertion block. An assertion block records the ground truth entities and dependencies that are expected to be extracted from the corresponding code snippet.

   For the code shown above, the ground truth entities and dependencies are shown in the assertion block which is as follows. 
   
   ```yaml
   // Assertion Block
   entity:
     items:
       - name: a
         type: variable
         loc: file0:1:1
       - name: outer.a
         type: variable
         loc: file0:4:5
       - name: b
         type: variable
         loc: file0:9:16
   dependency:
     type: set
     items:
       - src: function:'inner'
         dest: variable:'outer.a'
         loc: file0:8:9
       - src: module:'file0'
         dest: variable:'b'
         loc: file0:10:9
   ```
   
   There are two blocks in this assertion result:
   
   **The “entity” block** presents three entities, which are variables "a", "outer.a", and "b". Each entity has a "name" attribute representing the entity's name, a "type" attribute representing the entity's type, and a "loc" attribute representing the entity's location in the code.
   
   **The “dependency” block** presents two dependency relationships. The first dependency is from the function "inner" referring to the variable "outer.a", and its location in the code is "file0:8:9". The second dependency is from the module "file0" referring to the variable "b", and its location in the code is "file0:10:9".
   
   These assertions are used to verify whether the extracted entities and dependencies from the code match the expected results.

##### Collection Results

To sum up, an excerpt of the language specification, the code snippet, and the corresponding assertion block compose a test of the benchmark. The following table summarizes the benchmark collection results. #Test counts the tests collected in the benchmark. #Item is the number of entities or dependencies contained in the collected tests. One test might present multiple items. We designed 18 tests that cover 62 entities and 27 tests that cover 160 dependencies; in total, there are 45 tests (45 small programs) with 222 items.

| #Test-Entity | #Item-Denpendency | #Test-Entity | #Item-Denpendency | #Test-Total | #Item-Total |
| :----------: | :---------------: | :----------: | :---------------: | :---------: | :---------: |
|      18      |        62         |      27      |        160        |     45      |     222     |

#### Micro-BenchmarkB for RQ2(Section 4.2.2)

We collected a BenchmarkB to verify the accuracy of nondeterministic dependencies generated by methods. We reused the benchmark collected by the work of PyCG  which provides nondeterministic dependencies at function levels. Their benchmark consists of 206 unique tests, each including source code, the corresponding call dependencies, and a short description. We extended this suite into 233 tests to cover more implicit code behaviors. 

*Category*  in the following table shows the categories of the collected tests, *Description* lists a simple introduction, *Tests* enumerates several tests in each category, and *Count* is the total number of tests we collected. 

|      Category      | Description                                                  |                            Tests                             |    Count    |
| :----------------: | :----------------------------------------------------------- | :----------------------------------------------------------: | :---------: |
|     args_call      | call the parameter objects                                   | assigned_call, call, imported_assigned_call,<br />imported_call, nested_call, param_call |     14      |
|    assignments     | call the assigned objects                                    |          chained, recursive_tuple, starred,  tuple           |     15      |
|      builtins      | call built-in objects                                        |                     functions,map, types                     |     10      |
|      classes       | call first-class classes and their attributes and methods    | assigned_call, assigned_self_call, base_class_attr, <br />base_class_calls_child, call,direct_call, imported_attr_access,<br />imported_call,imported_call_without_init,<br />imported_nested_attr_accessInstance,nested_call,<br />nested_class_calls,parameter_call,return_call,<br />return_call_direct,self_assign_func,self_assignment,<br />self_call,static_method_call,super_class_return,tuple_assignment |     40      |
|       dicts        | call the callable object which is an element of a dict       | add_key,assign,call,ext_key,nested, new_key_param,<br />param,param_key,Return,return_assign,type_coercion,update |     22      |
|    direct_calls    | call the objects returned by functions                       | assigned_call,imported_return_call,return_call,with_parameters |     10      |
|      dynamic       | call the dynamic code through eval function                  |                             eval                             |      2      |
|     functions      | function calls                                               |   assigned_call,assigned_call_lit_param,Call,imported_call   |      4      |
|     generators     | call the callable objects produced by generators             | iter_param,iter_return,Iterable,iterable_assigned,no_iter,yield |     13      |
| higher_order_class | call and return first-class classess                         |                  mixin, return_func, simple                  |  8 （0+8）  |
|      imports       | call functions and objects which are imported in complicated  cases | import_all,import_from,init_import,init_func_import,<br />import_as,parent_import,relative_import,simple_import,<br />relative_import_with_name,submodule_import_from,<br />submodule_import_all,submodule_import,chained_import,<br />submodule_import_as |     14      |
|       kwargs       | call with keyward parameter passing                          |               assigned_call,call,chained_call                |     10      |
|      lambdas       | call anonymous functions                                     | call,calls_parameter,chained_calls,parameter_call,return_call |     14      |
|       lists        | call the callable object which is an element of a list       | comprehension_if,comprehension_val,ext_index,nested,<br />nested_comprehension,param_index,Simple,slice,list_param,slice | 22（16+6）  |
|        mro         | call functions in multiple inheritance                       | basic,basic_init,parents_same_superclass,self_assignment,<br />super_call,two_parents,two_parents_method_defined,self_assignment | 13（10+3）  |
|      returns       | return functions in complicated cases                        |     call,imported_call,nested_import_call,return_complex     |     12      |
|   unsure_lookup    | look up unsure names in branches or loops                    |                    branch,class_def,loop                     | 10 （0+10） |
|      SUMMARY       | /                                                            |                              /                               | 233(206+27) |

In the table, the "count" column with the format "n(0+n)" indicates that we have added a new type of implicit dependency and included n additional tests. Similarly, the "count" column with the format "m(k+n)" (where m equals k plus n) indicates that we have expanded the existing implicit dependency category collected by PyCG by adding n new tests. 

##### The newly added categories

When collecting implicit (i.e., nondeterministic) dependency datasets, we initially selected benchmarks used by PyCG. During subsequent research and analysis, we identified certain implicit dependency types missing from PyCG's dataset. As a result, we introduced two new types of implicit dependencies as test tests: "high_order_class" and "unsure_lookup"  to enlarge and enrich the benchmark.

Let's consider the code under "\Data\RQ2\micro-benchmark B\Benchmark-newlyaddedbyPyAnalyzer\higher_order_class\return_func" as an example:

```python
 1 	def create_class():
 2 		def fun():
 3 			...
 4 
 5 		class Simple:
 6 			def method(self):
 7 				return fun
 8 
 9 		return Simple
10
11
12	cls = create_class()
13	obj = cls()
14	func = obj.method()
15	func()
```

This code contains an implicit dependency, which is the implicit reliance on the `fun` function. In the above code, the create_class function returns a class called Simple, which contains a method named method. This method returns a reference to the function fun. First, the create_class() function is called, which returns a reference to the Simple class, and this reference is assigned to the variable cls. Next, an instance of the Simple class is created by calling cls(), and this instance is assigned to the variable obj. Then, by calling obj.method(), we obtain a reference to the function fun, and this reference is assigned to the variable func. Finally, calling func() actually invokes the fun() function.Although the fun function is defined within the create_class function, it is returned by the method method and called through func = obj.method() and func(). When func() is called, it effectively calls the fun() function, but the name fun is not directly referenced in the code, creating an implicit dependency.

##### The newly added tests to existing categories:

We have also added some additional tests to the PyCG dataset to cover more scenarios of implicit dependencies within the existing categories. This allows us to capture a wider range of implicit dependency situations and improve the dataset's comprehensiveness.

Let's consider the code under "\Data\RQ2\micro-benchmark B\Benchmark-newlyaddedbyPyAnalyzer\lists\list_param" as an example:

```python
 1 	def func1():
 2 		pass
 3 
 4 	def func2():
 5 		pass
 6 
 7 	def func3():
 8 		pass
 9 
10	ls = [func1, func2, func3]
11
12	def func(l):
13		for f in l:
14			f()
15
16	func(ls)
```

This test demonstrates calling function objects stored in a list.

The above code defines three functions: func1(), func2(), and func3(), each of which does nothing (pass statement). Then, it creates a list ls containing references to these three functions.  It defines a function func(l) that takes a list of functions as an argument and calls each function in the list. Finally,  it calls the func() function passing the ls list as an argument, which results in calling all three functions func1(), func2(), and func3() in succession.

#### Macro-BenchmarkC and Macro-BenchmarkD for RQ3 study(Section 4.2.3)

This section provides a detailed description of the two benchmarks. 

We collected two macro-benchmarks from real-world projects. Macro-BenchmarkC reuses the macro-benchmarks provided by PyCG, containing function-level dependencies from 5 real-world projects. The work of PyCG manually created this benchmark.

To construct a larger size of benchmarks, we automatically built the BenchmarkD to assess the recall of different methods when analyzing real-world projects. We collected ground-truth dependencies from execution traces that record deterministic and nondeterministic code behaviors. 

##### Collection process

1. First, we used the 191 projects collected in Section RQ4. We then selected 191 × 38.7%=74 projects since PyCG failed to scan the others and reported errors like MEMORY\_ERROR, TIME_OUT and ERROR. 
2. Next, we preserved the projects that contain sufficient tess.   Driven by tests, we utilized MonkeyType monkeytype to collect runtime information from execution traces, retrofitting run-time types to the corresponding code. 
3. After that, we employed  Pyre, maintained by Facebook, to directly export ground-truth call dependencies from type-decorated code. We further removed the outlier dependencies (introduced by Pyre) where their source entities are beyond the project code. 

To reduce possible bias, we also filtered out the projects where the collected ground-truth dependencies account for less than 10 items. Those dependencies correspond to the  macro-benchmark since they were generated from execution traces of real-world projects.  Please note that Pyre provides additional functionalities like type error detection. We only leveraged its basic command to dump function call dependencies. 

The following table summarizes collection results. We finally collected 8,233 ground-truth dependency items at function levels from execution traces of 54 projects. 

##### Comparison

The two macro-benchmarks consist of dependencies from 59 real-world projects with 255KSLOC.The table below summarizes collection results:

| Benchmark C | #SLOC  | Benchmark D |  #SLOC  |
| :---------: | :----: | :---------: | :-----: |
| 5 projects  | 10,031 | 54 projects | 245,167 |

### Project Collection(Section 4.3)

We collected the top-starred projects from GitHub to assess multiple tools’ efficiency for RQ4. Concretely, we programmatically access the GitHub search API endpoint for Python projects that are sorted based on star count descending. We initially accessed the top 200 projects. We further excluded toy and demo-like projects and tutorials. We finally collected 191 projects for method efficiency testing. The 191 projects have 10M SLOC, with diverse sizes of 19 ∼ 700𝐾 SLOC.

The table below illustrates the performance comparison of our PyAnalyzer and PyCG in the performance testing experiments. Our dataset has been expanded to 191 projects, and all our tools are capable of running successfully. However, PyCG can only run on 74 small to medium-sized projects and encounters errors on other projects. The maximum code size that PYCG can analyze is 26966.

| Tool       | Successful Runs | Failed Runs | Max Sloc |
| ---------- | :-------------: | :---------: | :------: |
| PyCG       |       74        |     117     |  26966   |
| PyAnalyzer |       191       |      0      |  746786  |

## Evaluation results(Section 5)

### Efficiency Measures(Section 5.4)

In the final analysis, we randomly selected 10 projects each from a pool of 89 projects with a code size less than 10kLOC and 102 projects with a code size greater than 10kLOC for evaluation. The following figure represents the completion time and peak memory consumption of various analysis tools on projects with a code size less than 10kLOC. The following figure shows that our PyAnalyzer is more time-efficient and memory-efficient when analyzing one project with 𝑆𝐿𝑂𝐶 ≤ 10𝐾.

<p align="center"><img src="Data\RQ4\results\less.png"/></p>

The following line chart depicts the completion time of various analysis tools on projects with a code size more than 10kLOC. When comparing the analysis on projects with a code size greater than 10kLOC, PyCG is not included in the comparison  since PyCG (our baseline) failed to scan the others and reported errors like MEMORY_ERROR, TIME_OUT and ERROR.  When scanning projects with sizes between ∼ 10𝐾 and ∼ 750𝐾, PyAnalyzer spends less time than baselines except for the commercial Understand. PyAnalyzer requires a little more memory amount than Understand and Depends, while taking less memory than the other four baselines.

<p align="center"><img src="Data\RQ4\results\more.png"/></p>

## LSIF

The LSIF outputs of PyAnalyzer improve developers’ experience with Python code through reliable dependencies. Our pyAnalyzer also dumps code dependencies into LSIF format. 

LSIF is a standard format for persisted code analyzer output, built upon the Language Server Protocol (LSP). It allows code editors and IDEs to provide features like autocomplete and find references. PyAnalyzer implemented common LSP requests such as textDocument/foldingRange and textDocument/references. 

The followings show a part of the analysis results of our PyAnalyzer (The analysis results are stored in the LISF format) obtained on the open-source project "sherlock-project/sherlock" from GitHub. 

- `workspaceRoot`: This object represents a source file. The source file is located at the workspace root.
- `version`: The version information.
- `positionEncoding`: The character position encoding.

- `id`: A unique identifier for this object.
- `type`: Indicates that this object's type.
- `label`: Specifies the type of the object.
- `start` and `end`: Indicate the starting and ending positions (line and character positions) of the range.
- `tag`: A tag object describing attributes of this range. 

```
{"id": 1, "type": "vertex", "label": "metaData", "version": "0.6.0-next.7", "positionEncoding": "utf-16"}
{"id": 2, "type": "vertex", "label": "source", "workspaceRoot": "file:///D:/test/UsabilityTest/repo/sherlock"}
{"id": 3, "type": "vertex", "label": "capabilities", "hoverProvider": true, "declarationProvider": false, "definitionProvider": true, "typeDefinitionProvider": true, "referencesProvider": true, "documentSymbolProvider": true, "foldingRangeProvider": true, "diagnosticProvider": true}
{"id": 4, "type": "vertex", "label": "document", "uri": "file:///d:/test/usabilitytest/repo/sherlock/sherlock/notify.py", "languageId": "python", "contents": "IiIiU2hlcmxvY2sgTm90aWZ5IE1vZHVsZQ0KDQpUaGlzIG1vZHVsZSBkZWZpbmVzIHRoZSBvYmplY3RzIGZvciBub3RpZnlpbmcgdGhlIGNhbGxlciBhYm91dCB0aGUNCnJlc3VsdHMgb2YgcXVlcmllcy4NCiIiIg0KZnJvbSByZXN1bHQgaW1wb3J0IFF1ZXJ5U3RhdHVzDQpmcm9tIGNvbG9yYW1hIGltcG9ydCBGb3JlLCBTdHlsZSwgaW5pdA0KDQoNCmNsYXN zIFF1ZXJ5Tm90aWZ5KCk6DQogICAgIiIiUXVlcnkgTm90aWZ5IE9iamVjdC4NCg0KICAgIEJhc2UgY2xhc3MgdGhhdCBkZXNjcmliZXMgbWV0aG9kcyBhdmFpbGFibGUgdG8gbm90aWZ5IHRoZSByZXN1bHRzIG9mDQogICAgYSBxdWVyeS4NCiAgICBJdCBpcyBpbnRlbmRlZCB0aGF0IG90aGVyIGNsYXNzZXMgaW5oZXJpdCBmcm9tIHRoaXMgYmFzZSBjbGFzcyBhbmQNCiAgICBvdmVycmlkZSB0aGUgbWV0aG9kcyB0byBpbXBsZW1lbnQgc3BlY2lmaWMgZnVuY3Rpb25hbGl0eS4NCiAgICAiIiINCiAgICBkZWYgX19pbml0X18oc2VsZiwgcmVzdWx0PU5vbmUpOg0KICAgICAgICAiIiJDcmVhdGUgUXVlcnkgTm90aWZ5IE9iamVjdC4NCg0KICAgICAgICBDb250YWlucyBpbmZvcm1hdGlvbiBhYm91dCBhIHNwZWNpZmljIG1ldGhvZCBvZiBub3RpZnlpbmcgdGhlIHJlc3VsdHMNCiAgICAgICAgb2YgYSBxdWVyeS4NCg0KICAgICAgICBLZXl3b3JkIEFyZ3VtZW50czoNCiAgICAgICAgc2VsZiAgICAgICAgICAgICAgICAgICAtLSBUaGlzIG9iamVjdC4NCiAgICAgICAgcmVzdWx0ICAgICAgICAgICAgICAgICAtLSBPYmplY3Qgb2YgdHlwZSBRdWVyeVJlc3VsdCgpIGNvbnRhaW5pbmcNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXN1bHRzIGZvciB0aGlzIHF1ZXJ5Lg0KDQogICAgICAgIFJldHVybiBWYWx1ZToNCiAgICAgICAgTm90aGluZy4NCiAgICAgICAgIiIiDQoNCiAgICAgICAgc2VsZi5yZXN1bHQgPSByZXN1bHQNCg0KICAgICAgICByZXR1cm4NCg0KICAgIGRlZiBzdGFydChzZWxmLCBtZXNzYWdlPU5vbmUpOg0KICAgICAgICAiIiJOb3RpZnkgU3RhcnQuDQoNCiAgICAgICAgTm90aWZ5IG1ldGhvZCBmb3Igc3RhcnQgb2YgcXVlcnkuICBUaGlzIG1ldGhvZCB3aWxsIGJlIGNhbGxlZCBiZWZvcmUNCiAgICAgICAgYW55IHF1ZXJpZXMgYXJlIHBlcmZvcm1lZC4gIFRoaXMgbWV0aG9kIHdpbGwgdHlwaWNhbGx5IGJlDQogICAgICAgIG92ZXJyaWRkZW4gYnkgaGlnaGVyIGxldmVsIGNsYXNzZXMgdGhhdCB3aWxsIGluaGVyaXQgZnJvbSBpdC4NCg0KICAgICAgICBLZXl3b3JkIEFyZ3VtZW50czoNCiAgICAgICAgc2VsZiAgICAgICAgICAgICAgICAgICAtLSBUaGlzIG9iamVjdC4NCiAgICAgICAgbWVzc2FnZSAgICAgICAgICAgICAgICAtLSBPYmplY3QgdGhhdCBpcyB1c2VkIHRvIGdpdmUgY29udGV4dCB0byBzdGFydA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9mIHF1ZXJ5Lg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIERlZmF1bHQgaXMgTm9uZS4NCg0KICAgICAgICBSZXR1cm4gVmFsdWU6DQogICAgICAgIE5vdGhpbmcuDQogICAgICAgICIiIg0KDQogICAgICAgIHJldHVybg0KDQogICAgZGVmIHVwZGF0ZShzZWxmLCByZXN1bHQpOg0KICAgICAgICAiIiJOb3RpZnkgVXBkYXRlLg0KDQogICAgICAgIE5vdGlmeSBtZXRob2QgZm9yIHF1ZXJ5IHJlc3VsdC4gIFRoaXMgbWV0aG9kIHdpbGwgdHlwaWNhbGx5IGJlDQogICAgICAgIG92ZXJyaWRkZW4gYnkgaGlnaGVyIGxldmVsIGNsYXNzZXMgdGhhdCB3aWxsIGluaGVyaXQgZnJvbSBpdC4NCg0KICAgICAgICBLZXl3b3JkIEFyZ3VtZW50czoNCiAgICAgICAgc2VsZiAgICAgICAgICAgICAgICAgICAtLSBUaGlzIG9iamVjdC4NCiAgICAgICAgcmVzdWx0ICAgICAgICAgICAgICAgICAtLSBPYmplY3Qgb2YgdHlwZSBRdWVyeVJlc3VsdCgpIGNvbnRhaW5pbmcNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXN1bHRzIGZvciB0aGlzIHF1ZXJ5Lg0KDQogICAgICAgIFJldHVybiBWYWx1ZToNCiAgICAgICAgTm90aGluZy4NCiAgICAgICAgIiIiDQoNCiAgICAgICAgc2VsZi5yZXN1bHQgPSByZXN1bHQNCg0KICAgICAgICByZXR1cm4NCg0KICAgIGRlZiBmaW5pc2goc2VsZiwgbWVzc2FnZT1Ob25lKToNCiAgICAgICAgIiIiTm90aWZ5IEZpbmlzaC4NCg0KICAgICAgICBOb3RpZnkgbWV0aG9kIGZvciBmaW5pc2ggb2YgcXVlcnkuICBUaGlzIG1ldGhvZCB3aWxsIGJlIGNhbGxlZCBhZnRlcg0KICAgICAgICBhbGwgcXVlcmllcyBoYXZlIGJlZW4gcGVyZm9ybWVkLiAgVGhpcyBtZXRob2Qgd2lsbCB0eXBpY2FsbHkgYmUNCiAgICAgICAgb3ZlcnJpZGRlbiBieSBoaWdoZXIgbGV2ZWwgY2xhc3NlcyB0aGF0IHdpbGwgaW5oZXJpdCBmcm9tIGl0Lg0KDQogICAgICAgIEtleXdvcmQgQXJndW1lbnRzOg0KICAgICAgICBzZWxmICAgICAgICAgICAgICAgICAgIC0tIFRoaXMgb2JqZWN0Lg0KICAgICAgICBtZXNzYWdlICAgICAgICAgICAgICAgIC0tIE9iamVjdCB0aGF0IGlzIHVzZWQgdG8gZ2l2ZSBjb250ZXh0IHRvIHN0YXJ0DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgb2YgcXVlcnkuDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgRGVmYXVsdCBpcyBOb25lLg0KDQogICAgICAgIFJldHVybiBWYWx1ZToNCiAgICAgICAgTm90aGluZy4NCiAgICAgICAgIiIiDQoNCiAgICAgICAgcmV0dXJuDQoNCiAgICBkZWYgX19zdHJfXyhzZWxmKToNCiAgICAgICAgIiIiQ29udmVydCBPYmplY3QgVG8gU3RyaW5nLg0KDQogICAgICAgIEtleXdvcmQgQXJndW1lbnRzOg0KICAgICAgICBzZWxmICAgICAgICAgICAgICAgICAgIC0tIFRoaXMgb2JqZWN0Lg0KDQogICAgICAgIFJldHVybiBWYWx1ZToNCiAgICAgICAgTmljZWx5IGZvcm1hdHRlZCBzdHJpbmcgdG8gZ2V0IGluZm9ybWF0aW9uIGFib3V0IHRoaXMgb2JqZWN0Lg0KICAgICAgICAiIiINCiAgICAgICAgcmVzdWx0ID0gc3RyKHNlbGYucmVzdWx0KQ0KDQogICAgICAgIHJldHVybiByZXN1bHQNCg0KDQpjbGFzcyBRdWVyeU5vdGlmeVByaW50KFF1ZXJ5Tm90aWZ5KToNCiAgICAiIiJRdWVyeSBOb3RpZnkgUHJpbnQgT2JqZWN0Lg0KDQogICAgUXVlcnkgbm90aWZ5IGNsYXNzIHRoYXQgcHJpbnRzIHJlc3VsdHMuDQogICAgIiIiDQogICAgZGVmIF9faW5pdF9fKHNlbGYsIHJlc3VsdD1Ob25lLCB2ZXJib3NlPUZhbHNlLCBjb2xvcj1UcnVlLCBwcmludF9hbGw9RmFsc2UpOg0KICAgICAgICAiIiJDcmVhdGUgUXVlcnkgTm90aWZ5IFByaW50IE9iamVjdC4NCg0KICAgICAgICBDb250YWlucyBpbmZvcm1hdGlvbiBhYm91dCBhIHNwZWNpZmljIG1ldGhvZCBvZiBub3RpZnlpbmcgdGhlIHJlc3VsdHMNCiAgICAgICAgb2YgYSBxdWVyeS4NCg0KICAgICAgICBLZXl3b3JkIEFyZ3VtZW50czoNCiAgICAgICAgc2VsZiAgICAgICAgICAgICAgICAgICAtLSBUaGlzIG9iamVjdC4NCiAgICAgICAgcmVzdWx0ICAgICAgICAgICAgICAgICAtLSBPYmplY3Qgb2YgdHlwZSBRdWVyeVJlc3VsdCgpIGNvbnRhaW5pbmcNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXN1bHRzIGZvciB0aGlzIHF1ZXJ5Lg0KICAgICAgICB2ZXJib3NlICAgICAgICAgICAgICAgIC0tIEJvb2xlYW4gaW5kaWNhdGluZyB3aGV0aGVyIHRvIGdpdmUgdmVyYm9zZSBvdXRwdXQuDQogICAgICAgIHByaW50X2FsbCAgICAgICAgICAgICAgLS0gQm9vbGVhbiBpbmRpY2F0aW5nIHdoZXRoZXIgdG8gb25seSBwcmludCBhbGwgc2l0ZXMsIGluY2x1ZGluZyBub3QgZm91bmQuDQogICAgICAgIGNvbG9yICAgICAgICAgICAgICAgICAgLS0gQm9vbGVhbiBpbmRpY2F0aW5nIHdoZXRoZXIgdG8gY29sb3IgdGVybWluYWwgb3V0cHV0DQoNCiAgICAgICAgUmV0dXJuIFZhbHVlOg0KICAgICAgICBOb3RoaW5nLg0KICAgICAgICAiIiINCg0KICAgICAgICAjIENvbG9yYW1hIG1vZHVsZSdzIGluaXRpYWxpemF0aW9uLg0KICAgICAgICBpbml0KGF1dG9yZXNldD1UcnVlKQ0KDQogICAgICAgIHN1cGVyKCkuX19pbml0X18ocmVzdWx0KQ0KICAgICAgICBzZWxmLnZlcmJvc2UgPSB2ZXJib3NlDQogICAgICAgIHNlbGYucHJpbnRfYWxsID0gcHJpbnRfYWxsDQogICAgICAgIHNlbGYuY29sb3IgPSBjb2xvcg0KDQogICAgICAgIHJldHVybg0KDQogICAgZGVmIHN0YXJ0KHNlbGYsIG1lc3NhZ2UpOg0KICAgICAgICAiIiJOb3RpZnkgU3RhcnQuDQoNCiAgICAgICAgV2lsbCBwcmludCB0aGUgdGl0bGUgdG8gdGhlIHN0YW5kYXJkIG91dHB1dC4NCg0KICAgICAgICBLZXl3b3JkIEFyZ3VtZW50czoNCiAgICAgICAgc2VsZiAgICAgICAgICAgICAgICAgICAtLSBUaGlzIG9iamVjdC4NCiAgICAgICAgbWVzc2FnZSAgICAgICAgICAgICAgICAtLSBTdHJpbmcgY29udGFpbmluZyB1c2VybmFtZSB0aGF0IHRoZSBzZXJpZXMNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBvZiBxdWVyaWVzIGFyZSBhYm91dC4NCg0KICAgICAgICBSZXR1cm4gVmFsdWU6DQogICAgICAgIE5vdGhpbmcuDQogICAgICAgICIiIg0KDQogICAgICAgIHRpdGxlID0gIkNoZWNraW5nIHVzZXJuYW1lIg0KICAgICAgICBpZiBzZWxmLmNvbG9yOg0KICAgICAgICAgICAgcHJpbnQoU3R5bGUuQlJJR0hUICsgRm9yZS5HUkVFTiArICJbIiArDQogICAgICAgICAgICAgICAgRm9yZS5ZRUxMT1cgKyAiKiIgKw0KICAgICAgICAgICAgICAgIEZvcmUuR1JFRU4gKyBmIl0ge3RpdGxlfSIgKw0KICAgICAgICAgICAgICAgIEZvcmUuV0hJVEUgKyBmIiB7bWVzc2FnZX0iICsNCiAgICAgICAgICAgICAgICBGb3JlLkdSRUVOICsgIiBvbjoiKQ0KICAgICAgICBlbHNlOg0KICAgICAgICAgICAgcHJpbnQoZiJbKl0ge3RpdGxlfSB7bWVzc2FnZX0gb246IikNCg0KICAgICAgICByZXR1cm4NCg0KICAgIGRlZiB1cGRhdGUoc2VsZiwgcmVzdWx0KToNCiAgICAgICAgIiIiTm90aWZ5IFVwZGF0ZS4NCg0KICAgICAgICBXaWxsIHByaW50IHRoZSBxdWVyeSByZXN1bHQgdG8gdGhlIHN0YW5kYXJkIG91dHB1dC4NCg0KICAgICAgICBLZXl3b3JkIEFyZ3VtZW50czoNCiAgICAgICAgc2VsZiAgICAgICAgICAgICAgICAgICAtLSBUaGlzIG9iamVjdC4NCiAgICAgICAgcmVzdWx0ICAgICAgICAgICAgICAgICAtLSBPYmplY3Qgb2YgdHlwZSBRdWVyeVJlc3VsdCgpIGNvbnRhaW5pbmcNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXN1bHRzIGZvciB0aGlzIHF1ZXJ5Lg0KDQogICAgICAgIFJldHVybiBWYWx1ZToNCiAgICAgICAgTm90aGluZy4NCiAgICAgICAgIiIiDQogICAgICAgIHNlbGYucmVzdWx0ID0gcmVzdWx0DQoNCiAgICAgICAgaWYgc2VsZi52ZXJib3NlID09IEZhbHNlIG9yIHNlbGYucmVzdWx0LnF1ZXJ5X3RpbWUgaXMgTm9uZToNCiAgICAgICAgICAgIHJlc3BvbnNlX3RpbWVfdGV4dCA9ICIiDQogICAgICAgIGVsc2U6DQogICAgICAgICAgICByZXNwb25zZV90aW1lX3RleHQgPSBmIiBbe3JvdW5kKHNlbGYucmVzdWx0LnF1ZXJ5X3RpbWUgKiAxMDAwKX0gbXNdIg0KDQogICAgICAgICMgT3V0cHV0IHRvIHRoZSB0ZXJtaW5hbCBpcyBkZXNpcmVkLg0KICAgICAgICBpZiByZXN1bHQuc3RhdHVzID09IFF1ZXJ5U3RhdHVzLkNMQUlNRUQ6DQogICAgICAgICAgICBpZiBzZWxmLmNvbG9yOg0KICAgICAgICAgICAgICAgIHByaW50KChTdHlsZS5CUklHSFQgKyBGb3JlLldISVRFICsgIlsiICsNCiAgICAgICAgICAgICAgICAgICAgICAgRm9yZS5HUkVFTiArICIrIiArDQogICAgICAgICAgICAgICAgICAgICAgIEZvcmUuV0hJVEUgKyAiXSIgKw0KICAgICAgICAgICAgICAgICAgICAgICByZXNwb25zZV90aW1lX3RleHQgKw0KICAgICAgICAgICAgICAgICAgICAgICBGb3JlLkdSRUVOICsNCiAgICAgICAgICAgICAgICAgICAgICAgZiIge3NlbGYucmVzdWx0LnNpdGVfbmFtZX06ICIgKw0KICAgICAgICAgICAgICAgICAgICAgICBTdHlsZS5SRVNFVF9BTEwgKw0KICAgICAgICAgICAgICAgICAgICAgICBmIntzZWxmLnJlc3VsdC5zaXRlX3VybF91c2VyfSIpKQ0KICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICBwcmludChmIlsrXXtyZXNwb25zZV90aW1lX3RleHR9IHtzZWxmLnJlc3VsdC5zaXRlX25hbWV9OiB7c2VsZi5yZXN1bHQuc2l0ZV91cmxfdXNlcn0iKQ0KDQogICAgICAgIGVsaWYgcmVzdWx0LnN0YXR1cyA9PSBRdWVyeVN0YXR1cy5BVkFJTEFCTEU6DQogICAgICAgICAgICBpZiBzZWxmLnByaW50X2FsbDoNCiAgICAgICAgICAgICAgICBpZiBzZWxmLmNvbG9yOg0KICAgICAgICAgICAgICAgICAgICBwcmludCgoU3R5bGUuQlJJR0hUICsgRm9yZS5XSElURSArICJbIiArDQogICAgICAgICAgICAgICAgICAgICAgICBGb3JlLlJFRCArICItIiArDQogICAgICAgICAgICAgICAgICAgICAgICBGb3JlLldISVRFICsgIl0iICsNCiAgICAgICAgICAgICAgICAgICAgICAgIHJlc3BvbnNlX3RpbWVfdGV4dCArDQogICAgICAgICAgICAgICAgICAgICAgICBGb3JlLkdSRUVOICsgZiIge3NlbGYucmVzdWx0LnNpdGVfbmFtZX06IiArDQogICAgICAgICAgICAgICAgICAgICAgICBGb3JlLllFTExPVyArICIgTm90IEZvdW5kISIpKQ0KICAgICAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgICAgIHByaW50KGYiWy1de3Jlc3BvbnNlX3RpbWVfdGV4dH0ge3NlbGYucmVzdWx0LnNpdGVfbmFtZX06IE5vdCBGb3VuZCEiKQ0KDQogICAgICAgIGVsaWYgcmVzdWx0LnN0YXR1cyA9PSBRdWVyeVN0YXR1cy5VTktOT1dOOg0KICAgICAgICAgICAgaWYgc2VsZi5wcmludF9hbGw6DQogICAgICAgICAgICAgICAgaWYgc2VsZi5jb2xvcjoNCiAgICAgICAgICAgICAgICAgICAgcHJpbnQoU3R5bGUuQlJJR0hUICsgRm9yZS5XSElURSArICJbIiArDQogICAgICAgICAgICAgICAgICAgICAgICAgIEZvcmUuUkVEICsgIi0iICsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgRm9yZS5XSElURSArICJdIiArDQogICAgICAgICAgICAgICAgICAgICAgICAgIEZvcmUuR1JFRU4gKyBmIiB7c2VsZi5yZXN1bHQuc2l0ZV9uYW1lfToiICsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgRm9yZS5SRUQgKyBmIiB7c2VsZi5yZXN1bHQuY29udGV4dH0iICsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgRm9yZS5ZRUxMT1cgKyBmIiAiKQ0KICAgICAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgICAgIHByaW50KGYiWy1dIHtzZWxmLnJlc3VsdC5zaXRlX25hbWV9OiB7c2VsZi5yZXN1bHQuY29udGV4dH0gIikNCg0KICAgICAgICBlbGlmIHJlc3VsdC5zdGF0dXMgPT0gUXVlcnlTdGF0dXMuSUxMRUdBTDoNCiAgICAgICAgICAgIGlmIHNlbGYucHJpbnRfYWxsOg0KICAgICAgICAgICAgICAgIG1zZyA9ICJJbGxlZ2FsIFVzZXJuYW1lIEZvcm1hdCBGb3IgVGhpcyBTaXRlISINCiAgICAgICAgICAgICAgICBpZiBzZWxmLmNvbG9yOg0KICAgICAgICAgICAgICAgICAgICBwcmludCgoU3R5bGUuQlJJR0hUICsgRm9yZS5XSElURSArICJbIiArDQogICAgICAgICAgICAgICAgICAgICAgICAgICBGb3JlLlJFRCArICItIiArDQogICAgICAgICAgICAgICAgICAgICAgICAgICBGb3JlLldISVRFICsgIl0iICsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgIEZvcmUuR1JFRU4gKyBmIiB7c2VsZi5yZXN1bHQuc2l0ZV9uYW1lfToiICsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgIEZvcmUuWUVMTE9XICsgZiIge21zZ30iKSkNCiAgICAgICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgICAgICBwcmludChmIlstXSB7c2VsZi5yZXN1bHQuc2l0ZV9uYW1lfSB7bXNnfSIpDQoNCiAgICAgICAgZWxzZToNCiAgICAgICAgICAgICMgSXQgc2hvdWxkIGJlIGltcG9zc2libGUgdG8gZXZlciBnZXQgaGVyZS4uLg0KICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlVua25vd24gUXVlcnkgU3RhdHVzICd7c3RyKHJlc3VsdC5zdGF0dXMpfScgZm9yICINCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJzaXRlICd7c2VsZi5yZXN1bHQuc2l0ZV9uYW1lfSciKQ0KDQogICAgICAgIHJldHVybg0KDQogICAgZGVmIF9fc3RyX18oc2VsZik6DQogICAgICAgICIiIkNvbnZlcnQgT2JqZWN0IFRvIFN0cmluZy4NCg0KICAgICAgICBLZXl3b3JkIEFyZ3VtZW50czoNCiAgICAgICAgc2VsZiAgICAgICAgICAgICAgICAgICAtLSBUaGlzIG9iamVjdC4NCg0KICAgICAgICBSZXR1cm4gVmFsdWU6DQogICAgICAgIE5pY2VseSBmb3JtYXR0ZWQgc3RyaW5nIHRvIGdldCBpbmZvcm1hdGlvbiBhYm91dCB0aGlzIG9iamVjdC4NCiAgICAgICAgIiIiDQogICAgICAgIHJlc3VsdCA9IHN0cihzZWxmLnJlc3VsdCkNCg0KICAgICAgICByZXR1cm4gcmVzdWx0DQo="}
{"id": 5, "type": "vertex", "label": "range", "start": {"line": 9, "character": 12}, "end": {"line": 9, "character": 23}, "tag": {"type": "definition", "text": "QueryNotify", "kind": 5, "fullRange": {"start": {"line": 9, "character": 6}, "end": {"line": 104, "character": 21}}}}
{"id": 6, "type": "vertex", "label": "resultSet"}
{"id": 7, "type": "edge", "label": "next", "outV": 5, "inV": 6}
{"id": 8, "type": "vertex", "label": "hoverResult", "result": {"contents": [{"language": "python", "value": "EntKind.Class QueryNotify"}, {"language": "python", "value": "Some custom contents..."}]}}
{"id": 9, "type": "edge", "label": "textDocument/hover", "outV": 6, "inV": 8}
{"id": 10, "type": "vertex", "label": "range", "start": {"line": 17, "character": 8}, "end": {"line": 34, "character": 14}}
{"id": 11, "type": "vertex", "label": "resultSet"}
{"id": 12, "type": "edge", "label": "next", "outV": 10, "inV": 11}
{"id": 13, "type": "vertex", "label": "hoverResult", "result": {"contents": [{"language": "python", "value": "EntKind.Method __init__"}, {"language": "python", "value": "def __init__(self: sherlock.sherlock.notify.QueryNotify, result: Any) -> Any"}, {"language": "python", "value": "Some custom contents..."}]}}
{"id": 14, "type": "edge", "label": "textDocument/hover", "outV": 11, "inV": 13}
{"id": 15, "type": "vertex", "label": "range", "start": {"line": 17, "character": 17}, "end": {"line": 17, "character": 21}}
{"id": 16, "type": "vertex", "label": "resultSet"}
...
```
