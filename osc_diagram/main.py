from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from diagrams import Cluster, Diagram
from diagrams.generic.virtualization import Qemu
from diagrams.outscale.security import IdentityAndAccessManagement
from diagrams.outscale.storage import Storage 
import os

key = os.environ['OSC_ACCESS_KEY']
secret = os.environ["OSC_SECRET_KEY"]
region = "eu-west-2"
service = "api"


def sn(str):
    if len(str) > 16:
        return str[:14] + "..."
    return str

def main():
    Driver = get_driver(Provider.OUTSCALE)
    driver = Driver(key=key, secret=secret, region=region, service=service)

    nodes = driver.list_nodes()

    print(nodes)

    with Diagram("All Vms", outformat=["png", "dot"], direction="BT"):
        for n in nodes:
            nextra = n.extra
            print(n.name, ": ", n.extra['VmId'])
            vm = Qemu(n.name + '\n`' + nextra['PublicIp'])
            with Cluster("SG:\n" + (n.name if n.name else "(no name)") + '\n' + n.extra['VmId']):
                sgs_cluster = []
                for sg in  n.extra['SecurityGroups']:
                    sgs_cluster.append(IdentityAndAccessManagement(sn(sg["SecurityGroupName"])))
                    print(sg)
            with Cluster("Devs:\n" + n.name + '\n' + n.extra['VmId']):
                bd_cluster = []
                for bd in  n.extra['BlockDeviceMappings']:
                    vol = driver.list_volumes('{"Filters": { "VolumeIds":["' + bd["Bsu"]["VolumeId"] +  '"]}}')
                    print(vol)
                    bd_cluster.append(Storage(bd["DeviceName"] + "\n" + bd["Bsu"]["VolumeId"] + "\n" + str(vol[0].size) + "GB"))
                    print(sg)
            vm >> sgs_cluster
            bd_cluster << vm


if __name__ == "__main__":
    main()
