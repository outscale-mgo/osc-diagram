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
            vm = Compute(n.name)
            with Cluster("SG:\n" + n.name + '\n' + n.extra['VmId']):
                sgs_cluster = []
                for sg in  n.extra['SecurityGroups']:
                    sgs_cluster.append(IdentityAndAccessManagement(sg["SecurityGroupName"]))
                    
            with Cluster("Devs:\n" + n.name + '\n' + n.extra['VmId']):
                bd_cluster = []
                for bd in  n.extra['BlockDeviceMappings']:
                    bd_cluster.append(Storage(bd["DeviceName"] + "\n" + bd["Bsu"]["VolumeId"]))
            vm >> sgs_cluster
            vm >> bd_cluster


if __name__ == "__main__":
    main()
