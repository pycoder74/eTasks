import os
def install_package(packagename):
    install=f'cmd /k pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org {packagename}'
    os.system(install)
    print(f'{packagename} installed')
if __name__ == '__main__':
    mod = input('Module: ')
    install_package(mod)
