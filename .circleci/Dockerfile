FROM docker:18.06.3-ce-git

RUN apk add --no-cache --virtual .build-deps \
    py-pip libffi-dev openssl openssl-dev python-dev gcc musl-dev make curl openjdk8-jre nodejs npm \
    && pip install --no-cache-dir docker-compose==1.24.1 awscli==1.16.224

RUN base=https://github.com/docker/machine/releases/download/v0.16.0 \
    && curl -L $base/docker-machine-$(uname -s)-$(uname -m) >/tmp/docker-machine \
    && mv /tmp/docker-machine /usr/local/bin/docker-machine \
    && chmod +x /usr/local/bin/docker-machine

RUN npm install @sentry/cli

# Installing glibc as a temporary workaround due to the following issue:
# https://github.com/codacy/codacy-coverage-reporter/issues/212
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub \
    && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.28-r0/glibc-2.28-r0.apk \
    && apk add glibc-2.28-r0.apk
