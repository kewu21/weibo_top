import sqlite3 as sqlite

DATABASE = 'networks_weibo'

def init():
    con = get_connection()
    cursor = con.cursor()
    create_weibo_user(cursor)
    create_weibo_relation(cursor)
    create_weibo_nor(cursor)
    con.commit()
    cursor.close()

def create_weibo_user(cursor):
    try:
        cursor.execute('''drop table if exists w_user''')
        cursor.execute('''create table w_user 
            (id integer primary key autoincrement,
            user_id integer unique not null,
            screen_name text not null,
            name text not null,
            foer_cnt integer not null,
            friend_cnt integer not null,
            desc text,
            location text,
            created_at date not null,
            status_cnt integer not null,
            verified integer,
            scanned integer)''')
    except sqlite.InterfaceError:
        print "can't create table w_user"

def create_weibo_relation(cursor):
    try:
        cursor.execute('''drop table if exists w_relation''')
        cursor.execute('''create table w_relation 
            (weibo_user integer, foer integer,
            primary key(weibo_user, foer))''')
    except sqlite.InterfaceError:
        print "can't create talbe w_relation"

def create_weibo_nor(cursor):
    cursor.execute('''drop table if exists w_non_r''')
    cursor.execute('''create table w_non_r 
        (weibo_user integer, foer integer,
        primary key(weibo_user, foer))''')
        
def get_connection():
    con = sqlite.connect(DATABASE,
        detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
    return con
