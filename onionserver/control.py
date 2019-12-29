



class CONTROL(object):
    

    def __init__(self):
        pass


    def hob_off(self):
        
        print ("Hob has been turned off")
        return "{Success: True}"


    def set_hob(self, value):
        statement = ("Hob has been set to %s") % (value)
        
        print (statement)
        return statement


