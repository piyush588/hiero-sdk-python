from setuptools import setup, find_packages

setup(
    name='Hedera-Python-Sdk',
    version='0.1.0',
    description='A mini Hedera SDK in Python',
    author='Nadine Loepfe',
    author_email='nadine.loepfe@hashgraph.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'grpcio',
        'grpcio-tools',
        'cryptography',
        'protobuf==5.27.2',
        'cryptography',
        'python-dotenv'
    ],
)
