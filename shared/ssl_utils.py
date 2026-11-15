import sys
import ssl
import warnings
import os
import certifi


class RelaxedSSLContext:
    """
    Provides SSL context configuration for corporate environments,
    reverting Python 3.13's stricter verification flags if needed and
    configuring certifi CA bundle.
    """

    @staticmethod
    def configure_ssl():
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
        os.environ['SSL_CERT_FILE'] = certifi.where()
        ssl.context = RelaxedSSLContext.create_relaxed_ssl_context()

    @staticmethod
    def create_relaxed_ssl_context(
        purpose=ssl.Purpose.SERVER_AUTH,
        *,
        cafile=None,
        capath=None,
        cadata=None
    ) -> ssl.SSLContext:
        ctx = ssl.create_default_context(
            purpose=purpose,
            cafile=cafile or certifi.where(),
            capath=capath,
            cadata=cadata
        )

        if sys.version_info >= (3, 13):
            warnings.warn(
                "Disabling VERIFY_X509_STRICT and VERIFY_X509_PARTIAL_CHAIN "
                "in create_default_context(). Reverts Python 3.13 stricter checks."
            )
            if hasattr(ssl, "VERIFY_X509_STRICT"):
                ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
            if hasattr(ssl, "VERIFY_X509_PARTIAL_CHAIN"):
                ctx.verify_flags &= ~ssl.VERIFY_X509_PARTIAL_CHAIN

        return ctx
