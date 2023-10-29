import { ConsoleSpanExporter } from '@opentelemetry/sdk-trace-base';
import { WebTracerProvider } from '@opentelemetry/sdk-trace-web';
import { BaseOpenTelemetryComponent } from '@opentelemetry/plugin-react-load';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { diag, DiagConsoleLogger } from '@opentelemetry/api';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions'
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
import { registerInstrumentations } from '@opentelemetry/instrumentation';


export default (serviceName) => {
  const provider = new WebTracerProvider({
    resource: new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: process.env.OTEL_SERVICE_NAME,
        [SemanticResourceAttributes.SERVICE_NAMESPACE]: process.env.SERVICE_NAMESPACE,
        [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.DEPLOYMENT_ENVIRONMENT
    }),
  });

  // https://www.npmjs.com/package/@opentelemetry/exporter-trace-otlp-http
  const exporter = new OTLPTraceExporter({
    // url: "http://localhost:4318/v1/traces", by default. http://127.0.0.1:3000 violate sop.
    // url: "http://lvh.me:4318/v1/traces",  // http
    // url: "http://otlp.lvh.me/v1/traces",  // http
    // url: "http://lvh.me/v1/traces",  // http to avoid CORS error
    // url: process.env.EXPORTER_OTLP_ENDPOINT,
  });

  provider.addSpanProcessor(new BatchSpanProcessor(new ConsoleSpanExporter()));
  provider.addSpanProcessor(new BatchSpanProcessor(exporter));

  provider.register({
    contextManager: new ZoneContextManager(),
  });
  registerInstrumentations({
    instrumentations: [
      // https://www.npmjs.com/package/@opentelemetry/instrumentation-fetch
      new FetchInstrumentation({
        // propagateTraceHeaderCorsUrls
        // https://github.com/open-telemetry/opentelemetry-js/discussions/2209
        // https://open-telemetry.github.io/opentelemetry-js/interfaces/_opentelemetry_instrumentation_fetch.FetchInstrumentationConfig.html
        // https://github.com/open-telemetry/opentelemetry-js/tree/main/examples/opentelemetry-web
        propagateTraceHeaderCorsUrls: [
          /http:\/\/api.lvh.me\/.*/,
        ],
      }),
    ],
  });

  const tracer = provider.getTracer(serviceName);

  BaseOpenTelemetryComponent.setTracer(serviceName)
  diag.setLogger(new DiagConsoleLogger());

  return tracer;
}
