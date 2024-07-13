from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
#from sklearn.metrics import accuracy_scorepy
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
 
# Create your views here.

def index(req):
    return render(req,'index.html')

def about(req):
    return render(req,'about.html')


def login(req):
    if req.method == 'POST':
        uemail = req.POST['uemail']
        upass = req.POST['passw']
        user = User.objects.filter(email = uemail,password =upass ).exists()
        if user:
            return render(req,'userhome.html')
    return render(req,'login.html')

def register(req):
    if req.method == 'POST':
        uname = req.POST['uname']
        uemail = req.POST['uemail']
        upass = req.POST['passw']
        cpass = req.POST['cpassw']
        num =  req.POST['num']
        if upass == cpass:
            User.objects.create(username = uname, email = uemail, password = upass, first_name = num)
            return render(req,'login.html')
    return render(req,'register.html')


def userhome(req):
    return render(req,'userhome.html')


def view(req):
    global df
    df = pd.read_csv('updated_eye_health_data.csv')
    data = df.to_html()
    return render(req,'view.html',{'data':data})


def module(req):
    try:
        global df,x_train, x_test, y_train, y_test
        # Split The Data in Train and Test
        x = df.drop('Anemia Status',axis=1)
        y = df['Anemia Status']
        sm  = SMOTE()
        a,b = sm.fit_resample(x,y)
        x_train, x_test, y_train, y_test = train_test_split(a, b, test_size = 0.3, random_state= 72)
        if req.method == 'POST':
            model = req.POST['algo']
            print("_______________________________")
            print(model)
            if model  == "0":
                msg = 'Please select Algorithem......'
                return render(req,'module.html',{'msg':msg})
            elif model == "1":
                de = DecisionTreeClassifier()
                de.fit(x_train,y_train)
                de_pred = de.predict(x_test)
                de_ac = accuracy_score(y_test,de_pred)
                msg = "The Accuracy score of DecisionTreeClassifier"+" "+str(de_ac)
                return render(req,'module.html',{'msg':msg})
            elif model == "2":
                ra = RandomForestClassifier()
                ra.fit(x_train,y_train)
                ra_pred = ra.predict(x_test)
                ra_ac = accuracy_score(y_test,ra_pred)
                msg = "The Accuracy score of RandomForestClassifier"+" "+str(ra_ac)
                return render(req,'module.html',{'msg':msg})
            elif model == "3":
                nb = GaussianNB()
                nb.fit(x_train,y_train)
                nb_pred = nb.predict(x_test)
                nb_ac = accuracy_score(y_test,nb_pred)
                msg = "The Accuracy score of naive_bayes"+" "+str(nb_ac)
                return render(req,'module.html',{'msg':msg})
    except NameError:
        msg = "View The Data Once"
        return render(req,'view.html',{'msg':msg})
    return render(req,'module.html')



def pred(req):
    col = x_train.columns
    print(col)
    if req.method == 'POST':
        dic = req.POST.dict()
        print(dic)
        del dic['csrfmiddlewaretoken']
        
        inp = []
        for i in dic.keys():
            inp.append(float(dic[i]))
        print(inp)
        ra = RandomForestClassifier()
        ra.fit(x_train,y_train)
        Output = ra.predict([inp])
        print(Output)
        if Output == 1:
            msg = 'NO Anemia '
            return render(req,'pred.html',{'col':col[:10],'col1':col[10:19],'msg':msg})
        else:
            msg = 'Anemia'
            return render(req,'pred.html',{'col':col[:10],'col1':col[10:19],'msg':msg})
    return render(req,'pred.html',{'col':col[:10],'col1':col[10:19]})