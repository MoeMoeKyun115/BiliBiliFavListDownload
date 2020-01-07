import psycopg2

class Postgresql():

    def __init__(self, config):
        self.connection = psycopg2.connect(
            database=config['database'], 
            user=config['user'], 
            password=config['password'], 
            host=config['host'], 
            port=config['port']
        )
        print("Database opened successfully")

    def get_db_flist(self, condition=''):
        cur = self.connection.cursor()
        cur.execute(f'SELECT video_id FROM videos {condition}')
        rows = cur.fetchall()
        db_flist = []
        for row in rows:
            db_flist.append(row[0])
        return db_flist

    def insert_flist(self, flist, flist_id):
        cur = self.connection.cursor()
        query_header = 'INSERT INTO videos VALUES '

        query_values = []
        for avid in flist:
            value = f"({avid}, {flist_id}, False, now())"
            query_values.append(value)
        
        query = query_header + ', '.join(query_values) + ';'
        # print(query)
        cur.execute(query)
        self.connection.commit()
        print(f'insert record count: {len(flist)}')

    def update_download_status(self, avid, status):
        cur = self.connection.cursor()
        query = f'UPDATE videos SET download={status}, update_date=now() WHERE video_id = {avid}'
        cur.execute(query)
        self.connection.commit()
        print(f'av{avid} downloaded')