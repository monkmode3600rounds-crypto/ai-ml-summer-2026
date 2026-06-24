Quantity_greater_than_0=df[df['Quantity']>0]
def Is_High_Sales(row):
    if row['Sales']> 499:
        return 'Yes'
    else:
        return 'No'

Quantity_greater_than_0['HighSales']=Quantity_greater_than_0.apply(Is_High_Sales, axis=1)

Coutry_Sales=Quantity_greater_than_0.groupby('Country')['Sales'].mean().reset_index()
Coutry_Sales=Coutry_Sales.sort_values(by='Sales', ascending=False)
Coutry_Sales.head()
