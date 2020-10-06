import sqlite3
from emploise import Employee
from os.path import isfile

conn = sqlite3.connect('e.db')
c=conn.cursor()


#c.execute("""CREATE TABLE employees (
      #      first text,
      #      last text,
      #      pay integer
      #      )""")


def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)",
                 {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


def get_emps_by_name(lastname):
    c.execute("SELECT * "
              "FROM employees "
              "WHERE last=:last", {'last': lastname})
    return c.fetchall()


def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees "
                  "WHERE first = :first AND last = :last",
                  {'first': emp.first, 'last': emp.last})

def full_name(name):

    c.execute("SELECT * "
              "FROM employees "
              "WHERE last=:name OR first =:name",
              {'name':name})
   # emp_3=Employee(c.fetchone()[0],c.fetchone()[1],c.fetchone()[2])
    return c.fetchone()

def  get_emps_from_selery(num):
    c.execute("SELECT * "
              "FROM employees "
              "WHERE pay>:num ",
              {'num': num})
    return c.fetchall()


#emp_1 = Employee('John', 'Doe', 8000)
emp_4 = Employee('Jane', 'aba', 100000)


remove_emp(emp_4)
#insert_emp(emp_2)

if  full_name('aba'):
    emp_3=Employee(full_name('aba')[0],full_name('aba')[1],full_name('aba')[2])
    print(emp_3.fullname)
    print(emp_3.email)
print(get_emps_from_selery(85000))
conn.close()