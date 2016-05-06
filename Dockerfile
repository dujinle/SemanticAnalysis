FROM ubuntu:14.04.3

MAINTAINER SemanticAnalysis authr dujinle

RUN cp /etc/apt/sources.list /etc/apt/sources.list.raw
ADD https://github.com/codemeow5/software/raw/master/ubt_sources_list_aliyun.txt /etc/apt/sources.list
RUN apt-get update && apt-get install wget -y

RUN apt-get install python-pip build-essential python-dev -y
RUN pip install tornado

EXPOSE 80

RUN echo Asia/Shanghai > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata

RUN mkdir /root/commons
COPY commons /root/commons

