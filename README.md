Clone, build, and isntall package from source

```bash
$ git clone [.git url from the top-right of this bitbucket page] 
$ cd ubspec_processing
$ python setup.py sdist bdist_wheel
& pip install dist/ubspec_processing-0.7.tar.gz
```

Test that the package was installed and see a list of functions

```bash
$ python
>>> import ubspec_processing
>>> dir( ubspec_processing )
>>> quit()
```

Download updates after cloning

```bash
$ git pull
```

Upload changes back to this repo

```bash
& git add .
$ git commit -m "commit message here"
& git push
```