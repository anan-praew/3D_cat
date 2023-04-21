import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/subj_s1_CC_20230321-171606_pitch.csv',index_col=0)
err = df.resp-df.mem;
err[err<-180] = err[err<-180]+360
err[err>180] = err[err>180]-360;

plt.scatter(df.mem,err)
plt.show()