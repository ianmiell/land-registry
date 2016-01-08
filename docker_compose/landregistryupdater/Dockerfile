FROM ubuntu:14.04
RUN apt-get update -y && apt-get install -y python-pygresql git python-pip wget postgresql-client
RUN pip install shutit
RUN git clone --recursive https://github.com/ianmiell/land-registry.git
WORKDIR land-registry
RUN find . -name build.cnf | xargs chmod 0600
RUN echo "0 0 * * * cd /land-registry/context/replenish/bin && ./build.sh" | crontab -
CMD ["cron","-f","-L","8"]
