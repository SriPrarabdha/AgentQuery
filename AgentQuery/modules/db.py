import psycopg2
from psycopg2.sql import SQL, Identifier

class PostgressDb():
    def __init__(self):
        self.conn = None
        self.curr = None

    def __enter__(self):
        return self
    
    def __exit__(self):
        if self.curr:
            self.curr.close()

        if self.conn:
            self.conn.close()

    def connect(self, url):
        try:
            self.conn = psycopg2.connect(url)
            self.curr = self.conn.cursor()
        except Exception as e:
            print("couldn't connect to the database!!!!" , e)

    def upsert(self, table_name , dict):
        columns = dict.keys()
        values = [SQL("%s")] * len(columns)
        sql_stmt = SQL(
            "INSERT INFO {} ({}) VALUES ({}) ON CONFLICT (id) DO UPDATE SET {}"
        ).format(
            Identifier(table_name),
            SQL(", ").join(map(Identifier, columns)),
            SQL(", ").join(values),
            SQL(", ").join(
                [
                    SQL("{} = Excluded.{}").format(Identifier(k), Identifier(k)) for k in columns
                ]
            )
        )

        self.curr.execute(sql_stmt, list(dict.values()))
        self.conn.commit()

    def delete(self, table_name, id):
        deleteStmt = SQL("DELETE FROM {} WHERE ID = {}").format(
            Identifier(table_name),
            id
        )
        self.curr.execute(deleteStmt)
        self.conn.commit()

    def get(self, table_name , id):
        select_stmt = SQL("SELECT * FROM {} WHERE id = %s").format(
            Identifier(table_name)
        )

        self.curr.execute(select_stmt , (id))
        return self.curr.fetchone()
    
    def get_all(self, table_name):
        select_all_stmt = SQL("SELECT * from {}").format(Identifier(table_name))

        self.curr.execute(select_all_stmt)
        return self.curr.fetchall()
    
    def run_sql(self, sql):
        self.curr.execute(sql)
        return self.curr.fetchall()
    
    def get_table_definition(self, table_name):
        get_def_stmt = ""


    