import psycopg2
import os

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

class user:
    def check(userid):
        cur.execute("SELECT * FROM accounts WHERE id = %s", (userid))       
        if cur.fetchone() is not None:
            return False
        else:
            return True
            
    def signup(name, email, gender, dob, b_group, aadhar, userid):
        try:
            cur.execute(f'INSERT INTO accounts  (id, name, email, gender, dob, b_group, aadhar) VALUES ({userid}, "{name}", "{email}", "{gender}",  "{gender}", "{dob}", {b_group}, {aadhar})')
            conn.commit()
            return 201
        except:
            return 400
    
    
    def signin(userid):
        cur.execute('SELECT * FROM accounts WHERE id = "id"')
        return cur.fetchone()