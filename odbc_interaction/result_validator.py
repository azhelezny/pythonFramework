import re

from jmx_interaction.structures import QueryType, AssertionField, ValidationType
from utils.util import replace_variables

"""
exceptions can be only for SELECT "table doesn't exists" for example
responses also can have variables

"update queries" can be validated using row_count
to validate UPDATE:
    if ResponseMessage - only check that row_count == expected (row/s updated)
    if ResponseText - extract number of expected updates from expected result, compare it with row_count

to validate SELECT:
    if ResponseMessage - expected result should be smartly compared with "exception".message
    if ResponseText - expected result should be converted to list of dicts and compared to result of request
        names of columns should be ignored
"""


def validate_result(request, actual_result, variables):
    """
    @type request: jmx_interaction.structures.RequestStructure
    @type actual_result: dict
    """
    query_type = request.query_type
    assertion_field = None
    validation_type = None
    """:type: ValidationType"""
    ignore_status = None

    for expected_result in request.expected_results:
        assertion_field = expected_result.assertion_field
        validation_type = expected_result.validation_type
        ignore_status = expected_result.ignore_status
        break

    expected_selection_error = actual_result.get("selection_error")
    actual_exception = actual_result.get("exception")
    if actual_exception is not None and not ignore_status:
        return {False: "unexpected error: " + str(actual_exception)}
    if expected_selection_error is not None and not ignore_status:
        return {False: "unexpected error: " + str(expected_selection_error)}

    for expected_result in request.expected_results:
        expected_result = replace_variables(expected_result, variables)
        if query_type == QueryType.Update:
            if assertion_field == AssertionField.ResponseMessage:
                return {
                    True: "TODO: add validation here when response message in will be presented in exception error message"}
            if assertion_field == AssertionField.ResponseData:
                expected = expected_result.request_result
                expected_row_count = get_number_from_message(expected)
                actual = actual_result.get("row_count")
                if expected_row_count != actual:
                    return {
                        False: "expected row count [" + expected + "] was not found in actual result [" + actual + "] full expected result: [" + expected + "]"}
                else:
                    return {True: ""}
        if request.query_type == QueryType.Select:
            if assertion_field == AssertionField.ResponseMessage:
                if actual_exception is not None:
                    return {True: "error message was expected: " + str(actual_exception)}
                if expected_selection_error is not None:
                    return {True: "error message was expected: " + str(expected_selection_error)}
                return {False: "error message was expected but absent"}
            if assertion_field == AssertionField.ResponseData:
                return validate_using_validation_type(get_headless_select_result(expected_result.request_result),
                                                      actual_result.get("rows"), validation_type)


def validate_using_validation_type(expected, actual, validation_type):
    """
        @type expected: str
        @type actual: str
        @type validation_type: ValidationType
    """
    if validation_type == ValidationType.Equals:
        if expected.lower() != actual.lower():
            return {False: "expected != actual: [" + expected + "] != [" + actual + "]"}
        return {True: ""}
    if validation_type == ValidationType.Substring:
        if expected.lower() not in actual.lower():
            return {False: "actual string [" + actual + "] doesn't have expected [" + expected + "] substring"}
        return {True: ""}
    if validation_type == ValidationType.Contains:
        regex = re.compile(expected)
        if regex.search(actual) is None:
            return {False: "actual string [" + actual + "] doesn't contains expected [" + expected + "]"}
        return {True: ""}
    if validation_type == ValidationType.Matches:
        m = re.match(actual, expected)
        if not m:
            return {False: "actual string [" + actual + "] doesn't match expected pattern [" + expected + "]"}
        return {True: ""}


def get_number_from_message(message):
    """
    @type message: str
    """
    m = re.match("^(\d+)", message)
    if m:
        return m.group(1)


def get_headless_select_result(select_result):
    """
    @type select_result: str
    """
    index = select_result.find("\n")
    if index == -1:
        return ""
    return select_result[index + 1:]
