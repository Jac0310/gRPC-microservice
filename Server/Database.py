from datetime import datetime
from influxdb import InfluxDBClient

class Database():
    def __init__(self, filename, host, port, username, password, dbname):
        # self.client = InfluxDBClient(host=host, port=port,
        #                                       username=username, password=password, database=dbname)
        self.client = InfluxDBClient(database=dbname)
        self.client.create_database(dbname) # can't connect ?
        self.client.switch_database(dbname)
        print(self.client.get_list_database())
        self.populatedb(filename)

    def populatedb(self, filename):
        lines = self.read_data(filename)
        json_body = []
        for rawline in lines:
            line = rawline.split(",")
            datetime_object = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
            json_body.append({
                    "measurement": "meterusage",
                    "time": datetime_object,
                    "fields": {
                        "meterusage": float(line[1].strip())
                    }
                })
        self.client.write_points(json_body)


    def read_data(self, filename):
        print(filename)
        with open(filename) as f:
            lines = f.readlines()[1:]
        return lines

if __name__ == "__main__":
    cl = Database(r"meterusage.csv", 'localhost', 8086, 'root', 'root', 'test')
    cl.database.query('select * from "test" ')
