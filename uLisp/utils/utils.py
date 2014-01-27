def get_method_name(string_method):
    return string_method[string_method.find("def") + 3:string_method.find("(")].strip()


def change_function(instance, signature, new_body):
    import inspect
    from textwrap import dedent

    new_code = dedent(inspect.getsource(getattr(instance, signature))).replace("pass", new_body)
    method_dict = {}
    exec(new_code.strip(), globals(), method_dict)
    bind(method_dict[signature], instance, signature)
    return instance.__dict__[signature]

import types


def bind(f, obj, new_f_name):
    obj.__dict__[new_f_name] = types.MethodType(f, obj)
