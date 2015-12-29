import wx
import os
import logging
from tendo import singleton

import data_types
import cardstate_parser
import cardstate_controller
import cardstate_displayer
import configurator

LOG_DIRECTION_FILE = 1
LOG_DIRECTION_CONSOLE = 2

class DisplayerFrame(wx.Frame, data_types.CardStateDisplayer):
    def __init__(self, parent, configurator):
        self.title = "Card State Monitor"
        self.exe_name = "CardStateMonitor.exe"
        self.size = (600, 700)
        self.style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER
        wx.Frame.__init__(self, parent, -1, self.title, wx.DefaultPosition, self.size, self.style)
        
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.configurator = configurator
        self.InitPanel()
        self.InitStatusBar()
        
        self.SetIcon(wx.Icon(self.exe_name, wx.BITMAP_TYPE_ICO))
        
    def InitPanel(self):
        panel = wx.Panel(self)
        
        self.ctrl_panel = cardstate_displayer.ControlPanel(panel, self.configurator)
        self.disp_panel = cardstate_displayer.DisplayPanel(panel, self.configurator)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ctrl_panel, 0, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL, 3)
        sizer.Add(self.disp_panel, -1, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL, 3)
        panel.SetSizer(sizer)

    def InitStatusBar(self):
        self.statusbar = self.CreateStatusBar(style = wx.NO_BORDER)
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusStyles([wx.SB_NORMAL, wx.SB_NORMAL])#wx.SB_RAISED,wx.SB_FLAT])
        self.statusbar.SetStatusWidths([-1, -1])
        
    def Display(self, cardList):
        self.disp_panel.Display(cardList)
        
        if not cardList or cardList.IsEmpty():
            self.statusbar.SetStatusText("Connect to " + self.configurator.GetTarget() + " failed", 1)
        else:
            self.statusbar.SetStatusText("Connected to " + self.configurator.GetTarget(), 1)

    def OnCloseWindow(self, event):
        self.Destroy()


class DisplayerApp(wx.App):
    def OnInit(self):
        self.config_file = "setting/setting"

        self.configurator = configurator.Configurator(self.config_file)
        self.frame = DisplayerFrame(None, self.configurator)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        
        self.cardStateController = cardstate_controller.CardStateControlThread(self.frame, self.configurator)
        self.cardStateController.start()
        return True


    def OnExit(self):
        if self.cardStateController.isRunning():
            self.cardStateController.stop()
            self.cardStateController.join()
            
        #self.frame.Destroy()
        
    
def create_logfile(filename):
    if not os.path.exists(os.path.dirname(os.path.abspath(filename))):
        os.makedirs(os.path.dirname(os.path.abspath(filename)))
        print "create dir"
    if not os.path.exists(filename):
        open(filename, 'w').close()
        print "create file" 
 
def configLogger(diretion, level = None, filename = None):
    formatStr= '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if diretion == LOG_DIRECTION_FILE and filename:
        logging.basicConfig(filename = filename, filemode = "a+", format = formatStr, level = level) 
    elif diretion == LOG_DIRECTION_CONSOLE:
        streamHandler = logging.StreamHandler()
        logging.basicConfig(format = formatStr, level = level)       
    else:
        pass
        
def main():
    print __name__
    log_filename = "log/run.log"
    create_logfile(log_filename)
    configLogger(LOG_DIRECTION_FILE, logging.INFO, log_filename)
    
    me = singleton.SingleInstance()
    app = DisplayerApp(False)#1, log_filename)
    app.MainLoop()
    
if __name__ == '__main__':
    #try:
        main()
    #except:
    #    pass
