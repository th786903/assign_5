# installing nfs
sudo yum install nfs-utils

# making software directory
sudo mkdir /var/software

# setting permissions
sudo chmod -R 777 /var/software

# setting up nfs
sudo systemctl enable rpcbind
sudo systemctl enable nfs-server
sudo systemctl enable nfs-lock
sudo systemctl enable nfs-idmap
sudo systemctl start rpcbind
sudo systemctl start nfs-server
sudo systemctl start nfs-lock
sudo systemctl start nfs-idmap

# setup export directory
sudo echo "/var/software *(rw,sync,no_root_squash,no_all_squash)" > etc/exports
sudo systemctl restart nfs-server

# let nfs service override centos7 firewall
sudo firewall-cmd --permanent --zone=public --add-service=nfs
sudo firewall-cmd --permanent --zone=public --add-service=mountd
sudo firewall-cmd --permanent --zone=public --add-service=rpc-bind
sudo firewall-cmd --reload

# set client up, setup mount point from storage, to head
sudo mkdir -p /mnt/nfs/var/scratch
sudo mount -t nfs 192.168.1.3:/var/scratch /mnt/nfs/var/scratch

# setup automount
sudo echo "192.168.1.3:/var/scratch /mnt/nfs/var/scratch nfs defaults 0 0" >> /etc/fstab


