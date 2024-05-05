FROM redhat/ubi9:latest

ENV PHP_VERSION 8.2
ENV APACHE_DOCUMENT_ROOT /var/www/html

ARG WEBSERVER_HTTP_PORT=8080
ARG WEBSERVER_HTTPS_PORT=8443

RUN dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
    dnf -y install https://rpms.remirepo.net/enterprise/remi-release-9.rpm && \
    dnf module reset php -y && dnf -y module install php:remi-8.2 && dnf -y install php

RUN yum -y update && \
    yum -y install php-pgsql php-gd php-zip php-ldap httpd net-tools libcap npm && \
    yum clean all && \
    dnf clean all

RUN useradd -rm -u 1001 openid && usermod -aG wheel openid

RUN cd /etc/yum.repos.d/ && \
    curl http://rpms.adiscon.com/v8-stable/rsyslog-rhel.repo -o rsyslog-rhel.repo && \
    yum -y install rsyslog

COPY 00-apache.conf /etc/rsyslog.d/
RUN rsyslogd

RUN mkdir /run/php-fpm

COPY app /var/www/html
WORKDIR /var/www/html

RUN mv /etc/httpd/conf/httpd.conf /tmp/
COPY httpd.conf /etc/httpd/conf/httpd.conf

RUN mv /etc/php-fpm.d/www.conf /tmp/
COPY www.conf /etc/php-fpm.d/www.conf

RUN mv /etc/php.ini /tmp/
COPY php.ini /etc/php.ini
    
RUN mkdir ./tmp && \
    touch /var/log/php-fpm/error.log && \
    touch /var/log/httpd/error_log && \
    chmod 644 /etc/httpd/conf/httpd.conf /etc/php-fpm.d/www.conf /etc/php.ini && \
    chmod 755 -R /var/log/php-fpm && \
    chown -hR openid:openid /run/httpd/ && \
    chown -hR openid:openid /var/www/ && \
    chown -hR openid:openid /etc/httpd/ && \
    chown -hR openid: /var/log/httpd/ && \
    chown -hR openid:openid /etc/php* && \
    chown -hR openid:openid /run/php-fpm && \
    chown -hR openid: /var/log/php-fpm && \
    chown -hR openid:openid /var/lib/php && \
    chown -hR openid:openid /var/lib/httpd && \
    chown -hR openid:openid /var/lib/rsyslog && \
    chown -hR openid:openid /etc/php.ini && \
    chown -hR openid:openid /etc/ssl && \
    chown -hR openid:openid /etc/pki

USER openid

EXPOSE $WEBSERVER_HTTP_PORT

CMD /usr/sbin/php-fpm -D; /usr/sbin/httpd -D FOREGROUND