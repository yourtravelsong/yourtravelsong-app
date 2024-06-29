class Counter:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Counter, cls).__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def get_value(self):
        return self.value