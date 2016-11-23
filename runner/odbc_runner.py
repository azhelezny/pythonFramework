import pyodbc

from structures.structures import QueryType


def run_request(request, variables):
    conn = pyodbc.connect(
        "DSN=SpliceODBC64;DRIVER=/home/splice/splice/lib64/libsplice_odbc.so;UID=splice;PWD=admin;URL=10.1.1.222;PORT=1527",
        autocommit=True)
    cursor = conn.cursor()
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
            return {row_count: []}
    return {row_count: rows}


def replace_variables(query, variables):
    result = ""
    print "query:" + query
    for key, value in variables.iteritems():
        result = query.replace(key, value)
        print "replacing " + key + " on " + value
    print "result:" + result
    return result
