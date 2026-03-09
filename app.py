from flask import Flask, request, render_template

app = Flask(__name__)

users = {
    "admin" : "password123",
    "cashier" : "cashierpass",
    "manager" : "managerpass"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
             return "Login successful!"
        
        return  render_template('login.html', error="Invalid username or password.")

    return render_template('login.html', error=None)


if __name__ == '__main__':
    app.run(debug=True)