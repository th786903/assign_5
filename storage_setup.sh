# installing nfs
sudo yum install nfs-utils

# making software directory
sudo mkdir /scratch

# setting permissions
sudo chmod -R 777 /scratch

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
sudo echo "/scratch *(rw,sync,no_root_squash,no_all_squash)" > etc/exports
sudo systemctl restart nfs-server

# let nfs service override centos7 firewall
sudo firewall-cmd --permanent --zone=public --add-service=nfs
sudo firewall-cmd --permanent --zone=public --add-service=mountd
sudo firewall-cmd --permanent --zone=public --add-service=rpc-bind
sudo firewall-cmd --reload

sudo cp /local/repository/source/* /scratch
