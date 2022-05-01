from pymongo import MongoClient
from decouple import config

Mongo_Uri = config('Mongo_URL')
mycli = MongoClient(Mongo_Uri)
mydb = mycli["Vampires"]
mycol = mydb["Users"]

class user:
    def check(userid):        
        if mycol.count_documents({"userid":userid}) == 0:
            return False
        else:
            return True
            
    def signup(name, email, gender, dob, b_group, aadhar, userid):
        try:
            mycol.insert_one({"_id":userid, "name": name, "email": email, "gender":gender, "dob":dob, "b_group": b_group, "aadhar":aadhar})
            return 201
        except:
            return 400
    
    def signin(userid):
        return mycol.find_one({'userid':userid})