from applications.safe.echo import Echo
from applications.safe.ls import Ls
from applications.safe.cd import Cd
from applications.safe.pwd import Pwd
from applications.safe.cat import Cat
from applications.safe.head import Head
from applications.safe.tail import Tail
from applications.safe.grep import Grep
from applications.safe.find import Find
from applications.safe.sort import Sort
from applications.safe.uniq import Uniq
from applications.safe.cut import Cut
from applications.safe.wc import Wc
from applications.safe.sed import Sed
from applications.unsafe._echo import _Echo
from applications.unsafe._ls import _Ls
from applications.unsafe._cd import _Cd
from applications.unsafe._pwd import _Pwd
from applications.unsafe._cat import _Cat
from applications.unsafe._head import _Head
from applications.unsafe._tail import _Tail
from applications.unsafe._grep import _Grep
from applications.unsafe._find import _Find
from applications.unsafe._sort import _Sort
from applications.unsafe._uniq import _Uniq
from applications.unsafe._cut import _Cut
from applications.unsafe._wc import _Wc
from applications.unsafe._sed import _Sed


class Application:

    def __init__(self, app, args, pipeData=None):

        self.app = app
        self.args = args
        self.pipeData = pipeData

    """
    Mapping each application to their correspoding application class and evaluating the
    application with the given arguments
    Returns the result of the application - which is the output of the call command
    """

    def applicationMap(self):

        appMap = {
            "echo": Echo,
            "ls": Ls,
            "cd": Cd,
            "pwd": Pwd,
            "cat": Cat,
            "head": Head,
            "tail": Tail,
            "grep": Grep,
            "find": Find,
            "sort": Sort,
            "uniq": Uniq,
            "cut": Cut,
            "wc": Wc,
            "sed": Sed,
            "_echo": _Echo,
            "_ls": _Ls,
            "_cd": _Cd,
            "_pwd": _Pwd,
            "_cat": _Cat,
            "_head": _Head,
            "_tail": _Tail,
            "_grep": _Grep,
            "_find": _Find,
            "_sort": _Sort,
            "_uniq": _Uniq,
            "_cut": _Cut,
            "_wc": _Wc,
            "_sed": _Sed
        }
        try:
            return appMap[self.app]().eval(self.args, self.pipeData)
        except KeyError:
            raise SyntaxError(f"{self.app}: command not found")
