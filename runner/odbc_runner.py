import pyodbc

from structures.structures import QueryType


def open_connection(autocmt=True):
    return pyodbc.connect(
        "DSN=SpliceODBC64;DRIVER=/home/splice/splice/lib64/libsplice_odbc.so;UID=splice;PWD=admin;URL=10.1.1.222;PORT=1527",
        autocommit=autocmt)


def run_request(conn, request, variables):
    cursor = conn.cursor()
    exception = None
    print "query:" + replace_variables(request.query, variables)
    try:
        cursor.execute(replace_variables(request.query, variables))
    except Exception as e:
        exception = e
    row_count = str(cursor.rowcount)
    rows = []
    if request.query_type == QueryType.Select:
        try:
            for row in cursor.fetchall():
                print "ROW: " + str(row)
                rows.append(row)
        except pyodbc.ProgrammingError as e:
            print e
    return [row_count, rows, exception]


def replace_variables(query, variables):
    result = query
    for key, value in variables.iteritems():
        result = query.replace("${" + key + "}", value)
    return result
