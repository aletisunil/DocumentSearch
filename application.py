import re
import nltk
from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
from flask import Flask, render_template, request
application = Flask(__name__)
nltk.download('punkt')
snow_stemmer = SnowballStemmer(language='english')

@application.route("/")
def home():
    return render_template("home.html")

@application.route("/addnewfile")
def addnewfile():
    return render_template("addnewfile.html")

@application.route("/search")
def search():
    return render_template("search.html")


@application.route("/addnew",methods=['GET', 'POST'])
def addnew():
    FileName = request.form['filename']
    FileContent=request.form['filecontent']
    if(FileName.strip()!="" and FileContent.strip()!=""):
        name="files/"+FileName+".txt"
        fw =open(name,"w+")
        fw.write(FileContent)
        fw.close()
        f = open("files/filelist.txt", "a")
        f.write(FileName+".txt\n")
        f.close()
        msg="File Added Successfully"
        return render_template("addnewfile.html",msg=msg)

@application.route("/searchquery",methods=['GET','POST'])
def searchquery():
    result=[]
    query=request.form['query']
    query=query.strip()
    query=snow_stemmer.stem(query)
    stop_wordsLocation="english.txt"
    with open(stop_wordsLocation,'r') as f1:
        stop_words=f1.readlines()
        stop_words= [i.strip() for i in stop_words]
    with open("files/filelist.txt",'r') as f3:
        flist=f3.readlines()
        for i in flist:
            file="files/"+i.strip()
            with open(file, 'r') as f:
                book1 = f.readlines()
                for i in range(len(book1)):
                    book1[i]=book1[i].strip()
                    book1[i] = re.sub(r"http\S+", "", book1[i])
                    soup = BeautifulSoup(book1[i], 'lxml')
                    book1[i] = soup.get_text()
                    book1[i]=re.sub('[^A-Za-z]+', ' ', book1[i])
                    book1[i] = re.sub(r"\'t", "will not", book1[i])
                    book1[i] = re.sub(r"\'re", " are", book1[i])
                    book1[i] = re.sub(r"\'s", " is", book1[i])
                    book1[i] = re.sub(r"\'d", " would", book1[i])
                    book1[i] = re.sub(r"\'ll", " will", book1[i])
                    book1[i] = re.sub(r"\'ve", " have", book1[i])
                    book1[i] = re.sub(r"\'m", " am", book1[i])
                    word_tokens = nltk.word_tokenize(book1[i])
                    word_tokens=[i.lower() for i in word_tokens]
                    stemm=[snow_stemmer.stem(i) for i in word_tokens]
                    temp=[]
                    for w in stemm:
                        if w not in stop_words:
                            temp.append(w)
                    book1[i]=temp

                with open(file, 'r') as f2:
                    book2 = f2.readlines()
                __=[]
                outRes=[]
                outRes.append(file)
                for _,line in enumerate(book1):
                    for i in line:
                        for j in query.split(" "):
                            if i==j and _ not in __:
                                __.append(_)
                                outRes.append(book2[_])
                                #print(book2[_])
                if len(outRes)>1:
                    result.append(outRes)
                
                
        print(result)
        print(snow_stemmer.stem("rounded"))
        return render_template("search.html",out=result)

                    
                    


if __name__ == '__main__':
    application.run(debug = True)
