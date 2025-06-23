# Laboratorio Semama 7 - Análisis de Seguridad Web con Docker, OWASP ZAP, Badstore y KaliGPT (CY-203 Hackeo Ético)

**Duración estimada:** 2.5 horas  
**Modalidad:** Práctica guiada en Kali Linux con Docker  
**Objetivo:** Comprender y aplicar las fases de reconocimiento, escaneo, enumeración y análisis de vulnerabilidades en aplicaciones web, utilizando tanto un sitio web desarrollado en clase como una aplicación vulnerable conocida (Badstore), reforzado con el uso de inteligencia artificial mediante **KaliGPT**.

---

### Nota sobre entornos Mac/Windows y VMs

Si estás usando **Docker en tu sistema host (Mac o Windows)** y accediendo desde una **VM de Kali Linux**, no podrás usar `localhost` directamente.

#### Encuentra la IP del host (Mac o Windows):
- **macOS:**
  ```bash
  ifconfig en0 | grep inet
  ```
- **Windows (PowerShell):**
  ```powershell
  ipconfig
  ```

Busca una IP como `192.168.x.x`. Supongamos que es:
```bash
export HOSTIP=192.168.50.187
```

Usa esta variable para todos los comandos desde Kali:
```bash
curl http://$HOSTIP:5050
```

---

### Parte 1: Desarrollo y Análisis de un Sitio Web Propio (Python Flask + Docker)

#### 1.1 Preparación del entorno

```bash
mkdir web-lab && cd web-lab
```

**app.py:**
```python
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
```

**Dockerfile:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 5050
CMD ["python", "app.py"]
```

Construir y ejecutar:
```bash
docker build -t flaskvuln .
docker run -d -p 5050:5050 flaskvuln
```

Desde Kali, accede en el navegador a `http://$HOSTIP:5050`

---

#### 1.2 Fase de reconocimiento y escaneo

**a. Revisar cabeceras HTTP:**
```bash
curl -I http://$HOSTIP:5050
```

**b. Escaneo de puertos desde Kali:**
```bash
nmap -sV -p 5050 $HOSTIP
```

**c. Descubrimiento de rutas ocultas:**
```bash
gobuster dir -u http://$HOSTIP:5050 -w /usr/share/wordlists/dirb/common.txt
```

**Resultado esperado:**
```bash
/login                (Status: 200) [Size: 210]
```

**d. Apoyo con KaliGPT (https://chatgpt.com/g/g-uRhIB5ire-kali-gpt):**

Sugerencia de prompt:
```text
Estoy auditando el sitio http://$HOSTIP:5050. Ya corrí nmap, curl y gobuster. ¿Qué debería revisar a continuación? Sugiere pruebas específicas para formularios o cabeceras.
```

---

### Parte 2: Análisis de sitio vulnerable conocido (Badstore alternativa o simulador)

Repositorio funcional confirmado:
```bash
git clone https://github.com/jvhoof/badstore-docker.git
cd badstore-docker
docker build -t badstore .
docker run -d -p 8081:80 badstore
```

Accede desde Kali a `http://$HOSTIP:8081`

#### 2.2 Ejecutar reconocimiento y escaneo

**a. curl y nmap:**
```bash
curl -I http://$HOSTIP:8081
nmap -sV -p 8081 $HOSTIP
```

**b. gobuster:**
```bash
gobuster dir -u http://$HOSTIP:8081 -w /usr/share/wordlists/dirb/common.txt
```

**c. KaliGPT para pruebas adicionales:**
```text
Estoy analizando http://$HOSTIP:8081. ¿Cuáles son los puntos de entrada más críticos? Dime pruebas de XSS o SQLi específicas que debería intentar.
```

---

### Recursos adicionales

- [OWASP ZAP User Guide](https://www.zaproxy.org/docs/desktop/start/)
- [Docker Docs](https://docs.docker.com/)
- [Repositorio Badstore Docker](https://github.com/jvhoof/badstore-docker)
- [KaliGPT para Pentesting](https://chatgpt.com/g/g-uRhIB5ire-kali-gpt)

---

**Profesor:** Esteban Mata Morales  
**Curso:** CY-203 Hackeo Ético  
**Universidad Fidélitas de Costa Rica**
