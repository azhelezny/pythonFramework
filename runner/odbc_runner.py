import pyodbc


def run_request(self, request):
    conn = pyodbc.connect("DRIVER={SQL Server};SERVER=JAYA01;DATABASE=splice;UID=admin;PWD=splice")
    cursor = conn.cursor()
    cursor.execute("SELECT * from sys.systables")

    for row in cursor.fetchall():
        print row

