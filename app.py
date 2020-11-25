from flask import Flask
from flask import render_template
from flask import jsonify
from jieba.analyse import extract_tags
import utils
import string
# import mysql.connector

#导入数据库模块
import pymysql

#导入前台请求的request模块
from flask import request   

import traceback 
app = Flask(__name__)

from flask import flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import config


#数据库配置
app.config.from_object(config)
app.config["SECRET_KEY"] = "12345678"
db = SQLAlchemy(app)
 
class LoginUsers(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    regName = db.Column(db.String(100))
    pwd = db.Column(db.String(200))
    pwdRepeat = db.Column(db.String(200))
    email = db.Column(db.String(200))
 
    def __init__(self, regName, pwd, pwdRepeat, email):
        self.regName = regName
        self.pwd = pwd
        self.pwdRepeat = pwdRepeat
        self.email = email
 
@app.route('/',methods=['GET','POST'])
def login_test():
    if request.method == 'POST':
        regName = request.form['regName']
        pwd = request.form['pwd']
        loginUser = LoginUsers.query.filter_by(regName=regName).first()
        if not regName or not pwd:
            flash('输入信息不全，请重新输入', 'warning')
        elif not loginUser:
            flash('用户不存在，请重新输入', 'warning')
        else:
            if loginUser.pwd != pwd:
                flash('密码错误，请重新输入', 'warning')
            else:
                flash('登录成功！！')
                return redirect(url_for('login_success'))
    return render_template('login_test.html', users=LoginUsers.query.all())
 
@app.route('/zhuce/', methods=['GET', 'POST'])

def zhuce():
    if request.method == 'POST':
        regName = request.form['regName']
        pwd = request.form['pwd']
        pwdRepeat = request.form['pwdRepeat']
        email = request.form['email']
        loginUser = LoginUsers.query.filter_by(regName=regName).first()
        if not regName or not pwd or not pwdRepeat or not email:
            flash('信息输入不全，请重新输入', 'warning')
        elif loginUser:
            flash('用户已经存在，请重新输入', 'warning')
        else:
            user = LoginUsers(regName, pwd, pwdRepeat, email)
 
            db.session.add(user)
            db.session.commit()
            flash('用户添加成功')
            return redirect(url_for('login_test'))
    return render_template('zhuce.html')
 
@app.route('/login_success/',methods=['GET','POST'])
def login_success():
    return render_template('main.html')
    
# db.create_all()   
    
@app.route('/main')
def hello_world():
    return render_template('main.html')

@app.route('/c1')
def get_c1_data():
	data = utils.get_c1_data()
	return jsonify({"confirm":data[0],"suspect":data[1],"heal":data[2],"dead":data[3]})

@app.route('/c2')
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})


@app.route("/l1")
def get_l1_data():
    data = utils.get_l1_data()
    day,confirm,suspect,heal,dead = [],[],[],[],[]
    for a,b,c,d,e in data[7:]:    #很多卫健委网站前7天都是没有数据的，所以把前7天砍掉了
        day.append(a.strftime("%m-%d")) #a是datatime类型
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day":day,"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})

@app.route("/l2")
def get_l2_data():
    data = utils.get_l2_data()
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data[7:]:
        day.append(a.strftime("%m-%d"))  # a是datatime类型
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})


@app.route("/r1")
def get_r1_data():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k,v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})


@app.route("/r2")
def get_r2_data():
    data = utils.get_r2_data() #格式 (('民警抗疫一线奋战16天牺牲1037364',), ('四川再派两批医疗队1537382',)
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)  # 移除热搜数字
        v = i[0][len(k):]  # 获取热搜数字
        ks = extract_tags(k)  # 使用jieba 提取关键字
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})
    return jsonify({"kws": d})


@app.route('/time')
def gettime():
	return utils.get_time()


@app.route('/tem')
def hello_world3():
    return render_template("index.html")

@app.route('/ajax', methods=["get","post"])
def hello_world4():
    return '10000'

if __name__ == '__main__':
    app.run(debug=True)
