#!/bin/bash
set -o nounset
# set -o errexit
# set -x
export DEBIAN_FRONTEND=noninteractive
DOCKER_CMD="docker run"
WORKAREA=/workarea
CHECK_EVERY=30
exec 3>&1 1>>${LOG_FILE} 2>&1

_log() {
   echo "$(date): $@" | tee /dev/fd/3
}

command_exists() {
	command -v "$@" > /dev/null 2>&1
}

if ! command_exists "cscli" &> /dev/null
then
    curl -Ls https://raw.githubusercontent.com/nuxion/cloudscripts/main/install.sh | sh
fi
if ! command_exists "jq" &> /dev/null
then
    apt-get install -y jq
fi

META=`curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/?recursive=true" -H "Metadata-Flavor: Google"`
DEBUG=`echo $META | jq .debug | tr -d '"'`
REGISTRY=`echo $META | jq .registry | tr -d '"'`

login_docker() {
    # https://${LOCATION}-docker.pkg.dev
    gcloud auth print-access-token  | docker login -u oauth2accesstoken  --password-stdin https://${REGISTRY}
}
