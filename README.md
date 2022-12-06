# Data Viz competition

This is a repository for the data visualization competition. The goal is to create a visualization of the data in the `data` folder. The data is a list of all the bike accidents that have occured in France from 2005 to 2018. The data is in the form of a CSV file.

## Project structure
### Exploratory analysis
The exploratory analysis is in the `exploratory_analysis` folder. It contains a Jupyter notebook that has been converted to HTML and PDF. The notebook is in English but can be translated to French on demand.

### Dashboard
The dashboard is in the root folder. It contains a Python file that contains the dashboard. The notebook is in English but can be translated to French on demand.

## How to run the dashboard
The dashboard is a Python file that uses streamlit. To run the dashboard, you need to install streamlit. The easiest way is to duplicate the environment we used. You can do so by running the following command in your terminal:

```bash
conda create -n viz -f environment.yml
```

Then, you can run the dashboard by running the following command in your terminal (with the project as cd):
    
```bash
streamlit run dashboard.py
```

It should open a new tab in your browser with the dashboard. If not, you can go to `localhost:8501` in your browser.