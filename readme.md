# Chat software(python)

## Lab environment
Language：Python  
Interpreter: Python 3.10 
Python package:
```
pandas=1.4.3
```
测试本程序的时候请尽可能安装不低于上述版本的Python包。

## Instruction
This program needs to run the `server.py` file first. Then run the `client.py` file, and multiple `client.py` can be run at the same time. For the convenience of testing, you can first use `main.py` to register users and modify user information, or you can directly use the username and password under `src/database/user.csv`.
Open a terminal:
```
python server/server.py
python client/client.py
python main.py
```
After the server runs successfully, it prompts:
```
Server is running at 127.0.0.1:6666
```
After the client runs successfully, the login window appears.