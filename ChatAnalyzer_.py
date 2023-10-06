#!/usr/bin/env python
# coding: utf-8

# In[1]:


def convert_chat(data,type_="one-on-one"):
    import warnings
    warnings.filterwarnings('ignore')
    lists=[]
    import regex as re
    import datetime
    import numpy as np
    import pandas as pd
    new_df=data
    new_df.columns=['chats']
    pattern1='\[\d{1,2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2} PM\]|\[\d{1,2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2} AM\]'
    new_df['dates']=new_df.chats.apply(lambda x:re.findall(pattern1,x))
    for i in range(len(new_df)):
        if re.search('\]',new_df.chats.loc[i]):
        
            n=re.split('\]',new_df.chats.loc[i])
            m=re.split(':',n[1])[0]
            lists.append(m)
        else:
            lists.append(np.nan)
    new_df['Sender']=lists 
    new_dff=new_df.dropna(subset=["Sender"])
    arr=new_dff.Sender.unique()
    
    for i in arr:
        if len(i)>0:
            try:
                new_dff['chats']=new_dff.chats.apply(lambda x:re.sub(i+":","",x))
            except:
                continue
    new_dff=new_dff.iloc[1:,:]
    new_dff['chats']=new_dff.chats.apply(lambda x:re.sub(pattern1,'',x))
    new_dff['dates']=new_dff.dates.apply(lambda x:re.sub('\[|\]','',str(x)))
    new_dff['time']=new_dff.dates.apply(lambda x:re.findall('\d{1,2}:\d{2}:\d{2} AM|\d{1,2}:\d{2}:\d{2} PM',x))
    new_dff['dates']=new_dff.dates.apply(lambda x:re.split(',',x)[0])
    new_dff['time']=new_dff.time.apply(lambda x:re.sub('\[|\]','',str(x)))
    new_dff['time']=new_dff.time.replace("'",'',regex=True)
    new_dff['dates']=new_dff.dates.replace("'",'',regex=True)
    
    def g(x):
        try:
        
            time=datetime.datetime.strptime(x,'%I:%M:%S %p')
            hour=int(time.strftime('%I'))
            if time.strftime("%p")=="AM":
                if hour==12 or hour<5:
                    bin='Mid-Night'
                elif 5<=hour<12:
                    bin='Morning'
            if time.strftime("%p")=='PM':
                if hour==12 or hour<5:
                    bin='Noon'
                elif 5<=hour<8:
                    bin='Evening'
                elif hour>=8:
                    bin="Night"
            return bin
        except:
            return np.nan
    new_dff['Times of Day']=new_dff.time.apply(g)
    def f(x):
        try:
            time=datetime.datetime.strptime(x,'%d/%m/%y')
            return time.strftime('%Y')
        except:
            return np.nan
    new_dff['Year']=new_dff.dates.apply(f)
    
    def day(x):
        try:
            time=datetime.datetime.strptime(x,'%d/%m/%y')
            return time.strftime('%A')
        except:
            return np.nan
    new_dff['Days']=new_dff.dates.apply(day)
    def month(x):
        try:
            time=datetime.datetime.strptime(x,'%d/%m/%y')
            return time.strftime('%m')
        except:
            return np.nan
    new_dff['month']=new_dff.dates.apply(month)
    new_dff.dropna(inplace=True)
    new_dff['dates']=pd.to_datetime(new_dff['dates'],dayfirst=True)
    
    if type_=="group":
    
    
        return new_dff
    if type_=="one-on-one":
        array=new_dff.Sender.value_counts().index[:2]
        new_dff=new_dff[(new_dff.Sender==array[0])|(new_dff.Sender==array[1])]
        return new_dff
    
    
    
