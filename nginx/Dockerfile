# https://opentelemetry.io/blog/2022/instrument-nginx/

# supports: 1.18, 1.22.0, 1.23.1
ARG VARIANT=1.18

FROM nginx:1.18 AS nginx-1.18
ADD https://github.com/open-telemetry/opentelemetry-cpp-contrib/releases/download/webserver%2Fv1.0.1/opentelemetry-webserver-sdk-x64-linux.tgz /opt
RUN echo "load_module /opt/opentelemetry-webserver-sdk/WebServerModule/Nginx/ngx_http_opentelemetry_module.so;\n$(cat /etc/nginx/nginx.conf)" > /etc/nginx/nginx.conf


FROM nginx:1.22.0 AS nginx-1.22.0
ADD https://github.com/open-telemetry/opentelemetry-cpp-contrib/releases/download/webserver%2Fv1.0.2/opentelemetry-webserver-sdk-x64-linux.tgz.zip /opt
RUN echo "load_module /opt/opentelemetry-webserver-sdk/WebServerModule/Nginx/1.22.0/ngx_http_opentelemetry_module.so;\n$(cat /etc/nginx/nginx.conf)" > /etc/nginx/nginx.conf


FROM nginx:1.23.1 AS nginx-1.23.1
ADD https://github.com/open-telemetry/opentelemetry-cpp-contrib/releases/download/webserver%2Fv1.0.2/opentelemetry-webserver-sdk-x64-linux.tgz.zip /opt
RUN echo "load_module /opt/opentelemetry-webserver-sdk/WebServerModule/Nginx/1.23.1/ngx_http_opentelemetry_module.so;\n$(cat /etc/nginx/nginx.conf)" > /etc/nginx/nginx.conf


FROM nginx-${VARIANT}

RUN apt-get update ; apt-get install unzip

RUN cd /opt ; \
    unzip opentelemetry-webserver-sdk-x64-linux.tgz.zip; \
    tar xvfz opentelemetry-webserver-sdk-x64-linux.tgz

RUN cd /opt/opentelemetry-webserver-sdk; \
    ./install.sh

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/opentelemetry-webserver-sdk/sdk_lib/lib

COPY opentelemetry_module.conf /etc/nginx/conf.d
