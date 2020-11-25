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

class Brand(db.Model):
    __tablename__ = "brand"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


class Moto(db.Model):
    __tablename__ = "moto"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    g_id = db.Column(db.Integer, db.ForeignKey(Brand.id))


@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        t = Moto.query.filter(Moto.email == email and Moto.password == password).first()
        if t:
            return redirect('home')
        else:
            return "不好意思！您输入的邮箱或密码有误请重新输入" \
                   "Sorry! The email or password you entered is incorrect, please re-enter"




@app.route("/home")
def home():
    b = Brand.query.all()
    m= Moto.query.all()
    return render_template("home.html", b=b, m=m)


@app.route("/delete/<id>")
def delete(id):
    de = Moto.query.filter(Moto.id == id).first()
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
        email = request.form.get("email")
        password = request.form.get("password")
        n_s = Moto(name=name, age=age, g_id=g_id, email=email, password=password)
        db.session.add(n_s)
        db.session.commit()
        return redirect("/home")



if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    u1 = Brand(name="KTM")
    u2 = Brand(name="Honda")
    u3 = Brand(name="Ducati")
    db.session.add_all([u1, u2, u3])
    db.session.commit()
    m1 = Moto(name="小曾", age="19",email="320654560@qq.com", password="123456", g_id=1)
    m2 = Moto(name="张傻傻", age="20",email="192201394@163.com", password="123456", g_id=1)
    m3 = Moto(name="袁嬷嬷", age="19",email="192201395@163.com", password="123456", g_id=2)
    m4 = Moto(name="马憨憨", age="19",email="192201396@163.com", password="123456", g_id=2)
    m5 = Moto(name="杨呆呆", age="19",email="192201397@163.com", password="123456", g_id=3)
    m6 = Moto(name="薛笨笨", age="19",email="192201398@163.com", password="123456", g_id=3)
    db.session.add_all([m1, m2, m3, m4, m5, m6])
    db.session.commit()

    app.run(debug=True, port=8800)