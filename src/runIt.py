import inspect
import functools


def runIt(func_name, params_dict):

    # 获取函数的参数
    func = globals()[func_name]
    func_params = inspect.getfullargspec(func).args
    # 构造参数字典的副本
    params_copy = params_dict.copy()
    # 在副本上检查并删除多余参数
    for param in params_dict.keys():
        if param not in func_params:
            print(f"移除多余参数 {param}")
            del params_copy[param]

    # 如果函数没有参数,使用空字典
    if not func_params:
        params_copy = {}

    # 构造eval字符串
    eval_str = f"{func_name}({','.join([f'{k}={v}' for k,v in params_copy.items()])})"

    # 使用eval调用函数并返回结果
    print(eval_str)
    return eval(eval_str)


def test_func(x, y):
    return x + y


params = {'x': 1, 'y': 2, 'z': 3}
print(runIt('test_func', params))
