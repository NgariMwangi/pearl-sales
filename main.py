from kra import Payroll
import psycopg2
from flask import Flask, request, render_template, Request, redirect, url_for, flash
from datetime import date
import json, ast
 
app = Flask(__name__)
app.config["SECRET_KEY"] = "#deno0707@mwangi"
#app.config["SECRET_KEY"] = "36d44b1536a758b6cfb4ab06430c574cecf024ad288c0bf0de2cb3a5f1cc63e8"
#conn = psycopg2.connect(user="postgres", password="deno0707",host="127.0.0.1", port="5432", database="myduka")
conn = psycopg2.connect(database="d66n9lkjhpv4d2", host="ec2-54-155-61-133.eu-west-1.compute.amazonaws.com", user="skfkvatvfaigmx", port=5432, password="36d44b1536a758b6cfb4ab06430c574cecf024ad288c0bf0de2cb3a5f1cc63e8")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS product1 (id serial PRIMARY KEY,name VARCHAR(100),buying_price INT,selling_price INT,stock_quantity INT);")
cur.execute("CREATE TABLE IF NOT EXISTS sale (id serial PRIMARY KEY,pid INT, quantity INT, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW() );")
cur.execute("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY,username VARCHAR(100), email VARCHAR(100),password VARCHAR(100),password2 VARCHAR(100) );")
conn.commit()

@app.route('/kra',methods=["POST","GET"])
def netpay():
    z=[]
    if request.method=="POST":
        q=request.form["name"]
        p=request.form["basic"]
        o=request.form["benefits"]
        p=(int(p))
        o=(int(o))
        x=Payroll(p,o)
        data = {"nm":q,"gs":x.gross_salary,"ns":x.nssf_var,"tx":x.taxable_pay,"py":x.paye,"nh":x.nhif,"dd":x.deductions,"nt":x.net_salary}

        # print("x before re", data)
        return redirect(url_for('netpay', x=data) )
        
    else:
        
        try:  
            x= request.args['x']          
            print("x after re55",x)
            print(type(x))
            print("h")
            # d = json.loads(x)
            d = ast.literal_eval(x)
            print("here")
            print(d)
            print(type(d))
            return render_template("kra.html",d=d)
        except:
            if request.method=="GET":
                d={}            
                return render_template("kra.html",d=d)
            else:
                return render_template("kra.html",d=d)
        
       

@app.route('/signup',methods=["POST","GET"])
def sign():
    if request.method=="POST":
        cur=conn.cursor()
        g=request.form["email"]
        print(g)
        p=request.form["password"]
        o=request.form["password2"]
        i=request.form["username"]
        cur.execute('select email from users')
        k=cur.fetchall()
        q=[]
        for yt in k:
            q.append(yt[0])

        g!=q
        print(k)
        print(q)
        print(g)
        print(type(g))
        if p==o:
                for ts in q:
                    if g !=ts:
                        cur.execute("""INSERT INTO users(username,email,password,password2) VALUES ( %(i)s,%(g)s,%(p)s,%(o)s)""", {
                            "i":i, "g": g, "p":p, "o": o, })              
                        return redirect("/products")
                
                    else:
                        flash('email already exist')
                    return redirect("/signup")
                
               
        else:
            flash('password can not be confirmed')          
            return redirect("/signup")

    else:
        return render_template("signup.html")

@app.route('/login', methods=["POST", "GET"])
def log():
    if request.method=="POST":
        cur=conn.cursor()
        h=request.form["email"]
        j=request.form["password"]
        cur.execute("select count(id) from users where email= %(h)s and password=%(j)s", {"h":h,"j":j})
        pro=cur.fetchall()
        for i in pro:
            if i[0]==1:
                return redirect("/products")
            else:
                flash('incorrect details')
                return redirect("/login")

    
       
        
        # for b in f:
        #     if b[2]==h:
        #         if b[3]==j:
        #             return redirect("/products")
        #         else:
        #             flash('incorrect password')
        #     else:
        #         flash('invalid Email')
    else:
        return render_template("signup.html")
    


