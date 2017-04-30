FROM ivotron/web2py-nginx

# install the hook

RUN apt-get update && \
    apt-get install -y git && \
    git clone https://github.com/carlos-jenkins/python-github-webhooks /app && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN cd /app && \
    pip install -r requirements.txt && \
    pip install SQLAlchemy

ADD webhook/executioner.py /app
ADD webhook/config.json /app
ADD webhook/push /app/hooks/

EXPOSE 5000

# add the web2py frontend

COPY frontend /opt/web2py/applications/popperci

EXPOSE 80

ADD entrypoint.sh /root/poppercientrypoint.sh

ENV WORKSPACE=/var/popperci/workspace
ENV CREDENTIALS=/var/popperci/credentials
ENV SQLITEDB=/var/popperci/db/storage.sqlite

CMD ["/root/poppercientrypoint.sh"]
