FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y postgresql

USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER app WITH SUPERUSER PASSWORD 'app';" &&\
    createdb -O app db

EXPOSE 5432

# CMD ["postgres"]