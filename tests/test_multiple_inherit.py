class Father:
    father_age = 45

class Mother:
    def __init__(self):
        self.mother_age = 45

    # def get_dict(self):
        # return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

class Child(Father, Mother):
    def __init__(self):
        self.age = 22
    def get_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    

if __name__ == "__main__":
    child = Child()
    print(child.get_dict())