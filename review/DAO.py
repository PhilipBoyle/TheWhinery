import json
import psycopg2
from datetime import date




class DAO:
    def __init__(self, username, dbname, password):
        self.dbname = dbname
        self.username = username
        self.password = password
        print('end init')

    def connect(self):
        connect_string = "dbname=" + self.dbname + " user=" + self.username + " host=206.189.124.205 port=5432 password='" + self.password + "'"
        try:
            print(connect_string)
            self.connection = psycopg2.connect(connect_string)

            print('connected')
        except:
            print('connection error')

    def create_table(self, table_name, **kwargs):
        self.create_table = 'CREATE TABLE ' + table_name + '('
        for (k, v) in kwargs.items():
            self.create_table = self.create_table + ' ' + k + ' ' + v + ','
        self.create_table = self.create_table[:-1] + ')'
        print (self.create_table)
        try:
            self.cursor = self.connection.cursor()
            print('cursor created')
            self.cursor.execute(self.create_table)
            print('table created')
            self.cursor.close()
            self.connection.commit()
        except:
            print ('sql failed')

    def select_all(self, values):
        try:
            self.cursor = self.connection.cursor()
            print('cursor created')
            self.cursor.execute(values)
            xx = self.cursor.fetchall()
            print(xx)
        except:
            print("select failed")

    def insert_json(self, url):
        with open(url, 'r') as file:
            data = json.load(file)
        for json_dict in data:
            wine6_insert = 'INSERT INTO wine6 ('
            wine6_values = ' VALUES ('

            for (key, value) in json_dict.items():
                real_value = str(value)
				
                #Error handling in the string
                if real_value == "None":
                    real_value = "Null"
                wine6_insert = wine6_insert + str(key) + ', '
				
				
                if key == 'points' or key == 'price' or real_value== 'Null':
                    wine6_values = wine6_values + str(real_value) + ', '
                else:
                    wine6_values = wine6_values + "'" + str(real_value.replace("'", "`")) + "'" + ', '
                self.full_insert = wine6_insert[:-2] + ')' + wine6_values[:-2] + ')'
                try:
                    print(self.full_insert)
                    self.cursor = self.connection.cursor()
                    print('cursor created')
                    self.cursor.execute(self.full_insert)
                    print('executed')
                    self.cursor.close()
                    print('cursor closed')
                    self.connection.commit()
                    print('changes commited')
                except:
                    print("insert failed")
                    self.cursor.close()


c = DAO('student7', 'northwind7', 'student:123')
c.connect()
#c.insert_json('fulldata.json')
#c.select_all('SELECT * FROM wine6')
c.create_table('review',idnum='serial NOT NULL PRIMARY KEY ',points='integer NOT NULL', title='varchar(255)', 
			description="varchar(1000)", taster_name="varchar(50)", taster_twitter_handle="varchar(255)", 
			price="integer", designation="varchar(255)", variety="varchar(255)", region_1="varchar(255)", 
			region_2="varchar(255)", province="varchar(255)", country="varchar(255)", winery="varchar(255) NOT NULL")
c.connection.close()
