import os
import sys

from jmx_interaction.structures import RequestStructure, JmxThread
from reporting.common_html import log_common_header, log_common_footer
from reporting.thread_html import log_thread_header, log_entry, log_thread_footer, log_validation_status

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reporting.reporter_utils import get_unix_timestamp, get_date_as_string

current_date = get_date_as_string(get_unix_timestamp())
report_dir = "../reports/report_" + current_date

threads = []
done_threads = []

request = RequestStructure("select * from sys.systables");
thread1 = JmxThread("thread1")
thread1.add_request(request)

request = RequestStructure("select * from sys.systables");
thread2 = JmxThread("thread2")
thread2.add_request(request)

threads.append(thread1)
threads.append(thread2)

os.makedirs(report_dir)
os.makedirs(report_dir + "/threads")

log_common_header(report_dir, "jmx_file_name")
for thread in threads:
    thread_name = thread.thread_name
    if thread in done_threads:
        thread_name += "~1"
    thread_path = report_dir + "/threads/" + thread_name + ".html"
    log_thread_header(thread_path, thread_name)
    for request in thread.requests:
        log_entry(thread_path, request, {})
        log_validation_status(thread_path, {False: "pishDrish"})
    log_thread_footer(thread_path)
log_common_footer(report_dir)

print report_dir
