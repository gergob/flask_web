from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from bson.objectid import ObjectId
from contact import Contact
from contacts_repository import ContactsRepository

app = Flask(__name__)
app.secret_key = "This is my super secret never guessed secret key."
repository = ContactsRepository()

# decorator for Flask application methods
def user_login_needed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_user_logged_in = session['user_logged_in']
        if not is_user_logged_in:
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)
    return decorated_function



@app.route("/")
@user_login_needed
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        user_name = request.form['username']
        password = request.form['password']
        if is_user_valid(user_name, password):
            session['user_logged_in'] = True 
            error_message = "User {} successfuly logged in.".format(user_name)
            flash(error_message)
            print(error_message)
            return redirect(url_for("index"))
        else:
            print("Invalid user.")
            flash("Invalid user/password!")
            return redirect(url_for("login"))
    else:
        error_message = "Invalid request method:{}".format(request.method)
        print(error_message)
        flash(error_message)
        return redirect(url_for("login"))

@app.route("/logout", methods=["GET"])
def logout():
    session['user_logged_in'] = False
    print("User logout successful.")
    flash("Logout successful") 
    return redirect(url_for("login"))

def is_user_valid(user_name, password):
    return user_name == "john" and password == "1234"

@app.route("/add_contact", methods=["GET","POST"])
@user_login_needed
def add_contact():
    if request.method == "GET":
        return render_template("add_contact.html")
    elif request.method == "POST":
        for item,val in request.form.items():
            print("{0}={1}".format(item, val))
        try:
            contact = Contact(first_name=request.form['first_name'], 
                last_name=request.form['last_name'], 
                birthday=request.form['birthday'], 
                website=request.form['website'], 
                home_phone=request.form['home_phone'], 
                mobile_phone=request.form['mobile_phone'], 
                work_phone=request.form['work_phone'], 
                email=request.form['email'])
            contact_id = repository.create(contact)
            print("Contact succesfully created with id={0}".format(contact_id))
        except Error as e:
            print(e)

        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/contacts")
@user_login_needed
def contacts():
    contacts_to_display = []
    contacts_from_db = repository.read()
    for c in contacts_from_db:
        tempContact = Contact.build_from_json(c)
        print("Contact converted: {0}".format(tempContact))
        contacts_to_display.append(tempContact)
    return render_template("contacts.html", contacts = contacts_to_display)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)


