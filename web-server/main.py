import store
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def get_list():
    return [1,2,3]

@app.get('/contact', response_class=HTMLResponse)
def get_list():
    return '''
        <h1>Solo hice esta pagina para llamar tonta a Evelyn.</h1>
        <p>Soy un parrafo de prueba, pero lo anterior es cierto.</p>
        '''
    #return {'name': 'William','name':'Evelyn Tonta'}

def run():
    store.get_users()

if __name__ == '__main__':
    run()