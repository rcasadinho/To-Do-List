from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database/tarefas.db"
db = SQLAlchemy(app)
app.config["DEBUG"] = True

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200))
    feita = db.Column(db.Boolean)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def home():
    todas_as_tarefas = Tarefa.query.all()
    print('Tarefas na página inicial:', todas_as_tarefas) 
    return render_template("index.html", lista_de_tarefas=todas_as_tarefas)


@app.route('/criar-tarefa', methods=['POST'])
def criar():
    conteudo_tarefa = request.form.get('conteudo_tarefa')
    print(f"Conteúdo da tarefa recebido: {conteudo_tarefa}")
    if conteudo_tarefa:
        tarefa = Tarefa(conteudo=conteudo_tarefa, feita=False)
        db.session.add(tarefa)
        db.session.commit()
        print("Tarefa adicionada com sucesso!")
    else:
        print("Nenhum conteúdo de tarefa recebido.")
    return redirect(url_for('home'))

@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/tarefa-feita/<id>')
def feita(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()
    tarefa.feita = not (tarefa.feita)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

app.run()