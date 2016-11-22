import os
import pyodbc

import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jmx_parser.JmxParser import JmxParser

"""
file_path = "/Users/azhelezny/Desktop/scenarios_jmeter/example.jmx"
#file_path = "/Users/azhelezny/projects/splice_machine/test-jmeter/src/test/jmeter/export.jmx"

parser = JmxParser(file_path)
parser.parse_jmx()
threads = parser.threads
for thread in threads:
    print thread.thread_name
    for request in thread.requests:
        print request
"""

#conn = pyodbc.connect("DRIVER=/usr/local/lib/libtdsodbc.so;SERVER=jaya01;DATABASE=splice;UID=splice;PWD=admin;PORT=1527")
#conn = pyodbc.connect("DSN=SpliceODBC64")
conn = pyodbc.connect("DRIVER=resources/libsplice_odbc.so;SERVER=jaya01;DATABASE=splice;UID=splice;PWD=admin;PORT=1527")
cursor = conn.cursor()
cursor.execute("SELECT * from sys.systables")

for row in cursor.fetchall():
    print row
