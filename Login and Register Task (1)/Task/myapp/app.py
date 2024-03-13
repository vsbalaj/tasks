from flask import Flask, redirect,url_for, render_template,request,session
import sqlite3

app=Flask(__name__)

app.secret_key="welcome my world"
DATABASE = 'mydatabase.db'

def create_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


@app.route('/')
def view():
    create_table()
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    connection.close()
    return render_template('login.html')

    
@app.route('/check_status', methods=['GET','POST'])
def che():
    if request.method=='POST':
        if 'Sign_in' in request.form:
            username=request.form['username']
            print(username)
            password=request.form['password']
            print(password)
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM books')
            books = cursor.fetchall()
            connection.close()
            correct=0
            for increment in range(len(books)):
                if username==books[increment-1][1] and password==books[increment-1][2]:
                    correct=1
                    break
                else:
                    correct=0
            if correct==1:
                return  render_template('sign_in.html', username=username, password=password)
            else:
                return render_template('invalid.html')
        elif 'Sign_up' in request.form:
            return redirect(url_for('sign_up'))
            

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/set_password', methods=['POST'])
def set_password():
    username = request.form['username']
    print(username)
    password = request.form['password']
    print(password)
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO books (username, password) VALUES (?, ?)', (username, password))
    connection.commit()
    connection.close()
    return redirect(url_for('view'))

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('view'))
    


if __name__=='__main__':
    app.run(debug=True)