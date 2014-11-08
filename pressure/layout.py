"""Pressure Layout classes"""

__all__ = ['Layout']

CONST_PHI = (1+5**0.5)/2.0  # Golden ratio


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
    def __init__(self, element, width=None, height=None, padding_horizontal=5,
                 padding_vertical=5):
        self.element = element
        self.x = 0.0
        self.y = 0.0
        self.width = element.width if width is None else width
        self.height = element.height if height is None else height
        self.padding_horizontal = padding_horizontal
        self.padding_vertical = padding_vertical
        self.width += self.padding_horizontal
        self.height += self.padding_vertical

    def box(self):
        """Returns the box of this child

        Returns
        -------
        box : tuple(float, float, float, float)
            Tuple of (x, y, width, height)
        """
        return (self.x, self.y, self.width, self.height)


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
    def __init__(self, ratio=CONST_PHI):
        self.ratio = ratio
