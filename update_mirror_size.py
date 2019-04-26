import re
import os

#Edit these before use
WORKER_NAME = "worker"
CONFIG_PATH = "path/to/worker.conf"

with open(CONFIG_PATH, "r") as f:
    lines = f.readlines()
    flag = False
    names = []
    for l in lines:
        if flag:
            temp = l.find('"')
            names.append(l[temp+1:l[temp+1:].find('"')+temp+1])
            flag = False
        if "[[mirrors]]" in l:
            flag = True

for mirror_name in names:
    log = "/var/log/tunasync/"+mirror_name+"/latest"
    with open(log) as f:
        buffer = f.readlines()
        match = re.findall("[0-9\\.]+[KMGT]", buffer[-1])
        if match:
            mirror_size = str(match[0])
        else:
            du_command = "du -sh /data0/mirrors/"+mirror_name+'/ |  grep -Po "[0-9\\.]+[KMGT]"'
            response = os.popen(du_command)
            mirror_size = response.read()

        commandUpdate = "tunasynctl set-size -w "+WORKER_NAME+" "+mirror_name+" "+mirror_size
        os.system(commandUpdate)
