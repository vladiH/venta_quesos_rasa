import sqlite3
conn = sqlite3.connect('quesos.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE orders
#              (text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# EXISTING ORDERS
# Create table
c.execute('''CREATE TABLE orders
             (order_date, order_number, order_email, cheese, price, status)''')

# data to be added
purchases = [('2023-01-28',123456,'yuri@gmail.com','mozzarella', 9, 'enviado'),
             ('2023-02-07',123457,'vladimir@hotmail.com','roquefort', 10, 'pendiente'),
             ('2023-01-06',123458,'yuri_vladi@outlook.com','andino', 13, 'entregado'),
            ]

# add data
c.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)', purchases)

# AVAILABLE INVENTORY
# Create table
c.execute('''CREATE TABLE inventory
             (cheese, brand, price, kg)''')
# data to be added
inventory = [
            ('cheddar', 'Chimay', 12, '1/2'),
            ('cheddar', 'Chimay', 20, '1'),
            ('mozzarella', 'vargas', 10, '1'),
            ('mozzarella', 'vargas', 5, '1/4'),
            ('mozzarella', 'vargas', 6, '1/2'),
            ('brie', 'Gloria', 10, '1'),
            ('brie', 'Gloria', 5, '1/2'),
            ('gouda', 'Gloria', 15, '1'),
            ('parmesano', 'Sargento', 8, '1'),
            ('roquefort', 'vargas', 9, '1'),
            ('camembert', 'vargas', 12, '1'),
            ('feta', 'Eddam', 10, '1'),
            ('blue', 'vargas', 6, '1'),
            ('americano', 'Jarlsberg', 9, '1'),
            ('suizo', 'vargas', 5, '1'),
            ]

# add data
c.executemany('INSERT INTO inventory VALUES (?,?,?,?)', inventory)


# Save (commit) the changes
conn.commit()

# end connection
conn.close()