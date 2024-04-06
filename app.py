from flask import Flask,flash,redirect,render_template,url_for,request,jsonify,session,abort
from flask_session import Session
from flask_mysqldb import MySQL
from datetime import date
from datetime import datetime
from sdmail import sendmail
from tokenreset import token
from itsdangerous import URLSafeTimedSerializer
from key import *
import time
app=Flask(__name__)
app.secret_key='hello'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']='admin'
app.config['MYSQL_DB']='insurance_operations'
mysql=MySQL(app)
#
Session(app)
@app.route('/')
def index():
    return render_template('index.html')
#=========================================login and register
@app.route('/clogin',methods=['GET','POST'])
def clogin():
    if session.get('customer'):
        return redirect(url_for('customer_dashboard'))
    if request.method=='POST':
        username=request.form['name']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT count(*) from CustomerRegistrations where name=%s and password=%s',[username,password])
        count=cursor.fetchone()[0]
        if count==1:
            session['customer']=username
            return redirect(url_for("customer_dashboard"))
        else:
            flash('Invalid username or password')
            return render_template('customer_login.html')
    return render_template('customer_login.html')

@app.route('/cregistration',methods=['GET','POST'])
def cregistration():
    if request.method=='POST':
        
        username = request.form['name']
        password=request.form['password']
        email=request.form['email']
        phnumber=request.form['phone']
        
        address=request.form['address']
        cursor=mysql.connection.cursor()
        cursor.execute('select cid from CustomerRegistrations where name=%s',[username])
        id1=cursor.fetchone()
        cursor.execute('select count(*) from CustomerRegistrations where cid=%s',[id1])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from CustomerRegistrations where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('customer_registration.html')
        elif count1==1:
            flash('Email already in use')
            return render_template('customer_registration.html')
            
        data={'customer_id':id1,'username':username,'email':email,'phone_number':phnumber,'address':address,'password':password}
        subject='Email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('cconfirm',token=token(data,salt),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('clogin'))
    

    return render_template('customer_registration.html')
@app.route('/cconfirm/<token>')
def cconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        cursor=mysql.connection.cursor()
        id1=data['customer_id']
        cursor.execute('select count(*) from CustomerRegistrations where cid=%s',[id1])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('clogin'))
        else:
            cursor.execute('INSERT INTO CustomerRegistrations (name,email, phone, address,password) VALUES (%s,%s, %s, %s, %s)',[data['username'], data['email'], data['phone_number'], data['address'],data['password']])

            mysql.connection.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('clogin'))
@app.route('/customer_dashboard')
def customer_dashboard():
    if session.get('customer'):
        return render_template('customer_dashboard.html')
    else:
        return redirect(url_for('clogin'))
@app.route('/clogout')
def clogout():
    if session.get('customer'):
        session.pop('customer')
        flash('Successfully logout')
        return redirect(url_for('clogin'))
    else:
        flash('Please login to continue')
        return redirect(url_for('clogin'))
import random
def genotp():
    u_c=[chr(i) for i in range(ord('A'),ord('Z')+1)]
    l_c=[chr(i) for i in range(ord('a'),ord('z')+1)]
    otp=''
    for i in range(3):
        otp+=random.choice(u_c)
        otp+=str(random.randint(0,9))
        otp+=random.choice(l_c)
    return otp
