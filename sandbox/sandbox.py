import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    print conn.autocommit
    for request in thread.requests:
        results = run_request(conn, request, variables)
        print "RESULTS"
        for key, value in results.iteritems():
            print key, value
        print "\n"
    conn.close()
