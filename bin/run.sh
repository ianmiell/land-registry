#!/bin/bash
# Example for running
DOCKER=${DOCKER:-docker}
IMAGE_NAME=land_registry
CONTAINER_NAME=$IMAGE_NAME
DOCKER_ARGS=''
while getopts "i:c:a:" opt
do
	case "$opt" in
	i)
		IMAGE_NAME=$OPTARG
		;;
	c)
		CONTAINER_NAME=$OPTARG
		;;
	a)
		DOCKER_ARGS=$OPTARG
		;;
	esac
done
${DOCKER} run -d --name ${CONTAINER_NAME} ${DOCKER_ARGS} ${IMAGE_NAME} /bin/sh -c '/root/start_postgres.sh && sleep infinity'