@app.route('/cusviewpolicie',methods=['GET','POST'])
def cusviewpolicie():
    if session.get('otp_sent')==True:
        session.pop('otp_sent')
    if session.get('customer'):
        otp_sent = session.get('otp_sent', False)
        if request.method=="POST":
            email=request.form['email']
            cursor=mysql.connection.cursor()
            cursor.execute('select count(*) from customerapplications where email=%s',[email])
            count=cursor.fetchone()[0]
            cursor.close()

            '''
            if count==1:
                flash('you can get an otp to the email')
                otp = genotp()
                subject = 'Otp to view the your policy'
                body = f'use this otp vie your policy profile {otp}'
                sendmail(email,subject,body) 
                return render_template('customerviewpolicie.html',otp=otp,email=email)
            else:
                flash('the entered email is not registered in policy application')
                return render_template('customerviewpolicie.html')
        return render_template('customerviewpolicie.html')'''
            if count == 1:
                session['otp_sent'] = True
                flash('An OTP has been sent to your email.')
                otp = genotp()
                subject = 'OTP to view your policy'
                body = f'Use this OTP to view your policy profile: {otp}'
                sendmail(email, subject, body)
                
                return redirect(url_for('otp', otp=otp, email=email,otp_sent=otp_sent))
            else:
                flash('The entered email is not registered in the policy application.')
                return render_template('customerviewpolicie.html')
    
        # Check if OTP has been sent to avoid resending on refresh
        return render_template('customerviewpolicie.html', otp_sent=otp_sent)
    return redirect(url_for('clogin'))
#=================otp
@app.route('/otp/<otp>/<email>/<otp_sent>',methods=['GET','POST'])
def otp(otp,email,otp_sent):
    if session.get('customer'):
        if request.method=="POST":
            otp1=request.form['otp']
            if otp==otp1:
                cursor=mysql.connection.cursor()
                cursor.execute('select * from customerapplications where email=%s',[email])
                view=cursor.fetchall()
                print(view)
                return render_template('customerviewpolicie.html',view=view,email=email,otp=otp)
            else:
                flash('the entered otp is wrong')
                # return render_template('customerviewpolicie.html')
                return render_template('customerviewpolicie.html',email=email,otp=otp)
            
        return render_template('customerviewpolicie.html', otp_sent=otp_sent,email=email,otp=otp)

        
    else:
        return redirect(url_for('clogin'))

#==============see the reply of customer message
@app.route('/viewreply',methods=['GET','POST'])
def viewreply():
    if session.get('customer'):
        cursor=mysql.connection.cursor()
        cursor.execute('select cid from customerregistrations where name=%s',[session['customer']])
        cid=cursor.fetchone()
        cursor.execute('select * from inquiries where customer_id=%s',[cid])
        view=cursor.fetchall()
        return render_template("viewreply.html",view=view)
    else:
        return redirect(url_for('clogin'))

#============================ Admin Dashboard

@app.route('/administrator_login',methods=['GET','POST'])
def alogin(): 
    if request.method=='POST':
        email=request.form['email']
        code = request.form['code']
        email1="adiseshu01213@gmail.com"
        code1="admin@123"
        if email == email1: 
            if code == code1:
                session['admin']=code1
                return redirect('admindashboard')
        else:
            flash("Unauthorized access")
            return redirect(url_for('alogin'))
    
    return render_template('administrator_login.html')
@app.route('/alogout')
def alogout():
    if session.get('admin'):
        session.pop('admin')
        flash('successfully log out')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('alogin'))
@app.route('/admindashboard',methods=['GET','POST'])
def admindashboard():
    if session.get('admin'):
        return render_template('admindashboard.html')
    else:
        flash('Please login to continue')
        return redirect(url_for('alogin'))
@app.route('/addcategorie',methods=['GET','POST'])
def addcategory():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from categories')
        categories=cursor.fetchall()
        if request.method=='POST':
            name=request.form['name']
            description=request.form['description']
            cursor.execute('insert into categories (name,description) values (%s,%s)',[name,description])
            mysql.connection.commit()
            cursor.close()
            flash('category added, now policie add to the particular category')
            return redirect(url_for('addcategory'))
        return render_template('categories.html',categories=categories) 
    return redirect(url_for('alogin'))  
@app.route('/deletecategory',methods=['GET','POST'])
def deletecategory():
    if session.get('admin'):
        if request.method=='POST':
            cid=request.form['caid']
            cursor=mysql.connection.cursor()
            cursor.execute('delete from Categories where category_id=%s',[cid])
            mysql.connection.commit()
            cursor.close()
            flash('deleted successfully')
            return redirect(url_for('addcategory'))
    return redirect(url_for('alogin'))
