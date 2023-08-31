from flask_app.models.user import User
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ---------------------------------------------------
# INDEX PAGE

@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------------------------------
# DASHBOARD PAGE - USERS CAN LOGIN AND RESGISTER

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---------------------------------------------------
# USER REGISTER

@app.route("/submit", methods=["POST"])
def submit():
    if not User.is_valid_user(request.form):
        return redirect('/dashboard')
    data={
        "first_name":request.form["first_name"],
        "last_name":request.form["lst_name"],
        "email":request.form["email"],
        "password":bcrypt.generate_password_hash(request.form["password"])
    }
    id=User.save(data)
    session['user_id'] = id
    return redirect("/show")

# ---------------------------------------------------
# USER LOGIN

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email({"email":request.form['email']})
    if not user:
        flash("Invalid Email","login")
        return redirect('/dashboard')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/dashboard')
    session['user_id'] = user.id
    return redirect('/show')

# ---------------------------------------------------
# USER LOGOUT

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/dashboard")