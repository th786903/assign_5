# installing nfs
sudo yum install nfs-utils

# make nfs directory mount points
sudo mkdir -p /scratch
sudo mkdir -p /software

# mount nfs shared directory to the mount point
sudo mount -t nfs 192.168.1.3:/scratch /scratch
sudo mount -t nfs 192.168.1.1:/software /software

#i think i have to echo into something like /mnt/nfs/var blah
# automount
sudo echo "192.168.1.3:/scratch /scratch nfs defaults 0 0" >> /etc/fstab
sudo echo "192.168.1.1:/software /software nfs defaults 0 0" >> /etc/fstab
