#importar la clase Flask desde el módulo flask
from flask import Flask

app = Flask(__name__) #Crear una instancia de la aplicación Flask

@app.route('/') #Decorador para definir la ruta de la aplicación
def hello_world():
    return 'Hello World with Flask!'

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
