import os
def install():
    wd = os.getcwd()
    print(wd)
    with open('requirements.txt') as f:
        for i in f.readlines():
            install=f'cmd /k pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org {i}'
            os.system(install)
if __name__ == '__main__':
    install()
