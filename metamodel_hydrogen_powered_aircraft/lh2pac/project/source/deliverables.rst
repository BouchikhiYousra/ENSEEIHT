Deliverables
============

Code
----

A series of Python scripts containing:

* Python code,
* documentation.

These scripts must be placed in the directory **project/results**.

Moreover, they must be properly formatted
in order to be correctly compiled when using **make html**:

* the header docstring will be converted into an HTML block,
* the Python comments starting with ``#%%`` will be converted into HTML blocks,
* the Python code will be executed,
* the text resulting from the method ``print``
  and the figure resulting from the Matplotlib ``show`` method
  will benefit from a special rendering.

.. note::

   You do not need to compile the project every time you change the Python script.
   You can use this Python script like any other Python script
   and compile the project only after the script writing is finished.
   When the project is compiled,
   only the scripts that have evolved are recompiled.

Here is an example of a well-formatted and documented Python code:

.. code::

   r"""
   Sum function
   ============

   In this example,
   we implement a function summing the elements of a vector :math:`x\in\mathbb{R}^d`:

   .. math::

       f(x)=\sum_{i=1}^d x_i
   """
   from numpy import array

   #%%
   # Firstly,
   # we define the function:
   def f(x):
       return x.sum()

   #%%
   # Then,
   # we evaluate this function from the input vector :math:`x=[1,2]`:
   y = f(array([1.,2.]))

   #%%
   # Lastly,
   # we print the output value:
   print(y)

   # Contrarily to the previous ones,
   # this comment will not be converted into an HTML block
   # because it does not start with #%%.
   # It will appear as a Python comment.

Report
------

An :ref:`reST-based <rest>` HTML report containing:

* an introduction,
* a section for each `sub-problem <problem.html>`_, ending with a synthesis.
* a general conclusion.

The syntheses and the general conclusion summarize the main facts
for someone who does not want to read the details.

Furthermore, all the results provided must be interpreted.

The reST files must be placed in the directory **project/source/report**
and referenced in **project/source/report/index.rst**, e.g.

.. code-block::

    Report
    ======

    .. toctree::
       :maxdepth: 2
       :caption: Table of contents:

       introduction
       part1
       part2
       part3
       conclusion

where the list contains the names of the files without their suffixes,
e.g. *introduction* instead of *introduction.rst*.