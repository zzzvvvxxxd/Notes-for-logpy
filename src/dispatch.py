from multipledispatch import dispatch
from functools import partial

namespace = dict()

#把dispath装饰器函数的namespace参数固定住，为dict()
# multipledispatch可以设置用户自己的namespace字典
# 就是为了让用户避免在使用默认的 multipledispatch.core.global_namespace的时候
# 遇到个项目同时运行，出现管理上的混乱
dispatch = partial(dispatch, namespace=namespace)

#Multiple Dispatch
#Doc： http://multiple-dispatch.readthedocs.org/en/latest/#