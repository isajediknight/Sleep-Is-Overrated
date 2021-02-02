# import the threading module
import threading


class thread(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

        # helper function to execute the threads

    def run(self):
        print(str(self.thread_name) + " " + str(self.thread_ID));


thread1 = thread("GFG", 1000)
thread2 = thread("GeeksforGeeks", 2000);
thread3 = thread("MOAR", 3000);
thread4 = thread("tHrEaDs", 4000);

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
print("not TEH END")
thread3.join()
thread4.join()

print("TEH END")