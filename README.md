# Fast API study case

## Set up local environment

### Create python virtual environment (venv)

Run the commands below to create a `venv` and activate it.

```bash
python3 -m venv .venv  
source .venv/bin/activate
```

Installing the requirements
```bash
pip3 install -r requirements.txt
```
Note: It's necessary to go to the folder
To Run the server using uvicorn
```bash
uvicorn main:app
```

To Run the server using python
```bash
python main.py
```

### To create the table courses go to class03 and run:
```bash
python create_tables.py
```

