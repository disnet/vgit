# Simple mock for vim module

class MockCurrent:
    def __init__(self):
        self.buffer = [] 

class Vim:
    def __init__(self):
        self.current = MockCurrent()

    def command(self, cmd):
        print "noop"

    def eval(self, cmd):
        print "noop"
