import sys
from os.path import dirname, abspath, join

project_path = dirname(abspath(__file__))
analysis_path = join(project_path, "analysis")
plugin_path = join(analysis_path, "plugins")


def extend():
    sys.path.extend([plugin_path, project_path, analysis_path])
