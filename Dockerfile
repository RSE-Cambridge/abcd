FROM postgres:alpine
MAINTAINER Jeffrey Salmond <js947@cam.ac.uk>
COPY sql/create.sql /docker-entrypoint-initdb.d/01-create.sql
COPY sql/views.sql /docker-entrypoint-initdb.d/02-views.sql
