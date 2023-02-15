import os
import sqlite3


def init():
    con = sqlite3.connect("duplicate.db")
    con.execute(
        '''
        CREATE TABLE IF NOT EXISTS duplicates (
	id INTEGER PRIMARY KEY
);
        '''
    )
    # con.execute("INSERT INTO [duplicates] ([id]) VALUES ('76561199046915102');")
    con.commit()
    con.close()
    if not os.path.isdir("result"):
        os.mkdir("result")
        os.mkdir("result/empty")
        os.mkdir("result/friends")
        os.mkdir("result/not_ru")
        os.mkdir("result/verified")
        os.mkdir("result/valid")
