"""This module provides the Road class that
characterizes the roads used for testing ADS.
Roads are identified by an identifying object (id)
that can be a unique number or a json data that includes
an id. Roads have Cartesian coordinate values xvalues and yvalues.
Roads can be Oracle (executed tests) or Non-Oracle (not-executed tests).
Oracle, Failing: is_failing=True/False, is_selectable=False
Non-Oracle: is_failing=False/None, is_selectable=True"""

class Road:
    def __init__(self, id,
                       xvalues,
                       yvalues,
                       is_failing,
                       is_selectable):
        self.id = id
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.is_failing = is_failing
        self.is_selectable = is_selectable