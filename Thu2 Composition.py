import typing
class A:
    base_speed = 100
    def  __init__(self,engine,wheels):
        self.engine = engine
        self.wheels = wheels
    
    def info(self):
        print(f"The car is {self.engine} engine car  and has {self.wheels} wheels")
    @staticmethod
    def hint():
        return "If you buy a car, you will get 2000 dollars!"
class B():
    top_speed = A.base_speed*2
    def __init__(self,car:A):
        
        self.car=car
        # self.car.color = color
    def run(self):
        print(f"B is running with speed {B.top_speed} km/h ")
    def stop(self):
        print(f"B is stopping with {self.car.base_speed} km/h ")
        
#Another way of composition
class C:
    def __init__(self):
        self.a = A("V12",8)
    def intro(self):
        return self.a.info()
    def getHint(self):
        return self.a.hint()
        
#------------------------------------------
if __name__ == "__main__":  
    car  = A("V8",4)
    # car.run() #Error  car  is a composition of A not inheritance : "has a " relationship
    car_behavior = B(car)
    car_behavior.run()
    car_behavior.stop()
    car2 = C()
    car2.intro()
    print(car2.getHint())
    # car.info()
    # car2 = B(car,"Red")
    # car2.car.info()
    # print(f"The car is {car2.car.color} color {car2.car.engine} engine car  and has {car2.car.wheels} wheels")
    pass