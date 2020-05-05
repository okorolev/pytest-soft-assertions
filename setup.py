from setuptools import setup, find_packages


requirements = [
    'pytest',
    'astor',
    'texttable',
    'pytest-ast-transformer>=1.0.3'
]

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='pytest-soft-assertions',
    version='0.1.1',
    packages=find_packages(exclude=['examples', 'tests']),
    entry_points={
        "pytest11": ["pytest_soft_asserts = pytest_soft_asserts.plugin"],
    },
    install_requires=requirements,
    long_description=readme,
    author='okorolev',
    author_email='johnnyprobel@gmail.com',
    keywords=['pytest', 'ast', 'soft-asserts', 'asserts', 'testing', 'debug'],
    classifiers=[
        "Framework :: Pytest",
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
    ],
    setup_requires=['pytest-runner'],
)
