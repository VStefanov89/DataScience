import pandas as pd
from sklearn.datasets import load_iris
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity


pd.set_option('display.expand_frame_repr', False)
df = pd.read_csv("dimension_data.csv")
print(df.columns)

# Dropping unnecessary columns
df.drop(['respid', 'On.a.scale.of.zero.to.ten..how.likely.are.you.to.recommend.our.services.to.a.friend.or.colleague.'],axis=1,inplace=True)

# Dropping missing values rows
df.dropna(inplace=True)
print(df.info())


# Bartlett’s test of sphericity checks whether or not the observed variables intercorrelate at all using the observed
# correlation matrix against the identity matrix. If the test found statistically insignificant, you should not employ
# a factor analysis.

chi_square_value,p_value=calculate_bartlett_sphericity(df)
print(chi_square_value, p_value)

# If p_value is above 0.05, that's mean that our dataset is not factorable. In our case that is no true, so we can
# continue with the analysis


# Create factor analysis object and perform factor analysis
fa = FactorAnalyzer()
fa.fit(df, 11)
# Check Eigenvalues
ev, v = fa.get_eigenvalues()
print(ev)

# Create scree plot using matplotlib
plt.scatter(range(1,df.shape[1]+1),ev)
plt.plot(range(1,df.shape[1]+1),ev)
plt.title('Scree Plot')
plt.xlabel('Factors')
plt.ylabel('Eigenvalue')
plt.grid()
plt.show()

fa = FactorAnalyzer(n_factors=3,rotation='varimax')
fa.fit(df)


# Loadings indicate how much a factor explains a variable. The loading score will range from -1 to 1.Values close
# to -1 or 1 indicate that the factor has an influence on these variables. Values close to 0 indicates that the factor
# has a lower influence on the variable.

print(pd.DataFrame(fa.loadings_,index=df.columns))


# Based on this table we can see that:
# - factor0 explains the common variance in people who rate the speed of their internet and people who experience a lot
#  of internet outages. This factor we can call it 'Internet Quality'
# - factor1 explains the common variance in people who give rate about how satisfied are they with their TV servece, people
# who rate how diversified is their TV and people who rate how is their TV signal reliability. This factor we can call it
# 'TV Quality'
# - factor2 explains the common variance in people who rate their quality of phone calls, people who rate their cell cover.
# This factor we can call it 'Cell phone quality'


print(pd.DataFrame(fa.get_factor_variance(),index=['Variance','Proportional Var','Cumulative Var']))

print(pd.DataFrame(fa.get_communalities(),index=df.columns,columns=['Communalities']))
