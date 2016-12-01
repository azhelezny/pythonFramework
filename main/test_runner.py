import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jmx_interaction.structures import RequestStructure, JmxThread
from reporting.common_html import log_common_header, log_common_footer, log_thread_status
from reporting.run_info import RunInfo
from reporting.test_status import TestStatus
from reporting.thread_html import log_thread_header, log_entry, log_thread_footer, log_validation_status
from reporting.reporter_utils import get_unix_timestamp, get_date_as_string, replace_in_file, get_time_as_string

current_date = get_date_as_string(get_unix_timestamp())
report_dir = "../reports/report_" + current_date

threads = []
done_threads = []

request = RequestStructure("select * from sys.systables")
thread1 = JmxThread("thread1")
thread1.add_request(request)

request = RequestStructure("select * from sys.systables")
thread2 = JmxThread("thread2")
thread2.add_request(request)

threads.append(thread1)
threads.append(thread2)

os.makedirs(report_dir)
os.makedirs(report_dir + "/threads")
os.makedirs(report_dir + "/css")

log_common_header(report_dir, "jmx_file_name")
common_run_info = RunInfo()
thread_counter = 0
for thread in threads:
    thread_counter += 1
    thread_name = "[" + str(thread_counter) + "] " + thread.thread_name
    thread_path = report_dir + "/threads/" + thread_name + ".html"

    log_thread_header(thread_path, thread_name)
    thread_run_info = RunInfo()
    run_info = RunInfo(TestStatus.SKIPPED, get_unix_timestamp(), 0, 1)
    for request in thread.requests:
        log_entry(thread_path, request, {})
        validation_result = {True: "pishDrish"}
        run_info.stop = get_unix_timestamp()
        run_info.status = TestStatus.PASSED
        for key, value in validation_result.iteritems():
            if not key:
                log_validation_status(thread_path, validation_result)
                run_info.status = TestStatus.FAILED
                break
    thread_run_info.sum_run_info(run_info)
    log_thread_footer(thread_path)
    replace_in_file(thread_path, {"${temporary_status}": thread_run_info.status,
                                  "${temporary_start_time}": get_date_as_string(thread_run_info.start),
                                  "${temporary_stop_time}": get_date_as_string(thread_run_info.stop),
                                  "${temporary_duration}": get_time_as_string(thread_run_info.get_duration())})
    log_thread_status(report_dir, thread_name, thread_run_info)
    common_run_info.sum_run_info(thread_run_info)
log_common_footer(report_dir, common_run_info)

print report_dir
