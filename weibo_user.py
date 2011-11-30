import sqlite3 as sqlite
from weibo_api import get_api
import datetime
import db

con = db.get_connection()
cursor = con.cursor()
api = get_api()

class WeiboUser():
    def __init__(self, user_id, scrn_name, name,
            foer_cnt, friend_cnt, 
            desc, location, created_at, status_cnt, verified,
            scanned):
        self.user_id = user_id
        self.scrn_name = scrn_name
        self.name = name
        self.foer_cnt = foer_cnt
        self.friend_cnt = friend_cnt
        self.desc = desc
        self.location = location
        if isinstance(created_at, datetime.datetime):
            self.created_at = created_at.date()
        else:
            self.created_at = created_at
        self.status_cnt = status_cnt
        self.verified = verified
        self.scanned = scanned

    @classmethod
    def save_weibo_api(cls, w_api):
        user = WeiboUser(w_api.id, w_api.screen_name, w_api.name,
                w_api.followers_count, w_api.friends_count,
                w_api.description, w_api.location, w_api.created_at,
                w_api.statuses_count, w_api.verified, False)
        user.save_new()
        return user

    @property
    def id(self):
        try:
            cursor.execute('''select id from w_user where user_id =
                    ?''',(self.user_id,))
            id = cursor.fetchone()[0]
        except sqlite.IntegrityError:
            print "can not find user ", self.user_id, "(",
            self.scrn_name, ") , it's not in database"
            id = 0
        return id
    
    @property
    def weibo_api_obj(self):
        return api.get_user(self.user_id)

    def save_new(self):
        self.scanned = False
        info = (self.user_id, self.scrn_name, self.name,
                self.foer_cnt, self.friend_cnt, self.desc, self.location,
                self.created_at, self.status_cnt, self.verified, self.scanned)
        try:
            cursor.execute('''insert into w_user(user_id, 
            screen_name, name, foer_cnt, friend_cnt,
            desc, location, created_at, status_cnt,
            verified, scanned) values 
            (?,?,?,?,?,?,?,?,?,?,?)''', info)
            con.commit()
        except sqlite.IntegrityError:
            print "can not save user", self.user_id, "(",self.scrn_name,") to the database"

    def update(self):
        info = (self.user_id, self.scrn_name, self.name,
                self.foer_cnt, self.friend_cnt,
                self.desc, self.location, self.created_at,
                self.status_cnt, self.verified, self.scanned, self.id)
        try:
            cursor.execute('''update w_user set user_id=?, 
            screen_name=?, name=?, foer_cnt=?, friend_cnt=?, desc=?,
            location=?, created_at=?, status_cnt=?, verified=?,
            scanned=? where id=?''', info)
            con.commit()
        except sqlite.IntegrityError:
            print "can not update user", self.user_id, "(",self.scrn_name,") to the database"
        pass
    
    def update_scanned(self):
        self.scanned = True
        try:
            cursor.execute('''update w_user set scanned=? where
                    user_id=?''', (self.scanned, self.user_id))
            con.commit()
        except sqlite.InternalError:
            print "can not update ", self.user_id, "(",self.screen_name,") to scanned"


    @classmethod
    def get_by_id(cls, twitter_id):
        cursor.execute('''select user_id,
            screen_name, name, foer_cnt, friend_cnt,
            desc, location, created_at, 
            status_cnt, verified, scanned from w_user
            where user_id = ?''', (twitter_id,))
        result = cursor.fetchone()
        if result:
            w_user = WeiboUser(*result)
            return w_user
        else: return None

    @classmethod
    def get_next_unscanned(cls):
        cursor.execute('''select user_id,
            screen_name, name, foer_cnt, friend_cnt,
            desc, location, created_at, 
            status_cnt, verified, scanned from w_user
            where scanned=0 limit 0,1''')
        result = cursor.fetchone()
        if result:
            w_user = WeiboUser(*result)
            return w_user
        else: return None
