from dotenv import dotenv_values


def get_env_value(key):
    config = dotenv_values('.env')
    return config[key]


def get_docker_repository_name():
    return get_env_value('DOCKER_REPOSITORY')


if __name__ == '__main__':
    print(f'RELEASE_DOCKER_REPOSITORY={get_docker_repository_name()}')
