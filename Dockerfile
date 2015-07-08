FROM centos:centos7

RUN yum -y update
RUN yum -y install gcc python-devel
RUN curl -kL https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

RUN pip install numpy

RUN mkdir -p /opt/t4j/chainerapp