---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Direct download from insee.fr

**TO BE COMPLETED**

The sources available in this package are all listed
[here](https://inseefrlab.github.io/DoReMIFaSol/reference/liste_donnees.html)

The following packages are necessary to execute the following examples:

```python
import pynsee.download
import pandas as pd
```



## Find years available for a data source

Let's assume we are interested in French census data (codename: `RP_LOGEMENT`). 

All datasets matching a given codename can be retrieved using `millesimesDisponibles`.
They are returned as a dict type and are easily converted into a standard pandas table:

```python
pd.DataFrame(pynsee.download.millesimesDisponibles("RP_LOGEMENT"))
```

## Request dataset from insee.fr website

The easiest approach is to use `telechargerDonnees`