import pyodbc

from structures.structures import QueryType


def run_request(request):
    conn = pyodbc.connect(
        "DSN=SpliceODBC64;DRIVER=/home/splice/splice/lib64/libsplice_odbc.so;UID=splice;PWD=admin;URL=10.1.1.222;PORT=1527",
        autocommit=True)
    cursor = conn.cursor()
    cursor.execute(request.query)
    row_count = str(cursor.rowcount)
    rows = []
    if request.query_type == QueryType.Select:
        try:
            for row in cursor.fetchall():
                rows.append(row)
        except pyodbc.ProgrammingError:
            return {row_count, {}}
            pass
    return {row_count, rows}
