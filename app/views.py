""" views.py """

from flask import render_template, request, session
from app import app, user_object, bucket_object

@app.route('/')
def index():
    """Handles rendering of index page
    """
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles registeration of users
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['confirm-password']

        msg = user_object.registeruser(username, email, password, cpassword)
        if msg == "Successfully registered. You can now login!":
            return render_template("bucketlist-login.html", resp=msg)
        else:
            return render_template("bucketlist-reg-login.html", resp=msg)
    return render_template("bucketlist-reg-login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles logging in
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        msg = user_object.login(email, password)
        if msg == "Successfully logged in, create buckets!":
            session['email'] = email
            return render_template('bucketlist-bucket.html', resp=msg)
        else:
            return render_template('bucketlist-login.html', resp=msg)
    return render_template("bucketlist-login.html")


@app.route('/bucketlist-bucket', methods=['GET', 'POST'])
def bucket():
    """Handles bucket creation
    """
    if 'email' in session.keys():
        if request.method == 'POST':
            bucket_name = request.form['bucket-name']
            msg = bucket_object.create_bucket(bucket_name)
            if msg == bucket_object.buckets:
                return render_template('bucketlist-bucket.html', bucketlist=msg)
            else:
                return render_template('bucketlist-bucket.html', resp=msg, bucketlist=bucket_object.buckets)
        return render_template('bucketlist-bucket.html', bucketlist=bucket_object.buckets)
    return render_template("bucketlist-login.html")

@app.route('/edits', methods=['GET', 'POST'])
def save_edits():
    """ Handles editing of buckets """
    if request.method == 'POST':
        edit_name = request.form['temp_bucket_name']
        org_name = request.form['org_bucket_name']
        msg = bucket_object.edit_bucket(edit_name, org_name)
        if msg == bucket_object.buckets:
            response = "Successfully edited bucket"
            return render_template('bucketlist-bucket.html', resp=response, bucketlist=msg)
        else:
            existing = bucket_object.buckets
            return render_template('bucketlist-bucket.html', resp=msg, bucketlist=existing)
    return render_template('bucketlist-bucket.html')

@app.route('/bucketlist-activity', methods=['GET', 'POST'])
def activity():
    """Handles creation of activities
    """
    return render_template("bucketlist-activity.html")
   