# Web Project

To run the local server, you have to follow the next instructions in the terminal:

```sh
cd web-server
python3 -m venv webproject
source webproject/bin/activate
pip3 install -r requirements.txt
uvicorn main:app --reload
```

This will start running a local server using uvicorn, html and FastAPI.