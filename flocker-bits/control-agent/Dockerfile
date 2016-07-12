# control-service Dockerfile
FROM cedbossneo/flocker-core:1.13.0
MAINTAINER Madhuri Yechuri <madhuri.yechuri@clusterhq.com>

EXPOSE 4523-4524
RUN sudo bash -c "echo 'flocker-control-api 4523/tcp    # Flocker Control API port' >> /etc/services"
RUN sudo bash -c "echo 'flocker-control-agent   4525/tcp    # Flocker Control Agent port' >> /etc/services"

RUN cd /tmp \
  && curl -o rclone-current-linux-386.zip -s http://downloads.rclone.org/rclone-current-linux-386.zip \
  && unzip /tmp/rclone-current-linux-386.zip \
  && mv /tmp/rclone-*-linux-386/rclone /usr/bin \
  && rm -r /tmp/rclone*

ADD crontab /etc/cron.d/backup
RUN chmod 0644 /etc/cron.d/backup
RUN /usr/bin/crontab /etc/cron.d/backup
ADD run.sh /run.sh
ADD backup.sh /root/backup.sh

CMD ["/run.sh"]
