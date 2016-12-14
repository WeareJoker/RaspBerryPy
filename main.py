import sys

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


def show_help():
    self_name = sys.argv[0]
    print("Available Command: ")
    print("%s migrate" % self_name)
    print("%s interface [interface to sniff & analysis]" % self_name)
    print("%s pcap [pcap filename to analysis" % self_name)


if __name__ == '__main__':
    try:
        func = {
            'migrate': migrate,
            'interface': from_interface,
            'pcap': from_pcap
        }[sys.argv[1]]
    except (IndexError, KeyError):
        show_help()
    else:
        func()
