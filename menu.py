class Menu:
    def __init__(self, options, prompt, _help, next_action):
        self.options = options
        self.next_action = next_action
        self.prompt = ' ' + prompt + ' '
        self._help = lambda *args: print(_help)
        self.user = None

    def edit_user(self, user):
        self.user = user
        self.prompt = user.username + self.prompt

    def ask(self, *args):
        while True:
            b = self.options.get(input(self.prompt), self._help)(self.user)
            if type(b) is int:
                return b - 1
            elif b is not None:
                self.next_action(b)
                

 