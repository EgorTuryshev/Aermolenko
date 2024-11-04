import pandas as pd
import os


excel_folder = 'D:\\data\\'

dict = {
   'update_AgentReady.xlsx': {'table': 'Agent', 'sheet': 'AgentReady'},
   'AgentTypeReady.xlsx': {'table': 'AgentType', 'sheet': 'Лист1'},
   'MaterialReady.xlsx': {'table': 'Material', 'sheet': 'Лист1'},
   'MaterialSupplier.xlsx': {'table': 'MaterialSupplier', 'sheet': 'MaterialSupplier'},
   'MaterialTypeReady.xlsx': {'table': 'MaterialType', 'sheet': 'Лист1'},
   'ProductMaterial.xlsx': {'table': 'ProductMaterial', 'sheet': 'Лист1'},
   'update_ProductReady.xlsx': {'table': 'Product', 'sheet': 'ProductReady'},
   'ProductSaleReady.xlsx': {'table': 'ProductSale', 'sheet': 'Лист1'},
   'ProductTypeReady.xlsx': {'table': 'ProductType', 'sheet': 'ProductTypeReady'},
   'ShopReady.xlsx': {'table': 'Shop', 'sheet': 'ShopReady'},
   'SupplierReady.xlsx': {'table': 'Supplier', 'sheet': 'Лист1'}
}



for file_name, mapping in dict.items():
    file_path = os.path.join(excel_folder, file_name)
    table_name = mapping['table']
    sheet_name = mapping['sheet']

    df = pd.read_excel(file_path, sheet_name=sheet_name)

    sql_queries = []
    for index, row in df.iterrows():
        values = ', '.join(f"'{str(x)}'" if isinstance(x, str) else str(x) for x in row)
        sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({values});"
        sql_queries.append(sql)

    with open(f"{table_name}_inserts.sql", 'w') as f:
        f.write('\n'.join(sql_queries))
