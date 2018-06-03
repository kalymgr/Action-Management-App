from setuptools import find_packages, setup

setup(
    name='actionmanagementapp',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,  # used to include templates, css etc. Data are declared in MANIFEST.in
    zip_safe=False,
    install_requires=[
        'flask', 'SQLAlchemy', 'pymysql'
    ],
)
