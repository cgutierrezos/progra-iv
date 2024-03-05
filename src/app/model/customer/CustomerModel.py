
class CustomerModel:

    def __init__(self):
        self.id = ""
        self.name = ""
        self.identification = ""


    def __str__(self):
        return f"id:{self.id}  name:{self.name},  identification:{self.identification}"

    