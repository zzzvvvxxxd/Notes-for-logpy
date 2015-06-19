from contextlib import contextmanager
from .util import hashable
from .dispatch import dispatch

_global_logic_variables = set()
_glv = _global_logic_variables

class Var(object):
    """ Logic Variable """

    _id = 1
    def __new__(cls, *token):
        if len(token) == 0:
            token = "_%s" % Var._id     #参数为空,表示是匿名变量,赋值为_id,id为该匿名变量的后台id,也反应了系统中当前匿名变量的个数
            Var._id += 1
        elif len(token) == 1:
            token = token[0]

        obj = object.__new__(cls)
        obj.token = token
        return obj

    def __str__(self):
        return "~" + str(self.token)
    __repr__ = __str__

    def __eq__(self, other):
        return type(self) == type(other) and self.token == other.token

    def __hash__(self):
        return hash((type(self), self.token))

#var()
#匿名函数，返回的是Var()类的一个实例，Var类用来表示变量，而变量的token代表变量的标识符
#v = var(1)
#返回的值，在概念上就是变量1，而非数字1（当然其实是Var类，其token为1）
#打印出来就是 ~1 ，这样便于区别变量和常量
var = lambda *args: Var(*args)

#vars()
#返回的是n个匿名变量组成的list
#例如：vars(3)
#返回的值就是[~_1, ~_2, ~_3]
vars = lambda n: [var() for i in range(n)]


@dispatch(Var)
def isvar(v):
    return True


@dispatch(object)
def isvar(o):
    return not not _glv and hashable(o) and o in _glv


#对逻辑变量的@contextmanager
@contextmanager
def variables(*variables):
    """ Context manager for logic variables

    >>> from __future__ import with_statement
    >>> from logpy import variables, var, isvar
    >>> with variables(1):
    ...     print(isvar(1))
    True

    >>> print(isvar(1))
    False

    Normal approach

    >>> from logpy import run, eq
    >>> x = var('x')
    >>> run(1, x, eq(x, 2))
    (2,)

    Context Manager approach
    >>> with variables('x'):
    ...     print(run(1, 'x', eq('x', 2)))
    (2,)
    """
    old_global_logic_variables = _global_logic_variables.copy()
    _global_logic_variables.update(set(variables))  #添加variables传入的新变量
    try:
        yield
    finally:
        _global_logic_variables.clear()             #删除所有元素
        _global_logic_variables.update(old_global_logic_variables)
