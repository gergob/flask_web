from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from contact import Contact
from contacts_repository import ContactsRepository

app = Flask(__name__)
repository = ContactsRepository()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_contact", methods=["GET","POST"])
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
def contacts():
    contacts_to_display = []
    contacts_from_db = repository.read()
    for c in contacts_from_db:
        tempContact = Contact.build_from_json(c)
        print("Contact converted: {0}".format(tempContact))
        contacts_to_display.append(tempContact)
    return render_template("contacts.html", contacts = contacts_to_display)


if __name__ == "__main__":
    app.run(debug=True)


