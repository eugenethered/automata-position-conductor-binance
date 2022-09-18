import requests
from dotenv import dotenv_values

DOCKER_REGISTRY_RELEASE_TAG_INFO_URL = 'https://hub.docker.com/v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}'


def get_env_value(key):
    config = dotenv_values('.env')
    return config[key]


def get_docker_namespace_name():
    return get_env_value('DOCKER_NAMESPACE')


def get_docker_repository_name():
    return get_env_value('DOCKER_REPOSITORY')


def get_current_version():
    return get_env_value('VERSION')


def get_released_version(version):
    url = DOCKER_REGISTRY_RELEASE_TAG_INFO_URL.format(namespace=get_docker_namespace_name(), repository=get_docker_repository_name(), tag=version)
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        json_payload = response.json()
        tag_active = json_payload['tag_status']
        if tag_active:
            return version
        return None


def normalize_version(version):
    return 0 if version is None else float(version)


if __name__ == '__main__':
    current_version = get_current_version()
    released_version = get_released_version(current_version)
    if normalize_version(current_version) > normalize_version(released_version):
        print('RELEASE_TO_DOCKER_REGISTRY=true')
    else:
        print('RELEASE_TO_DOCKER_REGISTRY=false')
