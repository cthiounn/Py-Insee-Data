.. role:: raw-html-m2r(raw)
   :format: html

Introduction to pynsee package
==============================

**Work in progress**

.. image:: https://github.com/InseeFrLab/Py-Insee-Data/actions/workflows/master.yml/badge.svg
   :target: https://github.com/InseeFrLab/Py-Insee-Data/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/InseeFrLab/pynsee/branch/master/graph/badge.svg?token=TO96FMWRHK
   :target: https://codecov.io/gh/InseeFrLab/Py-Insee-Data?branch=master
   :alt: Codecov test coverage

.. image:: https://readthedocs.org/projects/pynsee/badge/?version=latest
   :target: https://pynsee.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

``pynsee`` package contains tools to easily download data and metadata from INSEE APIs and website.

``pynsee`` gives a quick access to more than 150 000 macroeconomic series,
a dozen datasets of local data, numerous sources available on <https://www.insee.fr>
as well as key metadata and SIRENE database containing data on all French companies.
Have a look at the detailed API page with the following `link <https://api.insee.fr/catalogue/>`_.
This package is a contribution to reproducible research and public data transparency. 
It benefits from the developments made by INSEE's teams working on APIs.

Installation & API subscription
-------------------------------

The dataset available on <https://www.insee.fr> do not require authentication.
Credentials are necessary to access some of the APIs available on `pynsee`. 
API credentials can be created <https://api.insee.fr/catalogue/>

.. code-block:: python

   # Get the development version from GitHub
   # git clone https://github.com/InseeFrLab/Py-Insee-Data.git
   # cd Py-Insee-Data
   # pip install .

   # Subscribe to api.insee.fr and get your credentials!
   # Save your credentials with init_conn function :      
   from pynsee.utils.init_conn import init_conn
   init_conn(insee_key="my_insee_key", insee_secret="my_insee_secret")

   # Beware : any change to the keys should be tested after having cleared the cache
   # Please do : from pynsee.utils import clear_all_cache; clear_all_cache()

Data Search and Collection Advice
---------------------------------

Regarding APIs: 

* **Macroeconomic data** :
   First, use ``get_dataset_list`` to search first among the datasets.
   Alternatively, you can make a keyword-based search with ``search_macrodata``, e.g. ``search_macrodata('GDP')``.
   Then, get the data with ``get_dataset`` or ``get_series``
* **Local data** : use first ``get_local_metadata``, then get data with ``get_local_data``
* **Metadata** : e.g. function to get the classification of economic activities (Naf/Nace Rev2) ``get_activity_list`` 
* **Sirene (French companies database)** : use first ``get_all_columns``, and then use ``search_sirene``

Regarding data that can be downloaded directly from the website, the main entry point is ``telechargerDonnees``:

.. code-block:: python

   from pynsee.download import telechargerDonnees
   df = telechargerDonnees("FILOSOFI_COM", date = "2015")


For further advice, have a look at the documentation and the examples


French GDP growth rate
----------------------

Below is an example to easily download and represent French GDP growth series

.. image:: https://raw.githubusercontent.com/InseeFrLab/Py-Insee-Data/master/docs/examples/pictures/example_gdp_picture.png?token=AP32AXOVNXK5LWKM4OJ5THDAZRHZK
.. code-block:: python

   from pynsee.macrodata import *
  
   import pandas as pd
   import matplotlib.ticker as ticker
   import matplotlib.pyplot as plt

   # Subscribe to api.insee.fr and get your credentials!
   # Save your credentials with init_conn function :      
   from pynsee.utils.init_conn import init_conn
   init_conn(insee_key="my_insee_key", insee_secret="my_insee_secret")

   # Beware : any change to the keys should be tested after having cleared the cache
   # Please do : from pynsee.utils import clear_all_cache; clear_all_cache()

   # get macroeconomic datasets list
   insee_dataset = get_dataset_list()

   # get series key (idbank), for Gross domestic product balance
   id = get_series_list("CNT-2014-PIB-EQB-RF")

   id = id.loc[(id.FREQ == "T") &
               (id.OPERATION == "PIB") &
               (id.NATURE == "TAUX") &
               (id.CORRECTION == "CVS-CJO")]

   data = get_series(id.IDBANK)

   data = split_title(df = data, n_split=2)

   # define plot
   ax = data.plot(kind='bar', x="TIME_PERIOD", stacked=True, y="OBS_VALUE", figsize=(15,5))
   #add title
   plt.title("French GDP growth rate, quarter-on-quarter, sa-wda")
   # customize x-axis tickers
   ticklabels = ['']*len(data.TIME_PERIOD)
   ticklabels[::12] = [item for item in data.TIME_PERIOD[::12]]
   ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
   plt.gcf().autofmt_xdate()
   #remove legend
   ax.get_legend().remove()
   #remove x-axistitle
   ax.xaxis.label.set_visible(False)
   plt.show()

