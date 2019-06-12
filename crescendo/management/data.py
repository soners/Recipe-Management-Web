class Data():

    def __init__(self):
        self.user = None

    def logUser(self, id, name, email, token):
        self.user = (id, name, email, token)
