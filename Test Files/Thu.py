import time
import threading

class Timer:
    def __init__(self,duration):
        self.duration = duration
        self.start_time = time.time()
        self.is_running = True
    def is_elapsed(self):
        if not self.is_running:
            return False
        return (time.time() - self.start_time) >= self.duration

    def stop(self):
        self.is_running = False
    # def run(self):
    #     while True:
    #         time.sleep(self.interval)
    #         self.function(*self.args, **self.kwargs)
            
def event_handler(timer):
    print("Event handler opened")
    start_time = time.time()
    time.sleep(3)
    if timer.is_elapsed():
        print("Elapsed time reached")
        timer.stop()
        return
    
    # Your event handling code here
    print("Event handler closed")
    print("Execution time:", time.time() - start_time, "seconds")
    
    
def control_time():
    # global time
    # time = timer(10)  # Set the timer for 10 seconds
    # event_thread = threading.Thread(target=event_handler)
    # event_thread.start()
    # event_thread.join()  # Wait for the event handler to finish
    timer = Timer(10)  # Set the timer for 10 seconds
    while True:
        event_handler(timer)
        # if time.is_elapsed():
        #     print("Elapsed time reached, stopping control_time.")
        #     break
        # time.sleep(5)  # Sleep for 5 seconds before running the event handler again



# def event_handler():
#     print("Event handler opened")
#     # Your event handling code here
#     print("Event handler closed")

# def control_time():
#     while True:
#         event_handler()
#         time.sleep(5)  # Sleep for 5 seconds before running the event handler again

control_time()

