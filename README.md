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

#### Standard usage
Retrieve project data and meta-data in a convenient **[DataFrame]**
```py
import photosynq_py as ps

# use your photosynq account to login (you will be prompted for your password)
email = "john.doe@domain.com"
ps.login( email )

# retrieve a dataframe with data from the given project ID
projectId = 1224
df = ps.getProjectDataFrame( projectId, include_raw_data = False )

# logout
ps.logout();
```

#### Other Functions

Advanced users can retrieve project data and meta-data/info separately, as **[json]** strings.

`getProjectInfo`, `getProjectData` and `buildProjectDataFrame` (below) are components of `getProjectDataFrame` (above)
```py
ps.login( "john.doe@domain.com" )
projectId = 1224
info = ps.getProjectInfo( projectId )
data = ps.getProjectData( projectId, include_raw_data = False )
df = ps.buildProjectDataFrame( info, data )
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