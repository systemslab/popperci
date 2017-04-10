FROM python:2.7

RUN apt-get update && \
    apt-get install -y git && \
    git clone https://github.com/carlos-jenkins/python-github-webhooks /app && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

RUN cd /app && \
    pip install -r requirements.txt && \
    pip install SQLAlchemy

ADD executioner.py /app
ADD entrypoint.sh /app
ADD config.json /app
ADD push /app/hooks/

EXPOSE 5000

CMD ["/app/entrypoint.sh"]
