from setuptools import find_packages,setup
from typing import List

def get_requirements() -> List:
    """
    This function will return list of requirements

    """
    package_list: List[str] = []
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()
            for line in lines:
                required_package = line.strip()
                # ignore empty lines and -e .
                if required_package and required_package != '-e .':
                    package_list.append(required_package)
    
    except FileNotFoundError:
        print("requirements.txt not found!")
    
    return package_list

# print(get_requirements())

setup(
    name="Network Security",
    version="0.1",
    author="Kunal Srivastav",
    packages=find_packages(),
    install_requires=get_requirements()
)

