import hashlib

class Secretariat:
    def __init__(self, location, name, description, opening_hours):
        self.location = location
        self.name = name
        self.description = description
        self.opening_hours = opening_hours
        self.id = hashlib.sha1(str.encode(location+name)).hexdigest()
        print('[created secretariat w/ id = '+self.id+']')

class Storage:
    def __init__ (self):
        self.secretariatList = []
        self.localList = []

    def getSize(self):
        return len(self.secretariatList)

    def store(self, local, name, descr, hours):
        s = Secretariat(local, name, descr, hours)
        self.secretariatList.append(s)
        if s.location not in self.localList:
            self.localList.append(s.location)
        return s.id
    
        # testar
        # s_obj = {
        #     'location':local,
        #     'name':name,
        #     'description':descr,
        #     'opening_hours':hours
        # }

    def getSecretariat(self, ID):
        for s in self.secretariatList:
            if ID in s.id:
                obj = {}
                obj["location"] = s.location
                obj["name"] = s.name
                obj["description"] = s.description
                obj["opening_hours"] = s.opening_hours
                return(obj)

    def listSecLocations(self):
        return self.localList
    
    def listAll(self):
        return self.secretariatList