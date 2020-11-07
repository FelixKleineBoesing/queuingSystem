FROM postgres:13.0

ENV POSTGRES_USER=Saitama
ENV POSTGRES_PASSWORD=onepunchman
ENV POSTGRES_DB=Tracking

RUN echo "host    all    all    0.0.0.0/0    trust" >> /var/lib/postgresql/data/pg_hba.conf