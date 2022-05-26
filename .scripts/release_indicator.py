import os
import requests


SETUP_CFG_FILE = f'{os.getcwd()}/setup.cfg'
RELEASE_INFO_URL = 'https://pypi.org/pypi/{module}/json'


def read_from_file(file_path):
    with open(file_path, 'r') as data_file:
        return data_file.readlines()


def get_setup_value(setup_key):
    file_contents = read_from_file(SETUP_CFG_FILE)
    value = [line for line in file_contents if line.find(setup_key) >= 0]
    normalized_value = value[0].replace('\n', '').replace(' = ', '=').replace(f'{setup_key}=', '')
    return normalized_value


def get_module_name():
    return get_setup_value('name')


def get_current_version():
    return get_setup_value('version')


def get_released_version():
    url = RELEASE_INFO_URL.format(module=get_module_name())
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        json_payload = response.json()
        latest_released_version = json_payload['info']['version']
        return latest_released_version


def normalize_version(version):
    return 0 if version is None else int(version.replace('.', ''))


if __name__ == '__main__':
    current_version = get_current_version()
    released_version = get_released_version()
    if normalize_version(current_version) > normalize_version(released_version):
        print('RELEASE_TO_PIPY=true')
    else:
        print('RELEASE_TO_PIPY=false')
