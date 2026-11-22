"""Use the operating system's trusted certificates for outbound HTTPS."""

import ssl

import truststore


class RelaxedSSLContext:
    """Compatibility wrapper for the project's previous SSL helper name."""

    @staticmethod
    def configure_ssl() -> None:
        # Call before HTTP clients import SSLContext or create connections.
        truststore.inject_into_ssl()

    @staticmethod
    def create_relaxed_ssl_context(
        purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None
    ) -> ssl.SSLContext:
        """Return a verifying context backed by the system trust store."""
        return ssl.create_default_context(
            purpose=purpose, cafile=cafile, capath=capath, cadata=cadata
        )
