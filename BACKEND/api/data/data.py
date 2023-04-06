import sqlite3

def create_table_user():
    try:
        sqliteConnection = sqlite3.connect('data/dataset.db')
    
        create_table_users = """CREATE TABLE IF NOT EXISTS USERS(
                                    UserID INTEGER  PRIMARY KEY AUTOINCREMENT,
                                    HoTen TEXT NOT NULL,
                                    TenDN TEXT NOT NULL ,
                                    DiaChi TEXT NOT NULL,
                                    NgaySinh datetime,
                                    MatKhau TEXT NOT NULL);"""

        create_table_results = """CREATE TABLE IF NOT EXISTS RESULTS(
                                    ResultID INTEGER  PRIMARY KEY AUTOINCREMENT,
                                    UserID INTEGER ,
                                    LinkImg TEXT NOT NULL,
                                    TenBenh TEXT NOT NULL ,
                                    NgayTest DATE NOT NULL,
                                    DoChinhXac FLOAT NOT NULL,
                                    FOREIGN KEY(UserID) REFERENCES USERS(UserID));"""
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(create_table_users)
        cursor.execute(create_table_results)
        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")
            
        
def insertTableUser( HoTen, TenDN, DiaChi, NgaySinh, MatKhau):
    try:
        sqliteConnection = sqlite3.connect('data/dataset.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO USERS
                          (HoTen, TenDN, DiaChi, NgaySinh, MatKhau) 
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = ( HoTen, TenDN, DiaChi, NgaySinh, MatKhau)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into Users table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def insertTableResults(UserID, LinkImg, TenBenh, NgayTest, DoChinhXac):
    try:
        sqliteConnection = sqlite3.connect('data/dataset.db')
        cursor = sqliteConnection.cursor()
        print("Connected to Dataset")

        sqlite_insert_with_param = """INSERT INTO RESULTS
                          (UserID, LinkImg, TenBenh, NgayTest, DoChinhXac)
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (UserID, LinkImg, TenBenh, NgayTest, DoChinhXac)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into RESULTS table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            
# insertTableUser("1", "Trần Ngọc Hải", "Nhà A", "Thái Bình", "04/02/2001", "123456")
def getUeserByID(id):
    try:
        sqliteConnection = sqlite3.connect('data/dataset.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query = """select * from RESULTS where  UserID= ?"""
        # cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
        cursor.execute(sql_select_query, (id,))
        records = cursor.fetchall()
        Dict = []
        for i in records:
            keys = ("ResultID","UserID", "LinkImg", "TenBenh", "NgayTest", "DoChinhXac")
            # new_dict = {k: v for k, v in zip(keys, i)}
            new_dict = dict(zip(keys, i))
            Dict.append(new_dict)
        
        cursor.close()
        return Dict

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            
def Login(tenDN, matKhau):
    try:
        # sqliteConnection = sqlite3.connect('SQLite_Python.db')
        sqliteConnection = sqlite3.connect('data/dataset.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query_1 = """select UserID from USERS where  TenDN= ? and MatKhau =?"""
        # sql_select_query_2 = """select HoTen,TenDN,DiaChi,NgaySinh,MatKhau from USERS where  TenDN= ? and MatKhau =?"""
        sql_select_query_2 = """select * from USERS where  TenDN= ? and MatKhau =?"""
        results = {}
        
        rl1 = cursor.execute(sql_select_query_1, (tenDN, matKhau))
        records = rl1.fetchall()
        rl2 = cursor.execute(sql_select_query_2, (tenDN, matKhau))
        remarks = rl2.fetchall()[0]
        # keys = ("HoTen", "TenDN", "DiaChi", "NgaySinh", "MatKhau")
        keys = ("UserID", "HoTen", "TenDN", "DiaChi", "NgaySinh", "MatKhau")
        # new_dict = {k: v for k, v in zip(keys, remarks)}
        # print("Hello World")
        # print(len(records))
        new_dict = dict(zip(keys, remarks))
        if len(records[0]) == 0:
            results["UserID"] = 0
        else:
            results["UserID"] = str(records[0][0])
        results["User"] = new_dict
        cursor.close()
        # print(records)
        return results

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            
def update_table_users(UserID, HoTen, TenDN, DiaChi, NgaySinh, MatKhau):
    try:
        sqliteConnection = sqlite3.connect('data/dataset.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_update_query = """Update USERS set HoTen=?, TenDN=?, DiaChi=?, NgaySinh=?, MatKhau=? where UserID=?"""
        data = (HoTen, TenDN, DiaChi, NgaySinh, MatKhau, UserID)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The sqlite connection is closed")
            
def deleteResultByID(id):
    try:
        sqliteConnection = sqlite3.connect('data/dataset.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_query = """DELETE from RESULTS where ResultID = ?"""
        cursor.execute(sql_delete_query, (id,))
        sqliteConnection.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

if __name__ == '__main__':
    create_table_user()
    insertTableUser("Trần Thị Ngọc Khánh", "KhanhTran", "Thái Bình", "10/01/2001", "123456")
    insertTableUser("Trần Thị Huyền Trang", "TrangTran", "Thái Bình", "28/12/1991", "123456")
    insertTableUser("Ngô Tiến Sỹ", "SyNgo", "Nam Định", "16/16/1991", "123456")
    
    insertTableResults("1", "http.com.net", "Bệnh lá trắng", "30/03/2023", "99.83%")
    insertTableResults("1", "http.com.net", "Bệnh lá nâu", "30/03/2023", "99.83%")
    insertTableResults("2", "http.com.net", "Bệnh lá đen", "30/03/2023", "99.83%")
    insertTableResults("2", "http.com.net", "Bệnh lá vàng", "30/03/2023", "99.83%")
    
