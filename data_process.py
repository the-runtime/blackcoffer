import asyncio
import string
import re



class data_process:

    
    def __iscomplex(self,word):
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        
        self.num_syllables+=count

        if count > 2:
            return True
        else:
            False


    def __getwords(file_path):

        lis = []
        f = open(file_path,'r',encoding="utf-8")
        lines = f.readlines()
        for line in lines:
                tem = line.split()
                #print(tem)
                tem = tem[0]
                tem = tem.upper()
                lis.append(tem)
            
        f.close()

        return lis

    stop_auditor_data = __getwords(file_path="input/StopWords/StopWords_Auditor.txt")
    stop_currencies_data = __getwords(file_path="input/StopWords/StopWords_Currencies.txt")
    stop_dates_data = __getwords(file_path="input/StopWords/StopWords_DatesandNumbers.txt")
    stop_generics_data = __getwords(file_path="input/StopWords/StopWords_Generic.txt")
    stop_genericlong_data = __getwords(file_path="input/StopWords/StopWords_GenericLong.txt")
    stop_geo_data = __getwords(file_path="input/StopWords/StopWords_Geographic.txt")
    stop_names = __getwords(file_path="input/StopWords/StopWords_Names.txt")

    stopwords = stop_auditor_data+stop_currencies_data+stop_dates_data+stop_generics_data+stop_genericlong_data+stop_geo_data+stop_names


    pos_words = __getwords(file_path="input/MasterDictionary/positive-words.txt")
    neg_words = __getwords(file_path="input/MasterDictionary/negative-words.txt")

    def __init__(self,data):

        self.words_list = []
        self.posscore = 0
        self.negscore = 0
        self.num_words = 0
        self.num_cleanwords = 0
        self.num_complexwords = 0


        #print(data)
        self.num_sentence = len(data["Text"]["para"])

        self.num_syllables = 0

        text = data["heading"]
        text += data["Text"]["text"]
        #for r in data["Text"]["para"]:
        #            text +=r
        #if data["Text"]["head"]is not None:
        #    for r in data["Text"]["head"]:
        #        text += r

            
                
        text =text.replace("—","-")
        #text =text.replace("-"," ")
        #text = re.sub(r'[^\w\s]','',self.text)

        text =text.replace(" US "," UNITED STATES ")

        puncs = '!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~'

        text = text.translate(str.maketrans('', '', puncs))

        text = text.upper()

        self.text = text
        self.num_words = len(text.split())


    def remove_stopword(self):
        
        self.words_list = [x for x in self.text.split() if x not in data_process.stopwords]
        self.num_cleanwords = len(self.words_list)
        return "removed stop words"

    def get_posscore(self):
        i = 0
        for r in self.words_list:
            if r in data_process.pos_words:
                i = i+1 
        self.posscore = i
        return i
    
    def get_negscore(self):
        i = 0
        for r in self.words_list:
            if r in data_process.neg_words:
                i = i+1
        self.negscore = i
        return i
    
    def get_polarityscore(self):
        return (self.posscore-self.negscore)/((self.posscore+self.negscore)+0.000001)
    
    def get_subjectivityscore(self):
        return (self.posscore+self.negscore)/(len(self.words_list)+0.000001)

    def get_numcomplexwords(self):
        i = 0
        for word in self.text.split():
            if self.__iscomplex(word):
                i=i+1
        self.num_complexwords = i
        return i
    
    def get_wordcount(self):
        return self.num_cleanwords
    
    def get_avgsentencelenght(self):
        return self.num_words/self.num_sentence

    def get_percomplexword(self):
        return (self.num_complexwords/self.num_words)*100 

    def get_avgsyllperword(self):
        return self.num_syllables/self.num_words

    def get_numperpro(self):
        per_pro = []
        per_pro.append(re.findall(" I ",self.text))
        per_pro.append(re.findall(" WE ",self.text))
        per_pro.append(re.findall(" MY ",self.text))
        per_pro.append(re.findall(" OURS",self.text))
        per_pro.append(re.findall(" US ",self.text))

        return len(per_pro)
    

    def get_avgwordlen(self):
        total_letters = 0
        for r in self.text.split():
            total_letters+=len(r)
        return total_letters/self.num_words

