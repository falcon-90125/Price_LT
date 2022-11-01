import pandas as pd

def def_to_zakroma(price_my_to_xlsx, price_public_sale_to_xlsx):
    price_to_zakroma = price_my_to_xlsx.drop(price_my_to_xlsx.columns[[5]], axis='columns') #Удаляем ненужные столбцы , 7
    # price_sale = price_public_sale_to_xlsx.drop(price_public_sale_to_xlsx.columns[[4]], axis='columns')
    price_sale = price_public_sale_to_xlsx.dropna(axis=0)
    price_sale.rename(columns={'Базовый(РФ)/Вход ЭКС': 'Базовый(РФ)'}, inplace=True)
    mrc_list = []
    for i in range(len(price_sale)):
        mrc_list.append(round(price_sale.iloc[i,3]*1.15+0.5, 0)) #МРЦ*1.2 +0.5 для округления в большую сторону    
    price_sale['МРЦ'] = mrc_list
    price_sale['Вход ЭКС'] = price_sale['Базовый(РФ)']
    price_to_zakroma = pd.concat([price_to_zakroma,price_sale])
    return price_to_zakroma