def Analyze_chat(dfff):
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib import style
    style.use("ggplot")
    
    
    print("THERE ARE TOTAL ",len(dfff),"MESSAGES IN THE CHAT👌👌👌👌👌✌️🤞🤞🤞😉😉😉😉😉😉")
    
    
    msg_count=dfff['Sender'].value_counts()
    plt.pie(msg_count,labels=msg_count.index,autopct='%2.2f%%',shadow='True',)
    plt.title("Total Messages By Individual",color='grey')

    plt.show()
    print("LETS SEE THE MOST ACTIVE USER IN THE CHAT 😎 BY COUNTING MMESSAGES OF INDIVIDUAL")
    
    print("COUNTS OF MESSAGES BY INDIVIDUAL ARE :-")
    print("\n")
    
    print(msg_count)
    
    for i in range(2):
        print("\n")
    
    N=(dfff["chats"]=='\u200e \u200esticker omitted').sum()
    print("TOTAL NUMBER OF STICKERS SENT IN CHAT ARE :",N)
    m=(dfff['chats']==' \u200eThis message was deleted.').sum()
    print("TOTAL NUMBER OF DELETED MESSAGES ARE      :",m)
    print("\n")
    
    print("Lets see who deleted how much messages   😒😒😒😒😒😒😒😒😒😒😒😒😒")
    zi=dfff[dfff["chats"]=='\u200e \u200esticker omitted'].groupby("Sender").count()
    plt.pie(zi['chats'],labels=zi.index,autopct='%2.2f%%',shadow=True)
    plt.title("Messages deleted by Individuals")
    plt.show()
    print("******************************************************************************************")
    print("🤞🤞😁💕💕💕💕💕💕💕💕😊😊😊😊😉😝😝😫😫😫😫😆😆😁😁😁😂😃😃😃😎😎😎😎😎😎😙😙")
    print("Wanna see chat active time ?????????")
    print("\n")
    print("Lets check conversation trends 📈📈📈📈📈📈📈📉📉📉📉📉📈📈")
    

    
    count_by_dates=dfff[['dates','chats']].groupby(['dates']).count()
    plt.figure(figsize=(10,5))
    plt.plot(count_by_dates['chats'],label='count of msgs',marker='o',color='r',markersize=1
         ,markerfacecolor='g',markeredgecolor='black',linewidth=3)
    plt.legend()
    plt.xlabel('Dates',size=15)
    plt.ylabel('count of messages',size=12)
    plt.title('Conversation trends')
    plt.xticks(rotation=90)
    plt.show()
    n=count_by_dates.sort_values(by ='chats',ascending=False)
    print("Dates with Maximum Conversations")
    print(n.head(10))
    count_by_month=dfff[['month','Year','chats']].groupby(['month','Year'],as_index=False).count()
    plt.title("Conversation Trends monthly in Different Years")
    sns.barplot(x='month',y='chats',hue='Year',data=count_by_month)
    plt.show()
    count_by_days=dfff[['Days','chats']].groupby('Days',as_index=False).count()
    plt.title("Most Busy Days of Week",color="Green",fontfamily='sans-serif')
    sns.barplot(x='chats',y='Days',data=count_by_days)
    plt.show()
    
    count_by_time=dfff.groupby("Times of Day").count()
    plt.bar(count_by_time.index,count_by_time["chats"])
    plt.ylabel("messages count")
    plt.title("Most busy times of Day")
    plt.show()
    print("******************************************************************************************************")
    print("\n")
    print("Finally!!!🤩","Its times for emojis")
    print("😃😃😃😭😭😭😭😃😃😃😭😭😭😭😘😘😘🥰🥰🥰🥰😉😉😘😘😍😍😅😆😂🙄😊😊🙂☺️🥰🥰😆😀😄😍😍🥲😚🤔😶‍🌫️😘😘😘🥰🥰🥰🥰😉😉😘😘😍😍😅😆😂🙄😊😊🙂☺️🥰🥰😆😀😄😍😍🥲😚🤔😶‍🌫️😮🫥😶🤗🥰😘😚🤔😶‍🌫️🤔🤔\n🤩😑😏😯😯🤐😶‍🌫️🤩🫥😥😣😪😪🙄😶‍🌫️🫥😶😮😴😒🥱😫😪😛🤐🫥😮😴😝😜😪😯😯🤐😶‍🌫️🫡😶‍🌫️🙄😶‍🌫️🤐😞😟😞😧😰🤪😡🤢🤕🥴😱😨😧")
    
    
    import regex as re
    def count(x,data=dfff):
        sum=0
        for i in range(len(data)):
            n=re.findall(x,data.chats.iloc[i])
            sum+=len(n)
        return sum
    emojis=['😅','🤣','😂','🥹','😇','👀','😒','🙂','😡','🤬','😖','😕','🙁','😢','😭','😖','😟','😔','😕','☹','😎','😌','😘',
            '😉','😍','😁','☺','😊','❤️','🙄']
    count_emojis=[count(i) for i in emojis]
    
    sns.barplot(x=emojis,y=count_emojis)
    plt.xlabel("Emojis",size=15)
    plt.ylabel('Total Emoji use',size=15)
    plt.title('Analyzing Emojis😍😂',size=20,family='cursive',color='lightcoral')
    plt.show()
    print('count of Emojis are  : ')
    z=pd.DataFrame(emojis,count_emojis).sort_index(ascending=False)
    print(z[0])
    
    print("*********************************************************************************************")
    print("\n")
    print("LetS seE wHo is MorE expREssive in The wHOle Chats by couNTINg inDividuaLS emOjis 🤫🤭")
    print("\n")
    for i in dfff["Sender"].unique():
        emots=[count(j,dfff[dfff["Sender"]==i]) for j in emojis]
        print("Number of EmoJis SenT bY ",i,"In cHats are ",sum(emots))
    
    
    
    print("***********************************************************************************************")
    print("\n")
    print("we have seen EMojis ,Now lets cheCk frequently USed words in Chats........................")
    from sklearn.feature_extraction.text import CountVectorizer as CV
    cv=CV(max_features=50)
    vectors=cv.fit_transform(dfff['chats']).toarray()
    most_used_words=cv.get_feature_names_out()
    
    try:
        from PIL import Image
        from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
        text = str(most_used_words)


        wordcloud = WordCloud().generate(text)


        plt.figure(figsize=(10,10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title('Most Used Words in Conversation',fontfamily='Comic Sans MS',color='green',size=30)
        plt.show()
    except:
        print("try installing 'wordcloud' package to get wordcloud plot")
    count_of_words=pd.DataFrame(vectors,columns=most_used_words)
    print('Counts of Words are: \n')
    print(count_of_words.sum().sort_values(ascending=False))
    print("***********************************************************************************************")
    
    print("itSS aLL about the Chat.Waiting for YoUR more cHATs")
    print("*************************************************************************************The End")
    

