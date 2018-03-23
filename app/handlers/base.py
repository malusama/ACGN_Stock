def check_args(func):
    def wrapper(*args, **kwages):
        print(args, kwages)
        if args is not None:
            for i in args:
                if i is None:
                    raise ValueError
        if kwages is not None:
            for i in kwages.values():
                if i is None:
                    raise ValueError
        return func(*args, **kwages)
    return wrapper
