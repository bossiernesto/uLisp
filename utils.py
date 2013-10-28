def get_method_name(string_method):
    return string_method[string_method.find("def") + 3:string_method.find("(")].strip()


def change_function(instance, signature, new_body):
    import inspect

    new_code = inspect.getsource(getattr(instance, signature)).replace('pass', new_body)
    method_name = get_method_name(new_code)
    method_dict = {}
    exec(new_code.strip(), globals(), method_dict)
    setattr(instance, signature, method_dict[signature])
    print(inspect.getsource(instance.__dict__[signature].__func__))
    return instance.__dict__[signature]
