FROM alpine:latest
RUN apk add --no-cache tor

RUN echo "Log notice stdout" >> /etc/torrc
RUN echo "SocksPort 0.0.0.0:9150" >> /etc/torrc

EXPOSE 9150

CMD tor -f /etc/torrc