import pymysql

from opentelemetry.instrumentation import dbapi
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor

__version__ = "0.19b0"


class DjangoMySQLInstrumentor(BaseInstrumentor):
    _CONNECTION_ATTRIBUTES = {
        "database": "db",
        "port": "port",
        "host": "host",
        "user": "user",
    }

    _DATABASE_SYSTEM = "mysql"

    def _instrument(self, **kwargs):
        """Integrate with the PyMySQL library.
        https://github.com/PyMySQL/PyMySQL/
        """
        tracer_provider = kwargs.get("tracer_provider")

        dbapi.wrap_connect(
            __name__,
            pymysql,
            "connect",
            self._DATABASE_SYSTEM,
            self._CONNECTION_ATTRIBUTES,
            version=__version__,
            tracer_provider=tracer_provider,
        )

    def _uninstrument(self, **kwargs):
        """"Disable PyMySQL instrumentation"""
        dbapi.unwrap_connect(pymysql, "connect")

    # pylint:disable=no-self-use
    def instrument_connection(self, connection):
        """Enable instrumentation in a PyMySQL connection.

        Args:
            connection: The connection to instrument.

        Returns:
            An instrumented connection.
        """

        return dbapi.instrument_connection(
            __name__,
            connection,
            self._DATABASE_SYSTEM,
            self._CONNECTION_ATTRIBUTES,
            version=__version__,
        )

    def uninstrument_connection(self, connection):
        """Disable instrumentation in a PyMySQL connection.

        Args:
            connection: The connection to uninstrument.

        Returns:
            An uninstrumented connection.
        """
        return dbapi.uninstrument_connection(connection)
