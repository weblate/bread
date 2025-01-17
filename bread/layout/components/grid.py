import htmlgenerator


class Grid(htmlgenerator.DIV):
    def __init__(self, *children, gridmode=None, **attributes):
        """
        gridmode can be one of None, "narrow", "condensed", "full-width"
        """
        attributes["_class"] = attributes.get("_class", "") + " bx--grid"
        if gridmode is not None:
            attributes["_class"] += f" bx--grid--{gridmode}"
        super().__init__(*children, **attributes)


class Row(htmlgenerator.DIV):
    def __init__(self, *children, gridmode=None, **attributes):
        attributes["_class"] = attributes.get("_class", "") + " bx--row"
        if gridmode is not None:
            attributes["_class"] += f" bx--row--{gridmode}"
        super().__init__(*children, **attributes)


class Col(htmlgenerator.DIV):
    def __init__(self, *children, breakpoint=None, width=None, **attributes):
        """
        breakpoint: Can be one of "sm", "md", "lg", "xlg", "max"
        """
        colclass = "bx--col"
        if breakpoint is not None or width is not None:
            if width is None:
                raise ValueError("When breakpoint is given, width is also required")
            if breakpoint is None:
                raise ValueError("When width is given, breakpoint is also required")
            colclass += f"-{breakpoint}-{width}"
        attributes["_class"] = attributes.get("_class", "") + f" {colclass}"
        super().__init__(*children, **attributes)
