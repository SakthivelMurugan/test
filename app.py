from flask import Flask, render_template, redirect, url_for,request
import sqlite3 as sql
import json

app=Flask(__name__)

@app.route("/",methods=["POST","GET"])
def Add():
    if request.method=="POST":
        category=request.form.get("category")
        price=request.form.get("price")
        name=request.form.get("name")
        weight=request.form.get("weight")

        conn=sql.connect("datas.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("insert into products (category,price,name,weight) values (?,?,?,?)",(category,price,name,weight))
        conn.commit()

        return render_template("form.html")
    return render_template("form.html")

@app.route("/template")
def Template():
    conn=sql.connect("datas.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("select category,name from products")
    data=cur.fetchall()
    l=[]
    for i in data:
        if i["category"] not in l:
            l.append(i["category"])
    
    conn=sql.connect("datas.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("select * from category")
    n=cur.fetchall()

    return render_template("template.html",category=l,data=n)

@app.route("/product",methods=["post"])
def fun():
    data = request.get_json()
    data=data.get("data")
    conn=sql.connect("datas.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("select name from products where category=?",(data,))
    data=cur.fetchall()

    cur.execute("delete from category")
    conn.commit()

    for i in data:
        d=i["name"]
        conn=sql.connect("datas.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("insert into category (name) values(?)",(d,))
        conn.commit()

    return redirect(url_for("Template"))




if __name__=="__main__":
    app.run(debug=True)