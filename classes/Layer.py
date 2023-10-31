class Layer:
    def __init__(self) -> None:
        self.value = 0
        pass

    def setValue(self, _value):
        self.value = _value

    def getValue(self):
        return self.value