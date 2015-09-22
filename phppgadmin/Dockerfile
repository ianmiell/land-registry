FROM ubuntu:precise
RUN apt-get update -y && apt-get install -y phppgadmin vim
RUN sed -i 's/^allow from.*/allow from all/' /etc/apache2/conf.d/phppgadmin
RUN sed -i 's/^deny from.*//' /etc/apache2/conf.d/phppgadmin
RUN sed -i 's/ 5432;/ 15432;/' /usr/share/phppgadmin/conf/config.inc.php
RUN sed -i 's/template1/land_registry/' /usr/share/phppgadmin/conf/config.inc.php
RUN sed -i 's/localhost/themortgagemeter.com/' /usr/share/phppgadmin/conf/config.inc.php
CMD /bin/sh -c '/usr/sbin/apache2ctl start && sleep infinity'
