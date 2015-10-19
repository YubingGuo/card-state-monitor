import time
import Queue
import logging
import threading

import data_types
import cardstate_parser
import cardstate_collector

class CardStateControlThread(threading.Thread):
    def __init__(self, displayer, configurator):
        threading.Thread.__init__(self)
        self.displayer = displayer
        self.configurator = configurator
        self.queueSize = 10
        self.collectInterval = 5
        self.running = False
        self.queue = Queue.Queue(self.queueSize)
        self.collectThread = cardstate_collector.CardStateCollectThread(self.queue, self.configurator)
        self.cardStateParser = cardstate_parser.CardStateParser()
        
    def run(self):
        if self.running:
            logging.error("Card state collect thread has been running!")
            return

        self.collectThread.start()
        self.running = True
        while self.running:
            if not self.queue.empty():
                (result, out) = self.queue.get()
                cardList = self.cardStateParser.Parse(out)
                if self.displayer:
                    self.displayer.Display(cardList)
                else:
                    break
            else:
                time.sleep(1)
                
    def isRunning(self):
        return self.running
        
    def stop(self):
        self.collectThread.stop()
        self.collectThread.join()
        self.running = False
