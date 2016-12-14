import sys

from multiprocessing import Process

from analysis.analyser import analysis_pcap, analysis_sniff
from analysis.plugins import migrate
from config import extend

extend()


def from_interface():
    try:
        interface_name = sys.argv[2]
    except IndexError:
        show_help()
        return
    else:
        analysis_sniff(interface_name)


def from_pcap():
    try:
        pcap_name = sys.argv[2]
    except IndexError:
        show_help()
    else:
        analysis_pcap(pcap_name)


def run_web():
    from show_http.app import main
    main()


def show_help():
    self_name = sys.argv[0]
    print("Available Command: ")
    print("%s migrate" % self_name)
    print("%s interface [interface to sniff & analysis]" % self_name)
    print("%s pcap [pcap filename to analysis" % self_name)
    print("%s web" % self_name)
    print("%s run [interface]" % self_name)


def run():
    migrate()
    from_interface()
    sniff_process = Process(target=from_interface)

    try:
        run_web()
    except KeyboardInterrupt:
        sniff_process.join()


if __name__ == '__main__':
    try:
        func = {
            'migrate': migrate,
            'interface': from_interface,
            'pcap': from_pcap,
            'web': run_web,
            'run': run
        }[sys.argv[1]]
    except (IndexError, KeyError):
        show_help()
    else:
        func()
