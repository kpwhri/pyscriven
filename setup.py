from distutils.core import setup
import setuptools

setup(name='pyscriven',
      version='0.0.1',
      description='Simplify report-building by programmatically constructing documents.',
      url='https://github.com/kpwhri/pyscriven',
      author='dcronkite',
      author_email='dcronkite@gmail.com',
      license='MIT',
      classifiers=[  # from https://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3 :: Only',
          'License :: OSI Approved :: MIT License',
      ],
      keywords='data science table report',
      entry_points={
          'console_scripts':
              [
              ]
      },
      install_requires=['matplotlib', 'pytablewriter'],
      package_dir={'': 'src'},
      packages=setuptools.find_packages('src'),
      zip_safe=False
      )
