import os
import ConfigParser

COLLECT_SECTION = "Collect"
DISPLAY_SECTION = "Display"
CONFIG_TARGET = "target"
CONFIG_INTERVAL = "interval"
CONFIG_IGNORE = "ignore"

DEFAULT_TARGET = "192.168.129.2"
DEFAULT_INTERVAL = 3
DEFAULT_IGNORE = False

class Configurator():
    def __init__(self, config_file):
        self.createConfigFileIfNotExist(config_file)
        
        self.config_file = config_file
        self.config_parser = ConfigParser.ConfigParser()
        
        self.target = DEFAULT_TARGET
        self.interval = DEFAULT_INTERVAL
        self.ignore = DEFAULT_IGNORE
        
        self.ReadFromFile()
        
    def createConfigFileIfNotExist(self, config_file):
        if not os.path.exists(config_file):
            if not os.path.exists(os.path.dirname(os.path.abspath(config_file))):
                os.makedirs(os.path.dirname(os.path.abspath(config_file)))
            open(config_file, 'w').close()
        
        return True

    def createOptionIfNotExist(self):
        self.config_parser.read(self.config_file)
        
        if not self.config_parser.has_section(COLLECT_SECTION):
            self.config_parser.add_section(COLLECT_SECTION)
        if not self.config_parser.has_section(DISPLAY_SECTION):
            self.config_parser.add_section(DISPLAY_SECTION)

        if not self.config_parser.has_option(COLLECT_SECTION, CONFIG_TARGET) or \
           not self.config_parser.get(COLLECT_SECTION, CONFIG_TARGET):
            self.config_parser.set(COLLECT_SECTION, CONFIG_TARGET, DEFAULT_TARGET)
        if not self.config_parser.has_option(COLLECT_SECTION, CONFIG_INTERVAL) or \
           not self.config_parser.get(COLLECT_SECTION, CONFIG_INTERVAL):
            self.config_parser.set(COLLECT_SECTION, CONFIG_INTERVAL, DEFAULT_INTERVAL)
        if not self.config_parser.has_option(DISPLAY_SECTION, CONFIG_IGNORE) or \
           not self.config_parser.get(DISPLAY_SECTION, CONFIG_IGNORE):
           self.config_parser.set(DISPLAY_SECTION, CONFIG_IGNORE, DEFAULT_IGNORE)

        self.config_parser.write(open(self.config_file,"w"))
        
    def ReadFromFile(self):
        self.createOptionIfNotExist()
        try:
            self.config_parser.read(self.config_file)
            self.target = self.config_parser.get(COLLECT_SECTION, CONFIG_TARGET)
            self.interval = self.config_parser.getint(COLLECT_SECTION, CONFIG_INTERVAL)
            self.ignore = self.config_parser.getboolean(DISPLAY_SECTION, CONFIG_IGNORE)
        except:
            self.createOptionIfNotExist()
            print "Invalid option is found in config file!"
        
    def WriteToFile(self):
        #self.config_parser.read(self.config_file)
        self.config_parser.set(COLLECT_SECTION, CONFIG_TARGET, self.target)
        self.config_parser.set(COLLECT_SECTION, CONFIG_INTERVAL, self.interval)
        self.config_parser.set(DISPLAY_SECTION, CONFIG_IGNORE, self.ignore)
        self.config_parser.write(open(self.config_file,"w"))

    def ShouldIgnoreUninst(self):
        return self.ignore
        
    def GetInterval(self):
        return self.interval
    
    def GetTarget(self):
        return self.target
        
    def Get(self):
        return (self.target, self.interval, self.ignore)
        
    def Set(self, values):
        
        self.target = values[0]
        self.interval = values[1]
        self.ignore = values[2]

        self.WriteToFile()
        
        return True