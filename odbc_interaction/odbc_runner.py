import pyodbc

from jmx_interaction.structures import QueryType


def open_connection(autocmt=True):
    return pyodbc.connect(
        "DSN=SpliceODBC64;DRIVER=/home/splice/splice/lib64/libsplice_odbc.so;UID=splice;PWD=admin;URL=10.1.1.222;PORT=1527",
        autocommit=autocmt)


def run_request(conn, request, variables):
    cursor = conn.cursor()
    exception = None
    selection_error = None
    query = replace_variables(request.query, variables)
    print "Running query:" + query
    try:
        cursor.execute(query)
    except Exception as e:
        exception = e
    row_count = str(cursor.rowcount)
    rows = []
    if request.query_type == QueryType.Select:
        try:
            for row in cursor.fetchall():
                rows.append(row)
        except Exception as e2:
            selection_error = e2
    return {"row_count": row_count, "rows": rows, "exception": exception, "selection_error": selection_error}


def replace_variables(query, variables):
    result = query
    for key, value in variables.iteritems():
        result = query.replace("${" + key + "}", value)
    return result
