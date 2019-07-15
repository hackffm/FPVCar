
class Component():
    """docstring for module."""

    def __init__(self, _type_):
        self.type = _type_

# -- Helper -----------------------
    def is_type(self, _type):
        if self.type == _type:
            return True
        else:
            return False