@app.route('/update_category/<cid>',methods=['GET','POST'])
def update_category(cid):
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from categories')
        categories=cursor.fetchall()
        if request.method=='POST':
            cursor=mysql.connection.cursor()
            cid = cid
            name=request.form['name']
            description=request.form['description']
            cursor.execute('update categories set name=%s, description=%s where category_id=%s',[name,description,cid])
            mysql.connection.commit()
            cursor.close()
            flash('categories updates successfully')
            return redirect(url_for('addcategory'))
        return render_template('update_category.html',categories=categories)
    else:
        return redirect(url_for('alogin'))
#============================
#========= add policies
@app.route('/add_policies',methods=['GET','POST'])
def add_policies():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from policies')
        policies=cursor.fetchall()
        cursor.execute('select * from categories')
        categories=cursor.fetchall()
        
        if request.method=='POST':
            c_area=request.form['area']
            amount=request.form['amount']
            category_id=request.form['category_id']
            cursor.execute('select name from categories where category_id=%s',[category_id])
            name=cursor.fetchone()
            cursor.execute('select description from categories where category_id=%s',[category_id])
            description=cursor.fetchone()
            cursor=mysql.connection.cursor()
            cursor.execute('insert into Policies (name,description,coverage_area,premium,category_id) values (%s,%s,%s,%s,%s)',[name,description,c_area,amount,category_id])
            mysql.connection.commit()
            cursor.close()
            flash('policies added')
            return redirect(url_for('add_policies'))
        return render_template('addpolicies.html',policies=policies,categories=categories)
    else:
        return redirect(url_for('alogin'))
@app.route('/deletepolicie',methods=['GET','POST'])
def deletepolicie():
    if session.get('admin'):
        if request.method=='POST':
            pid=request.form['pid']
            cursor=mysql.connection.cursor()
            cursor.execute('delete from Policies where policy_id=%s',[pid])
            mysql.connection.commit()
            cursor.close()
            flash('deleted successfully')
            return redirect(url_for('add_policies'))
    return redirect(url_for('alogin'))
@app.route('/update_policies/<cid>',methods=['GET','POST'])
def update_policies(cid):
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from Policies where policy_id=%s',(cid,))
        policies=cursor.fetchall()
        if request.method=='POST':
            cursor=mysql.connection.cursor()
            cid = cid
            area=request.form['area']
            amount=request.form['amount']
            cursor.execute('update Policies set coverage_area=%s, premium=%s where policy_id=%s',[area,amount,cid])
            mysql.connection.commit()
            cursor.close()
            flash('policies updated successfully')
            return redirect(url_for('add_policies'))
        return render_template('update_policie.html',p=policies)
    else:
        return redirect(url_for('alogin'))


