"""
Photosynq-Python

This package allows you to login to the photosynq API and retrieve project data in the form of a DataFrame.

See :func:`~photosynq_py.auth.login`
See :func:`~photosynq_py.buildDataFrame.getProjectDataFrame`

See the online readme for more information: https://github.com/Photosynq/PhotosynQ-Python

"""
from photosynq_py.auth import login, logout
from photosynq_py.getJson import getProjectData, getProjectInfo
from photosynq_py.buildDataFrame import getProjectDataFrame, buildProjectDataFrame