from flask import Flask, render_template, request, flash
import Email

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        #fr = request.form['email']
        #password = request.form['password']
        to = request.form['toemail']
        msg = request.form['message']
        try:
            Email.Emailsender(to,'Enkripsi',msg)
            return render_template("result.html", emaile = to )
        except:
            return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
