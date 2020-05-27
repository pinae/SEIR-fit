# SEIR-fit
Fit a SEIR model to real data

You can try this without installation in an interactive Jupyter Notebook on: 
https://mybinder.org/v2/gh/pinae/SEIR-fit/master?filepath=SEIR-Plots.ipynb

# Setup

```sh
$ python3 -m venv env
$ source env/bin/activate
$ pip install -U pip wheel
$ pip install -r requirements.txt
```

# Additional setup required for Altair

Generating SVG or PNG files requires that the Selenium driver for your browser is installed, e.g.
`chromedriver`.

For details see the [altair_saver documentation](https://github.com/altair-viz/altair_saver#selenium)
