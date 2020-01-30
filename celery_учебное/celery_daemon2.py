# https://www.linode.com/docs/development/python/task-queue-celery-rabbitmq/

# /etc/systemd/system/celeryd.service
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=/etc/default/celeryd
WorkingDirectory=/home/celery/downloaderApp
ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

[Install]
WantedBy=multi-user.target
    

# /etc/default/celeryd
# The names of the workers. This example create two workers
CELERYD_NODES="worker1 worker2"
# The name of the Celery App, should be the same as the python file
# where the Celery tasks are defined
CELERY_APP="downloaderApp"
# Log and PID directories
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"
# Log level
CELERYD_LOG_LEVEL=INFO
# Path to celery binary, that is in your virtual environment
CELERY_BIN=/home/celery/miniconda3/bin/celery
    



sudo mkdir /var/log/celery /var/run/celery
sudo chown celery:celery /var/log/celery /var/run/celery
sudo systemctl daemon-reload
sudo systemctl enable celeryd
sudo systemctl start celeryd




