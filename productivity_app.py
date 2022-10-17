import datetime

from flask import Flask, render_template, request, redirect, url_for, flash,json
import pandas as pd
import os
app = Flask(__name__ )
BASE="http://52.23.240.197:8080"
@app.route("/logs",methods=["GET"])
def logs():
    df=pd.read_csv("activity_logs.csv", index_col=0).sort_values(by="Datetime", ascending=False)
    lst=[]
    for dt,act in zip(df["Datetime"],df["Activity"]):
       lst.append({"dt":dt,"act":act})
    return render_template("logs.html",lst=lst,BASE=BASE)
@app.route("/save_log",methods=["POST"])
def save_logs():
    d1=[]
    df=pd.read_csv("activity_logs.csv",index_col=0)
    for i in range(len(df)):
        d2=[request.form[f"{i}d"],request.form[f"{i}"]]
        print(d2)
        d1.append(d2)
    dfn=pd.DataFrame(d1,columns=df.columns,index=[x for x in range(len(d1))])
    dfn.to_csv("activity_logs.csv")
    print(dfn)
    return ""

@app.route("/tasks",methods=["GET"])
def tasks():
    df=pd.read_csv("todo.csv", index_col=0).sort_values(by=["Done", "Date_Created"], ascending=[True, True])
    lst=[]
    for dt,task,done in zip(df["Date_Created"],df["Task"],df["Done"]):
       lst.append({"dt":dt,"task":task,"done":done})
    return render_template("tasks.html",lst=lst,BASE=BASE)
@app.route("/save_task",methods=["POST"])
def save_task():
    d1=[]
    df=pd.read_csv("todo.csv",index_col=0)
    for i in range(len(df)):
        print(request.form)
        try:
            if request.form[f"{i}c"]=="on":
                check="checked"
            else:
                check="zzz"
        except:
            check="zzz"
        d2=[request.form[f"{i}"],check,request.form[f"{i}d"]]
        print(d2)
        d1.append(d2)
    dfn=pd.DataFrame(d1,columns=df.columns,index=[x for x in range(len(d1))])
    dfn.to_csv("todo.csv")
    print(dfn)
    return ""
@app.route("/new_task",methods=["POST"])
def new_task():
    task=request.form["task"]
    df=pd.read_csv("todo.csv",index_col=0)
    pd.concat([df,pd.DataFrame([[task,"zzz",datetime.datetime.today().strftime("%Y-%m-%d %H:%M")]],columns=df.columns,index=[len(df)])]).to_csv("todo.csv")
    return redirect(f"{BASE}/tasks")
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