#===================== add customers
@app.route('/applypolicies',methods=['GET','POST'])
def applypolicies():
    if session.get('admin') or session.get('customer'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from categories')
        categories = cursor.fetchall()
        cursor.execute('select * from policies')
        policies=cursor.fetchall()
        print(policies)
        if request.method=='POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            income = request.form['income']
            health = request.form['health']
            health_problems = request.form.get('health_problems', '')  # Get health problems if provided
            policy_id = request.form['policy_id']
            #print('--------------------------------------',policy_id)
            date=request.form['date']
            cursor.execute('select count(*) from customerapplications where email=%s',[email])
            count1=cursor.fetchone()[0]
            if count1==1:
                flash('email already in use')
                return redirect(url_for('applypolicies'))
            cursor.execute('select coverage_area from policies where policy_id=%s',[policy_id])
            policy_name=cursor.fetchone()
            cursor.execute('select category_id from policies where policy_id=%s',[policy_id])
            category_id=cursor.fetchone()
            cursor.execute('select name from categories where category_id=%s',[category_id])
            
            category_name=cursor.fetchone()
            cursor.execute('INSERT INTO customerapplications (customer_name, policy_id, category_id, application_date, phone_number, address, average_income, health, health_problems, email, policy_name, category_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [name, policy_id, category_id, date, phone, address, income, health, health_problems, email, policy_name, category_name])
            mysql.connection.commit()
            cursor.close()
            flash('policie applied successfully')
        return render_template('applypolicie.html',categories=categories,policies=policies)

    return redirect(url_for('index'))
@app.route('/policiesdashboard')
def policiesdashboard():
    if session.get('admin'):
        return render_template('policiesdashboard.html')
    return redirect(url_for('alogin'))
#=========view appllied policies
@app.route('/viewpolicies',methods=['GET','POST'])
def viewpolicies():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from CustomerApplications')
        view=cursor.fetchall()
        return render_template('viewpolicies.html',view=view)
    return redirect(url_for('alogin'))


@app.route('/deletecustomerpolicie/<aid>',methods=['GET','POST'])
def delcuspolicie(aid):
    if session.get('admin'):
       
        cursor=mysql.connection.cursor()
        cursor.execute('delete from customerapplications where application_id=%s',[aid])
        mysql.connection.commit()
        cursor.close()
        flash('application deleted successfully')
        return redirect(url_for('applypolicies'))


    return redirect(url_for('alogin'))
@app.route('/updatecustomerpolicie/<aid>',methods=['GET','POST'])
def updatecuspolicie(aid):
    if session.get('admin'):
        cursor=mysql.connection.cursor()

        cursor.execute('select * from categories')
        categories = cursor.fetchall()
        cursor.execute('select * from policies')
        policies=cursor.fetchall()
        cursor.execute('select * from CustomerApplications where application_id=%s',(aid,))
        view=cursor.fetchall()
        if request.method=='POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            income = request.form['income']
            health = request.form['health']
            health_problems = request.form.get('health_problems', '')  # Get health problems if provided
            policy_id = request.form['policy_id']
            #print('--------------------------------------',policy_id)
            date=request.form['date']
            cursor.execute('select coverage_area from policies where policy_id=%s',[policy_id])
            policy_name=cursor.fetchone()
            cursor.execute('select category_id from policies where policy_id=%s',[policy_id])
            category_id=cursor.fetchone()
            cursor.execute('select name from categories where category_id=%s',[category_id])
            
            category_name=cursor.fetchone()
            cursor.execute('UPDATE customerapplications SET policy_id=%s, category_id=%s, application_date=%s, '
                           'phone_number=%s, address=%s, average_income=%s, health=%s, health_problems=%s, '
                           'email=%s, policy_name=%s, category_name=%s WHERE application_id=%s',
                           (policy_id, category_id, date, phone, address, income, health, health_problems,
                            email, policy_name, category_name, aid))

            mysql.connection.commit()
            cursor.close()
            flash('update customer policies')
            return redirect(url_for('policiesdashboard'))

        return render_template('updatecuspolicie.html',view=view,categories=categories,policies=policies)

    return redirect(url_for('alogin'))
#====================inquries and questions
@app.route('/questions',methods=['GET','POST'])
def questions():
    if session.get('customer'):
        if request.method=='POST':
            message=request.form['message']
            cursor=mysql.connection.cursor()
            cursor.execute('select cid from customerregistrations where name=%s',[session['customer']])
            cid=cursor.fetchone()
            cursor.execute('insert into inquiries (customer_id,message) values (%s,%s)',[cid,message])
            mysql.connection.commit()
            cursor.close()
            flash('your message submitted to admin')
            return redirect(url_for('questions'))
        return render_template('questions.html')  
    
    return redirect(url_for('clogin'))

#=========admin view questions
@app.route('/viewmessages',methods=['GET','POST'])
def viewmessages():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from inquiries')
        view=cursor.fetchall()
        return render_template('viewmessages.html',view=view)
    return redirect(url_for('alogin'))
@app.route('/replymessages/<iid>',methods=['GET','POST'])
def replymessages(iid):
    if session.get('admin'):
        if request.method=="POST":
            reply=request.form['reply']
            cursor=mysql.connection.cursor()
            cursor.execute('update inquiries set reply=%s where inquiry_id=%s',[reply,iid])
            mysql.connection.commit()
            cursor.close()
            flash('message sent sucessfully')
            return redirect(url_for('viewmessages'))
    return redirect(url_for('alogin'))
app.run(use_reloader=True,debug=True)
      
    








