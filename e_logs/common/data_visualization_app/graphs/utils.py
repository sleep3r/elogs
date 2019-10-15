import os
import importlib as im


def resolve(name):
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "objects")
    for filename in os.listdir(dir):
        if filename not in ["__init__.py", "__pycache__"]:
            module_name = "e_logs.common.data_visualization_app.graphs.objects." + filename.split(".")[0]
            print(module_name)
            module = im.import_module(module_name)
            if name in module.verbose_names.keys():
                return module.verbose_names[name]
    return None


def avaliable_graphs():
    dir = os.path.dirname(os.path.abspath(__file__))
    names = []
    for filename in os.listdir(dir):
        module_name = filename.split(".")[0]
        module = im.import_module(module_name)
        names.append(list(module.verbose_names.keys()))
    return names
