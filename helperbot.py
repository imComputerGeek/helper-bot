
# Description : Entry point for Simple Question Answer Chatbot
# HelperBot
# A project by Gautam aka imComputerGeek 

# use it. ;)



##############################################################################################################################
#specific modules needed for working
#
#
try:
    print("Helper> Please wait, while I am loading my dependencies")
    
    import re
    import random
    from bs4 import BeautifulSoup
    import urllib                #new line
    import requests
    from googlesearch import search #"pip3 install git+https://github.com/abenassi/Google-Search-API" #"pip3 install google"

    from DocumentRetrievalModel import DocumentRetrievalModel as DRM
    from ProcessedQuestion import ProcessedQuestion as PQ
    from nltk.corpus import wordnet,stopwords
except:
    print("couldn't load dependecies... please install nltk, regex,beautifulsoup4,requests, google(pip3 install google)")
    exit(1)


# for getting keywords from userQuery
def buildSearchQuery(question):
    qt = question.split()
    searchQuery = []
    for word in qt:
        if word not in stopwords.words('english'):
            searchQuery.append(word)
    return searchQuery



########################################################################################################################################################

# For getting and filtering the texts from the webpages and returning noise free texts

class Get_txt:
    def get(self,urls):
        article_text=''
        try:
            for url in urls:
                try:
                    #print(url)
                    html = requests.get(url).content
                    #1 Recoding
                    unicode_str = html.decode("utf8")
                    encoded_str = unicode_str.encode("ascii",'ignore')
                    news_soup = BeautifulSoup(encoded_str, "html.parser")
                    a_text = news_soup.find_all('p')
                    #2 Removing
                    #y=[re.sub(r'<.+?>',r'',str(a)) for a in a_text]
                    #text=str(y).replace("\\'s","'s")

            
            
                    # break into lines and remove leading and trailing space on each
                    lines = (line.strip() for line in str(a_text).splitlines())
            
                    # break multi-headlines into a line each
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            
                    # drop blank lines
                    text = '\n'.join(chunk for chunk in chunks if chunk)

                    # removing the special characters
                    #text_clr = re.sub(r"()#/@;\":{}`+!?=~|", "",str(a_text))
                    clear_txt=re.sub(r'<.+?>',r'',str(a_text))

                    #
                    clear_txt = re.sub(r'\[([^\[\]]*)\]','',str(clear_txt))
                    clear_txt=clear_txt.replace("[","").replace("]","")
                    clear_txt=clear_txt.replace("\'t","'t").replace("\'re","'re").replace("\'d","'d").replace("\'nt","'nt").replace("(","").replace(")"," ").replace("II","2").replace("III","3").replace("IV","4").replace("V","5").replace("VI","6").replace("VII","7").replace("VIII","8").replace("IX","9").replace("X","10").replace("XI","11").replace("XII","12").replace("XIII","13").replace("XIV","14").replace("XV","15").replace("XVI","16").replace("XVII","17").replace("XVIII","18").replace("XIX","19").replace("XX","20")
                    #print(clear_txt)
                
                    article_text = article_text + clear_txt
                    #print(article_text)
                except:
                    #return None
                    article_text += ''
                
        except:
            return "oops! something bad happened"
        return article_text


##########################################################################################################################################
# For getting the search urls from 
# class has many functionality like blocking website
# and blocking websites from more than one time in a single search
class Srch:
    def searc(self,srch):
        urls=[]
        self.srch=srch
        #print(self.srch)
        #srch=str(input('>'))
        blocked_websites=('twitter.com','auto.ndtv.com','www.google.com','www.amazon.in','music.youtube.com','www.facebook.com','www.youtube.com','studio.youtube.com','www.carwale.com','www.amazon.com','www.facebook.com','www.facebook.in','www.gmail.com','www.instagram.com')
        prevUrl=None
        urlList=[]
        try:
            urlList=search(self.srch,tld="co.in", num=9, stop=9, pause=3)
        except:
            return urls
        
        try:
            #for result in search(self.srch,tld="co.in", num=9, stop=9, pause=1):
            for result in urlList:
                if result.split("://")[1].split("/")[0] in blocked_websites:
                    #print('blocked website',result.split("://")[1].split("/")[0])
                    result=None
                    continue
                else:
                    if prevUrl==result.split("://")[1].split("/")[0]:
                        continue
                    else:
                        urls.append(result)
                        prevUrl=result.split("://")[1].split("/")[0]
            prevUrl=None

            return urls
        except:
            return urls



########################################################################################################################






########################################################################################################################
# before starting
#
#
print("Helper> Hey! I am ready. Ask me Factual questions only :P")
print("Helper> You can say me 'Bye' anytime you want")
print("Helper> if you aren't satisfied with answer then ask differently or ask in detail...")

# Greet Pattern
greetPattern = re.compile("^\ *((hi+)|((good\ )?morning|evening|afternoon)|(he((llo)|y+)))\ *$",re.IGNORECASE)


a=Srch()
#x=a.searc()
b=Get_txt()
#text=b.get(x)



#############################################################################################################################
#
#
#        Main loop starting point
#

isActive = True
while isActive:
    userQuery = input("You> ")
    if(not len(userQuery)>0):
        print("Helper> You need to ask something")
    elif greetPattern.findall(userQuery):
        response = "Hello!"
    elif userQuery.strip().lower() in ("bye","good bye","goodbye","exit","goodbye!","ok bye","ok bye!"):
        response = "Bye Bye!"
        isActive = False
    elif userQuery.strip().lower() in ('who build you?','who build you','who built you','who made you','who made you','who built this chatbot','who built this helper','who are you','who are you?'):
        response = "Gautam kumar aka. imComputerGeek... A guy with beautiful mind! :)"
        
    else:
        # searching user input on internet
        x=a.searc(userQuery)
        # Extracting texts from url
        text=b.get(x)
        # Retrieving paragraphs : Assumption is that each paragraph in dataset is
        # separated by new line character
        paragraphs = []
        
        for para in text.splitlines():
            if(len(para.strip()) > 0):
                paragraphs.append(para.strip("\n"))

        #print(paragraphs)

        # Processing Paragraphs
        drm = DRM(paragraphs,True,True)
        
        # Proocess Question
        pq = PQ(userQuery,True,False,True)
        # Get Response From Bot
        
        response =drm.query(pq)
        #print(response)
        bs=''

        ran=random.randrange(4,6)
        
        # For generating random length of answer
        for r in range(0,ran):
            try:
                bs = str(bs)+str(response[r])
            except:
                break
        
        response = bs
        #print("ans from here")

        # cleaning up some variables
        x=None
        text=None
        paragraphs.clear()
    if response!=None:
        print("Helper>",response)

    # cleaning response was necessary otherwise if you don't ask question then it will give last query's answer
    response = None

#####################################################################################################################
