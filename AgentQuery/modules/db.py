import psycopg2
from psycopg2.sql import SQL, Identifier
from datetime import datetime 
import json

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
    
    def datetime_handler(self, obj):
        """
        Handle datetime objects when serializing to JSON.
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj) 

    def get_table_definition(self, table_name):
        """
        Generate the 'create' definition for a table
        """

        get_def_stmt = """
        SELECT pg_class.relname as tablename,
            pg_attribute.attnum,
            pg_attribute.attname,
            format_type(atttypid, atttypmod)
        FROM pg_class
        JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace
        JOIN pg_attribute ON pg_attribute.attrelid = pg_class.oid
        WHERE pg_attribute.attnum > 0
            AND pg_class.relname = %s
            AND pg_namespace.nspname = 'public'  -- Assuming you're interested in public schema
        """
        self.cur.execute(get_def_stmt, (table_name,))
        rows = self.cur.fetchall()
        create_table_stmt = "CREATE TABLE {} (\n".format(table_name)
        for row in rows:
            create_table_stmt += "{} {},\n".format(row[2], row[3])
        create_table_stmt = create_table_stmt.rstrip(",\n") + "\n);"
        return create_table_stmt

    def get_all_table_names(self):
        get_all_tables_stmt = (
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"
        )
        self.cur.execute(get_all_tables_stmt)
        return [row[0] for row in self.cur.fetchall()]

    def get_table_definitions_for_prompt(self):
        table_names = self.get_all_table_names()
        definitions = []
        for table_name in table_names:
            definitions.append(self.get_table_definition(table_name))
        return "\n\n".join(definitions)

    def get_table_definition_map_for_embeddings(self):
        table_names = self.get_all_table_names()
        definitions = {}
        for table_name in table_names:
            definitions[table_name] = self.get_table_definition(table_name)
        return definitions

    def get_related_tables(self, table_list, n=2):

        related_tables_dict = {}

        for table in table_list:
            # Query to fetch tables that have foreign keys referencing the given table
            self.cur.execute(
                """
                SELECT 
                    a.relname AS table_name
                FROM 
                    pg_constraint con 
                    JOIN pg_class a ON a.oid = con.conrelid 
                WHERE 
                    confrelid = (SELECT oid FROM pg_class WHERE relname = %s)
                LIMIT %s;
                """,
                (table, n),
            )

            related_tables = [row[0] for row in self.cur.fetchall()]

            self.cur.execute(
                """
                SELECT 
                    a.relname AS referenced_table_name
                FROM 
                    pg_constraint con 
                    JOIN pg_class a ON a.oid = con.confrelid 
                WHERE 
                    conrelid = (SELECT oid FROM pg_class WHERE relname = %s)
                LIMIT %s;
                """,
                (table, n),
            )

            related_tables += [row[0] for row in self.cur.fetchall()]

            related_tables_dict[table] = related_tables
            
        related_tables_list = []
        for table, related_tables in related_tables_dict.items():
            related_tables_list += related_tables

        related_tables_list = list(set(related_tables_list))

        return related_tables_list



    