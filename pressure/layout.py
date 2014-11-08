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


class LayoutChildren(LayoutChild):
    """Grouping of LayoutChild children

    Attributes
    ----------
    children : list of LayoutChild
    """
    def __init__(self, children):
        self.children = [child if isinstance(child, LayoutChild)
                         else LayoutChild(child) for child in children]
        self._x = 0.0
        self._y = 0.0
        LayoutChild.__init__(self, None, width=0, height=0)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        delta = value-self._x
        self._x = value
        if not delta:
            return
        for child in self.children:
            child.x += delta

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        delta = value-self._y
        self._y = value
        if not delta:
            return
        for child in self.children:
            child.y += delta

    @property
    def width(self):
        return sum(child.width for child in self.children)

    @width.setter
    def width(self, value):
        pass

    @property
    def height(self):
        return max(child.height for child in self.children)

    @height.setter
    def height(self, value):
        pass


class Layout(LayoutChildren):
    """An optimizeable Layout

    Attributes
    ----------
    ratio : float
        width/height ration to optimize around. Default CONST_PHI.


    Methods
    -------
    add_children(*element)
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
        LayoutChildren.__init__(self, [])

    def add_children(self, *children):
        """Adds children to the layout

        If multiple children are provided, they will be placed side by side

        Parameters
        ----------
        child_1 : element
        ...
        child_n : element
        """
        if not children:
            return
        elif len(children) == 1:  # Single child
            self.children.append(children)
        else:
            self.children.append(LayoutChildren(children))

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
