
CTRL_TYPE_UNKNOWN = 0
CTRL_TYPE_S_RESET = 1
CTRL_TYPE_H_RESET = 2
CTRL_TYPE_SLEEP = 3
CTRL_TYPE_SLEEP_REL = 4
CTRL_TYPE_CHECK = 5
CTRL_TYPE_MOUNT = 6
CTRL_TYPE_UNMOUNT = 7

STATE_TYPE_INVALID = 0
STATE_TYPE_UNINST = 1
STATE_TYPE_HIZ = 2
STATE_TYPE_NOHWINFO = 3
STATE_TYPE_INST = 4
STATE_TYPE_ACT = 5
STATE_TYPE_BLOCK = 6
STATE_TYPE_PBLOCK = 7
STATE_TYPE_NOT_READY = 8
STATE_TYPE_CHECK = 9
STATE_TYPE_FULL_ALAMR = 10
STATE_TYPE_PARTIAL_ALARM = 11
STATE_TYPE_SLEEP = 12

STATE_STR_INSTALLED = "Installed"
STATE_STR_BASIC = "Basic"
STATE_STR_FAULT = "Fault"
STATE_STR_USE = "Use"
STATE_STR_NE = "Ne"
STATE_STR_SPECIFIC = "Specific"

class CardStates():
    def __init__(self, installed, basic, fault, use, ne, specific):
        self.states = {}
        self.states[STATE_STR_INSTALLED] = installed
        self.states[STATE_STR_BASIC] = basic
        self.states[STATE_STR_FAULT] = fault
        self.states[STATE_STR_USE] = use
        self.states[STATE_STR_NE] = ne
        self.states[STATE_STR_SPECIFIC] = specific

    def __eq__(self, other):
        if not isinstance(other, CardStates):
            return NotImplemented
        return other.states == self.states
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def GetState(self, stateName):
        if stateName:
            return self.states[stateName]
        else:
            return ''
    
    def Type(self):
        installed_state = self.states["Installed"]
        basic_state = self.states["Basic"]
        specific_state = self.states["Specific"]
        fault_state = self.states["Fault"]
        
        state_type = STATE_TYPE_INVALID

        if installed_state == "UNINST":
            state_type = STATE_TYPE_UNINST
        elif installed_state == "Hiz":
            state_type = STATE_TYPE_HIZ
        elif installed_state == "INST_NoHwInfo":
            state_type = STATE_TYPE_NOHWINFO
        elif installed_state == "INST_READY":
            state_type = STATE_TYPE_INST
        else:
            state_type = STATE_TYPE_INVALID
        
        if state_type == STATE_TYPE_INST:
            if basic_state == "ACT":
                state_type = STATE_TYPE_ACT
            elif basic_state == "BLK":
                state_type = STATE_TYPE_BLOCK
            elif basic_state == "PBLK":
                state_type = STATE_TYPE_PBLOCK
            elif basic_state == "NotReady":
                state_type = STATE_TYPE_NOT_READY
            elif basic_state == "CHECK":
                state_type = STATE_TYPE_CHECK
            else:
                pass
        
            if specific_state == "SLP":
                state_type = STATE_TYPE_SLEEP
        
        if fault_state == "ALM":
            if state_type == STATE_TYPE_INST or state_type == STATE_TYPE_NOHWINFO:
                state_type = STATE_TYPE_FULL_ALAMR
            else:
                state_type = STATE_TYPE_PARTIAL_ALARM
        elif fault_state == "ERR" or fault_state == "ALM_ERR":
			state_type = STATE_TYPE_PARTIAL_ALARM
        else:
            pass
        
        return state_type
        
        
class Card():
    def __init__(self, name, installed, basic, fault, use, ne, specific):
        self.name = name
        self.states = CardStates(installed, basic, fault, use, ne, specific)

    def GetName(self):
        return self.name
    
    def GetStates(self):
        return self.states

    def GetState(self, stateName):
        return self.states.GetState(stateName)
        
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return other.name == self.name and other.states == self.states

    def __ne__(self, other):
        return not self.__eq__(other)
    
class CardList():
    def __init__(self):
        self.list = []
        self.index = 0;
    
    def Append(self, card):
        self.list.append(card)
    
    def GetSize(self):
        return len(self.list)
        
    def IsEmpty(self):
        return len(self.list) == 0
        
    def __len__(self):
        return len(self.list)
        
    def __getitem__(self, index):
        if index < len(self.list):
            return self.list[index]
        return None

    def __eq__(self, other):
        if not isinstance(other, CardList):
            return NotImplemented

        if len(other.list) != len(self.list):
            return False
        
        for i in range(len(self.list)):
            if other.list[i] != self.list[i]:
                return False
                
        return True
        
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __iter__(self):
        self.index = 0
        return self
            
    def next(self):
        if self.index == len(self.list):
            raise StopIteration

        card = self.list[self.index]
        self.index += 1
        return card
        

class CardStateDisplayer():
    def Display(self, cardList):
        print "CardStateDisplayer::Display!!!!"
