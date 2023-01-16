import store
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/')
def get_list():
    return [1,2,3]

@app.get('/contact', response_class=HTMLResponse)
def get_list():
    return '''
        <head>
            <title>My webpage</title>
        </head>
        <body style='background-color: blue;'>
            <h1 style='color:rgb(100,100,100);'>Welcome to my webpage!</h1>
            <p style='color:rgb(255,0,0);'>This is some text on my webpage.</p>
            <ul>
                <li style=color:rgb(0,255,0);>Item 1</li>
                <li style=color:rgb(0,255,0);>Item 2</li>
                <li style=color:rgb(0,255,0);>Item 3</li>
            </ul>
            <img src='Mexico.png' alt='Link' width='50%' height='50%'>
        </body>
        '''
    #return {'name': 'William','name':'Evelyn Tonta'}


#@app.get('/contact2', response_class=HTMLResponse)
#def get_list():
    #return '''
        ##<h1>Solo hice esta pagina para llamar tonta a Evelyn.</h1>
        ##<title>Tu cuenta</title>
        ##<p>Soy un parrafo de prueba, pero lo anterior es cierto.</p>
        #'''

#def run():
    #store.get_users()

if __name__ == '__main__':
    run()