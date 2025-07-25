from setuptools import find_packages, setup

package_name = 'advanced_task'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='orin_nano1',
    maintainer_email='giordanoschool@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rgb_publisher   = advanced_task.RGB_publisher:main',
            'llm_integration = advanced_task.LLM_integration:main',
        ],
    },
)
