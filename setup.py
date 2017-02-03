from distutils.core import setup

setup(name='kadro',
      version='0.1',
      description='Pandas Wrapper with Composable Grammar Support',
      author='Vincent D. Warmerdam',
      author_email='vincentwarmerdam@gmail.com',
      url='https://github.com/koaning/kadro',
      packages=['kadro',],
      install_requires=['pandas', 'numpy', 'pytest'],)