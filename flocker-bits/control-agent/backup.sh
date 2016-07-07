#!/bin/sh
/usr/bin/rclone copy /var/lib/flocker Openstack:flocker-backup-${STACK}
