When in doubt, follow [PEP-8] (https://www.python.org/dev/peps/pep-0008/).

Code layout
-----------

-   Use 4 spaces for indentation. Do not use tab.
-   The first line of each executable file should be: \#!/usr/bin/env python

Importing
---------

-   Your code should import modules, not classes:
    -   Use "`import` `optparse`" instead of "`from` `optparse` `import` `OptionParser`"
    -   This keeps the global namespace cleaner (and easier to know where things come from)
    -   This does not affect performance (the full module is parsed in either case)
    -   This helps with the use of 'reload()' when developing in interactive mode
    -   Note that "`from` `PySide` `import` `QtGui`" is fine. QtGui is a module.


Naming conventions
------------------

-   Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability.
    -   Examples: `[1]` `brainmix.py` `[2]` `affine_registration.py` `[3]` `image_viewer.py`
-   Python packages should also have short, all-lowercase names, although the use of underscores is discouraged.
    -   Examples: `[1]` `brainmix/` `[2]` `modules/` `[3]` `gui/`
-   Class names should normally use the CapWords convention.
    -   Examples: `[1]` `BrainMix()` `[2]` `AffineRegistration()` `[3]` `ImageViewer()`
-   Function names should be lowercase, with words separated by underscores as necessary to improve readability.
    -   Examples: `[1]` `register()` `[2]` `create_menus()`
-   Variables names should be mixedCase.
    -   Examples: `[1]` `mainWindow` `[2]` `self.alignedImages`

See the definition of [module and package from the Python documentation] (https://docs.python.org/2/tutorial/modules.html).


Docstrings
----------

Docstrings for functions and classes should be compatible with Sphinx so that ReadTheDocs documentation can be created automatically. See [Sphinx Napoleon] (https://sphinxcontrib-napoleon.readthedocs.org).


Python3 Compatibility
---------------------
-  Print statements:
   - This is ok: `print 'Num = {0}'.format(number)`
   - Avoid this: `print 'Num = %d' % number`


PEP8 standards
--------------

1.  Always include a space around operators. Example: a==1 is wrong, a == 1 is correct.
2.  Include spaces after commas. Example: \[a,b,c\] is wrong, \[a, b, c\] is correct.
3.  Include 2 blank lines above class definitions
4.  Include a blank line above the first method of the class (usually the \_\_init\_\_() method)
5.  (Recommended) No more than 79 characters per line.

Some editors and development environments contain PEP8 style-checking tools.



