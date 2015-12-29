import string

card_slot_id_dict = {'LCP': (1, 15),
                      'LSP': (2, 3, 4, 5, 6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22, 23),
                      'LBR': (30, 31, 33, 34),
                      'LNI': (32, 35),
                      'LCA': (11, ),
                      'LBI': (29, ),
                      'LPS': (12, 13, 14, 26, 27, 28)}

def calculate_slot_id_of_card(card_name):

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

def calculate_cnt_id_of_card(card_name):

    cnt_id_list = []

    card_name = card_name.upper().replace('-', '')
    name_length = len(card_name)

    if (name_length < 3):
        return cnt_id_list

    card_type = card_name[0:3]
    
    if (card_type == 'LCP'):
        if (card_name == 'LCP0'):
            cnt_id_list.append(48)
        elif (card_name == 'LCP1'):
            cnt_id_list.append(49)
        else:
            pass
    elif (card_type == 'LSP'):
        card_id = int(card_name[3:])
        if (0 <= card_id < 16):
            cnt_id_list.append(card_id * 2)
            cnt_id_list.append(card_id * 2 + 1)
        else:
            pass
    else:
        pass

    return cnt_id_list
