import os

from reporting import styles
from reporting.reporter_utils import replace_in_file, get_date_as_string, get_time_as_string
from utils.util import write_str_to_file


def log_common_header(file_path, title):
    """
    @type file_path:str
    @type title:str
    """
    file_content = """
    <html>
    <head>
    <META http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">
    <title>""" + title + """</title>
    <link href=\"css/classes.css\" type=\" text/css\" rel=\"stylesheet\">
    </head>

    <body>
     <table class=\"clear\">
      <tr>
       <th colspan=\"2\">
        <div class=\"title\">
         <div id=\"${temporary_status}\">""" + title + """</div>
        </div>
       </th>
      </tr>
      <tr>
       <td class=\"topLine\" colspan=\"2\">
        <div id=\"skipped\">Started at ${temporary_start_time} </div>
       </td>
      </tr>
      <tr>
       <td colspan=\"2\">
        <div id=\"skipped\">Finished at ${temporary_stop_time} </div>
       </td>
      </tr>
      <tr>
       <td class=\"topBottomLines\" colspan=\"2\">
        <div id=\"skipped\" > Duration ${temporary_duration} </div>
       </td >
      </tr >
      """
    write_str_to_file(file_path + "/index.html", file_content)


def log_thread_status(file_path, thread_name, run_info):
    """
    @type file_path:str
    @type thread_name:str
    @type run_info:reporting.run_info.RunInfo
    """
    file_content = """
      <tr>
       <td class=\"configOrTest\">T</td>
       <td class=\"testName\" ><a href = 'threads/""" + thread_name + """.html' target = \"logs\">
            <div id='""" + run_info.status + "'>" + thread_name + """</div>
            </a>
        </td>
      </tr >
    """
    write_str_to_file(file_path + "/index.html", file_content)


def log_common_footer(file_path, common_run_info):
    """
    @type file_path:str
    """
    file_content = """
     </table>
    </body>
    </html>"""
    write_str_to_file(file_path + "/index.html", file_content)
    replace_in_file(file_path + "/index.html", {"${temporary_status}": common_run_info.status,
                                                "${temporary_start_time}": get_date_as_string(common_run_info.start),
                                                "${temporary_stop_time}": get_date_as_string(common_run_info.stop),
                                                "${temporary_duration}": get_time_as_string(
                                                    common_run_info.get_duration())})

    target_file_name = ""
    for file_name in os.listdir(file_path + "/threads"):
        target_file_name = file_name

    frame_content = """
    <html><head><link href=\"main.css\"/></head><frameset cols=\"20%,80%\">
    <frame src=\"index.html\" name=\"menu\">
    <frame src=\"threads/""" + target_file_name + """\" name=\"logs\"></frameset></html>
    """

    write_str_to_file(file_path + "/index.frame.html", frame_content)
    write_str_to_file(file_path + "/css/main.css", styles.getMainCssFile)
    write_str_to_file(file_path + "/css/composite.css", styles.getTestCssFile)
    write_str_to_file(file_path + "/css/classes.css", styles.getClassCssFile)
