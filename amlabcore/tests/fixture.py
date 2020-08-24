import uuid
import pytest
import redis
import docker as dockerlib

from amlab.config.tests import REDIS_HOST, REDIS_PORT
from .utils import ping_redis

__all__ = (
    'global_sid',
    'docker',
    'redis_server',
)


@pytest.fixture(scope='session')
def global_sid():
    return uuid.uuid1()


@pytest.fixture(scope='session')
def docker():
    return dockerlib.from_env().api


@pytest.yield_fixture(scope='session')
def redis_server(global_sid, docker):
    docker.pull(f'redis:5.0.9')
    redis_contianer = docker.create_container(
        image=f'redis:5.0.9',
        name=f'test-redis-{global_sid}',
        ports=[REDIS_PORT],
        host_config=docker.create_host_config(
            port_bindings={6379: REDIS_PORT},
            privileged=True
        )
    )
    docker.start(container=redis_contianer['Id'])
    ping_redis(port=REDIS_PORT)
    yield redis.Redis(host='localhost', port=REDIS_PORT, db=0)
    docker.kill(container=redis_contianer['Id'])
    docker.remove_container(container=redis_contianer['Id'])
