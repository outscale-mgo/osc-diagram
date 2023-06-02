from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
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
    Driver = get_driver(Provider.OUTSCALE)
    driver = Driver(key=ak, secret=sk, region=region, service=service)

    nodes = driver.list_nodes()

    with Diagram("All Vms", outformat=format, direction="BT"):
        for n in nodes:
            nname = n.name
            nextra = n.extra
            ip = nextra['PublicIp'] if 'PublicIp' in nextra else ""
            vm = Compute(sn(nname) + '\n`' + ip)
            with Cluster("SG:\n" + nname + '\n' + nextra['VmId']):
                sgs_cluster = []
                if 'SecurityGroups' in nextra:
                    for sg in  nextra['SecurityGroups']:
                        sg_name = sg["SecurityGroupName"]
                        sgs_cluster.append(IdentityAndAccessManagement(sn(sg_name)))
                    
            with Cluster("Devs:\n" + nname + '\n' + nextra['VmId']):
                bd_cluster = []
                if 'BlockDeviceMappings' in nextra:
                    for bd in  nextra['BlockDeviceMappings']:
                        dev_name = bd["DeviceName"]
                        bd_cluster.append(Storage(sn(dev_name) + "\n" + bd["Bsu"]["VolumeId"]))
            vm >> sgs_cluster
            vm >> bd_cluster


if __name__ == "__main__":
    main()
