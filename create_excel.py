import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

loction_list = []
# create geolocator object
geolocator = Nominatim(user_agent="coreys app")

# input zip code
zipcode = ['Soho New York']
for zip in zipcode:
    # get location from zip code
    location = geolocator.geocode(zip)

    # check if location is found
    if location:
        # print longitude and latitude
        dict = {'zip':zip, "Longitude": location.longitude, "Latitude": location.latitude}
        loction_list.append(dict)
        

    else:
        print("Location not found.")

df_temp = pd.DataFrame(loction_list)
df_temp.to_csv('locations.csv', index=False)
exit()

df_temp = pd.read_csv(r'C:\Users\satni\PyProjects\NYC-Property-Data\final.csv')
df_temp['row_number'] = df_temp.groupby(['borough','neighborhood','address', 'apartment_number']).cumcount() + 1
df_temp.to_csv('final.csv', index=False)
# %matplotlib inline
# %config InlineBackend.figure_format = 'retina'
cols = ['BOROUGH', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY',
       'TAX CLASS AT PRESENT', 'BLOCK', 'LOT', 'EASE-MENT',
       'BUILDING CLASS AT PRESENT', 'ADDRESS', 'APARTMENT NUMBER', 'ZIP CODE',
       'RESIDENTIAL UNITS', 'COMMERCIAL UNITS', 'TOTAL UNITS',
       'LAND SQUARE FEET', 'GROSS SQUARE FEET', 'YEAR BUILT',
       'TAX CLASS AT TIME OF SALE', 'BUILDING CLASS AT TIME OF SALE',
       'SALE PRICE', 'SALE DATE']
cols = [col.lower().replace(" ","_") for col in cols]

url_prefix = 'https://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales'
years = range(2010,2020)
b = ['manhattan', 'queens', 'bronx', 'brooklyn']

links = []
for borough in b:
    try:
        links += [f"{url_prefix}/annualized-sales/{year}/{year}_{borough}.xls{'x' if year > 2017 else ''}" for year in years ]
        links += [url_prefix + f"/rollingsales_{borough}.xls", url_prefix + f"/annualized-sales/2009_{borough}.xls",
                f"https://www1.nyc.gov/assets/finance/downloads/pdf/09pdf/rolling_sales/sales_2008_{borough}.xls", 
                f"https://www1.nyc.gov/assets/finance/downloads/excel/rolling_sales/sales_2007_{borough}.xls",
                *[f"https://www1.nyc.gov/assets/finance/downloads/sales_{borough}_0{n}.xls" for n in range(3,7)] ]
    except Exception as e:
        print(e)
df_list = []
for link in links:
    try:
        dfs = pd.read_excel(link, skiprows=4, names=cols, parse_dates=[20])
        drop_dupes = dfs.drop_duplicates()
        df_list.append(drop_dupes)
    except Exception as e:
        print(e)
        
df = pd.concat(df_list)
df = df[(df.sale_price > 100000)]
df = df[['borough','neighborhood','land_square_feet','building_class_category', 'block','lot', 'address', 'apartment_number', 'gross_square_feet', 'sale_price', 
         'year_built', 'sale_date', 'zip_code']]
df['row_number'] = df.groupby(['borough','neighborhood','address', 'apartment_number']).cumcount() + 1

df.to_csv('final.csv', index=False)
#df_list.to_csv('final.csv', index = False)