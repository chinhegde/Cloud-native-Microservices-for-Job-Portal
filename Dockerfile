FROM python

RUN mkdir -p /application
RUN cd /application
COPY . /application

RUN pip3 install flask
RUN pip3 install boto3
RUN pip3 install jwt
RUN pip3 install requests

CMD ["python3", "/application/app.py"]