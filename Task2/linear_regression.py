import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import seaborn as sns
from sklearn.model_selection import train_test_split
import numpy as np


#We have here very big data. What i am willing to do is to compare each column in our dataset with SalePrice and which
#one has biggest correlation i will perform regression analysis with them, plot some graphs and extract the coefficients of
#the model. I will make some commends about it.



pd.set_option('display.expand_frame_repr', False)

housing_data = pd.read_csv("housing_price_data.csv")
print(housing_data.info())

# Find correlation for each column with sale price column
correlation_info = {}
for col in housing_data.columns:
    if col == "Id":
        continue

    if housing_data[col].dtype != "int64" and housing_data[col].dtype != "float64":
        continue

    housing_data = housing_data[housing_data[col].notna()]

    corr = pearsonr(housing_data[col], housing_data.SalePrice)
    correlation_info[col] = corr


srt_corr = {k: v for k, v in sorted(correlation_info.items(), key=lambda item: item[1], reverse=True)}
print(srt_corr)

#Here we can see clearly what kind of features has biggest correlation with the SalePrice of the property. I will use the
#biggest first two for my regression model, which is 'OverallQual' and 'GrLivArea'.


biggest_corr_features = list(srt_corr.keys())[1:3]
print(biggest_corr_features)


#I will split the data 80:20, to be able to compare with the present values. Is it my model working good????

train, test = train_test_split(housing_data, test_size=0.2)
print(train)
print(test)

#Multiple regression with the first two features with the biggest correlation

x = train[biggest_corr_features]
y = train['SalePrice'].to_numpy()
print(x)
print(y)

x = sm.add_constant(x)
model = sm.OLS(y, x)
result = model.fit()

print(result.summary())
print(result.params)
r2 = result.rsquared

params = result.params.tolist()

validation_data = pd.DataFrame(columns=["intercept", "quality_coeff", "living_area_coeff", "quality", "area",
                                        "actual_price"])

validation_data["quality"] = test.OverallQual
validation_data["area"] = test.GrLivArea
validation_data["actual_price"] = test.SalePrice
validation_data["intercept"] = params[0]
validation_data["quality_coeff"] = params[1]
validation_data["living_area_coeff"] = params[2]
validation_data["predicted_price"] = validation_data.intercept + validation_data.quality_coeff * validation_data.quality +\
    validation_data.living_area_coeff * validation_data.area

print(validation_data)
actual_price = np.asarray(validation_data.actual_price)
predicted_price = np.asarray(validation_data.predicted_price)

plt.scatter(x=actual_price, y=predicted_price)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title(f"R-squared: {r2:.2f}")
sns.regplot(x=actual_price,y=predicted_price,ci=None, scatter_kws={"color": "black"}, line_kws={"color": "red"})
plt.savefig("Scatter plot")
plt.show()

plt.plot(actual_price - predicted_price)
plt.title("Residuals")
plt.savefig("Residuals plot")
plt.show()

# From the summary method we can see all need information about our model. As we can see, we have here R-squared of 0.70,
# which means that 70 percent of the actual values ot SalePrice laid down on our best fit line. This is not so bad for me.
# This number varies between 0 and 1, which means that if we have 1 for R-squared value, which in practice it's not
# possible, that's mean that all values a perfectly explained by our model.
# About coefficients:
# Our model generates intercept of -117906.11. The intercept is the value when all of the predictor variables are equal
# to zero. It is good to know this value, but sometimes this does not make sense.In our case if we have 0 quality of our
# house and 0 squared feet, this mean that for this kind of property "they" should give money to us.
# OverallQual coefficient of 35025.69 is telling us that for 1 quality up or down, the price should increase ot decrease
# with that value. It is the same for our living area feature. When these numbers are positive that's mean our slope
# will be upwards.
# From our residual plot, we can see that residuals are static, which is good indication that our model might be good.
