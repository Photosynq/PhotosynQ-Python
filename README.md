PhotosynQ | Python
=====================

Truly Collaborative Plant Research
----------------------------------

**[PhotosynQ]** helps you to make your plant research more efficient. For an advanced analysis, this package allows to pull data from projects right into **[Python]**.

New python users should consider installing **[Anaconda]** which includes both the python interpreter and the **[Jupyter]**  python editor.

***

### Installation
Install using pip in the terminal.

```bash
pip install git+https://github.com/Photosynq/PhotosynQ-Python.git
```

***

### Getting started
* A user account for **[PhotosynQ]** is required to access data. 
* We recommend using **[Jupyter]** to edit and run python code.
* Project info and data will be retrieved in the form of json strings, in later versions a function will be provided to convert project data into a convenient **[DataFrame]**, similar to the **[PhotosynQ R package]**


```py
import photosynq_py as ps
```

#### Login (you will be promted to enter your photosynq account information)
```py
ps.login()
```

#### Get Project Information
```py
projectId = 1224
info = getProjectInfo( projectId )
```

#### Get Project Data
```py
projectId = 1224
data = getProjectData( projectId )
```

#### Logout
```py
ps.logout()
```



[PhotosynQ]: https://photosynq.org "PhotosynQ"

[Python]: https://www.python.org/ "Python"

[Jupyter]: http://jupyter.org/ "Jupyter"

[Anaconda]: https://www.continuum.io/downloads "Anaconda"

[DataFrame]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html "DataFrame"

[PhotosynQ R package]: https://github.com/Photosynq/PhotosynQ-R "PhotosynQ R package"