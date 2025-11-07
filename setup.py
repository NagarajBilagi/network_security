from setuptools import find_packages, setup
from typing import List

"""This setup module used to build and distribute Python packages. 
It typically contains information about the package, 
such as its name, version, and dependencies, 
as well as instructions for building and installing the package"""


def get_Requirements():
    """
    this function returns the list of requirements 
    """
    requirement_list = []

    try:    
        with open ("requirements.txt","r") as file:
            lines= file.readlines()
            print('lines:', lines)
            for line in lines:
                requirement = line.strip()
                print('requirement :', requirement)
                if requirement and requirement!= '-e .':
                    requirement_list.append(requirement)

    
    except FileNotFoundError :
        print("requirements.txt file not found")

    return requirement_list

# this function is used to define metadata and configuration for the package   
setup(name= "Network Security",
      version= "0.0.1",
      packages= find_packages(),                            #Locates all the packages present in this project
      install_requires = get_Requirements(),           
      author= "Nagaraj",
      author_email="nagarajbilagi@gmail.com"
      )
                   

            
                    





    