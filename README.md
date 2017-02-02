# PhotosynQ-Python

Install using pip
```bash
pip install git+https://github.com/Photosynq/PhotosynQ-Python.git
```

Example Usage
```py
from photosynq_py import *
login()
projectId = 1224
info = getProjectInfo( projectId )
data = getProjectData( projectId )
logout()
```