class Data():

    def __init__(self):
        self.user = None

    def logUser(self, id, email, token):
        self.user = (id, email, token)
