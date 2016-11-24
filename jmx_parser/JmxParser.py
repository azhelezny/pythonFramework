from xml.dom import minidom

import io

from structures.structures import JmxThread, ExpectedResult, RequestStructure, AssertionField, ValidationType
from utils.util import StructureParseException, IncorrectBehaviorException, replace_illegal_xml_characters


class JmxParser:
    def __init__(self, file_path):
        self.threads = []
        self.variables = {}
        file_data = ""
        # with io.open(file_path, 'r', encoding="utf-8", errors="surrogateescape") as myfile:
        with io.open(file_path, 'r') as myfile:
            file_data = myfile.read()
        self.doc = minidom.parseString(file_data)
        # self.doc = minidom.parse(file_path)
        self.current_thread = 0

    def get_variables(self):
        return self.variables

    def get_threads(self):
        return self.threads

    def parse_jmx(self):
        var_sets = self.doc.getElementsByTagName("Arguments")
        for var_set in var_sets:
            for collection_props in var_set.getElementsByTagName("collectionProp"):
                for var_description in collection_props.getElementsByTagName("elementProp"):
                    var_parameters = var_description.getElementsByTagName("stringProp")
                    name = ""
                    value = ""
                    for var in var_parameters:
                        if var.getAttribute("name") == "Argument.name":
                            name = str(var.firstChild.nodeValue)
                        if var.getAttribute("name") == "Argument.value":
                            value = str(var.firstChild.nodeValue)
                    self.variables[name] = value
        thread_sets = self.doc.getElementsByTagName("ThreadGroup")
        for thread in thread_sets:
            self.threads.append(JmxThread(thread.getAttribute("testname")))
            self.current_thread = len(self.threads) - 1
            # hash tree after ThreadGroup
            hash_tree = thread.nextSibling.nextSibling
            self.dive_into(hash_tree, self.is_enabled(thread))

        pass

    def dive_into(self, group, enabled):
        if not enabled:
            return
        nodes = group.childNodes
        for node in nodes:
            if node.nodeName == "JDBCSampler":
                if not self.is_enabled(node):
                    continue
                query_parameters = self.get_query(node)
                query = query_parameters[0]
                query_type = query_parameters[1]
                query_name = self.get_query_name(node)
                try:
                    expected_results = self.get_expected_results(node)
                except IndexError:
                    raise StructureParseException("unable to parse structure, thread: [" + self.threads[
                        self.current_thread].thread_name + "] query name: " + query_name)
                except IncorrectBehaviorException:
                    raise StructureParseException("extra result resolvers, thread: [" + self.threads[
                        self.current_thread].thread_name + "] query name: " + query_name)
                request = RequestStructure(query, query_type)
                for expected_result in expected_results:
                    request.add_expected_result(expected_result)
                self.threads[self.current_thread].add_request(request)
            if "Controller" in node.nodeName:
                self.dive_into(node.nextSibling.nextSibling, self.is_enabled(node) and enabled)

    @staticmethod
    def is_enabled(node):
        if not node.hasAttribute("enabled"):
            return True
        return node.getAttribute("enabled").lower().strip() == "true"

    @staticmethod
    def get_query(node):
        query = ""
        query_type = 0
        for string_prop in node.getElementsByTagName("stringProp"):
            if string_prop.getAttribute("name") == "query":
                query = str(string_prop.firstChild.nodeValue + ";")
            if string_prop.getAttribute("name") == "queryType":
                value = string_prop.firstChild.nodeValue
                if value == "Update Statement":
                    query_type = 1
        return [query, query_type]

    @staticmethod
    def get_query_name(node):
        return str(node.getAttribute("testname"))

    @staticmethod
    def get_expected_results(node):
        response_assertion_nodes = node.nextSibling.nextSibling.getElementsByTagName("ResponseAssertion")
        if len(response_assertion_nodes) > 1:
            raise IncorrectBehaviorException
        response_assertion_node = response_assertion_nodes[0]
        expected_results = []

        assertion_field = AssertionField.ResponseData
        ignore_status_filed = False
        assertion_type = ValidationType.No

        for response_assertion_properties in response_assertion_node.childNodes:
            if response_assertion_properties.nodeName == "#text":
                continue
            if response_assertion_properties.nodeName == "stringProp":
                if response_assertion_properties.firstChild.nodeValue == "Assertion.response_message":
                    assertion_field = AssertionField.ResponseMessage
            if response_assertion_properties.nodeName == "boolProp":
                ignore_status_filed = response_assertion_properties.firstChild.nodeValue.lower() == "true"
            if response_assertion_properties.nodeName == "intProp":
                assertion_type = int(response_assertion_properties.firstChild.nodeValue)

        expected_outputs = []
        for assertion_string_node in response_assertion_node.getElementsByTagName("collectionProp"):
            for string_prop_node in assertion_string_node.getElementsByTagName("stringProp"):
                if string_prop_node.hasChildNodes():
                    expected_outputs.append(str(string_prop_node.firstChild.nodeValue))
        if len(expected_outputs) == 0:
            expected_results.append(ExpectedResult("", assertion_type, assertion_field, ignore_status_filed))
        else:
            for expected_output in expected_outputs:
                expected_results.append(
                    ExpectedResult(expected_output, assertion_type, assertion_field, ignore_status_filed))

        return expected_results
