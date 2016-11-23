import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jmx_parser.JmxParser import JmxParser
from runner.odbc_runner import run_request

file_path = "../resources/example.jmx"

parser = JmxParser(file_path)
parser.parse_jmx()
threads = parser.threads
variables = parser.variables
for thread in threads:
    print thread.thread_name
    for request in thread.requests:
        print "REQUEST\n" + request.__str__()
        results = run_request(request, variables)
        print "RESULTS\n"
        for key, value in results.iteritems():
            print key
            print value