Poverty in Paris urban area
---------------------------

Below is an example to easily download and represent French GDP growth series

.. image:: https://raw.githubusercontent.com/InseeFrLab/Py-Insee-Data/master/docs/examples/pictures/poverty_paris_urban_area.svg?token=AP32AXNFHNAH2NEK2LKWENTAZO7YY

.. code-block:: python
   
   # Subscribe to api.insee.fr and get your credentials!
   # Save your credentials with init_conn function :      
   from pynsee.utils.init_conn import init_conn
   init_conn(insee_key="my_insee_key", insee_secret="my_insee_secret")

   # Beware : any change to the keys should be tested after having cleared the cache
   # Please do : from pynsee.utils import clear_all_cache; clear_all_cache()

   from pynsee.localdata import *

   import pandas as pd
   import matplotlib.cm as cm
   import matplotlib.pyplot as plt
   import descartes
   import geopandas as gpd

   # get a list all data available : datasets and variables
   metadata = get_local_metadata()

   # geographic metadata
   nivgeo = get_nivgeo_list()

   # get geographic area list
   area = get_area_list()

   # get all communes in Paris urban area
   areaParis = get_included_area('unitesUrbaines2020', ['00851'])

   # get selected communes identifiers
   code_com_paris = areaParis.code.to_list()

   # get numeric values from INSEE database
   dataParis = get_local_data(dataset_version='GEO2020FILO2017',
                          variables =  'INDICS_FILO_DISP_DET',
                          nivgeo = 'COM',
                          geocodes = code_com_paris)

   #select poverty rate data, exclude paris commune
   data_plot = dataParis.loc[dataParis.UNIT=='TP60']
   data_plot = data_plot.loc[data_plot.CODEGEO!='75056']

   #get communes limits
   map_com = gpd.read_file(get_map_link('communes'))
   map_arr_mun = gpd.read_file(get_map_link('arrondissements-municipaux'))
   map_idf = pd.concat([map_com, map_arr_mun])

   # merge values and geographic limits
   mapparis = map_idf.merge(data_plot, how = 'right',
                        left_on = 'code', right_on = 'CODEGEO')

   #plot
   fig, ax = plt.subplots(1,1,figsize=[15,15])
   mapparis.plot(column='OBS_VALUE', cmap=cm.viridis,
       legend=True, ax=ax, legend_kwds={'shrink': 0.3})
   ax.set_axis_off()
   ax.set(title='Poverty rate in Paris urban area in 2017')
   plt.show()
   fig.savefig('poverty_paris_urban_area.svg',
               format='svg', dpi=1200,
               bbox_inches = 'tight',
               pad_inches = 0)


How to avoid proxy issues ?
---------------------------

.. code-block:: python

   # Use the proxy_server argument of the init_conn function to change the proxy server address   
   from pynsee.utils.init_conn import init_conn
   init_conn(insee_key="my_insee_key",
             insee_secret="my_insee_secret",
             proxy_server="http://my_proxy_server:port")

   # Beware : any change to the keys should be tested after having cleared the cache
   # Please do : from pynsee.utils import *; clear_all_cache()

Support
-------

Feel free to open an issue with any question about this package using <https://github.com/InseeFrLab/Py-Insee-Data> Github repository.

Contributing
------------

All contributions, whatever their forms, are welcome. See ``CONTRIBUTING.md``
