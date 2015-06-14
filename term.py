from .dispatch import dispatch
from .unification import unify, reify, _reify, _unify


@dispatch((tuple, list))
def arguments(seq):
    return seq[1:]


@dispatch((tuple, list))
def operator(seq):
    return seq[0]

'''
  dispatch设定第一个参数为object，第二个参数为list或者tuple
  感觉这里的功能是将op添加到后面的列表args中去
  例如：
    print term(1, [1,2,3])
  结果：
    (1, 1, 2, 3)
  实际应用中：
  op -- 谓词
  args -- 实体
'''
@dispatch(object, (tuple, list))
def term(op, args):
    return (op,) + tuple(args)

#term(isGirlfriend, lyj, zwq)
#感觉这样更符合我之前的学习
'''
@dispatch(object, object, object)
def term(op, a, b):
    return (op, a, b)
'''

def unifiable_with_term(cls):
    _reify.add((cls, dict), reify_term)
    _unify.add((cls, cls, dict), unify_term)
    return cls


def reify_term(obj, s):
    op, args = operator(obj), arguments(obj)
    op = reify(op, s)
    args = reify(args, s)
    new = term(op, args)
    return new


def unify_term(u, v, s):
    u_op, u_args = operator(u), arguments(u)
    v_op, v_args = operator(v), arguments(v)
    s = unify(u_op, v_op, s)
    if s is not False:
        s = unify(u_args, v_args, s)
    return s
