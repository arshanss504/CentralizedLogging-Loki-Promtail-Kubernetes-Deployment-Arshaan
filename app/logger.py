#The logger should be imported in every module where logs are generated.
#If logger.py is missing, logs might go to the default Python logger (which may not write to files) unless set.

#If you want to Configure logging to stdout. Messages sent to stdout are displayed on the console. CONSOLE LOGS
#logging.basicConfig(stream=sys.stdout, level=logging.INFO)
#logger = logging.getLogger(__name__)




import logging
import os
from opentelemetry.instrumentation.logging import LoggingInstrumentor




# Ensure logs directory exists
# LOG_DIR = "logs"
# os.makedirs(LOG_DIR, exist_ok=True)

# LOG_FILE = os.path.join(LOG_DIR, "app.log")


desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
logs_dir = os.path.join(desktop_path, "logs")
LOG_FILE = os.path.join(logs_dir, "app.log")


'''
# OpenTelemetry Logging Instrumentation
LoggingInstrumentor().instrument(set_logging_format=True)

# Create logger
logger = logging.getLogger("my_app_logger")
logger.setLevel(logging.DEBUG)

# File Handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)


# Formatter




# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Attach handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Logger initialized. Logs will include trace IDs and be written to logs/app.log")

'''

class OpenTelemetryLoggingFilter(logging.Filter):
    def filter(self, record):
        span = get_current_span()
        trace_id = span.get_span_context().trace_id if span else "N/A"
        span_id = span.get_span_context().span_id if span else "N/A"

        # Append trace ID and span ID to the log message
        record.msg = f"{record.msg} [trace_id={trace_id}] [span_id={span_id}]"
        return True  # Keep the log entry

logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE),  # Log to file
        logging.StreamHandler()  # Log to console
    ],
)

logger = logging.getLogger("my_app_logger")
logger.addFilter(OpenTelemetryLoggingFilter())  # Apply filter to all logs



#You're absolutely right! If logs don't explicitly extract and log the trace_id from OpenTelemetry's active span, the logs written to files won't correlate with traces in Grafana.