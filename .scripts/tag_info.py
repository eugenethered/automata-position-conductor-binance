from dotenv import dotenv_values


def get_env_value(key):
    config = dotenv_values('.env')
    return config[key]


def get_current_version():
    return get_env_value('VERSION')


if __name__ == '__main__':
    print(f'RELEASE_DOCKER_TAG={get_current_version()}')
