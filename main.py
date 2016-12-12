import sys
from config import analysis_path, project_path, plugin_path

sys.path.extend([plugin_path, project_path, analysis_path])

from analysis.analyser import migrate, analysis

if __name__ == '__main__':
    try:
        argv = sys.argv[1]

    except IndexError:
        print("%s [ migrate || filename ]" % sys.argv[0])
        print("Requires more than one argv.")

    else:
        if argv == "migrate":
            migrate()
        else:
            analysis(argv)
