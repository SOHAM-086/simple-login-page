from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='Templates')

# Database connection
conn = mysql.connector.connect(
    host="127.0.0.1",  # Change if needed
    user="root",       # Change if needed
    password="root",   # Change if needed
    database="data"    # Make sure your database is named correctly
)
cursor = conn.cursor()

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login_validation', methods=['POST'])
def login_validation():
    user_name = request.form.get('Uname')
    password = request.form.get('Pass')

    # Debugging: Print the form data to ensure it's being captured
    print(f"Attempting login with username: {user_name} and password: {password}")
    
    if not user_name or not password:
        # If either the username or password is empty, return an error message
        print("Username or password is empty!")
        return render_template("login.html", error="Both username and password are required.")

    try:
        # Updated query to use correct column names 'name' and 'password' for the 'user' table
        cursor.execute("SELECT * FROM user WHERE name = %s AND password = %s", (user_name, password))
        user = cursor.fetchall()

        # Debugging: Check the result of the query
        print(f"Query returned {len(user)} result(s)")

        if len(user) > 0:
            # Successfully authenticated, redirect to home page
            print("User authenticated, redirecting to home page.")
            return redirect(url_for('home'))
        else:
            # Failed authentication
            print("Invalid credentials, staying on login page.")
            return render_template("login.html", error="Invalid credentials")
    except mysql.connector.Error as err:
        # Handle database connection errors
        print(f"Database error: {err}")
        return render_template("login.html", error="Database error occurred.")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/add_user', methods=['POST'])
def add_user():
    user_name = request.form.get('Uname')
    email = request.form.get('Email')
    password = request.form.get('Pass')

    try:
        # Correct query with the correct column names 'name', 'email', and 'password'
        cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (user_name, email, password))
        conn.commit()
        print("User added to the database successfully.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('login.html', error="There was an issue with registration.")

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

