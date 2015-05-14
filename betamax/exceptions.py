class BetamaxError(Exception):
    def __init__(self, message):
        super(BetamaxError, self).__init__(message)

    # REVIEW: From "Beyond PEP 8": always define nice __repr__
    def __repr__(self):
        return 'BetamaxError("%s")' % self.message
