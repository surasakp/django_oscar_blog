FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

ADD oscar-blog /app

WORKDIR /app/

RUN pip install virtualenv

RUN virtualenv -p python3 /appenv && \
    . /appenv/bin/activate

# Add entrypoint script
ADD scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
