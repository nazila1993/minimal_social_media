from model import User, Post
from menu import Menu

m2 = Menu(
    dict(
        c=lambda:print('c'),
        back=lambda:1,
        home=lambda:2,
    ),
    next_action=None,
    prompt=">>>",
    _help="wrong: sc",
)

m1 = Menu(
    dict(
        posts=Post.view_all,
        users=User.view_all,
        newpost=Post.submit,
        back=lambda *args: 1,
    ),
    next_action=None,
    prompt='>>',
    _help='a, b, c, x', 
)

def login(user):  
    m1.edit_user(user) 
    m1.ask()

m0 = Menu(
    options = dict(
        register=User.register, 
        login=User.login,
        quit=lambda *args: exit(),
    ),
    next_action = login,
    _help="Register, login, quit",
    prompt='>',
)