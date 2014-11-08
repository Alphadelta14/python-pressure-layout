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
    children : list of LayoutChild


    Methods
    -------
    addChildren(*element)
        Add groups of children
    optimize()
        Set the positions of the children in an optimized fashion
    align_horizontal()
        Set the positions of the children in one row
    align_vertical()
        Set the positions of the children in one column
    """
    def __init__(self, ratio=CONST_PHI):
        self.ratio = ratio
        self.children = []
        self.__class__.__init__(self, None, width=0, height=0)

    def align_horizontal(self):
        """Sets children up horizontally

        Returns
        -------
        size : type(float, float)
            Width and height of layout
        """
        width = 0
        height = 0
        for child in self.children:
            child.x = width
            child.y = 0
            width += child.width
            height = max(height, child.height)
        self.width = width
        self.height = height
        return (width, height)

    def align_vertical(self):
        """Sets children up vertically

        Returns
        -------
        size : type(float, float)
            Width and height of layout
        """
        width = 0
        height = 0
        for child in self.children:
            child.x = 0
            child.y = height
            height += child.height
            width = max(width, child.width)
        self.width = width
        self.height = height
        return (width, height)

    def optimize(self):
        """Sets children up in an optimized fashion.

        The children maintain column manners and try to be in a box
        closest to the ratio as possible.

        Returns
        -------
        size : type(float, float)
            Width and height of layout
        """
        return (0.0, 0.0)
