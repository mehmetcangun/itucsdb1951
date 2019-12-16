import os
DB_URL = os.getenv("DATABASE_URL")

import psycopg2 as dbapi2

def get_all_orders():
  orders = []
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select * from orders"
      cursor.execute(query)
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      for i in cursor:
        res = dict(zip(desc, list(i) ))
        orders.append( res )
  return orders

def get_order(key, type):
  res = None
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = ""
      if type == "restaurant":
        query = "select * from orders where restaurant_id = %s;"
      elif type == "user":
        query = "select * from orders where user_id = %s;"
      else:
        query = "select * from orders where order_id = %s;"
      cursor.execute(query, (key, ))
      data = cursor.fetchone()
      if data:
        order = list( data )
        desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
        res = dict(zip(desc, order ))
  return res

def add_order(order):
  order_id = -1
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "insert into orders(price, note, type, rate, end_at, restaurant_id, user_id) values(%s, %s, %s, %s, %s, %s, %s) RETURNING order_id;"
      cursor.execute(query, order)
      connection.commit()
      order_id = cursor.fetchone()[0]
  return order_id

def connect_order_and_food(orderfood):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "insert into order_food(order_id, food_id, amount) values(%s, %s, %s);"
      cursor.execute(query, orderfood)
      connection.commit()

def update_order(order):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "update orders set price = %s, note = %s, type = %s, rate = %s, end_at = %s where order_id = %s;"
      cursor.execute(query, order)
      connection.commit()

def delete_order(order_key):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "delete from orders where order_id = %s;"
      cursor.execute( query, (order_key,) )
      connection.commit()

