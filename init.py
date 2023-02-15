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
    con.execute("INSERT INTO [duplicates] ([id]) VALUES ('76561199046915102');")
    con.commit()
    con.close()