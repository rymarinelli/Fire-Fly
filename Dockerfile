FROM openjdk:8-alpine
RUN apk --update add wget tar bash
RUN wget https://apache.claz.org/spark/spark-3.0.1/spark-3.0.1-bin-hadoop2.7.tgz
RUN tar -xzf spark-3.0.1-bin-hadoop2.7.tgz && \
    mv spark-3.0.1-bin-hadoop2.7 /spark && \
    rm spark-3.0.1-bin-hadoop2.7.tgz