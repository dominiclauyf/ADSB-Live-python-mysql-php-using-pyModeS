import pyModeS as pms
import socket
import time
import pymysql

plane = []
db = pymysql.connect(host="localhost",
                     user="root",
                     password="",
                     db="airplane",
                     cursorclass=pymysql.cursors.DictCursor)

dbcur=db.cursor()
reset_sql=f"DELETE FROM `airplane`"
dbcur.execute(reset_sql)
db.commit()


class Plane:
    def __init__(self, icao):
        self.icao = icao
        icao_sql=f"Insert Into airplane(ICAO) Value ('{self.icao}')"
        dbcur.execute(icao_sql)
        # initialize odd and even msg
        self.msg1 = None
        self.msg2 = None
        # count time计算时间
        self.time = 1
        self.cs=self.la=self.long=self.alt=self.gs=self.hd=self.roc="Null"
        

    def arrdata(self, msg, t):
        self.msg = msg
        self.t = t
        self.tc = pms.adsb.typecode(self.msg)
        if 1 <= self.tc <= 4:
            self.callsign()

        if 5 <= self.tc <= 18:
            self.position()

        if self.tc == 19:
            self.velocity()

    def position(self):
        if  pms.adsb.oe_flag(self.msg):
            # odd msg and time
            self.msg1 = self.msg
            self.t1 = self.t
        else:
            # even msg and time
            self.msg2 = self.msg
            self.t2 = self.t

        self.latitude_longitude()
        self.altitude()

    def latitude_longitude(self):
        print(f"{self.msg1}  {self.msg2}")
        if self.msg1 and self.msg2:
            try:
                # latude,longtitute
                self.la,self.long = pms.adsb.position(
                    self.msg1, self.msg2, self.t1, self.t2)
            except:
                print('error')

    def altitude(self):
        # altitude高度
        self.alt = pms.adsb.altitude(self.msg)

    def callsign(self):
        # callsign飞机机号
        self.cs = pms.adsb.callsign(self.msg)

    def velocity(self):
        # groundspeed速度,heading飞行方向,rateofclimb上升速度
        self.gs,self.hd,self.roc,self.type = pms.adsb.velocity(self.msg)

    def insert_data(self):
        sql=f"Update `airplane` Set `callsign`='{self.cs}', `latitude`={self.la}, `longitude`={self.long}, `altitude`={self.alt}, `ground_speed`={self.gs}, `heading`={self.hd}, `rate_of_climb`={self.roc}, `live`={1} Where ICAO='{self.icao}'"
        dbcur.execute(sql)
        db.commit()
        # print(sql)

        


def data():
    print("listening")
    while True:
        data_byte = socket.recv(512)
        data_str = bytes.decode(data_byte)
        data = data_str.replace('*', '').replace(';', '').replace('\r\n', '')
        datatime = time.time()
        # print(data)
        decode(data, datatime)

# msg,time


def decode(msg, t):
    if len(msg) == 28:           # wrong data length
        df = pms.df(msg)
        if df == 17:
            icao = pms.adsb.icao(msg)
            # check plane
            flag = False
            for x in plane:
                if x.icao == icao:
                    flag = True
                    a = x
            if flag:
                pass
            else:
                a = Plane(icao)
                plane.append(a)
            
            a.arrdata(msg, t)
            a.insert_data()
            # print(plane)


print("strat")
socket = socket.socket()
socket.connect(('localhost', 47806))
data()

print('end')
