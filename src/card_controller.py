import os
import logging
from data_types import *
from eatt_helper import *

ctrl_id_dict = {
                   "S_RESET"       : 1,
                   "H_RESET"       : 23,
                   "SLEEP"         : 19,
                   "SLEEP_RELEASE" : 22,
                   "BLOCK"         : 2,
                   "UNBLOCK"       : 3
               }

card_slot_id_dict = {
                        'LCP': (1, 15),
                        'LSP': (2, 3, 4, 5, 6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22, 23),
                        'LBR': (30, 31, 33, 34),
                        'LNI': (32, 35),
                        'LCA': (11, ),
                        'LBI': (29, ),
                        'LPS': (12, 13, 14, 26, 27, 28)
                    }

class CardController():
    def __init__(self, eatt_root_path):
        self.eatt_helper = EattHelper(eatt_root_path)
        
        #self.Control("lcp-1", "S-Reset")
        
    def CalculateSlotId(self, card_name):
        card_name = card_name.upper().replace('-', '')
        name_length = len(card_name)

        if (name_length < 3):
            return 0

        card_type = card_name[0:3]

        if (name_length == 3):
            card_id = 0
        else:
            card_id = int(card_name[3:])

        try:
            slot_id = card_slot_id_dict[card_type][card_id]
        except:
            slot_id = 0

        return slot_id

    def CalculateCtrlId(self, ctrl_type):
        ctrl_type = ctrl_type.upper().replace('-', '_')

        try:
            ctrl_id = ctrl_id_dict[ctrl_type]
        except:
            ctrl_id = 0

        return ctrl_id

    def Control(self, card_name, ctrl_type):
        slot_id = self.CalculateSlotId(card_name)
        ctrl_id = self.CalculateCtrlId(ctrl_type)

        if (slot_id == 0 or ctrl_id ==0):
            logging.error("Parameter %s or %s is invalid!" % (card_name, ctrl_type))
            return (False, "Parameter %s or %s is invalid!" % (card_name, ctrl_type))
        else:
            logging.info("Control(%d-%d)!" % (slot_id, ctrl_id))
            return self.eatt_helper.CardControl(slot_id, ctrl_id)
