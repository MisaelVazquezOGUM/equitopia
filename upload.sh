#!/bin/bash
print_help() {
	echo "upload.sh - utility to upload changes to test server"
	echo "Usage: ./upload.sh file FILES"
	echo "       ./upload.sh module MODULES"
}

upload_file() {
	echo "Make sure you aren't passing any directory, otherwise it can mess up the remote modules."
	echo "If you need to upload a directory, please use the module option".
	read -p "Press ENTER to continue or C-c to exit >" yorn 

	shift
	while test $# -gt 0
	do
		echo -n "Uploading file $1 ..."
		sshpass -p '214gGy&Nk&' scp -r $1 root@74.208.24.94:/odoo/custom/addons/$1
		echo "done."

		shift
	done
}

upload_module() {
	shift
	while test $# -gt 0
	do
		echo -n "Deleting remote module $1 ..."
		sshpass -p '214gGy&Nk&' ssh root@74.208.24.94 'rm -rf $1'
		echo "done."

		echo -n "Uploading module $1 ..."
		sshpass -p '214gGy&Nk&' scp -r $1 root@74.208.24.94:/odoo/custom/addons/$1
		echo "done."

		shift
	done
}

case $1 in
	"file")
		upload_file $@
		;;
	"module")
		upload_module $@
		;;
	*)
		print_help
		;;
esac
		
