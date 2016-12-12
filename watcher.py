import os
import sys

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from multiprocessing import Process
from main import analysis


class PcapHandler(FileSystemEventHandler):
    analysis_process_list = list()

    def __init__(self, observer, filename):
        self.observer = observer
        self.filename = filename

    def on_created(self, event):
        if not event.is_directory:  # and event.src_path.endswith(self.filename):
            filename = os.path.basename(event.src_path)
            print("%s created" % filename)
            if filename.split('.')[-1] != 'pcap':
                return
            print("Start Analysis %s" % filename)
            # analysis(os.path.basename(event.src_path))
            p = Process(target=analysis, args=(filename,))
            p.start()
            PcapHandler.analysis_process_list.append(p)


def main(argv):
    from config import project_path
    path = project_path
    filename = argv[1]

    observer = Observer()
    event_handler = PcapHandler(observer, filename)

    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    observer.join()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("%s [pcap name]" % sys.argv[0])
        exit(1)

    try:
        main(sys.argv)
    except KeyboardInterrupt:
        for analysis_process in PcapHandler.analysis_process_list:
            analysis_process.join()
