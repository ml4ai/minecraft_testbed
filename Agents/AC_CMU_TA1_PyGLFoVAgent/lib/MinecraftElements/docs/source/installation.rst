Installation
============


Requirements
------------

This module may be used with Python version 3.4 and later.  Installation is
best performed using `pip`_.


Installation using pip
----------------------

This module can be installed as a package using `pip`.  Assuming `pip` is
installed, the package can be installed (for users) from the root folder by::

    pip install --user -e . 

Once installed, the module can be imported from arbitrary locations.


Adding as a Submodule to a Project
----------------------------------

As an alternative, this repository could be cloned into existing code as a 
*submodule*.  This can be done with the following command::

    git submodule add https://gitlab.com/cmu_asist/MinecraftElements

If the generated folder is empty, a recursive update may need to be performed::

    git submodule update --init --recursive

(See `Working with Submodules`_)

Additionally, cloning a repo with this submodule will require the `recursive`
flag::

    git clone --recursive <project url>


Documentation
-------------
Documentation for this module can be built using `Sphinx`_, which is also installed with `pip`_.  The source and build files for the documentation is in the `docs` folder.

Requirements
~~~~~~~~~~~~
Note that build targets may require additional dependencies to be installed.  For building a PDF of the documentation using Latex, basic Latex dependencies need to be installed.  On Ubuntu-based systems, this can be done by installing the following packages using `aptitude`::

    apt-get install texlive-latex-recommended
    texlive-latex-extra texlive-fonts-recommended


Building Documentation
~~~~~~~~~~~~~~~~~~~~~~
To build a PDF of the *MinecraftElements Manual*, from the `docs` folder, run the build command with the latexpdf target::

    cd docs
    make latexpdf

This will create a `build` subfolder, and `latex` subfolder within build.  The final pdf file, `MinecraftElements_Manual.pdf` will be written to the `latex` subfolder, which can be moved to the root directory easily.  In Linux or OSX, this is done with::

    mv build/latex/MinecraftElements_Manual.pdf ..

While in Windows, this would be done by::

    move build\latex\MinecraftElements_Manual.pdf ..




.. _pip: https://pip.pypa.io/en/stable/

.. _Working with Submodules: https://github.blog/2016-02-01-working-with-submodules/

.. _Sphinx: https://www.sphinx-doc.org/en/master/