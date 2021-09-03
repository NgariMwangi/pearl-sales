import psycopg2 
conn = psycopg2.connect(user="Postgres", password="deno0707",
                        host="localhost", port="", database="myduka")
cur = conn.cursor()
cur.execute("select * from products")
record = cur.fetchall
for r in record:
    print(f"id{r[0]} name{r[1]} buyingprice{r[2]} sellingprice{r[3]} stock-quantity{r[4]}")

cur.close
conn.close

