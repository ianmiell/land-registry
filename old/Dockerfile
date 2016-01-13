FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y -qq curl git python-pip
RUN pip install shutit

WORKDIR /opt
RUN git clone https://github.com/ianmiell/land-registry
WORKDIR /opt/land-registry
RUN shutit build --delivery dockerfile

EXPOSE 5432
ENTRYPOINT ["/run.sh"]                                                                                                                                                        
