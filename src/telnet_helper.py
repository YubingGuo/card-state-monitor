import telnetlib
import time
import logging
import re

class TelnetHelper():
    def __init__(self, ip, port, username = "", password = "", prompt = "", login_timeout = 5):
        self.ip_address = ip
        self.port = port
        self.username = username
        self.password = password
        self.prompt = prompt
        self.login_timeout = login_timeout

    def readUntil(self, tn, until, timeout):
        if not tn or not until:
            return (False, '')

        read_result = ''
        start_time = time.time()
        while read_result.find(until) == -1:
            read_result += tn.read_very_eager()
            if (time.time() - start_time) > timeout:
                return (False, '')
        
        return (True, read_result)
        

    def executeCommand(self, tn, cmd, timeout):
        try:
            tn.write(cmd)
            (result, stdout) = self.readUntil(tn, self.prompt, timeout)
            
            if result:
                logging.debug('"%s" execution done' % cmd)
                return (True, stdout)
            else:
                logging.error('"%s" execution timeout' % cmd)
                return (False, '')

        except:
            logging.error('"%s" execution failed' % cmd)
            return (False, out)


    def executeCommands(self, tn, cmd_list, timeout):
        out = ''
        if not tn or not cmd_list:
            return (False, '')

        for cmd in cmd_list:
            (result, stdout) = self.executeCommand(tn, cmd, timeout)

            if result:
                out += stdout
            else:
                return (False, '')
        
        return (True, out)
        
        
    def login(self, timeout = 5):
        try:
            tn = telnetlib.Telnet(self.ip_address, self.port, timeout)
            (result, out) = (True, '')
            
            if self.username:
                (result, out) = self.readUntil(tn, 'login: ', timeout)
                if result:
                    tn.write(self.username + '\n')  

            if self.password and result:
                (result, out) = self.readUntil(tn, 'password: ', timeout)
                if result:
                    tn.write(self.password + '\n')

            if self.prompt and result:
                (result, out) = self.readUntil(tn, self.prompt, timeout)

            if result:
                return tn
            else:
                return None

        except:
            logging.error('telnet to "%s":"%s" failed' % self.ip_address % self.port)
            return None


    def close(self, tn):
        if tn:
            tn.write("quit\n")
            tn.close()

        
    def execute(self, cmd_list = [], timeout = 5):
        telnet = self.login(self.login_timeout)
        if telnet and cmd_list:
            (result, out) = self.executeCommands(telnet, cmd_list, timeout)
            self.close(telnet)
            return (result, out)
        else:
            return (False, '')
