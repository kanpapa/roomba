from setuptools import setup

package_name = 'dispvolt'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kanpapa',
    maintainer_email='kanpapa@kanpapa.com',
    description='The node that displays the Roomba\'s battery voltage on the Roomba\'s LED.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dispvolt_node = dispvolt.dispvolt_node:main'
        ],
    },
)
