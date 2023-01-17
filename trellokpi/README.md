# Trello API Project

To run the program, you have to follow the next instructions in the terminal:

```sh
cd py-project
cd trellokpi
python3 -m venv trello
source trello/bin/activate
pip3 install requirements.txt
python3 gettrellodata.py
python3 main.py
```

This will create a .csv with the data from the Trello API, then, running main.py will create an image with a bar chart of the members of a specific board.