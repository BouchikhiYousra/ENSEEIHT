.. _rest:

Introduction to the reST syntax
===============================


`reStructuredText (reST) <https://docutils.sourceforge.io/rst.html>`_ is an easy-to-read,
what-you-see-is-what-you-get plaintext markup syntax and parser system.
This is the default plaintext markup language used by `Sphinx <https://www.sphinx-doc.org/>`_,
the generator of the current HTML project.
Here is a short but normally sufficient introduction to reST.
For a deeper insight, please refer to `the Sphinx documentation <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_.

Sections
--------

Split a page into sections:

.. code-block:: rst

    Main title
    ==========

    Sub-title
    ---------

    Sub-sub-title
    ^^^^^^^^^^^^^

Paragraphs
----------

Separate paragraph with blank lines.

.. code-block:: rst

    This is a paragraph.
    This is the same paragraph.

    This is a new paragraph separated from the previous one with a blank line.

This is a paragraph.
This is the same paragraph.

This is a new paragraph separated from the previous one with a blank line.

Text formatting
---------------

Surround a text with one asterisk
and without whitespace between the text and the asterisk.

.. code-block:: rst

    Put a expression in *italics*.

    Put a expression in **bold**.

    Cannot but an expression both in ***italics and bold***.

Put a expression in *italics*.

Put a expression in **bold**.

Cannot but an expression both in ***italics and bold***.

Hyperlink
---------

External
^^^^^^^^

Use ```expression <url>`_``.

This is an hyperlink to an external content: `DuckDuckGo <https://duckduckgo.com/>`_.

Internal
^^^^^^^^

Place a label ``.. _my_label:`` just before the element to be referenced
(do not forget the starting underscore)
and refer to it with ``:ref:`my_label```.

This is an hyperlink to an internal content: :ref:`image_example`
located on the current page.

This is another hyperlink to an internal content: :ref:`project_index`
located on the index page of the project.

Lists
-----

Unnumbered list
^^^^^^^^^^^^^^^

.. code-block:: rst

    * A item.
    * Another item.

      * A sub-item (pay attention to the indentation!).
      * Another sub-item.

    * Another item
      written on two lines (pay attention to the indentation!).

      #. A first sub-item.
      #. A second sub-item.

* A item.
* Another item.

  * A sub-item (pay attention to the indentation!).
  * Another sub-item.

* Another item
  written on two lines (pay attention to the indentation!).

  #. A first sub-item.
  #. A second sub-item.

Numbered list
^^^^^^^^^^^^^

.. code-block:: rst

    #. A item.
    #. A second item.

       * A sub-item (pay attention to the indentation!).
       * Another sub-item.

    #. A third item
       written on two lines (pay attention to the indentation!).

       #. A first sub-item.
       #. A second sub-item.

#. A item.
#. A second item.

   * A sub-item (pay attention to the indentation!).
   * Another sub-item.

#. A third item
   written on two lines (pay attention to the indentation!).

   #. A first sub-item.
   #. A second sub-item.

Code insertion
--------------

.. code-block:: rst

    Insert inline code: ``y = f(x)``

Insert inline code: ``y = f(x)``

Insert a block code using the *code* directive:

.. code-block:: rst

    .. code::

       def f(x):
          return 2*x

.. code::

   def f(x):
      return 2*x

.. code-block:: rst

    Insert a block code ending a sentence with two colons,
    indenting the block and surrounding it with blank lines::

       def f(x):
          return 2*x

    After the blank line and deindentation,
    this is a normal text paragraph again.

Insert a block code ending a sentence with two colons,
indenting the block and surrounding it with blank lines::

   def f(x):
      return 2*x

After the blank line and deindentation,
this is a normal text paragraph again.

Image insertion
---------------

.. code-block:: rst

    .. _image_example:
    .. figure:: _static/gemseo.png
       :width: 30%

       Image caption.

.. _image_example:
.. figure:: _static/gemseo.png
   :width: 30%

   Image caption.

LaTeX-based mathematics
-----------------------

.. code-block:: rst

    .. math::

       (a + b)^2  &=  (a + b)(a + b) \\
                  &=  a^2 + 2ab + b^2

       (a - b)^2 = a^2 - 2ab + b^2

.. math::

   (a + b)^2  &=  (a + b)(a + b) \\
              &=  a^2 + 2ab + b^2

   (a - b)^2 = a^2 - 2ab + b^2

Blocks
------

.. code-block:: rst

    .. note::

       This is a *note* block.

    .. seealso::

       This is a *seealso* block.

    .. warning::

       This is a *warning* block.

.. note::

   This is a *note* block.

.. seealso::

   This is a *seealso* block.

.. warning::

   This is a *warning* block.