import os
import sys
import importlib

plugin_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, plugin_path)

plugin_directory_list = [_ for _ in os.listdir(plugin_path) if _.startswith("__") is False and _ != 'example']

plugin_list = [importlib.import_module(plugin) for plugin in plugin_directory_list]


def get_model_list():
    from ..database import engine

    total_table = list()

    table_names = engine.table_names()
    for plugin in plugin_list:
        for model_obj in dir(plugin.model):
            if model_obj.lower() in table_names:
                total_table.append(getattr(plugin.model, model_obj))

    return total_table

table_list = get_model_list()
