import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from odbc_interaction.result_validator import get_number_from_message, validate_result
from jmx_interaction.JmxParser import JmxParser
from odbc_interaction.odbc_runner import run_request, open_connection

file_path = "../resources/example.jmx"

parser = JmxParser(file_path)
parser.parse_jmx()
threads = parser.threads
variables = parser.variables
for thread in threads:
    print thread.thread_name
    conn = open_connection(True)
    for request in thread.requests:
        results = run_request(conn, request)
        print "Request: [" + request.query + "] assume success [" + str(request.expected_results[0].ignore_status) + "]"
        print "Results"
        for key, value in results.iteritems():
            print key, ":", value
        print "Validation Result:" + str(validate_result(request, results, variables))

        print "\n"
    conn.close()
