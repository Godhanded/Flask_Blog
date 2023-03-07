posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','bg-green-400')
        return redirect(url_for('home'))
    
    return render_template("register.html", title="Register",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data=='foo@gmail.com' and form.password.data=='123':
            flash('You have been logged in!','bg-green-300')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull. Check username and password','bg-rose-400')
    return render_template("login.html", title="login",form=form)

