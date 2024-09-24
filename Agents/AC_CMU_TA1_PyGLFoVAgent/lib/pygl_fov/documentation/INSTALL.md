# Installation

* Python 3.5 or later

## pip commands

The code requires PyOpenGL and PyOpenGLU to be installed.  Additionally, either GLFW or GLUT needs to be installed as well.  These should be able to be installed via pip:

    pip install pyopengl
    pip install glfw

Additionally, Numpy and PIL are required

    pip install numpy
    pip install pillow

For visualization, matplotlib is needed

    pip install matplotlib


## OpenGL and GLU

OpenGL drivers may already be installed, depending on the graphics card drivers
used.  If OpenGL _is not_ installed, software renderers can be used instead.

### Ubuntu

Most Linux distributions utilize the Mesa3D libraries for OpenGL and the GL
Utility (GLU).  These can be installed using `apt`:

    sudo apt-get install libgl1-mesa-dev
    sudo apt-get install libglu1-mesa-dev

### Windows

TODO

### MacOS

TODO


## GLFW or GLUT

### Linux

GLFW is the _modern_ OpenGL context handler, which can be installed via pip

    pip install glfw

### Windows

### MacOS


## PyOpenGL

### Linux

    pip install pyopengl
    pip install pyopengl_accelerate

### Windows

### MacOS


## numpy

### Linux

    pip install numpy

### Windows

### MacOS


## Python Image Library

### Linux

    pip install pillow

### Windows

### MacOS