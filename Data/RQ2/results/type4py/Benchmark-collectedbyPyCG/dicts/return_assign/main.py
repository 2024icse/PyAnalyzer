def func2():
    pass


def func1() ->Callable:
    return func2


d = {'a': func1()}
d['a']()
