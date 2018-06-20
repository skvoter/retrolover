from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='retrolover',
      version='1.0.1',
      description='Tool for downloading ROMS for your retropie',
      python_requires='>=3',
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3 :: Only',
      ],
      url='https://github.com/skvoter/retrolover',
      author='Kirill Korovin',
      author_email='skvoter46@gmail.com',
      packages=['retrolover'],
      install_requires=[
          'beautifulsoup4',
          'requests'
      ],
      entry_points={
          'console_scripts': ['retrolover=retrolover.retrolover:main'],
      },
      include_package_data=True,
      zip_safe=False)
