from dotenv import dotenv_values


def get_env_value(key):
    config = dotenv_values('.env')
    return config[key]


def get_docker_namespace():
    return get_env_value('DOCKER_NAMESPACE')


if __name__ == '__main__':
    print(f'RELEASE_DOCKER_NAMESPACE={get_docker_namespace()}')
