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

def main(ak=key, sk=secret, format=["png", "dot"], region=region, service=service):
    Driver = get_driver(Provider.OUTSCALE)
    driver = Driver(key=ak, secret=sk, region=region, service=service)

    nodes = driver.list_nodes()

    with Diagram("All Vms", outformat=format, direction="BT"):
        for n in nodes:
            nname = n.name
            if len(nname) > 16:
                nname=nname[:16] + "..."
            vm = Compute(nname)
            with Cluster("SG:\n" + nname + '\n' + n.extra['VmId']):
                sgs_cluster = []
                if 'SecurityGroups' in n.extra:
                    for sg in  n.extra['SecurityGroups']:
                        sg_name = sg["SecurityGroupName"]
                        if len(sg_name) > 16:
                            sg_name=sg_name[:16] + "..."
                        sgs_cluster.append(IdentityAndAccessManagement(sg_name))
                    
            with Cluster("Devs:\n" + nname + '\n' + n.extra['VmId']):
                bd_cluster = []
                if 'BlockDeviceMappings' in n.extra:
                    for bd in  n.extra['BlockDeviceMappings']:
                        dev_name = bd["DeviceName"]
                        if len(dev_name) > 16:
                            dev_name=dev_name[:16] + "..."
                        bd_cluster.append(Storage(dev_name + "\n" + bd["Bsu"]["VolumeId"]))
            vm >> sgs_cluster
            vm >> bd_cluster


if __name__ == "__main__":
    main()
