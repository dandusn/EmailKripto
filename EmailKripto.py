import codecs

from flask import Flask, render_template, request
import Email
from Keccak_new import Keccak256
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
        En = request.form.get('wencrypt') != None
        Sig = request.form.get('signature') != None

        print(En)
        print(Sig)
        str = msg

        if Sig:
            ##SIGNATURE
            Ec = ecdsa
            a = request.form['a']
            b = request.form['b']
            c = request.form['c']
            prime = request.form['prime']
            d = Ec.CurveModP(int(a), int(b), int(c), int(prime))
            print(d.show_points())
            p = Ec.Point(3, 5)
            k = Ec.generate_keypair(d, p, d.nth_order(p))
            str = codecs.encode(str,'utf-8')
            u = Ec.sign(str,d,p,d.nth_order(p),k)
            z = Ec.parse_sign(u[0],u[1],u[2])
            print(z)
            str = codecs.decode(str,"utf-8")
            str += "|"
            str += z
            print(str)

        if En:
            ##ENKRIPSI
            Fr = Fierkes()
            for i in range(16):
                Fr.fn.assighnString(str, False)
                str = Fr.Encrypt()

        if Sig:
            str = codecs.encode(str,'utf-8')
            v = Ec.sign(str, d, p, d.nth_order(p), k)
            w = Ec.parse_sign(v[0], v[1], v[2])
            str = codecs.decode(str, 'utf-8')
            str += "|"
            str += w

        try:
            if En and Sig:
                Email.Emailsender(to,'EnSig',str)
            elif En and not Sig:
                Email.Emailsender(to, 'En', str)
            elif not En and Sig:
                Email.Emailsender(to, 'Sig', str)
            else:
                Email.Emailsender(to, 'Plain', str)
            print(str)
            return render_template("result.html", emaile = to )
        except Exception as e:
            return render_template("index.html", error = e)


if __name__ == '__main__':
    app.run(debug=True)
