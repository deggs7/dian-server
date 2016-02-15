FROM python:2.7.10
ADD . /dian
WORKDIR /dian
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
