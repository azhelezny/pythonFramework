from reporting.test_status import TestStatus


class RunInfo:
    def __init__(self, status=TestStatus.SKIPPED, start_time=0, stop_time=0, total_tests=0):
        """
        @type status: reporting.test_status.TestStatus
        @type start_time: long
        @type stop_time: long
        @type total_tests: int
        @type failed_tests: int
        """
        self.status = status
        self.start = start_time
        self.stop = stop_time
        self.duration = stop_time - start_time
        self.total_tests = total_tests
        self.failed_tests = 0
        if status == TestStatus.FAILED:
            self.failed_tests += 1

    def sum_run_info(self, run_info):
        """
        @type run_info: RunInfo
        """
        if run_info.start < self.start:
            self.start = run_info.start
        if run_info.stop > self.stop:
            self.stop = run_info.stop

        self.duration = self.stop - self.start

        if self.status == TestStatus.SKIPPED and run_info.status != TestStatus.SKIPPED:
            self.status = run_info.status
        if self.status != TestStatus.FAILED and run_info.status == TestStatus.FAILED:
            self.status = TestStatus.FAILED

        self.failed_tests += run_info.failed_tests
        self.total_tests += run_info.total_tests
