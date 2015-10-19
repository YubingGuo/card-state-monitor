import time
import Queue
import logging
import threading
import telnet_helper

class CardStateCollector():
    def __init__(self, target):
        self.ip = target
        self.port = "15007"
        self.username = ""
        self.password = ""
        self.prompt = 'AaShell>'
        self.login_timeout = 2
        self.execute_timeout = 2
        self.cmd_list = ["card state show all@BTSOMexe\n"]

        self.telnetHelper = telnet_helper.TelnetHelper(self.ip, self.port, self.username, self.password, self.prompt, self.login_timeout)


    def Collect(self):
        try:
            (result, out) = self.telnetHelper.execute(self.cmd_list, self.execute_timeout)
            #logging.info("telnet and execute commonds success")
            return (result, out)
        except:
            #logging.warning("telnet and execute commonds failed")
            return (False, '')


class CardStateCollectThread(threading.Thread):
    def __init__(self, queue, configurator):
        threading.Thread.__init__(self)
        self.running = False
        
        self.queue = queue
        self.configurator = configurator
        self.initConfig()
        
    def canBeRun(self):
        if self.queue and self.configurator and not self.running:
            return True
        return False
        
    def initConfig(self):
        if self.configurator:
            self.interval = self.configurator.GetInterval()
            self.target = self.configurator.GetTarget()
            self.collector = CardStateCollector(self.target)
    
    def compareConfigurator(self):
        self.interval = self.configurator.GetInterval()
        if self.target != self.configurator.GetTarget():
            self.target = self.configurator.GetTarget()
            self.collector = CardStateCollector(self.target)
        
    def run(self):
        if not self.canBeRun():
            return

        self.running = True
        while self.running:
            self.compareConfigurator()
            start_time = time.time()
            (result, out) = self.collector.Collect()
            
            if self.queue.full():
                self.queue.get()
            self.queue.put((result, out))
            
            used_time = time.time() - start_time
            if  used_time < self.interval:
                time.sleep(self.interval - used_time)
            
    def stop(self):
        self.running = False
        
    def isRunning(self):
        return self.running
