import pandas as pd
from pydataset import data
from sklearn.decomposition import FactorAnalysis
import matplotlib.pyplot as plt
import numpy as np


pd.set_option('display.expand_frame_repr', False)
df = data('bioChemists')
df = df.iloc[1:250]
x = df[['art', 'kid5', 'phd', 'ment']]
print(x)

factor = FactorAnalysis(n_components=2)
x_factor = factor.fit_transform(x)
print(x_factor)

thisdict = {"Single": "0", "Married": "1"}

