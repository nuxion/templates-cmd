from importlib import import_module

def get_class(fullclass_path):
    """get a class or object from a module. The fullclass_path should be passed as:
    package.my_module.MyClass
    """
    module, class_ = fullclass_path.rsplit(".", maxsplit=1)
    mod = import_module(module)
    cls = getattr(mod, class_)
    return cls

def from_path_to_module_str(fp) -> str:
    """ experimental:
    from "examples/model.py" it should return
    "example.model"
    """
    return fp.rsplit(".", maxsplit=1)[0].replace("/", ".")
