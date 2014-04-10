import nltk
from sklearn import svm

def scorer(tokens):
    emo_score=0
    word_cnt=0
    question_cnt=0
    exclam_cnt=0
    #tokens=nltk.word_tokenize(line)
    #print tokens #[:len(tokens)]
    for word in tokens:
        if(word.isalpha()):
            word_cnt+=1
            try:
                emo_score+=emo_dict[word.lower()]
            except:
                emo_dict[word.lower()]=0;
        elif(word=='!'):
            exclam_cnt+=1
        elif(word=='?'):
            question_cnt+=1
    #print line
    temp=[]
    temp=[emo_score,exclam_cnt,question_cnt,word_cnt]
    return(temp)

    

emo_dict={}
ipfile=open('emotion.txt')
rawstring=ipfile.read()
emotokens=nltk.word_tokenize(rawstring)
for word in emotokens:
    word=word.translate(None,'.')    
    if(word.isalpha()):
        try:
            emo_dict[word.lower()]+=1
        except:
            emo_dict[word.lower()]=1
ipfile.close()
ipfile=open('neutrality.txt')
rawstring=ipfile.read()
emotokens=nltk.word_tokenize(rawstring)
for word in emotokens:
    word=word.translate(None,'.')
    if(word.isalpha()):
        try:
            emo_dict[word.lower()]-=1
        except:
            emo_dict[word.lower()]=-1
ipfile.close()


trainData=[]
trainClass=[]
ipfile=open('emotion.txt')
for line in ipfile:
    tokens=nltk.word_tokenize(line)
    temp=scorer(tokens)
    trainData.append(temp)
    trainClass.append(1)
ipfile.close()
ipfile=open('neutrality.txt')
for line in ipfile:
    tokens=nltk.word_tokenize(line)
    temp=scorer(tokens)
    trainData.append(temp)
    trainClass.append(-1)
    #print emo_score,exclam_cnt,question_cnt,word_cnt
ipfile.close()

classifier=svm.SVC(kernel='linear')
#print classifier
classifier.fit(trainData,trainClass)

print classifier.n_support_

sentence='Trash'
while(1):
    sentence=raw_input('Sentence: ')
    if(sentence=='Done'):
        break
    tokens=nltk.word_tokenize(sentence)
    question=scorer(tokens)
    ans=classifier.predict(question)
    int_ans=ans[0]
    for word in tokens:
        if(word.isalpha()):
            emo_dict[word.lower()]+=int_ans
    if(int_ans>0):
        print 'Emotional'
    else:
        print 'Neutral'