@app.route('/dashboard')
def dash():
    cur=conn.cursor()
    cur.execute("select count(id) from product1")
    pro=cur.fetchall()
    y=pro[0]
    pro=y[0]
    cur.execute("select count(id) from sale")
    sales=cur.fetchall()
    x=sales[0]
    sales=x[0]
    cur = conn.cursor()
    cur.execute("""select sum((product1.selling_price-product1.buying_price)*sale.quantity) as profit, product1.name from sale 
        join product1 on product1.id=sale.pid
        GROUP BY product1.name""")
    graph=cur.fetchall()
    
    v=[]
    y=[]
    for i in graph:
        v.append(i[1])
        y.append(i[0])
        
    cur.execute(""" select to_char("created_at", 'mm-dd-yyyy'),sum((product1.selling_price-product1.buying_price)*sale.quantity) as profit
from sale join product1 on product1.id=sale.pid
        GROUP BY sale.created_at""")
    line=cur.fetchall()
    # print(line)
    dat=[]
    profit=[]
    for u in line:
        dat.append(u[0])
        profit.append(u[1])
    print(len(dat))
    print(len(profit))
    
    
    return render_template("dashboard.html", pro=pro,sales=sales,y=y,v=v,graph=graph,dat=dat,profit=profit)
    

@app.route('/')
def hello_world():
    cur = conn.cursor()
    cur.execute("""select sum((product1.selling_price-product1.buying_price)*sale.quantity) as profit, product1.name from sale 
        join product1 on product1.id=sale.pid
        GROUP BY product1.name""")
    graph=cur.fetchall()
    print(graph)
    print(type(graph))
    v=[]
    y=[]
    for i in graph:
        v.append(i[1])
        print(v)
        y.append(i[0])
        print(y)
    print(y)

    return render_template('index.html', y=y,v=v,graph=graph)


@app.route('/change')
def products():
    return render_template('change.html')


@app.route('/products', methods=["POST", "get"])
def product():

    if request.method == "POST":
        cur = conn.cursor()
        product_name = request.form["name"]
        buying_price = request.form["buying_price"]
        selling_price = request.form["selling"]
        stock_quantity = request.form["stock"]
        print(product_name)
        print(buying_price)
        cur.execute("""INSERT INTO product1(name,buying_price,selling_price,stock_quantity) VALUES ( %(n)s,%(bp)s,%(sp)s,%(st)s)""", {
                    "n": product_name, "bp": buying_price, "sp": selling_price, "st": stock_quantity, })
        conn.commit()
        return redirect("/products")
    else:
        cur = conn.cursor()
        cur.execute("select * from product1")
        record = cur.fetchall()
        list1 = record
        record = cur.fetchall()
        return render_template('products.html', list1=list1)


@app.route('/sales/<int:id>')
def sales(id):
    cur = conn.cursor()
    cur.execute("""select sale.id, product1.name, product1.stock_quantity,(product1.selling_price-product1.buying_price)*sale.quantity as profit from product1
    join sale on sale.pid=product1.id where  pid= %(id)s""", {"id": id})
    sale = cur.fetchall()
    lst4 = sale
    return render_template('sales.html', lst4=lst4)


@app.route('/sales', methods=["POST", "GET"])
def sale():
    if request.method == "POST":
        pid = request.form["Item-id"]
        sale_quantity = request.form["item-quantity"]
        x = (int(sale_quantity))

        cur = conn.cursor()
        cur.execute(
            """select stock_quantity from product1 where id=%(pid)s""", {"pid": pid})
        sq = cur.fetchone()
        y = list(sq)
        z = y[0]-x
        print(y[0])
        if z <= 0:
            flash('Quantity ordered is higher that stock available')
            return redirect(url_for("product"))
        else:
            cur.execute("""update product1 set stock_quantity=%(z)s where id=%(pid)s""", {
                        "pid": pid, "z": z})
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO sale (pid,quantity) VALUES (%s,%s)", (pid, sale_quantity))
            conn.commit()
            return redirect(url_for("sa"))


@app.route('/sal')
def sa():
    cur = conn.cursor()
    cur.execute("""select sale.id, product1.name, product1.stock_quantity,(product1.selling_price-product1.buying_price)*sale.quantity as profit from product1
    join sale on sale.pid=product1.id """,)
    sale = cur.fetchall()
    lst4 = sale

    return render_template('sales.html', lst4=lst4)


if __name__ == "__main__":
    app.run(debug=True)
