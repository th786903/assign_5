# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


tourDescription = \
"""
This profile provides the template for a full research cluster with head node, scheduler, compute nodes, and shared file systems.
First node (head) should contain: 
- Shared home directory using Networked File System
- Management server for SLURM
Second node (metadata) should contain:
- Metadata server for SLURM
Third node (storage):
- Shared software directory (/software) using Networked File System
Remaining three nodes (computing):
- Compute nodes  
"""

#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)

prefixForIP = "192.168.1."

link = request.LAN("lan")

for i in range(6):
  if i == 0:
    node = request.XenVM("head")
    node.routable_control_ip = "true"
    
     #initiate nfs
    node.addService(pg.Execute(shell="sh", command="sudo yum -y install nfs-utils libnfsidmap"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl enable rpcbind"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl enable nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start rpcbind"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start rpc-statd"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start nfs-idmapd"))
    
    #create folders
    node.addService(pg.Execute(shell="sh", command="sudo mkdir /scratch"))   
    node.addService(pg.Execute(shell="sh", command="sudo mkdir -m 777 /software"))
    
    #added export permission
    node.addService(pg.Execute(shell="sh", command="sudo echo "/software 192.168.1.0/28(rw,sync,no_root_squash) 192.168.1.16(rw,sync,no_root_squash)" > etc/exports"))
    node.addService(pg.Execute(shell="sh", command="sudo exportfs -r"))
    
    #firewall
    node.addService(pg.Execute(shell="sh", command="sudo firewall-cmd --permanent --zone public --add-service mountd"))
    node.addService(pg.Execute(shell="sh", command="sudo firewall-cmd --permanent --zone public --add-service rpc-bind"))
    node.addService(pg.Execute(shell="sh", command="sudo firewall-cmd --permanent --zone public --add-service nfs"))
    node.addService(pg.Execute(shell="sh", command="sudo firewall-cmd --reload"))
    #mount
    node.addService(pg.Execute(shell="sh", command="sudo mount 192.168.1.3:/scratch /scratch"))
    node.addService(pg.Execute(shell="sh", command="sudo echo "192.168.1.3:/scratch /scratch nfs rw,sync,hard,intr 0 0" >> etc/fstab))
    #install mpi ----------- just testing mounting
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/install_mpi.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/install_mpi.sh"))
  elif i == 1:
    node = request.XenVM("metadata")
  elif i == 2:
    node = request.XenVM("storage")
    
    #initiate nfs
    node.addService(pg.Execute(shell="sh", command="sudo yum -y install nfs-utils libnfsidmap"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl enable rpcbind"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl enable nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start rpcbind"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start rpc-statd"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start nfs-idmapd"))
    
    node.addService(pg.Execute(shell="sh", command="sudo mkdir -m 777 /scratch"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* scratch'"))
    
    
    node.addService(pg.Execute(shell="sh", command="sudo echo "/scratch 192.168.1.0/28(rw,sync,no_root_squash) 192.168.1.16(rw,sync,no_root_squash)" > etc/exports"))
    node.addService(pg.Execute(shell="sh", command="sudo exportfs -r"))
    
    #firewall
    node.addService(pg.Execute(shell="sh", command="sudo firewall-cmd --permanent --zone public --add-service mountd"))
    node.addService(pg.Execute(shell="sh", command="sudo firewall-cmd --permanent --zone public --add-service rpc-bind"))
    node.addService(pg.Execute(shell="sh", command="sudo firewall-cmd --permanent --zone public --add-service nfs"))
    node.addService(pg.Execute(shell="sh", command="sudo firewall-cmd --reload"))
  else:
    node = request.XenVM("compute-" + str(i-2))

    node.cores = 4
    node.ram = 4096
    
    node.addService(pg.Execute(shell="sh", command="sudo yum -y install nfs-utils libnfsidmap"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl enable rpcbind"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start rpcbind"))
    
    node.addService(pg.Execute(shell="sh", command="sudo mkdir /software"))
    node.addService(pg.Execute(shell="sh", command="sudo mkdir /scratch"))
    
    node.addService(pg.Execute(shell="sh", command="sudo mount 192.168.1.1:/software /software"))
    node.addService(pg.Execute(shell="sh", command="sudo echo "192.168.1.1:/software /software nfs rw,sync,hard,intr 0 0" >> etc/fstab))
    node.addService(pg.Execute(shell="sh", command="sudo mount 192.168.1.3:/scratch /scratch"))
    node.addService(pg.Execute(shell="sh", command="sudo echo "192.168.1.3:/scratch /scratch nfs rw,sync,hard,intr 0 0" >> etc/fstab))
    

    
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
  
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/passwordless.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))
  
  # This code segment is added per Benjamin Walker's solution to address the StrictHostKeyCheck issue of ssh
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/ssh_setup.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo -H -u ka837933 bash -c '/local/repository/ssh_setup.sh'"))
 
  node.addService(pg.Execute(shell="sh", command="sudo su ka837933 -c 'cp /local/repository/source/* /users/ka837933'"))

  # start adding stuff here
  # %%

    

    
  
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
