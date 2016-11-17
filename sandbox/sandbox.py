from jmx_parser.JmxParser import JmxParser

file_path = "/Users/azhelezny/Desktop/scenarios_jmeter/example.jmx"
#file_path = "/Users/azhelezny/projects/splice_machine/test-jmeter/src/test/jmeter/export.jmx"

parser = JmxParser(file_path)

parser.parse_jmx()
threads = parser.threads
for thread in threads:
    print thread.thread_name
    for request in thread.requests:
        print request