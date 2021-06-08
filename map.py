# ===========================================================================================
# Dataset:              House Sales in King County, USA
# Source:               Kaggle
# Link:                 https://www.kaggle.com/harlfoxem/housesalesprediction
# Description:          The dataset contains house sale prices in King County, Seattle.
#                       It includes homes sold between May 2014 and May 2015.
#                       There are 21 columns and 21,613 rows.
# Goal:                 Run this python script to display the mean sale price of each neighbourhood in King County.
# Additional Dataset:   Shape area and length of each zipcode in King County (GeoJSON file format).
# Link:                 https://gis-kingcounty.opendata.arcgis.com
# ===========================================================================================
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import webbrowser
import folium                               # Python wrapper for Leaflet.js
from folium.plugins import MarkerCluster

# settings
pd.set_option('display.max_columns', None)


def loadData(df):
    data = df
    # print("Total columns and rows of the dataset:" + str(data.shape))
    # print("Total rows with missing data values:" + str(data.isnull().any(axis=1).sum()))
    # print(data.info())

    data['date'] = pd.to_datetime(data['date'])
    data['zipcode'] = data['zipcode'].astype(int)
    return data


def zipcodeMean(df):
    data = df
    zipcode_Mean = []
    for i in data['zipcode'].unique().tolist():
        price_Mean = data[data['zipcode'] == i]['price'].mean()
        lat = data[data['zipcode'] == i]['lat'].mean()
        long = data[data['zipcode'] == i]['long'].mean()
        zipcode_Mean.append([str(i), price_Mean, lat, long])

    zip_ls = []
    price_ls = []
    lat_ls = []
    long_ls = []
    for j in zipcode_Mean:
        zip_ls.append(j[0])
        price_ls.append(j[1])
        lat_ls.append(j[2])
        long_ls.append(j[3])
    zipcode_df = pd.DataFrame(list(zip(zip_ls, price_ls, lat_ls, long_ls)), columns=['Zipcode', 'Price', 'Latitude', 'Longitude'])
    return zipcode_df


def interactiveMap(path, df, area):
    html_page = f'{path}'
    map = folium.Map(location=[47.6062, -122.3321], zoom_start=10)      # Seattle Coordinates
    folium.Choropleth(geo_data=area,
                      data=df, columns=['Zipcode', 'Price'],
                      key_on='feature.properties.ZIPCODE',
                      fill_color='BuPu', fill_opacity=0.7, line_opacity=0.2, legend_name='SALE PRICE').add_to(map)
    # map.save('ChoroplethMap.html')
    marker_cluster = MarkerCluster().add_to(map)
    for i in range(df.shape[0]):
        location = [df['Latitude'][i], df['Longitude'][i]]
        toolTip = 'Zipcode:{}'.format(df['Zipcode'][i])
        folium.Marker(location,
                      popup=""" <i>Mean Sale Price:</i><br> <b>${:,.2f}</b> 
                      """.format(round(df['Price'][i], 2)), tooltip=toolTip).add_to(marker_cluster)
    map.save(html_page)
    webbrowser.open_new('file://' + html_page)


def main():
    hp = pd.read_csv("data/houseData.csv")
    df = loadData(hp)
    agg_zipcode = zipcodeMean(df)
    kingCounty_geo = r'data/Zipcodes_for_King_County_and_Surrounding_Area___zipcode_area.geojson'
    dataMap = interactiveMap('/Users/derrinechia/PycharmProjects/HousePrices/templates/MeanSalePrice_KingCounty.html', agg_zipcode, kingCounty_geo)


if __name__ == "__main__":
    main()

