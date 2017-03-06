PhotosynQ | Python
=====================

[![Build Status](https://travis-ci.org/Photosynq/PhotosynQ-Python.svg?branch=master)](https://travis-ci.org/Photosynq/PhotosynQ-Python)

Truly Collaborative Plant Research
----------------------------------

**[PhotosynQ]** helps you to make your plant research more efficient. For advanced analysis, this package allows you to pull data right into **[Python]**.

New python users should consider installing **[Anaconda]** which includes both the python interpreter and the **[Jupyter]**  python editor.

For advanced users, we recommend using **[Spyder]** to edit and run python code. 

***

### Installation
Install using pip in the terminal.

```bash
pip install git+https://github.com/Photosynq/PhotosynQ-Python.git
```

***

### Getting started
* A user account on **[PhotosynQ]** is required

#### Standard usage
Retrieve project data and meta-data in a convenient **[DataFrame]**
```py
import photosynq_py as ps

# use your photosynq account to login (you will be prompted for your password)
email = "john.doe@domain.com"
ps.login(email)

# retrieve a dataframe with data from the given project ID
projectId = 1224
df = ps.get_project_dataframe(projectId, include_raw_data=False)

# logout
ps.logout();
```

#### Other Functions

Advanced users can retrieve project data and meta-data/info separately, as **[json]** strings.

`getProjectInfo`, `getProjectData` and `buildProjectDataFrame` (below) are components of `getProjectDataFrame` (above)
```py
ps.login( "john.doe@domain.com" )
projectId = 1224
info = ps.get_project_info(projectId)
data = ps.get_project_data(projectId, include_raw_data=False)
df = ps.buildProjectDataFrame(info, data)
ps.logout()
```
[DataFrame]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html "DataFrame"

[PhotosynQ]: https://photosynq.org "PhotosynQ"

[Python]: https://www.python.org/ "Python"

[Jupyter]: http://jupyter.org/ "Jupyter"

[Anaconda]: https://www.continuum.io/downloads "Anaconda"

[DataFrame]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html "DataFrame"

[PhotosynQ R package]: https://github.com/Photosynq/PhotosynQ-R "PhotosynQ R package"

[json]: http://www.json.org/ "json"

[Spyder]: https://pythonhosted.org/spyder/ "Spyder, the Scientific PYthon Development EnviRonment"