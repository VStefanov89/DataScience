import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

"""
We have here very big data. What i am willing to do is to find for each column in our dataset, which one has biggest
correlation and with this feature i will perform regression analysis, plot some graphs and extract the coefficients of
the model. I will make some commends about it.
"""


pd.set_option('display.expand_frame_repr', False)



housing_data = pd.read_csv("housing_price_data.csv")
print(housing_data.info())

correlation_info = {}
for col in housing_data.columns:
    print(col)

    if col == "Id":
        continue

    if housing_data[col].dtype != "int64" and housing_data[col].dtype != "float64":
        continue

    housing_data = housing_data[housing_data[col].notna()]

    corr = pearsonr(housing_data[col], housing_data.SalePrice)
    correlation_info[col] = corr


srt_corr = {k: v for k, v in sorted(correlation_info.items(), key=lambda item: item[1], reverse=True)}
print(srt_corr)
"""
Here we can see clearly what kind of features has more correlation with the SalePrice of the property. I will use the
biggest first two for my regression model, which is 'OverallQual' and 'GrLivArea'
"""
biggest_corr_features = list(srt_corr.keys())[1:3]
print(biggest_corr_features)


"""
Multiple regression with the first two features with the biggest correlation
"""

x = housing_data[biggest_corr_features]
y = housing_data['SalePrice'].to_numpy()
print(x)
print(y)

x = sm.add_constant(x)
model = sm.OLS(y, x)
result = model.fit()

print(housing_data)
print(result.params)
print(result.summary())

print(result.resid)
print(result.fittedvalues)
plt.plot(result.resid)
#plt.show()

fig = plt.figure(figsize=(12,8))
fig = sm.graphics.plot_regress_exog(result, 'GrLivArea', fig=fig)
