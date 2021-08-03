import sqlite3


class DatabaseManager():
    """
    A class used to manage database access.

    ...

    Attributes
    ----------
    db_file : PosixPath
        path element with full database path
    table_settings : str
        string with table's settings name

    Methods
    -------
    create_connection
        create a GET query
    get_status
        get current user's status
    """

    def __init__(self, db_file):
        self.db_file = db_file
        self.tbl_settings = 'settings'
        self.db_conn = None
        self.db_cur = None

    def create_connection(self):
        """
        Create database connection to use in others methods
        """
        try:
            self.db_conn = sqlite3.connect(self.db_file)
            return True
        except sqlite3.Error as error:
            return error
    
    def close_connection(self):
        """
        Close database connection
        """
        if self.db_conn is not None:
            self.db_conn.close()
    
    def initialitze_database(self):
        try:
            db_cursor = self.db_conn.cursor()
            # Create table
            db_cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                            id integer PRIMARY KEY,
                            url	TEXT NOT NULL,
                            token TEXT NOT NULL);''')

            db_cursor.execute('''INSERT INTO {}(url, token) values ("http://URL", "token")'''.format(self.tbl_settings))

            # Save (commit) the changes
            self.db_conn.commit()
            return True
        except sqlite3.Error as error:
            return error
    
    def fetch_settings(self):
        """
        Fetch user settings
        """
        query = 'SELECT * from {}'.format(self.tbl_settings)
        self.db_cur = self.db_conn.cursor()
        self.db_cur.execute(query)

        user_settings = self.db_cur.fetchone()
        if user_settings:
            return user_settings
        else:
            return False
    
    def update_settings(self, settings):
        try:
            query = 'UPDATE {} set url="{}", token="{}" where id=={}'.format(
                self.tbl_settings, settings['server_url'],
                settings['user_token'],
                settings['user_id']
            )
            self.db_cur = self.db_conn.cursor()
            self.db_cur.execute(query)
            self.db_conn.commit()
            return True
        except sqlite3.Error as error:
            return error
