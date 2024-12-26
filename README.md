A Voxel Engine written in Python using PyOpenGL. It initially was based on the tutorial by [StanislavPetrovV](https://github.com/StanislavPetrovV/Minecraft) but I wanted to incorporate a different rendering pipeline using instacing.

I also have intentions to rewrite this in C++ for a more comprehensive implementation but am using this as the groundworks.

This implementation uses OpenGL 3.3 using PyOpenGL. The bindings in the are pretty much the same as those in the C++ bindings which will make the conversion easier. This is why I chose PyOpenGL over something more convenient like ModernGL as found in StanislavPetrovV's tutorial.

Run simply using:

    python3 app.py

Dependencies:
- pygame     2.6.1
- PyOpenGL   3.1.7
- numpy      2.0.2
- PyGLM      2.7.3
- numba      0.60.0  (NOT CURRENTLY, but will in future)
