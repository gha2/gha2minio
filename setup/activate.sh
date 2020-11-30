#!/bin/bash


MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[  -f /etc/redhat-release ]]
then
	# shellcheck disable=SC1090
	source "${MYDIR}"/../venv_rhel/bin/activate
	PS1='[gha2minio_rhel] \h:\W \u\$ '
elif [[ "$OSTYPE" == "darwin"* ]]
then
	# shellcheck disable=SC1090
	source "${MYDIR}"/../venv/bin/activate
	PS1='[gha2minio_mac] \h:\W \u\$ '
else
	echo
	echo "Not on a RHEL or Centos or MacOs system. Exiting!"
	# shellcheck disable=SC2034
	read a
	exit 1
fi


