Pressure Layout
===============
Automatic Layout Generator for Python

pressure-layout is a Python abstract implementation of a layout manager. The purpose of this project was to reduce the amount of development time in designing user interfaces for interchangeable components. It was originally going to be used specifically for PyQt, but it was able to grow into something even more abstract.

Using
=====

```
    from pressure import Layout
    
    # Creating the layout
    layout = Layout()
    
    # Adding some element
    # NB: my_element should have a width and height attribute
    layout.add_children(my_element)
    
    # Move all elements around in a good layout
    # (w, h) are the size of the resulting layout
    w, h = layout.optimize()
    
    # LayoutChild rules are now available
    print([child.box() for child in layout.children])

```