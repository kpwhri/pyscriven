# pyscriven

Simplify report-building by programmatically constructing documents.  

## Getting Started

pyscriven provides an interface for building *.rst (reStructuredText) files, with particular interest in building reports for data science purposes. The `report.rst` file can then be converted to a wide variety of formats using [pandoc](https://pandoc.org).

### Prerequisites

* Python 3.6+
* Packages listed in requirements.txt
    * pytablewriter - building tables
    * matplotlib - include images/graphs/etc.

### Installing

Begin by cloning this repository and then installing the package

```
git clone git@github.com:kpwhri/pyscriven.git
cd pyscriven
python setup.py install
```

## Usage

### Generating a *.rst File
```python
from pyscriven import RestWriter, Table

rst_list = [
    ('heading', 'Example Table'),
    ('table', Table(header=('Term', 'Frequency'),
                    data=[('python', 3), ('anaconda', 2), ('boa', 5)]
    ))
]
with RestWriter(fp=path) as out:
    out.write_all(rst_list)
```

The above code will generate the following `.rst`  document:

```text

==============
Document Title
==============

--------
Subtitle
--------

Example Table
=============

.. table:: 

    +--------+---------+
    |  Term  |Frequency|
    +========+=========+
    |python  |        3|
    +--------+---------+
    |anaconda|        2|
    +--------+---------+
    |boa     |        5|
    +--------+---------+

``` 

### Converting to Other Formats

Specify a format that pandoc specifies it can generate from a `.rst` file. I also like providing a `--table-of-contents` when appropriate.

```python
import pypandoc
pypandoc.convert_file(path, 'docx', outputfile=outpath, 
                      extra_args=['--table-of-contents'])
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/kpwhri/pyscriven/tags). 


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

