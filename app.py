# -- * -- coding : utf-8 -- * --
# @Author	    	:	Xue_Yuan_jie
# @Project	    	:	kaoshi32
# @File		    	:	app.py
# @Time		    	:	2020/11/01 8:27
# @Contact	    	:	192201393@qq.com
# @License	    	:	(C) Copyright 2019-2020
# @Software(IDE)	:	PyCharm
# @Site		    	:	https://www.jetbrains.com/pycharm/
# @Version	    	:	Python 3.8.0
from flask import Flask, request, render_template, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import config
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

class GG(db.Model):
    __tablename__ = "gg"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.String(64))
    g_id = db.Column(db.Integer, db.ForeignKey(GG.id))


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/home")
def home():
    g_all = GG.query.all()
    s_all = Student.query.all()
    return render_template("home.html", g_all=g_all, s_all=s_all)


@app.route("/delete/<id>")
def delete(id):
    de = Student.query.filter(Student.id == id).first()
    db.session.delete(de)
    db.session.commit()
    return redirect("/home")


@app.route("/new", methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template("new.html")
    else:
        g_id = request.form.get("g_id")
        name = request.form.get("name")
        age = request.form.get("age")
        n_s = Student(name=name, age=age, g_id=g_id)
        db.session.add(n_s)
        db.session.commit()
        return redirect("/home")


@app.route("/update/<id>", methods=['GET', 'POST'])
def update(id):
    sz = Student.query.filter(Student.id == id).first()
    if request.method == 'GET':
        return render_template("update.html")
    else:
        sz.name = "笨笨"
        sz.age = "99"
        sz.g_id = 3
        db.session.commit()
        return redirect("/home")




if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    g1 = GG(name="大数据一班")
    g2 = GG(name="大数据二班")
    g3 = GG(name="大数据三班")
    db.session.add_all([g1, g2, g3])
    db.session.commit()
    s1 = Student(name="杨呆呆", age="20", g_id=1)
    s2 = Student(name="张傻傻", age="20", g_id=1)
    s3 = Student(name="袁嬷嬷", age="19", g_id=2)
    s4 = Student(name="马憨憨", age="19", g_id=2)
    s5 = Student(name="王笨笨", age="19", g_id=3)
    s6 = Student(name="薛笨笨", age="19", g_id=3)
    db.session.add_all([s1, s2, s3, s4, s5, s6])
    db.session.commit()

    app.run(debug=True, port=8800)