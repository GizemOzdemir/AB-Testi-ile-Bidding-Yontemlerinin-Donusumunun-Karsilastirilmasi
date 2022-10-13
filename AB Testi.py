#import glob
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# GÖREV 1

# ADIM 1:ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı
# değişkenlere atayınız.

#all_data = pd.DataFrame()
#for f in glob.glob("datasets/ab_testing.xlsx"):
    #df_control = pd.read_excel(f,"Control Group")
    #df_test = pd.read_excel(f, "Test Group")

df_control = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")

df_control
df_test

# ADIM 2 : Kontrol ve test grubu verilerini analiz ediniz.

df_control.info()
df_test.info()

df_control.describe().T
df_test.describe().T


# ADIM 3 : Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.


df_birleşim = pd.concat([df_control,df_test], axis=0)
#df_birleşim = pd.concat([df_control,df_test])---- (Aynı çıktıyı verecektir. Yan yana birleşim yapmak için axis=1 demek gerekir.)

###################################################################################################################################################################
# GÖREV 2

# ADIM 1: Hipotezi tanımlayınız.

# H0 : M1 = M2 [kontrol ve test grubunun kazançları arasında anlamlı bir farklılık yoktur.)
# H1 : M1!= M2

# ADIM 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz.

df_control["Purchase"].mean()
df_test["Purchase"].mean()

#################################################################################################################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi

# ADIM 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
# Bunlar Normallik Varsayımı ve Varyans Homojenliğidir. Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni
# üzerinden ayrı ayrı test ediniz.

test_stat, pvalue = shapiro(df_birleşim.iloc[:40,2:3])
print('test stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df_birleşim.loc[df_control["Purchase"]])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df_birleşim.iloc[40:80,2:3])
print('test stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# test ve control grupları için p-value>0.05 böylece H0 reddedilemez.

# H0: Varyanslar Homojendir.
# H1: Varyanslar Homojen Değildir.

test_stat, pvalue = levene(df_control["Purchase"],
                           df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# test ve control grupları için p-value>0.05 , varyanslar homojendir.

# ADIM 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

#Varsayımlar sağlandığından bağımsız iki örneklem t testi (parametrik test) kullanılır.

test_stat, pvalue = ttest_ind(df_test["Purchase"],
                              df_control["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# ADIM 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları arasında istatistiki
# olarak anlamlı bir fark olup olmadığını yorumlayınız.

#p-value= 0.3493 H0 reddedilemez.
#[kontrol ve test grubunun kazançları arasında anlamlı bir farklılık yoktur.]


#################################################################################################################################################
# GÖREV 4:Sonuçların Analizi

# ADIM 1: Hangi testi kullandınız, sebeplerini belirtiniz.

#ttest kullanıldı sebebii varyans homojenliği ve normal dağılım varsayımına uygun oldugu için


# ADIM 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

#müşteriye max bidding ve test bidding methodlarının kazançları arasında anlamlı bir farklılık yok derim.




