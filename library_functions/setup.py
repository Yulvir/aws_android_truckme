from setuptools import setup, find_packages

setup(name='library_functions',
      python_requires='>=3',
      version='1.0.0',
      description='library functions',
      url='http://github.com/user/example',
      license='Truckme',
      author='Truckme',
      author_email='null@example.com',
      packages=find_packages(),
      install_requires=['boto3', 'qrcode', 'awscli', 'pillow', 'hurry.filesize'],
      zip_safe=False)
