import re


class StructureParseException(Exception):
    pass


class IncorrectBehaviorException(Exception):
    pass


class IncorrectValidationException(Exception):
    pass


def replace_variables(query, variables):
    result = query
    for key, value in variables.iteritems():
        result = query.replace("${" + key + "}", value)
    return result


def replace_illegal_xml_characters(str_to_replace):
    RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                     u'|' + \
                     u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                     (unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff),
                      unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff),
                      unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff))
    return re.sub(RE_XML_ILLEGAL, "?", str_to_replace)
