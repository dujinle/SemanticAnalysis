FROM ubuntu:14.04.3

MAINTAINER SemanticAnalysis authr dujinle

RUN cp /etc/apt/sources.list /etc/apt/sources.list.raw
ADD https://github.com/codemeow5/software/raw/master/ubt_sources_list_aliyun.txt /etc/apt/sources.list
RUN apt-get update && apt-get install wget -y

RUN apt-get install python-pip build-essential python-dev -y
RUN pip install tornado

EXPOSE 80

RUN echo Asia/Shanghai > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata

ADD https://github.com/dujinle/WeEnv/blob/master/sources.list /etc/apt/sources.list
ADD https://github.com/dujinle/WeEnv/blob/master/local /var/lib/locales/supported.d/local

EXPOSE 8082

RUN locale-gen --purge
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8


RUN mkdir /root/SemanticAnalysis
RUN mkdir /root/SemanticAnalysis/commons
COPY commons /root/SemanticAnalysis/commons

RUN mkdir /root/SemanticAnalysis/mainpy
COPY mainpy /root/SemanticAnalysis/mainpy

RUN mkdir /root/SemanticAnalysis/webroot
COPY webroot /root/SemanticAnalysis/webroot

RUN mkdir /root/SemanticAnalysis/data
COPY data /root/SemanticAnalysis/data

COPY semantic /root/SemanticAnalysis/semantic
RUN chmod +x /root/SemanticAnalysis/semantic

CMD /root/SemanticAnalysis/semantic start
