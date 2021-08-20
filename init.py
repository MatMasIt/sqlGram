import  uuid
def init(c):
    if  c["DATA"]["masterToken"] == "null":
        uid=str(uuid.uuid4())
        c["DATA"]["masterToken"] = uid
        with open('conf.ini', 'w') as configfile:
            c.write(configfile)
        c.read("conf.ini")
        return uid
    elif c["DATA"]["firstTime"] == "yes":
        return c["DATA"]["masterToken"]
    return False
def setInited(c,chat):
    c["DATA"]["allowedIds"]=str(chat.id)
    c["DATA"]["firstTime"] = "no"
    with open('conf.ini', 'w') as configfile:
        c.write(configfile)
    c.read("conf.ini")