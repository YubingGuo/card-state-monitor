import re
import data_types

class CardStateParser():

    '''
    parse output of "card state show all@BTSOMexe" to CardList
    '''
    def Parse(self, content):
        cardList = data_types.CardList()
        allCardStr = re.findall( r'^l[a-z]{2}-?[0-9]{0,2}.*', content, re.I|re.M)
        
        for cardStr in allCardStr:
            elements = cardStr.split()
            if len(elements) == 7:
                card = data_types.Card(elements[0], elements[1], elements[2], elements[3], elements[4], elements[5], elements[6])
                cardList.Append(card)
                
        return cardList

    def ReadContent(self, file):
        all_the_text=''
        file_object = open(file)
        try:
            all_the_text = file_object.read()
        except:
            print "Open file %s failed" % file
        finally:
            file_object.close()

        return all_the_text

    def ReadCardFromFile(self):
        file="D:\Study\SourceCode\python_test\output.txt"

        content = self.ReadContent(file)
        cardList = self.Parse(content)
        
        return cardList

#print cardStateMap["lcp-1"]
 
