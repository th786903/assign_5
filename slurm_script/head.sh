#!/bin/bash

# the folliwng came from https://www.slothparadise.com/how-to-install-slurm-on-centos-7-cluster/

sudo yum install mariadb-server mariadb-devel -y

# created global users so UID and GID is consistent across every node
export MUNGEUSER=991
sudo groupadd -g $MUNGEUSER munge
sudo useradd  -m -c "MUNGE Uid 'N' Gid Emporium" -d /var/lib/munge -u $MUNGEUSER -g munge  -s /sbin/nologin munge
export SLURMUSER=992
sudo groupadd -g $SLURMUSER slurm
sudo useradd  -m -c "SLURM workload manager" -d /var/lib/slurm -u $SLURMUSER -g slurm  -s /bin/bash slurm

# install epel-release because we're using CentOS
sudo yum install epel-release

# installing munge
sudo yum install munge munge-libs munge-devel -y

# install tools to create the secret munge key
sudo yum install rng-tools -y
sudo rngd -r /dev/urandom

# create key
sudo /usr/sbin/create-munge-key -r
sudo dd if=/dev/urandom bs=1 count=1024 > /etc/munge/munge.key
sudo chown munge: /etc/munge/munge.key
sudo chmod 400 /etc/munge/munge.key

# send the key to shared directory
sudo cp /etc/munge/munge.key /scratch

# correcting permissions
sudo chown -R munge: /etc/munge/ /var/log/munge/
sudo chmod 0700 /etc/munge/ /var/log/munge/

# starting the service
sudo systemctl enable munge
sudo systemctl start munge

# installing slurm dependencies
sudo yum install openssl openssl-devel pam-devel numactl numactl-devel hwloc
sudo yum install hwloc-devel lua lua-devel readline-devel rrdtool-devel ncurses-devel man2html libibmad libibumad pam-devel 'perl(ExtUtils::Embed)' -y

# installing the LATEST version of slurm into shared software folder
cd /software
sudo wget https://download.schedmd.com/slurm/slurm-18.08.3.tar.bz2
sudo yum install rpm-build
sudo rpmbuild -ta slurm-18.08.3.tar.bz2

# moving rpms for installation on server and compute nodes
sudo cd /root/rpmbuild/RPMS/x86_64
sudo mkdir /software/slurm-rpms
sudo cp * /software/slurm-rpms

#create file to check that rpms have been moved
sudo echo "I am done" > /scratch/rpmMove.txt

# install rpms
sudo yum --nogpgcheck localinstall /software/slurm-rpms/*
