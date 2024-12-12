FROM ubuntu:latest
LABEL authors="Xiaomi"

ENTRYPOINT ["top", "-b"]