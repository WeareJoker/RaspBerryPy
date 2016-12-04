import os
import sys
import importlib

plugin_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, plugin_path)

plugin_directory_list = [_ for _ in os.listdir(plugin_path) if _.startswith("__") is False]

plugin_list = [importlib.import_module(plugin) for plugin in plugin_directory_list]
