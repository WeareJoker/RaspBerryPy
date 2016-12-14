import os
import time
import sys

from multiprocessing import Process
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin',
    WLAN_DB=os.path.join(app.root_path, 'DB/wlan_scan.db'),
    SNIFF_DB=os.path.join(app.root_path, 'DB/sniff_pkt.db')
))

def get_db(DB):
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, DB):
        #print(repr("g.%s = connect_db(app.config['%s'])"%(DB,DB)))
        exec("g.%s = connect_db(app.config['%s'])"%(DB,DB))
    

def connect_db(DB_filename):
    """Connects to the specific database."""
    rv = sqlite3.connect(DB_filename)
    rv.row_factory = sqlite3.Row
    return rv

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'WLAN_DB'):
        g.WLAN_DB.close()
    if hasattr(g, 'SNIFF_DB'):
        g.SNIFF_DB.close()

def init_db():
    """Initializes the database."""
    get_db('WLAN_DB')
    get_db('SNIFF_DB')

@app.before_request
def before_request():
    init_db()

def get_one(list):
    for i in list:
        yield i

def proc_scanning(inet_iface):
    rv = sqlite3.connect(app.config['WLAN_DB'])
    rv.row_factory = sqlite3.Row

    while 1:
        result = os.popen('iwlist %s scan | \
            grep -E "Address|Channel:|ESSID|Encryption"'%inet_iface).read().split('\n')

        cur = rv.execute('delete from ESSID_SCAN_LIST')
        rv.commit()

        gen = get_one(result)
        index = 0
        for i in range(len(result)/4):
            index += 1

            address_data = next(gen)
            idx = address_data.find("Address:")
            address = address_data[idx+9:]

            chan_data = next(gen)
            idx = chan_data.rfind(":")
            channel = chan_data[idx+1:]

            enc_data = next(gen)
            idx = enc_data.rfind(":")
            enc = enc_data[idx+1:]

            essid_data = next(gen)
            idx = essid_data.rfind(":")
            essid = essid_data[idx+2:-1]

            if enc == "on":
                enc = 1;
            else:
                enc = 0;

            rv.execute("insert into ESSID_SCAN_LIST values (?, ?, ?, ?, ?, ?)", \
                [index, essid, address, channel, 0, enc])
            rv.commit()

        time.sleep(15)



def get_interface_by_script():
    result = os.popen('bash shell_scripts/get_interface.sh').read().split()
    if result:
        return result[0]
    else:
        return None


@app.route('/refresh')
def refresh():
    # catch channel and essid from "iwlist" command.
    # raw_essid_data = os.popen('iwlist %s scan | grep -E "ESSID|Channel:"' % get_interface_by_script()).read()


    #if not now_decrypting:
    #    now_decrypting = 0
    #else:
    #    now_decrypting = 1

    # ap_info_hash = []
    # for info in raw_essid_data.split('\n'):
    #    # first, is it channel?
    #    #is_channel = info.find("Channel")
    #    #if is_channel != -1:   # takes much cost
    #    if info.strip()[0] == "C" : # is it channel?
    #       chan = info.strip()[8:]
    #    elif info.strip()[0] == "E" # is it essid?
    #        ess = info.strip()[7:-1]
    #        ap_info_hash

    #session['essid_list'] = essid_list
    #session['now_decrypting'] = now_decrypting
    return redirect(url_for('main'))


@app.route('/connect_wifi', methods=['POST'])
def connect_wifi():
    if request.method == 'POST':
        essid = request.form['ESSID']
        AP_password = request.form['AP_password']
        bash_path = os.path.join(app.root_path, "shell_scripts/connect_wifi.sh")
        inet_iface = app.config['inet_iface']

        
        result = os.popen('bash %s %s %s %s' % (bash_path, essid, AP_password, inet_iface)).read()
        #if result == "You're connected.\n":
        #    return "Success!"
        #else:
    
    return redirect(url_for('main'))

@app.route('/start_sniff', methods=['POST'])
def start_sniff():
    if request.method == 'POST':

        essid = request.form['ESSID']
        enc = request.form['encryption']
        channel = request.form['channel']
        
        if not enc:
            pass
        else:
            mon_iface = app.config['mon_iface']
            password = request.form['AP_password']
        
            os.popen("iwconfig %s channel %s"%(mon_iface, channel))
            

            auto_path = os.path.join(app.root_path, "autorun/autorun_setting")
            with open(auto_path, "wt") as f:
                f.write("%s %s %s %s" % ("wpa", essid, password, channel))

            wdec_path = os.path.join(app.root_path, "wdecrypt/wdecrypt")
            
            #os.popen("%s wlan0 -e %s -p %s -o tap0 &"\
            #    %(wdec_path, essid, password))

            os.popen("%s %s -e %s -p %s -o tap0 &"\
                %(wdec_path, mon_iface, essid, password))

    return redirect(url_for('main'))        


@app.route('/stop_sniff')
def stop_sniff():
    wdec_pid = os.popen("ps -ef | grep wdecrypt | awk '{print $2}'").read()

    if len(wdec_pid.split('\n')) > 3:
        os.popen("kill -9 %s" % wdec_pid)

    return redirect(url_for('main'))

@app.route('/', methods=['POST', 'GET'])
def login():
    error=None
    if session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            if request.form['username'] != app.config['USERNAME']:
                error = 'Invalid username'
            elif request.form['password'] != app.config['PASSWORD']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('main'))

    return render_template('login.html', error=error)

@app.route('/main')
def main():
    inet_iface = app.config['inet_iface']
    iwconfig = os.popen("iwconfig %s"%inet_iface).read().split('\n')
    
    is_valid = iwconfig[0].find("ESSID:")
    if is_valid != -1 :
        idx = is_valid
        now_essid = iwconfig[0][ idx + 6 : -1]
        
        idx = iwconfig[1].find("Point:");
        now_mac = iwconfig[1][ idx + 7 : ].strip()
        if now_essid == 'off/any ':
            now_essid = "NOTHING"
        else:   
            db = g.WLAN_DB
            db.execute('update ESSID_SCAN_LIST set is_connected = 1 \
                where ESSID =%s and Address="%s"'%(now_essid, now_mac))
            db.commit() 
    else:
        now_essid = None

    wdec_pid = os.popen("ps -ef | grep wdecrypt | awk '{print $2}'").read()
    if len(wdec_pid.split('\n')) > 3:
        now_decrypting = 1
    else:
        now_decrypting = 0

    db = g.WLAN_DB
    cur = db.execute('select * from ESSID_SCAN_LIST limit 6')
    essid_list = cur.fetchall()

    #if session.get('essid_list') is None:
    #    return redirect(url_for('refresh'))

    return render_template('main.html', essid_list=essid_list,\
     now_essid = now_essid, now_decrypting = now_decrypting)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("USAGE : %s internet_dev monitor_dev"%sys.argv[0])
        sys.exit()

    proc = Process(target=proc_scanning, args=(sys.argv[1],))
    proc.start()
    
    app.config.update(dict(
        inet_iface = sys.argv[1],
        mon_iface = sys.argv[2]
    ))

    dummy_iface = os.path.join(app.root_path, "wdecrypt/dummy.sh")
    os.popen("bash %s add tap0"%dummy_iface)


    os.popen("ifconfig %s down"%app.config['mon_iface'])
    os.popen("iwconfig %s mode monitor"%app.config['mon_iface'])
    os.popen("ifconfig %s up"%app.config['mon_iface'])


    app.run(host='0.0.0.0', debug=True)
