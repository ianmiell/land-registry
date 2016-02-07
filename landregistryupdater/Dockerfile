FROM ubuntu:14.04
RUN apt-get update -y && apt-get install -y python-pygresql git python-pip wget postgresql-client
RUN pip install shutit
RUN git clone https://github.com/ianmiell/land-registry.git
RUN echo "0 0 * * * cd /land-registry/shutit/context/replenish/bin && ./build.sh 2>&1 >> /lrupdater.log" | crontab -
CMD ["cron","-f","-L","8"]
