# Teste básico Allgoo

Projeto Web Python 3 com a framework Flask e as bibliotecas Flask-Login, OAuth e Flask-MongoEngine.
Flask é considerada uma microframework baseada no Werkzeug e Jinja2. Possibilitando criar aplicações web com pouquissimas
linhas de código. Flask-Login é usada para controlar os endpoints que demandam usuário autenticado, que é fornecido pelo OAuth.
MongoEngine é uma ORM que possibilita utilizar a banco de dados NoSQL Mongo. MongoDB oferece facilidades para escalar aplicações distribuídas como redes sociais.

## Configuração
### Máquina Virtual
É recomendável utilizar uma máquina virtual python para executar o projeto. Entretanto, caso desejável executar o projeto com o interpretador previamente instalado, pule para o próximo tópico.

Para criar a máquina virtual, basta executar o seguintes comando:

Linux:
```bash
python3 -m venv /pasta-projeto/env
```

Windows:
```bash
c:\>c:\Python35\python -m venv \pasta-projeto\env
```
OBS: É possível que você tenha que instalar a [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) antes na sua máquina.

Em seguida, ative a máquina virtual executando o seguinte comando:

Linux:
```bash
. venv/bin/activate
```
Windows:
```bash
\venv\Scripts\activate
```
### Instalando as Dependências
Com a máquina ativada, é necesário instalar as dependências do projeto com o client PIP. Portanto, execute o seguinte comando:
```bash
pip install -r requirements.txt
```

## Inicializando a Aplicação
Atenção: É preciso ter o client Mongo em execução nas configurações padrões (localhost:27017).
Para inserir alguns dados de exemplo, basta executar o comando:
```bash
python wsgi.py --init-db
```
Em seguida, inicialize a aplicação:
```bash
python wsgi.py
```

Pronto, para acessar aplicação, basta acessar a URL [localhost:5000](http://127.0.0.1:5000):
