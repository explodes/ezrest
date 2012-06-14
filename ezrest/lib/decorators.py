from ezrest.parameters import UnsetParameter

def cachedvalue(func):
    var_name = '_cached_%s_' % func.__name__
    def wrapper(self):
        value = getattr(self, var_name, UnsetParameter)
        if value == UnsetParameter:
            value = func(self)
            setattr(self, var_name, value)
        return value
    return wrapper
