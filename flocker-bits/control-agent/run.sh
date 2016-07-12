#!/bin/bash
cat <<EOF > /root/.rclone.conf
[Openstack]
type = swift
user = ${OS_USERNAME}
key = ${OS_PASSWORD}
auth = ${OS_AUTH_URL}
tenant = ${OS_TENANT_NAME}
region = ${OS_REGION}
storage_url =
EOF

mkdir -p /var/lib/flocker
rclone copy Openstack:flocker-backup-${STACK} /var/lib/flocker
cron
/usr/sbin/flocker-control -p tcp:4523 -a tcp:4524
