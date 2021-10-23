import requests

# Referências sobre o uso do requests:
#
# Fazendo requisições:
# https://docs.python-requests.org/en/master/user/quickstart/#make-a-request
# Usando JSON retornado:
# https://docs.python-requests.org/en/master/user/quickstart/#json-response-content

def version_exists(package_name, version):
    print(package_name)
    data = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    if data.status_code==404:
        return False
    if version in data.json()['releases'].keys():
        return True
    return False

def latest_version(package_name):
    
    print(package_name)
    data = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    print(data.status_code)
    if data.status_code==404:
        return None
    return data.json()['info']['version']

