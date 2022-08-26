from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict


pd.set_option('display.expand_frame_repr', False)

housing_data = pd.read_csv("../housing_price_data.csv")
housing_data = housing_data.sort_values("YearBuilt")
housing_data = housing_data.reset_index()
values = housing_data.SalePrice
print(housing_data)

# I will try to perfomr ARIMA model for my model of choice. In order to do that i have to do several steps to be able
# to perform a good ARIMA model


# First we will be using Augmented Dickey-Fuller (ADF) test to check is our data stationary. The Null hypothesis of this test
# is that the data is not stationary, but if the p_value of that test shows value below 0.05, we can reject that null
# hypothesis and say that the data is stationary


p_value = 1
d = 0
while p_value >= 0.05:
    res = adfuller(values.dropna())
    print('Augmented Dickey-Fuller Statistic: %f' % res[0])
    print('p-value: %f' % res[1])
    if res[1] > 0.05:
        values = values.diff()
        d += 1
    p_value = res[1]


values = housing_data.SalePrice
# The Genuine Series
fig, axes = plt.subplots(2, 2)
axes[0, 0].plot(values)
axes[0, 0].set_title('The Genuine Series')
plot_acf(values, ax=axes[0, 1])

# Order of Differencing: First
axes[1, 0].plot(values.diff())
axes[1, 0].set_title('Order of Differencing: First')
plot_acf(values.diff().dropna(), ax=axes[1, 1])
plt.savefig("Data and autocorrelations")
plt.show()


# From this chart we can clearly see that the data become stationary on the first differencing, so our d_value is 1


# No we want to find the 'p' for our ARIMA model, in order to do that we should plot the Partial Autocorrelation. This
# plot below shows us that partial autocorrelation is going extremely fast in negative territory, which  indicating the
# series might have been over differenced, so for that reason we can conclude that 'p' will be equal to 0

figure, axes = plt.subplots(1, 2)
axes[0].plot(values.diff())
axes[0].set_title('Order of Differencing: First')
axes[1].set(ylim=(0, 5))
plot_pacf(values.diff().dropna(), ax=axes[1])
plt.savefig("Partial Autocorrelation")
plt.show()


# How we want to find our 'q' value for our ARIMA model. In order to do that we will ACF plot to find the number of
# Moving Averages term. It is theoretically, the lagged forecast's error. We can see from the plot that our data again
# is going too fast in negative territory, so again we can conclude that the data is stationary and our 'q' value is
# equal to 0


fig1, axes = plt.subplots(1, 2)
axes[0].plot(values.diff())
axes[0].set_title('Order of Differencing: First')
axes[1].set(ylim=(0, 1.2))
plot_acf(values.diff().dropna(), ax=axes[1])
plt.savefig("Autocorrelation")
plt.show()



# Creating our ARIMA models with values p, q, d, which we know from above

mymodel = ARIMA(housing_data.SalePrice, order=(0, 0, 1))
modelfit = mymodel.fit()
print(modelfit.summary())


# Our model is showing that the p values for our coefficients are 0, so we could say than our model is statistically significant


# Plotting Residual Errors
myresiduals = pd.DataFrame(modelfit.resid)
fig2, ax = plt.subplots(1, 2)
myresiduals.plot(title="Residuals", ax=ax[0])
myresiduals.plot(kind='kde', title='Density', ax=ax[1])
plt.savefig("Residuals Error")
plt.show()


# And this is our forecast plot

plot_predict(modelfit)
plt.savefig("Forecast")
plt.show()
