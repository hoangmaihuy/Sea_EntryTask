sudo yum install epel-release
sudo yum update -y && sudo reboot
sudo yum install python-devel python-setuptools python-pip wget 
sudo pip install --upgrade pip
sudo pip install Django==1.11.20 
wget https://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm
sudo rpm -ivh mysql57-community-release-el7-9.noarch.rpm
sudo yum install mysql-server
sudo systemctl start mysqld
