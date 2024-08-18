
### Method A
```python
# tracks = ma.load_data("track") # None
# https://github.com/Marsilea-viz/marsilea/blob/main/scripts/example_figures/tracks.py
# Please downlaod data from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE137105
```

### Method B
```
save_pdata_path = Path("data/GSE137105_RAW/pdata.ftr")
pdata = pd.read_feather(save_pdata_path)
```
