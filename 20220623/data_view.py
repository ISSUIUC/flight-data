import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

print("Printing head: ")
print(df.head)

plt.plot(df["barometer_data.altitude"])
plt.show()
