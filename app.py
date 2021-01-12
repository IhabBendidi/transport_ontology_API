import flask
import rdflib
from flask import request

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = "data"
app.config["DEBUG"] = True

g = rdflib.Graph()
#g.parse("data/pub-transportation.owl.rdf")

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
    # TODO : Add filter about days
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




@app.route('/api/pollution', methods=['GET'])
def get_pollution():
    # TODO : Add filter about days
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


app.run() #host= '0.0.0.0')
