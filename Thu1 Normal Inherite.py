class A:
    def  __init__(self,engine,wheels):
        self.engine = engine
        self.wheels = wheels
    
    def info(self):
        print(f"The car is {self.engine} engine car  and has {self.wheels} wheels")
        
    # def sound(self):
    #     print("A Vroom ")
class B(A):
    def __init__(self,engine,wheels,color):
        super().__init__(engine,wheels)
        self.color = color
    
    def info(self):
        print(f"The car is {self.color} color {self.engine} engine car  and has {self.wheels} wheels")
        
    def sound(self):
        print("B Loud Vroom ")

if __name__ == "__main__":
    car  = A("V8",4)
    car.info()
    # car.sound()
    car2 = B("V6",4,"Red")
    car2.info()
    car2.sound()