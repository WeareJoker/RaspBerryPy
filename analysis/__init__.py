def append_system_path():
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

append_system_path()

from .analyser import analysis
