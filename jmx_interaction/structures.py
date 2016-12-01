class QueryType:
    def __init__(self):
        pass

    Select = 0
    Update = 1


class AssertionField:
    def __init__(self):
        pass

    ResponseData = 0
    ResponseMessage = 1


class ValidationType:
    def __init__(self):
        pass

    No = 0
    Equals = 8
    Contains = 2
    Matches = 1
    Substring = 16
    NotEquals = 12
    NotContains = 6
    NotMatches = 5
    NotSubstring = 20


class ExpectedResult:
    def __init__(self, request_result="", validation_type=ValidationType.No,
                 assertion_field=AssertionField.ResponseData, ignore_status=False):
        self.request_result = request_result  # type: str
        self.validation_type = validation_type  # type: int
        self.assertion_field = assertion_field  # type: int
        self.ignore_status = ignore_status  # type: bool


class RequestStructure:
    def __init__(self, query, query_type=QueryType.Select):
        self.query_type = query_type  # type: int
        self.query = query  # type: str
        self.expected_results = []  # type: list[ExpectedResult]

    def add_expected_result(self, expected_result):
        self.expected_results.append(expected_result)

    def __str__(self):
        result = self.query + "\n"
        result += "- >QueryType: " + str(self.query_type) + "\n"
        for expected_result in self.expected_results:
            result += "-- >Expected: " + expected_result.request_result + "\n"
            result += "-- >Validation type: " + str(expected_result.validation_type) + "\n"
            result += "-- >Assertion field: " + str(expected_result.assertion_field) + "\n"
            result += "-- >Ignore Status: " + str(expected_result.ignore_status)
        return result


class JmxThread:
    def __init__(self, thread_name):
        self.thread_name = thread_name  # type: str
        self.requests = []  # type: list[RequestStructure]

    def add_request(self, request):
        self.requests.append(request)
