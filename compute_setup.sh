# installing nfs
sudo yum install nfs-utils

# make nfs directory mount points
sudo mkdir -p /mnt/nfs/var/scratch
sudo mkdir -p /mnt/nfs/var/software

# mount nfs shared directory to the mount point
sudo mount -t nfs 192.168.1.3:/var/scratch /mnt/nfs/var/scratch
sudo mount -t nfs 192.168.1.1:/var/software /mnt/nfs/var/software

# automount
sudo echo '192.168.1.3:/var/scratch /mnt/nfs/var/scratch nfs defaults 0 0' >> etc/fstab
sudo echo '192.168.1.1:/var/software /mnt/nfs/var/software nfs defaults 0 0' >> etc/fstab
