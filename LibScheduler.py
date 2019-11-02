import threading
import time 
import sys

MAIN_TICK_INTERVAL_SECS = 1

class TestWorkItem:
    def GetIntervalSeconds(_):
        return 60

    def Execute(a):
        print ("Running")
        return False

class FastWorkItem:
    def GetIntervalSeconds(_):
        return 5

    def Execute(a):
        print ("Running fast")
        time.sleep(10)
        return False

class ScheduledItem:
    """ Reprisents task that has been sceduled to run """
    def __init__(self, item):
        self.Item = item
        self.LastExecuted = 0
        self._lock = threading.Lock()
        self._isExecuting = False
    
    def CanExecute(self):
        """ Checks if the task can be executed at this time """
        with self._lock:
            return not self._isExecuting

    def Execute(self):
        """ Executes the task """

        with self._lock:
            if self._isExecuting:
                raise Exception("Cannot execute this item. CanExecute() == False")

            self._isExecuting = True
        try:
           self.Item.Execute()
        except:
            e = sys.exc_info()
            print("Task threw exception during execution - " + str(e))

        with self._lock:
           self._isExecuting = False
        
class Scheduler:
    _items = []
    def RegisterWorkItem(self, item):
        self._items.append(ScheduledItem(item))

    def Run(self):
        x = threading.Thread(target=self._RunInternal)
        x.start()

    def _RunInternal(self):
        while (True):
            for item in self._items:
                now = time.time()
                diff = now - item.LastExecuted
                if (now - item.LastExecuted) >= item.Item.GetIntervalSeconds():
                    if (item.CanExecute()):
                        t = threading.Thread(target=item.Execute)
                        t.start()
                        item.LastExecuted = now
                    else:
                        print("Item is due to execute, but was skipped because it was not ready")

            time.sleep(MAIN_TICK_INTERVAL_SECS)


