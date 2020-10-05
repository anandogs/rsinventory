import pandas as pd


if __name__ == '__main__':

	products = pd.read_excel('/Users/anandoghose/Desktop/Line Sheet Indigo Collection.xlsx', header=2)
	products = products.dropna(subset=['Vendor SKU/Style']).reset_index(drop=True)
	products = products.loc[:,['Vendor SKU/Style', 'RS Online', 'Jaypore', 'Okhai','Warehouse']]
	skus = products.loc[:,['Vendor SKU/Style']]
	products.rename(columns={'Vendor SKU/Style': 'SKU', 'RS Online': 'Rs Online'}, inplace=True)


	skus.to_excel('/Users/anandoghose/Desktop/skus.xlsx', index=False)
	products.to_excel('/Users/anandoghose/Desktop/products.xlsx', index=False)
