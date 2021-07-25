import yaml
from hashlib import sha1 as sha
from uuid import uuid4
from time import sleep
from datetime import datetime
from getpass import getpass


class Object:
    def __init__ (self, attrs):
        pass
        
    def __str__(self):
       return str(self.__dict__)

    @classmethod
    def create(cls, **kwargs):
        kwargs.update(_id=str(uuid4()))
        cls.objects.append(cls(kwargs))
        cls.save()

    @classmethod
    def find(cls, **kwargs):
        key = list(kwargs.keys())[0]
        value = list(kwargs.values())[0] # or k,v = list(d.items())[0]
        return [i for i in cls.objects if getattr(i, key) == value]
        
    
    @classmethod
    def save(cls):
        with open (f'{cls.__name__}.yaml', 'w') as f:
            l = [i.__dict__ for i in cls.objects] #chon yaml listi az dic ast bayad b dict tabdil konim
            yaml.dump(l , f)
    
    @classmethod
    def load(cls):
        try:
            with open(f'{cls.__name__}.yaml')as f:
                l = yaml.safe_load(f)
            cls.objects = [cls(i) for i in l] # harvaght bekhahim instance ya object besazim ba seda zadan class misazim
        except:
            pass


class User(Object):
    objects = []
    def __init__ (self, attrs):
        self._id = attrs.get("_id")
        self.username = attrs.get("username")
        self.password = attrs.get("password")
        self.followings = attrs.get("followings") if attrs.get("followings") else []

    @classmethod
    def register(cls, *args):
        while True:
            username = input("Username: ")
            if username not in [i.username for i in cls.objects]:
                    break
            else:
                print("sorry, Taken!")
        while True:
            password = input("password: ")
            if len(password) >= 3:
                password = sha(password.encode()).hexdigest()
                break
            else:
                print("Too short!")
        return cls.create(username= username, password=password, followings=[])

    @classmethod
    def login(cls, *args):
        c = 3
        while True:
            username = input("username: ")
            password = getpass("password: ")
            users = User.find(username=username)
            if users:
                user = users[0]
                if sha(password.encode()).hexdigest() == user.password:
                    return user
            c -= 1
            print(f'check your cridentials {c} chances left!')
            if c == 0:
                print('You sould wait 60 seconds.')
                sleep(60)
                c = 3

    @classmethod
    def view_all(cls, user, *args):
        l = [i for i in cls.objects if i._id != user._id]
        for i, u in enumerate(l):
            f = 'Following' if u._id in user.followings else ' '*9
            print(f, i+1, u.username)
        print()
        try:
            n = input('follow / unfollow user # ? ')
            u = l[int(n)-1] # chera bracket gozashtim ?
            if u._id in user.followings:
                user.followings.remove(u._id)
                print('unfollowed')
            else:
                user.followings.append(u._id)
                print('followed')
            cls.save()
            
        except:
            pass


class Post(Object):
    objects = []
    def __init__(self, attrs):
        self._id = attrs.get('_id')
        self.user_id = attrs.get('user_id')
        self.title = attrs.get('title')
        self.body = attrs.get('body')
        self.date = attrs.get('date')

    @classmethod
    def submit(cls, user):
        cls.create(
            title=input('Title: '),
            body=input('Text: '),
            user_id=user._id,
            date=datetime.now().strftime('%Y-%b-%d')
        )
    
    @classmethod
    def view_all(cls, *args):
        for i, post in enumerate(cls.objects):
            print(i+1, post.title)
        print()
        try:
            n = input('Post # ? ')
            post = cls.objects[int(n)-1]
            print(post.title, post.date, post.body, sep='\n')
        except:
            pass


class Comment(Object):
    objects = []
    def __init__(self, attrs):
        self._id = attrs.get('_id')
        self.user_id = attrs.get('user_id')
        self.text = attrs.get('text')
        self.post_id = attrs.get('post_id')
        self.date = attrs.get('date')
    
    @classmethod
    def submit(cls, user, post):
        cls.create(
            text=input('text'),
            date=datetime.now().strftime('%Y/%b/%d'),
            user_id=user._id,
            post_id=post._id,
        )

    @classmethod
    def view(cls, post):
        l = [i for i in cls.objects if i.post_id == post._id] #post._id hamun argument vorodi k idisho mikhad#commenthae in posti k mikhaymo mikeshim birun
        
        # l = comment.find(post_id = post._id)
        # l2 = []
        # for i in l:#l hamun commenthae hast k post idishun = post._id va entekhab shodeas
        #     user=User.find(_id=i.user_id)[0]#find kon useri k idishun barabare i.user_id k unique hast
        #     #barae in k b jae userid esme idio benevise yani user masalan ali in text comment karde
        #     l2.append(user.username + ': ' + i.text)

        for i in l:
            print(User.find(_id=i.user_id)[0].username+':')
            print(i.text)
            if not i == l[-1]:
                print('.'*40)


User.load()
Post.load()
Comment.load()
