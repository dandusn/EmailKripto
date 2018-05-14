from flask import Flask, render_template, request
import Email
from Fierkes import Fierkes
from Fiestel import Fiestel

import ecdsa

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html', emaile = "wew")

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        to = request.form['toemail']
        msg = request.form['message']
        a = request.form['a']
        b = request.form['b']
        c = request.form['c']
        prime = request.form['prime']

        Fr = Fierkes()
        Ec = ecdsa
        c = Ec.CurveModP(int(a), int(b), int(c), int(prime))
        print(c.show_points())
        p = Ec.Point(3, 5)
        k = Ec.generate_keypair(c, p, c.nth_order(p))
        str = msg
        str = str.encode('utf-8')
        z = Ec.parse_sign(Ec.sign(str,c,p,c.nth_order(p),k))
        str = str.decode("utf-8")
        str += z

        for i in range(16):
            Fr.fn.assighnString(str, False)
            str = Fr.Encrypt()

        str = str.encode('utf-8')
        w = Ec.parse_sign(Ec.sign(str,c,p,c.nth_order(p),k))
        str = str.decode("utf-8")
        str += w
        str = str.encode('utf-8')

        try:
            Email.Emailsender(to,'Enkripsi',str)
            return render_template("result.html", emaile = to )
        except Exception as e:
            return render_template("index.html", error = e)


if __name__ == '__main__':
    app.run(debug=True)
