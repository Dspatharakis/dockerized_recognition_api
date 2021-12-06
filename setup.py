from distutils.core import setup

setup(
    name='Edge server package',
    version='0.1',
    packages=['edge_server'],
    entry_points={
        'console_scripts': [
            'edge-server = edge_server.edge_server:main',
            'edge-server-client = edge_server.post:main',
        ],
    },
)
