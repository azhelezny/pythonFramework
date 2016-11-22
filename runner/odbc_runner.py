import pyodbc

from structures.structures import QueryType


def run_request(request):
    conn = pyodbc.connect(
        "DSN=SpliceODBC64;DRIVER=/home/splice/splice/lib64/libsplice_odbc.so;UID=splice;PWD=admin;URL=10.1.1.222;PORT=1527",
        autocommit=True)
    cursor = conn.cursor()
    cursor.execute(request.query)
    rows = []
    if request.query_type == QueryType.Select:
        for row in cursor.fetchall():
            rows.append(row)
    elif request.query_type == QueryType.Update:
        rows.append(str(cursor.rowcount))
    return rows
