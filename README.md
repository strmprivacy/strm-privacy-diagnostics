 # STRM Privacy Diagnostics


This package contains diagnostics for your data, by means of computing k-Anonymity, l-Diversity and t-Closeness.

You can compute the scores by passing your data and indicating which columns are quasi-identifiers and sensitive attributes. 

A 'quasi identifier' is a data attribute on an individual that together with other attributes could identify them. E.g. your length probably doesn't discern you from a larger group of people, but the combination of your length, age and city of birth will if someone has some knowledge about you.

A 'sensitive attribute' is a sensitive data point, like a specific medical diagnosis or credit score.  

## Framework
You can use this package in the context of data privacy and -security frameworks, such as NIST, SOC2 or ISO 27001/27701. 

### NIST Privacy Framework
Leverage this package in the NIST Privacy Framework for the following sub-categories:
- CT.DP-P1: Data are processed in an unobservable or unlinkable manner (e.g., data actions take place on local devices, privacy-preserving cryptography).
- CT.DP-P2: Data are processed to limit the identification of individuals (e.g., de-identification privacy techniques, tokenization).

### ISO 27001 / 27701
We're doing an inventory of the sections in ISO 27001 / 27701 for which Privacy Diagnostics can be helpful - stay tuned!

### SOC2 type I/II
We're exploring the relevant categories in SOC2 type I/II for which you can leverage this Privacy Diagnostics package - stay tuned!

## Installation
Install the package via Pip:

```
pip install strmprivacy-diagnostics
```

## Usage
Simply import the package and
* point it to your input data
* calculate the statistics by passing the quasi identifiers and sensitive attributes
* print a report by passing the quasi identifiers and sensitive attributes

```python
from strmprivacy.diagnostics import PrivacyDiagnostics

# create an instance of the diagnostics class
d = PrivacyDiagnostics("/path/to/csv")

# calculate the statistics
d.calculate_stats(
    qi=['qi1', 'qi2', ...],  # names of quasi identifier columns,
    sa=['sa1', 'sa2', ...],  # names of sensitive attributes
)

# create report
d.create_report(
    qi=['qi1', 'qi2', ...],  # names of quasi identifier columns,
    sa=['sa1', 'sa2', ...],  # names of sensitive attributes
)

d.stats
>>> {'k': xxx, 'l': {'col1': xxx, ...}, 't': xxx}
```
