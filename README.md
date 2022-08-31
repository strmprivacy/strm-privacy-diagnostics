# STRM Privacy Diagnostics


This package contains diagnostics for you data, by means of k-Anonymity, l-Diversity and t-Closeness

## Installation


```
pip install strmprivacy-diagnostics
```

## Usage


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
```