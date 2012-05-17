import threading
import time

class t(threading.Thread):
    def __init__(self,name):
        self.tname = name
        threading.Thread.__init__(self)
    def run(self):
        for i in range(10000):
            a =str(self.name) + " is still running" + str(i)
            print a
class t_watcher(threading.Thread):
    def __init__(self,t1):
        self.t1 = t1
        threading.Thread.__init__(self)
    def run(self):
        while (self.t1.is_alive()):
            time.sleep(.1)
        print "DONE"
        #self.t1._Thread__stop()

if __name__ == "__main__":
    thread1 = t("thread1")
    watcher = t_watcher(thread1)
    thread1.start()
    watcher.start()
