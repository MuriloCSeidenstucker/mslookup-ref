from mslookup_ref.infra.log.logger import get_logger
from mslookup_ref.main.server.server import app

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting MSLookup application")
    HOST = "0.0.0.0"
    PORT = 5000
    try:
        logger.debug("Configuring server with host=%s, port=%s", HOST, PORT)
        app.run(host=HOST, port=PORT)
    except Exception as e:
        logger.critical(
            "Failed to start MSLookup application: %s", {str(e)}, exc_info=True
        )
        raise
    finally:
        logger.info("Shutting down MSLookup application")
