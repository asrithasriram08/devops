# Exercise 9 - Jenkins Multi-Stage Pipeline

This pipeline builds a small Flask application, runs its unit test, and
deploys the application source to the workspace directory
`python-app-deploy`.

Create a Jenkins Pipeline job using **Pipeline script from SCM**, select Git,
and point it at this repository. Jenkins must have Python 3 and pip available
on its agent.

The stages are:

1. **Build** - installs the pinned Flask dependency.
2. **Test** - runs `unittest`.
3. **Deploy** - copies the application and dependency manifest to the mock
   deployment directory.

Run the same checks locally with:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s .
```
