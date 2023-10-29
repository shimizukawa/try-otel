FROM node:16

WORKDIR /code

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,rw,source=package.json,target=package.json \
    --mount=type=bind,rw,source=package-lock.json,target=package-lock.json \
    npm install \
    npx update-browserslist-db@latest

COPY --chown=node:node . /code/
RUN mkdir -p /code/node_modules/ && chmod -R node:node /code/node_modules/

# https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/
# https://opentelemetry.io/docs/reference/specification/sdk-environment-variables/
# https://opentelemetry.io/docs/reference/specification/resource/sdk/
# https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/
ENV OTEL_SERVICE_NAME "react-front"
ENV SERVICE_NAMESPACE "myapp"
ENV DEPLOYMENT_ENVIRONMENT "demo"

# https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/
# https://opentelemetry.io/docs/reference/specification/protocol/exporter/#configuration-options
ENV EXPORTER_OTLP_ENDPOINT "http://localhost:4317/v1/traces"

CMD npm run dev
