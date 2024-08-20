import osc_sdk_python
from diagrams import Cluster, Diagram
from diagrams.outscale.compute import Compute
from diagrams.outscale.security import IdentityAndAccessManagement
from diagrams.outscale.storage import Storage 
import os

key = ""
secret = ""

try:
    key = os.environ['OSC_ACCESS_KEY']
    secret = os.environ["OSC_SECRET_KEY"]
except:
    pass

region = "eu-west-2"
service = "api"

def sn(str):
    if len(str) > 16:
        return str[:14] + "..."
    return str

def main(ak=key, sk=secret, format=["png", "dot"], region=region, service=service):
    driver = osc_sdk_python.Gateway(access_key=ak, secret_key=sk, region=region)

    nodes = driver.ReadVms()["Vms"]

    with Diagram("All Vms", outformat=format, direction="BT"):
        for n in nodes:
            nname = n["Tags"][0]["Value"] if len(n["Tags"]) else "(no Name)"
            ip = n['PublicIp'] if 'PublicIp' in n else ""
            vm = Compute(sn(nname) + '\n`' + ip)
            with Cluster("SG:\n" + nname + '\n' + n['VmId']):
                sgs_cluster = []
                if 'SecurityGroups' in n:
                    for sg in n['SecurityGroups']:
                        sg_name = sg["SecurityGroupName"]
                        sgs_cluster.append(IdentityAndAccessManagement(sn(sg_name)))
                    
            with Cluster("Devs:\n" + nname + '\n' + n['VmId']):
                bd_cluster = []
                if 'BlockDeviceMappings' in n:
                    for bd in  n['BlockDeviceMappings']:
                        dev_name = bd["DeviceName"]
                        bd_cluster.append(Storage(sn(dev_name) + "\n" + bd["Bsu"]["VolumeId"]))
            vm >> sgs_cluster
            vm >> bd_cluster


if __name__ == "__main__":
    main()
