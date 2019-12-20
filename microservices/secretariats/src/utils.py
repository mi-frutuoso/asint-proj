import hashlib
import pickle
import os.path

class Secretariat:
    def __init__(self, location, name, description, opening_hours):
        self.location = location
        self.name = name
        self.description = description
        self.opening_hours = opening_hours
        self.id = hashlib.sha1(str.encode(location+name)).hexdigest()
        print('[created secretariat w/ id = '+self.id+']')

    def update(self, newInfo):
        self.location = newInfo["location"]
        self.name = newInfo["name"]
        self.description =  newInfo["description"]
        self.opening_hours = newInfo["opening_hours"]

class Storage:
    def __init__ (self):
        if os.path.isfile('storage.dat'):
            self.load()
            print("[Secretariat storage loaded]")
        else:
            self.secretariatList = []

    def getSize(self):
        return len(self.secretariatList)

    def store(self, local, name, descr, hours):
        s = Secretariat(local, name, descr, hours)
        self.secretariatList.append(s)
        self.export()
        return s.id

    def edit(self, ID, newInfo):
        for s in self.secretariatList:
            if ID in s.id:
                s.update(newInfo)
                self.export() # update current state of storage 
                #break        
                return "ok"
        return "notok"

    def delete(self, ID):
        for i, o in enumerate(self.secretariatList):
            if o.id == ID:
                del self.secretariatList[i]
                break
        self.export() # update current state of storage

    def getSecretariat(self, ID):
        for s in self.secretariatList:
            if ID in s.id:
                obj = {}
                obj["location"] = s.location
                obj["name"] = s.name
                obj["description"] = s.description
                obj["opening_hours"] = s.opening_hours
                return(obj)
    
    def listAll(self):
        list_all = []
        for s in self.secretariatList:
            obj = {}
            obj["location"] = s.location
            obj["name"] = s.name
            obj["description"] = s.description
            obj["opening_hours"] = s.opening_hours
            obj["id"] = s.id
            list_all.append(obj)
        return list_all

    def export(self):
        with open("storage.dat", 'wb') as fp:
            pickle.dump(self.secretariatList, fp) #, protocol=pickle.HIGHEST_PROTOCOL

    def load(self):
        with open("storage.dat", 'rb') as f:
            sl = pickle.load(f)
        self.secretariatList = []
        self.secretariatList = sl