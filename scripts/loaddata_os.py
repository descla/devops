import sys
from datetime import datetime
from pathlib import Path
import json
import toml
from rdcheck.models import t_linux_result
import os, django
sys.path.extend(["/data/ftp/OS"])
os.environ.setdefault("DJANGO_SETTING_MODULE", "devops.setting")
django.setup()


class load_data():
    dataDir = "/data/ftp/OS"
    curDate = datetime.today().strftime("%Y%m%d")
    tomlDir = Path(dataDir, curDate)
    bakupDir = Path(dataDir, curDate, "bak")

    def readToml(self, tomlFile):
        try:
            data = toml.load(str(tomlFile))
        except Exception as e:
            data = {}
            print("readFile {tomlFile} error: [{e}]".format(tomlFile=tomlFile.name, e=e))
        else:
            data = {
                'ip': data["global"]["ip"],
                'hostname': data["global"]["hostname"],
                'ts': data["global"]["ts"],
                'metric': json.dumps(data["metric"])
            }
        return data

    def load_linux(self):
        result = t_linux_result()
        tomlFiles = list(self.tomlDir.glob("*_*.toml"))
        if not tomlFiles:
            sys.exit()
        for rcFile in tomlFiles:
            data = self.readToml(rcFile)
            if data:
                try:
                    result.ip = data['ip']
                    result.hostname = data['hostname']
                    result.ts = data['ts']
                    result.metric = data['metric']
                    result.save()
                except Exception as e:
                    print(e)


