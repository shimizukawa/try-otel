# https://github.com/open-telemetry/opentelemetry-cpp-contrib/blob/main/instrumentation/nginx/README.md

# supports: 1.22.0
ARG VARIANT=1.22.0
FROM nginx:${VARIANT}

RUN apt-get update ; apt-get install unzip

# download: https://github.com/open-telemetry/opentelemetry-cpp-contrib/suites/8782080474/artifacts/398699370
# save as: otel_ngx_module-debian-11.3-stable.so.zip
COPY otel_ngx_module-debian-11.3-stable.so.zip /opt
RUN cd /opt ; \
    unzip otel_ngx_module-debian-11.3-stable.so.zip -d nginx-${VARIANT}
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/nginx-${VARIANT}/

RUN echo "load_module /opt/nginx-${VARIANT}/otel_ngx_module.so;\n$(cat /etc/nginx/nginx.conf)" > /etc/nginx/nginx.conf

# COPY otel-nginx.toml /etc/nginx/conf.d
