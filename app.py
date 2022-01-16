from flask import Flask, render_template, jsonify, json, request, session,  redirect, url_for
from flask.helpers import flash
from flask.sessions import NullSession
from flaskext.mysql import MySQL
import pymysql
from pymysql.cursors import Cursor 
import sns_noti
import md5
from datetime import datetime
import threading
import content
from shutil import copyfile
import url_share_all


app = Flask(__name__)
app.secret_key = 'Harsh@1526'

mysql=MySQL()
#mysql_config....................................................................................................................................
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sanjivani'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)
#................................................................................................................................................
def sqlconnect():
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    conn.autocommit(True)
    
    return cursor

@app.route("/")
def home():
    cursor=sqlconnect()
    col= cursor.execute ("SELECT * FROM donations;")
    palletes=cursor.execute("SELECT * FROM portfolio;")
    success_stories=cursor.execute("SELECT * FROM success_stories;")
    portfolioTitle=[]
    badge=[]
    portfolioImage=[]
    title=[]
    fund=[]
    supporters=[]
    percent=[]
    urgency=[]
    taxBenifit=[]
    cardImage=[]
    successTitle=[]
    successContent=[]
    successImage=[]
    status=""
    for i in range(1,col+1):
        
        cursor.execute("SELECT * FROM donations WHERE id=%s",(i))
        account=cursor.fetchone()
        title.append(account['title'])
        fund.append(account['fund'])
        supporters.append(account['supporters'])
        percent.append(account['donation_percent'])
        urgency.append(account['urgency'])
        taxBenifit.append(account['tax_benifit'])
        cardImage.append(account['image'])

    for i in range(1,palletes+1):
        cursor.execute("SELECT * FROM portfolio WHERE id=%s",(i))
        account=cursor.fetchone()
        portfolioTitle.append(account['title'])
        badge.append(account['badge'])
        portfolioImage.append(account['image'])
    
    for i in range(1,success_stories+1):
        cursor.execute("SELECT * FROM success_stories WHERE id=%s",(i))
        account=cursor.fetchone()
        successTitle.append(account['title'])
        successContent.append(account['content'])
        successImage.append(account['image'])
   
    cards=content.content('static/CSS/images/donations/')
    
    if 'loggedin' in session:
        status='loggedin'
    else:
        status='loggedout'
    
    slides=content.content('static/CSS/images/carousel/')
    print(str(title))
    
    return render_template("sanjivani.html",slides=slides, cards=col , title=title ,cardImage=cardImage, fund=fund, supporters=supporters, percent=percent, urgency=urgency,tax_benifit=taxBenifit, portfolioTitle=portfolioTitle, portfolioImage=portfolioImage, badge=badge, palleteNo=palletes, successTitle=successTitle, successContent=successContent, successImage=successImage, successNumber=success_stories, userStatus=status)
  
        

@app.route("/donate", methods=['POST','GET'])
def donate():
    
         if request.method=='GET':
            donateID=request.values.get('donate')
            session['donateId']=donateID
            if 'loggedin' in session:
                 return render_template('donation.html', donateId=donateID)
            else:
                 return redirect('/owner')


   


      
    
    

@app.route("/owner")
def owner():
    if 'loggedin' in session:
        return redirect('/dashboard')
    else:

      return render_template('index.html')
    
    
@app.route("/share", methods=['POST'])
def share():
    if request.method=='POST':
        url=request.form['url']
        title=request.form['title']
        site=request.form['site']
        link=url_share_all.siteShare(url,title,site)
        return jsonify({"link":link})
    




@app.route("/login", methods=['POST'])
def login():
    msg=""
    
    cursor=sqlconnect()
    if request.method == 'POST' and 'phone' in request.form and 'password' in request.form:
         # Create variables for easy access
         phone = request.form['phone']
         password = request.form['password']
         # Check if account exists using MySQL
         enc_pwd=md5.str2has(password)
         cursor.execute('SELECT * FROM users WHERE phone = %s AND password = %s', (phone, enc_pwd))
         # Fetch one record and return result
         account = cursor.fetchone()
   
         # If account exists in accounts table in out database
         if account:
            # Create session data, we can access this data in other routes
             print("exist")
             session['phone'] = account['phone']
             session['username']=account['username']
             print(account['is_active'])
             print(account['last_login'])
             otp="1234"
             session['otp']=otp;
             
             msg="otp"
            
             
         else:
              msg = '101 Incorrect username/password!'
              return jsonify({'msg':msg})
    else:
        msg="Some error"
        return jsonify({'msg':msg})
    return jsonify({"msg":msg})

@app.route("/auth", methods=['POST'])
def auth():
    otp_front=request.form['otp']
    msg=""
    phone=session['phone']
    otp_back=session['otp'];
    print("guess what?")
    if(otp_front==otp_back):
         session['loggedin'] = True
         print("all ok")
         session.pop('otp',None)
         print(session['username'])
         msg="loggedin"
         return jsonify({
         "msg":msg, 
         })
    else:
             # Account doesnt exist or username/password incorrect
        msg = 'Wrong OTP'
        return jsonify({'msg':msg})
    


@app.route("/dashboard", methods=['GET'])
def dashboard():
    if 'loggedin' in session:
        cursor=sqlconnect()
        cursor.execute('UPDATE users SET is_active = %s WHERE users.username = %s',(int(1),session['username']))
        cursor.execute('SELECT * FROM users WHERE username = %s ', (session['username']))
        account = cursor.fetchone()
        session['id'] = account['id']
        session['name']=account['first_name']
        session['email']=account['email']
        session['is_active']=account['is_active']
        session['privellage']=account['privellage']
        print(account['is_active']);
        last_login=account['last_login']
        print(last_login)
        now=datetime.now()
        session['last_login']=now.strftime("%Y-%m-%d %H:%M:%S")
        print(session['last_login'])
        date_joined=account['date_joined']
        if session['privellage']=='president':
            return render_template("home.html")
        elif session['privellage']=='doner':
            return redirect('/')

        
        
    else:
        return redirect("/owner")

    

@app.route("/logout", methods=['POST','GET']) 
def logout():
    if(request.method=='POST' and 'info' in request.form):

     if(request.form['info']=="logout"):
       
       cursor=sqlconnect()
       cursor.execute('UPDATE users SET is_active = %s WHERE users.username = %s',(int(0),session['username']))
       cursor.execute('UPDATE users SET last_login=%s WHERE users.username = %s',(session['last_login'],session['username']))

       session.pop('loggedin', None)
       session.pop('id', None)
       session.pop('username', None)
       session.pop('is_active',None)
       session.pop('email',None)
       session.pop('phone',None)
       return jsonify({"msg":"loggedout"})
     elif(request.form['info']=="timeout"):
       cursor=sqlconnect()
       cursor.execute('UPDATE users SET is_active = %s WHERE users.username = %s',(int(0),session['username']))
       cursor.execute('UPDATE users SET last_login=%s WHERE users.username = %s',(session['last_login'],session['username']))
       return jsonify({"status":"offline"})
         
     else:
        return jsonify({"msg","some error"})
    else:
        return redirect("/dashboard")


    
if __name__ == "__main__":
    app.run(debug=True)