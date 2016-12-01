import random
from pydoc import html

from utils.util import write_str_to_file

table_entry_top = """<tr>
                <td><pre>"""

table_entry_bottom = """</pre></td>
                </tr>"""


def log_thread_header(file_path, thread_name):
    """
    @type file_path: str
    @type thread_name: str
    """
    title = thread_name
    header_content = """
    <html>
    <head>
    <META http-equiv="Content-Type\" content=\"text/html; charset=UTF-8\">
    <title>""" + title + """</title>
    <link href=\"../css/composite.css\" type=\"text/css\" rel=\"stylesheet\">
    </head>

    <body>
    <h2 class=\"testName\" id=\"${temporary_status}\">""" + title + """</h2>
    <h3> Started: ${temporary_start_time} </h3>
    <h3> Finished: ${temporary_stop_time} </h3>
    <h3> Time Spend: ${temporary_duration} </h3>
    <div class=\"invisible\"></div>
    <table class=\"testResults\">
    """
    write_str_to_file(file_path, header_content)


def log_entry(file_path, request, request_execution_result):
    """
    @type file_path: str
    @type request: jmx_interaction.structures.RequestStructure
    @type request_execution_result: dict
    """
    entry_id = str(random.random() * random.choice([10, 20, 30, 100, 500, 1000, 10000, 100000]))
    diff_operations_div_id = "diffOperations_" + entry_id
    diff_content_table_id = "diffContent_" + entry_id

    file_content = table_entry_top + """<pre id='""" + diff_operations_div_id + """' class ='diffContentTableClass'>
""" + html.escape(request.__str__()) + """</pre>
<pre id='""" + diff_content_table_id + """' style='display: none'>\n
""" + html.escape(str(request_execution_result)) + "</pre>"
    file_content += table_entry_bottom
    write_str_to_file(file_path, file_content)


def log_validation_status(file_path, validation_status):
    """
    @type file_path: str
    @type validation_status: dict
    """
    i = 0
    for key, value in validation_status.iteritems():
        if i >= 1:
            break
        color = 'green'
        if not key:
            color = 'red'
        file_content = table_entry_top + "<font color='" + color + "'>" + str(validation_status)
        file_content += "</font>" + table_entry_bottom
        write_str_to_file(file_path, file_content)
        i += 1


def log_thread_footer(file_path):
    """
    @type file_path: str
    """
    footer_content = """
    <script language=\"javascript\" type=\"text/javascript\">\n
                           function expandCollapse(id){\n
                              var element = document.getElementById('diffContent_'+id);\n
                              var currentElement = document.getElementById('btn_'+id);\n
                               if(element.style.display == 'none'){
                                   element.style.display = 'block';
                                   currentElement.value = '--Collapse';
                               }
                               else{
                                   element.style.display = 'none';
                                   currentElement.value = '--Expand'
                               }
                             }\n
                            function addButton(toElement, id) {\n
                              var btn = document.createElement(\"input\");\n
                              btn.setAttribute(\"type\", \"button\");\n
                              btn.setAttribute(\"value\", \"--Expand\");\n
                              btn.setAttribute(\"name\", id);\n
                              btn.setAttribute(\"id\", 'btn_'+id);\n
                              btn.onclick = function(){expandCollapse(id);}\n
                              var foo = document.getElementById(toElement);\n
                              foo.appendChild(btn);}\n
                            window.onload = function(){\n
                              var tables = document.getElementsByClassName(\"diffContentTableClass\");\n
                              for (i = 0; i < tables.length; i++) {\n
                                var id = tables[i].id;\n
                                id=id.substring(id.indexOf('_')+1);\n
                                addButton('diffOperations_' + id, id);\n
                              }\n
                           }\n</script>\n
    </table>
    </body>
    </html>"""
    write_str_to_file(file_path, footer_content)
