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
        [SemanticResourceAttributes.SERVICE_NAME]: "react-load-example"
    }),
  });

  const exporter = new OTLPTraceExporter();

  provider.addSpanProcessor(new BatchSpanProcessor(new ConsoleSpanExporter()));
  provider.addSpanProcessor(new BatchSpanProcessor(exporter));

  provider.register({
    contextManager: new ZoneContextManager(),
  });
  registerInstrumentations({
    instrumentations: [new FetchInstrumentation()],
  });

  const tracer = provider.getTracer(serviceName);

  BaseOpenTelemetryComponent.setTracer(serviceName)
  diag.setLogger(new DiagConsoleLogger());

  return tracer;
}
