from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from diagrams import Cluster, Diagram
from diagrams.outscale.compute import Compute
from diagrams.outscale.security import IdentityAndAccessManagement
from diagrams.outscale.storage import Storage 
import os

key = os.environ['OSC_ACCESS_KEY']
secret = os.environ["OSC_SECRET_KEY"]
region = "eu-west-2"
service = "api"

def main():
    Driver = get_driver(Provider.OUTSCALE)
    driver = Driver(key=key, secret=secret, region=region, service=service)

    nodes = driver.list_nodes()

    print(nodes)

    with Diagram("All Vms", outformat=["png", "dot"], direction="BT"):
        for n in nodes:
            print(n.name, ": ", n.extra['VmId'])
            vm = Compute(n.name)
            with Cluster("SG:\n" + n.name + '\n' + n.extra['VmId']):
                sgs_cluster = []
                for sg in  n.extra['SecurityGroups']:
                    sgs_cluster.append(IdentityAndAccessManagement(sg["SecurityGroupName"]))
                    print(sg)
            with Cluster("Devs:\n" + n.name + '\n' + n.extra['VmId']):
                bd_cluster = []
                for bd in  n.extra['BlockDeviceMappings']:
                    bd_cluster.append(Storage(bd["DeviceName"] + "\n" + bd["Bsu"]["VolumeId"]))
                    print(sg)
            vm >> sgs_cluster
            vm >> bd_cluster


if __name__ == "__main__":
    main()
