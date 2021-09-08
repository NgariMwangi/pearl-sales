import psycopg2
from flask import Flask, request, render_template, Request, redirect, url_for, flash
app = Flask(__name__)
# app.config["SECRET_KEY"] = "#deno0707@mwangi"
app.config["SECRET_KEY"] = "36d44b1536a758b6cfb4ab06430c574cecf024ad288c0bf0de2cb3a5f1cc63e8"

#conn = psycopg2.connect(user="postgres", password="deno0707",host="127.0.0.1", port="5432", database="myduka")
conn = psycopg2.connect(dbname="d66n9lkjhpv4d", host="ec2-54-155-61-133.eu-west-1.compute.amazonaws.com", user="skfkvatvfaigmx", port=5432,  password="36d44b1536a758b6cfb4ab06430c574cecf024ad288c0bf0de2cb3a5f1cc63e8")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS product1 (id serial PRIMARY KEY,name VARCHAR(100),buying_price INT,selling_price INT,stock_quantity INT);")
cur.execute("CREATE TABLE IF NOT EXISTS sale (id serial PRIMARY KEY,pid INT, quantity INT, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW() );")
conn.commit()


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
