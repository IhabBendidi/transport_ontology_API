# Public Transport Ontology Project

### Installation :

On the root folder of the project, run on terminal :

```
pip3 install -r requirement.txt
```

### Usage :

To launch the app, on the root folder of the project, run on terminal :

```
python3 app.py
```

A front end of the web app is accessible at `http://127.0.0.1:5000`

### APIs to use :

```
curl -X GET 'http://127.0.0.1:5000/api/moyen_transports'
```


```
curl -X GET 'http://127.0.0.1:5000/api/individu_transports?individu=Alexis'
```


```
curl -X GET 'http://127.0.0.1:5000/api/statistics?moyen=Uber'
```


```
curl -X GET 'http://127.0.0.1:5000/api/pollution?moyen=bus'
```


```
curl -X GET 'http://127.0.0.1:5000/api/get_details?location=eiffel+tower'
```
