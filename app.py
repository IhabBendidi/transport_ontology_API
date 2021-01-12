import flask
import rdflib
from flask import request
from flask import render_template, redirect, url_for
import wikipedia
from forms import SearchForm
from flask_wtf.csrf import CSRFProtect, CSRFError

import os
SECRET_KEY = os.urandom(32)

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = "data"
app.config["DEBUG"] = True

csrf = CSRFProtect(app)

g = rdflib.Graph()

g.parse("data/transit_ontology.owl")


@app.route('/api/moyen_transports', methods=['GET'])
def moyen_transports():
    code = 200
    try :
        qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        PREFIX ex: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>
                        SELECT ?subject
                        	WHERE { ?subject rdfs:subClassOf ex:moyen_transports}""")
        if len(list(qres))==0:
            code = 200
            transports = []
        else :
            transports = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres)]
    except :
        transports = None
        code = 503
    return {"code":code,"response":transports}


@app.route('/api/individu_transports', methods=['GET'])
def individu_transports():
    #TODO : GET DATA OF EACH TRANSPORT
    code = 200
    individu = request.args.get('individu')
    if individu == '':
        code = 404
        transports = None
    else :
        try :
            qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX owl: <http://www.w3.org/2002/07/owl#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                            PREFIX xd: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

                            SELECT ?object
                                WHERE { xd:""" + individu + """ xd:commutewith ?object}""")
            transports = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres)]
        except :
            code = 503
            transports = None
    return {"code":code,"response":transports}

@app.route('/api/statistics', methods=['GET'])
def day_statistics():
    moyen = request.args.get('moyen')
    if moyen == '':
        code = 404
        stat = None
    else :
        code = 200
        try :
            qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX owl: <http://www.w3.org/2002/07/owl#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                            PREFIX xd: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

                            SELECT ?personne
                            WHERE {
                                        ?personne rdf:type xd:Person.
                                        ?personne xd:commutewith xd:""" + moyen + """.
                            }""")
            stat = len(list(qres))
        except :
            code = 503
            stat = None
    return {"code":code,"response":stat}



@app.route('/api/get_details', methods=['GET'])
def get_location():
    location = request.args.get('location')
    source = None
    if location == '':
        code = 404
        response = None
    else :
        code = 200
        try :
            response = wikipedia.summary(location)
            source = "wikipedia"
        except :
            code = 503
            response = None
    return {"code":code,"response":response,"source":source}


@app.route('/api/pollution', methods=['GET'])
def get_pollution():
    moyen = request.args.get('moyen')
    if moyen == '':
        code = 404
        response = None
    else :
        code = 200
        try :
            qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                PREFIX ex: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

                                SELECT ?pollution_level ?type
                                    WHERE { ?type rdf:type ex:""" + moyen + """.
                                    ?type ex:pollution_level ?pollution_level.}""")
            response = str(list(qres)[0].asdict()['pollution_level'])
        except :
            code = 503
            response = None
    return {"code":code,"response":response}





def get_pollution(moyen):
    if moyen == '':
        code = 404
        response = None
    else :
        code = 200
        try :
            qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                PREFIX ex: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

                                SELECT ?pollution_level ?type
                                    WHERE { ?type rdf:type ex:""" + moyen + """.
                                    ?type ex:pollution_level ?pollution_level.}""")
            response = str(list(qres)[0].asdict()['pollution_level'])
        except :
            code = 503
            response = None
    return {"code":code,"response":response}


def day_statistics(moyen):
    if moyen == '':
        code = 404
        response = None
    else :
        code = 200
        try :
            qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX owl: <http://www.w3.org/2002/07/owl#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                            PREFIX xd: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

                            SELECT ?personne
                            WHERE {
                                        ?personne rdf:type xd:Person.
                                        ?personne xd:commutewith xd:""" + moyen + """.
                            }""")
            stat = len(list(qres))
            if stat == 0 :
                response = []
                response.append({"moyen":moyen,"statistic":stat})
                qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX owl: <http://www.w3.org/2002/07/owl#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                            PREFIX ex: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

                            SELECT ?pollution_level ?type
                                WHERE { ?type rdf:type ex:"""+moyen+""".
                                ?type ex:pollution_level ?pollution_level}""")
                for row in qres:
                    moyen = str(row.asdict()['type']).split("#")[1]
                    qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                    PREFIX xd: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

                                    SELECT ?personne
                                    WHERE {
                                                ?personne rdf:type xd:Person.
                                                ?personne xd:commutewith xd:""" + moyen + """.
                                    }""")
                    stat = len(list(qres))
                    response.append({"moyen":moyen,"statistic":stat})

        except :
            code = 503
            response = None
    return {"code":code,"response":response}



def individu_transports(individu):
    #TODO : GET DATA OF EACH TRANSPORT
    code = 200
    if individu == '':
        code = 404
        transports = None
    else :
        try :
            qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX owl: <http://www.w3.org/2002/07/owl#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                            PREFIX xd: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

                            SELECT ?object
                                WHERE { xd:""" + individu + """ xd:commutewith ?object}""")
            transports = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres)]
        except :
            code = 503
            transports = None
    return {"code":code,"response":transports}



def get_location(location):
    source = None
    if location == '':
        code = 404
        response = None
    else :
        code = 200
        try :
            response = wikipedia.summary(location)
            source = "wikipedia"
        except :
            code = 503
            response = None
    return {"code":code,"response":response,"source":source}


@app.route('/', methods = ['GET', 'POST'])
def home_page():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect((url_for('search_results', query=form.search.data)))
    output = moyen_transports()
    individus = ['Olaf','Marie','Alexis']
    if output['code'] == 200:
        return render_template('index.html' , transports = output["response"],individus = individus,form=form)
    elif output['code'] == 404:
        return render_template('404.html')
    else:
        return render_template('503.html')

@app.route('/transport/<title>', methods = ['GET'])
def template_transport(title):
    output = get_pollution(title)
    statistics = day_statistics(title)
    if output['code'] == 200 :
        pollution = output['response']
    else :
        pollution = str(0)
    print(statistics)
    if statistics['code'] == 200 :
        response = statistics['response']
    else :
        response = []
    return render_template('template_transport.html', statistics = response ,pollution = pollution , title = title)


@app.route('/individus/<individu>', methods = ['GET'])
def template_individu(individu):
    output = individu_transports(individu)
    if output['code'] == 200 :
        transports = output['response']
    else :
        transports = []
    return render_template('template_individus.html' ,transports = transports , individu = individu)


@app.route('/search_results/<query>')
def search_results(query):
  output = get_location(query)
  source = output['source']
  content = output['response']
  return render_template('search_results.html', query=query, content=content,source=source)


#app.run() #host= '0.0.0.0')
#app.run(threaded=True, port=5000)
