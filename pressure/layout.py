"""Pressure Layout classes"""

__all__ = ['Layout']

CONST_PHI = (1+5**0.5)/2.0


class LayoutChild(object):
    """A container for an arbitrary element.

    Attribute values are measured in pixels.

    Attributes
    ----------
    element : mixed
        Contained element that this represent
    x : float
    y : float
    width : float
    height : float
    padding_horizontal : float, default=5
    padding_vertical : float, default=5

    Methods
    -------
    box()
        Get the offset and dimensions of this container
    """
    pass


class Layout(LayoutChild):
    """An optimizeable Layout

    Attributes
    ----------
    ratio : float
        width/height ration to optimize around. Default CONST_PHI.

    Methods
    -------
    addChildren(*element)
        Add groups of children
    optimize()
        Set the positions of the children in an optimized fashion
    """
    pass



