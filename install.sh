#!/usr/bin/env bash

#
#  gem5 installer 
#
#  disclaimer: you can use this script or read the documentation
#              on the gem5 website
#
#


if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

requirements=\
"
build-essential 
git 
m4 
scons 
zlib1g 
zlib1g-dev 
libprotobuf-dev 
protobuf-compiler 
libprotoc-dev 
libgoogle-perftools-dev 
python-dev 
python
python3
libboost-all-dev
automake
"

version=$(cat /etc/*release | grep "ID_LIKE")
if [[ $version =~ "debian" ]] ; then
    sudo apt-get install $requirements
else
    for pkg in $requirements ; do  echo $pkg ; done 
    echo "You have to figure out how to install the packages"
    echo "for your distributation of linux"
    echo "you could create a docker for this project"
    exit 1 
fi

git clone https://gem5.googlesource.com/public/gem5

if ! [ -d gem5 ] ; then echo "gem5 was not created ! " ; exit 1 ; fi 
echo "Complete!"
