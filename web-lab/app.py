from flask import Flask, request, render_template_string
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Portal de prueba</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        passwd = request.form.get('password')
        return f"Usuario: {user}, Password: {passwd}"
    return '''
        <form method="post">
            Usuario: <input name="username"><br>
            Clave: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)