import pandas as pd
# import . models
from . models import Stock, SKU, Location

df = pd.read_csv('/Users/anandoghose/Desktop/inventory_export_1.csv', low_memory=False)




df['SKU'].dropna(inplace=True)
df['SKU'].drop_duplicates(inplace=True)

for i in range(len(df)):
    sku_code = df.loc[i,'SKU']
    print(sku_code)
    sku_list = SKU.objects.create(sku_code=sku_code)
    sku_list.save()