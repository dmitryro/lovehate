from functools import wraps

from django.template import RequestContext
from django.shortcuts import render_to_response


def render_to(tpl):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            out = func(request, *args, **kwargs)
            if isinstance(out, dict):
                out = render_to_response(tpl, out, RequestContext(request))
            return out
        return wrapper
    return decorator



def run_async(func):
        """
                run_arun_async
                        def task1():
                                do_something
                        @run_async
                        def task2():
                                do_something_too
                        t1 = task1()
                        t2 = task2()
                        ...
                        t1.join()
                        t2.join()
        """
        from threading import Thread
        from functools import wraps

        @wraps(func)
        def async_func(*args, **kwargs):
                func_hl = Thread(target = func, args = args, kwargs = kwargs)
                func_hl.start()
                return func_hl

        return async_func
