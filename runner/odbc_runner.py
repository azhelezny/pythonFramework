import pyodbc

from structures.structures import QueryType


def open_connection(autocmt=True):
    return pyodbc.connect(
        "DSN=SpliceODBC64;DRIVER=/home/splice/splice/lib64/libsplice_odbc.so;UID=splice;PWD=admin;URL=10.1.1.222;PORT=1527",
        autocommit=autocmt)


def run_request(conn, request, variables):
    cursor = ""
    try:
        cursor = conn.cursor()
    except Exception as e:
        if e.__class__ == pyodbc.ProgrammingError:
            conn = open_connection(True)
            cursor = conn.cursor()
    print "query:" + replace_variables(request.query, variables)
    cursor.execute(replace_variables(request.query, variables))
    row_count = str(cursor.rowcount)
    rows = []
    if request.query_type == QueryType.Select:
        try:
            for row in cursor.fetchall():
                print "ROW: " + row
                rows.append(row)
        except pyodbc.ProgrammingError:
            print "ERROR"
    conn.close()
    return {row_count: rows}


def replace_variables(query, variables):
    result = ""
    for key, value in variables.iteritems():
        result = query.replace("${" + key + "}", value)
    return result
