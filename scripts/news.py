class News:
    header=""
    
    def setHeader(self,title):
        if type(title) is str:
            self.header=title
        else :
            raise Exception("Class News awaits a string") 

    def __init__(self,title):
        self.setHeader(title)

    def is_about_token(self,tokenName):
        #TODO clean tokenName further and header
        tmp=str.lower(self.header)
        string=str.lower(tokenName)
        if string in tmp:
            return True
        else:
            return False
    
    
class NewsBox:
    crypto=""
    list_news=[]
    def __init__(self,crypto):
        self.crypto=crypto

    def deliver_news(self,news):
        if news.is_about_token(self.crypto):
            self.list_news.append(news)
        return                            
        
    
    def consult(self):
        for i in self.list_news:
            print(i.header)
        return






