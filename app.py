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
    qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX ex: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>
                    SELECT ?subject
                    	WHERE { ?subject rdfs:subClassOf ex:moyen_transports}""")
    transports = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres)]
    return {"data":transports}


@app.route('/api/individu_transports', methods=['GET'])
def individu_transports():
    individu = request.args.get('individu')
    if individu == '':
        return {"data":'Please input the correct name of a person'}
    qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX xd: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

        SELECT ?object
            WHERE { xd:""" + individu + """ xd:commutewith ?object}""")
    transports = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres)]
    #TODO : GET DATA OF EACH TRANSPORT
    return {"data":transports}

@app.route('/api/statistics', methods=['GET'])
def day_statistics():
    qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX xd: <http://www.semanticweb.org/clementsiegrist/ontologies/2021/0/pub-transportation#>

                    SELECT ?personne
                    WHERE {
                                ?personne rdf:type xd:Person.
                                ?personne xd:commutewith xd:Uber.
                    }""")
    # TODO : Add filter about days
    return {"data":len(list(qres))}




app.run() #host= '0.0.0.0')
