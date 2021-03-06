"""Pressure Layout classes"""

import operator

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
        self._padding_horizontal = padding_horizontal
        self._padding_vertical = padding_vertical
        self.width = element.width if width is None else width
        self.height = element.height if height is None else height
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

    @property
    def padding_horizontal(self):
        return self._padding_horizontal

    @padding_horizontal.setter
    def padding_horizontal(self, value):
        delta = value-self._padding_horizontal
        if not delta:
            return
        self.width += value
        self._padding_horizontal = value

    @property
    def padding_vertical(self):
        return self._padding_vertical

    @padding_vertical.setter
    def padding_vertical(self, value):
        delta = value-self._padding_vertical
        if not delta:
            return
        self.height += value
        self._padding_vertical = value

    def __str__(self):
        return '{cls}<dims={box}>'.format(cls=self.__class__, box=self.box())


class Layout(LayoutChild):
    """An optimizeable Layout

    Attributes
    ----------
    children : list of LayoutChild
    ratio : float
        width/height ration to optimize around. Default CONST_PHI.
    align : Layout.HORIZONTAL or Layout.VERTICAL or Layout.OPTIMIZED
        default alignment of this layout
    padding : float
        spacing between children

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
    HORIZONTAL = 1
    VERTICAL = 2
    OPTIMIZED = 3

    def __init__(self, *children, **kwargs):
        self.ratio = kwargs.get('ratio', CONST_PHI)
        self.align = kwargs.get('align', Layout.OPTIMIZED)
        self.padding = kwargs.get('padding', 5)
        self.children = [self.child(child, padding_horizontal=self.padding,
                                    padding_vertical=self.padding)
                         for child in children]
        self._x = 0.0
        self._y = 0.0
        LayoutChild.__init__(self, None, width=0, height=0)
        if self.align == Layout.HORIZONTAL:
            self.align_horizontal()
        elif self.align == Layout.VERTICAL:
            self.align_vertical()
        elif self.align == Layout.OPTIMIZED:
            self.optimize()

    def child(self, element, *args, **kwargs):
        if isinstance(element, LayoutChild):
            return element
        return LayoutChild(element, *args, **kwargs)

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
        if not self.children:
            return 0
        return max(child.width+child.x+child.padding_horizontal/2
                   for child in self.children)-self.x+self.padding_horizontal
        return sum(child.width for child in self.children)

    @width.setter
    def width(self, value):
        if not self.children:
            return
        child = self.children[-1]
        child.x = self.x+value-child.width-self.padding_horizontal

    @property
    def height(self):
        if not self.children:
            return 0
        return max(child.height+child.y+child.padding_vertical/2
                   for child in self.children)-self.y+self.padding_vertical
        return max([0]+[child.height for child in self.children])

    @height.setter
    def height(self, value):
        pass

    def add_children(self, *children, **kwargs):
        """Adds children to the layout

        If multiple children are provided, they will be placed according
        to alignment (horizontal by default)

        Parameters
        ----------
        child_1 : element
        ...
        child_n : element
        align : Layout.HORIZONTAL or Layout.VERTICAL or Layout.OPTIMIZED
        """
        align = kwargs.get('align', Layout.HORIZONTAL)
        if not children:
            return
        elif len(children) == 1:  # Single child
            self.children.append(self.child(children[0],
                                            padding_horizontal=self.padding,
                                            padding_vertical=self.padding))
        else:
            self.children.append(Layout(*children, ratio=self.ratio,
                                        align=align, padding=self.padding))

    def optimize(self):
        """Sets children up in an optimized fashion.

        The children maintain column manners and try to be in a box
        closest to the ratio as possible.

        Returns
        -------
        size : type(float, float)
            Width and height of layout
        """
        # Sort children from fattest to thinnest
        children = sorted(self.children, key=operator.attrgetter('width'),
                          reverse=True)
        total_height = sum(child.height for child in children)

        best_score = 1e100
        best = [children]
        for num_col in xrange(1, len(children)+1):
            height_cap = total_height/num_col*1.05
            cols = []
            for cidx, child in enumerate(children):
                for col in cols:
                    # Check to see if this child fits into the column
                    if sum(c.height for c in col)+child.height < height_cap:
                        col.append(child)
                        break
                else:
                    #  Otherwise, create a new column with just this element
                    cols.append([child])
            width = sum(max(c.width for c in col) for col in cols)
            height = max(sum(c.height for c in col) for col in cols)
            # score is half perimeter with a penalty on height
            score = width+height*self.ratio
            if score < best_score:
                best = cols
                best_score = score
        cols = best
        for col in cols:
            # Sort column by original children order
            col.sort(key=lambda c: self.children.index(c))

        # Commit the layout to the children
        x = self.padding_horizontal/2
        col_width = 0
        max_height = 0
        for col in cols:
            x += col_width  # increase x by last column width
            y = self.padding_vertical/2
            try:
                col_width = max(c.width for c in col)
            except ValueError:
                col_width = 0
            col_height = 0
            for child in col:
                # TODO: centering
                child.x = x+child.padding_horizontal/2
                child.y = y+child.padding_vertical/2
                child.width = col_width
                y += child.height
            max_height = max(max_height, y)
        return (x+col_width+self.padding_horizontal/2,
                max_height+self.padding_vertical/2)
