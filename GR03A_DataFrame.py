import pandas as pd

def txt_to_dataframe():

    #CREATING DATAFRAME FROM TXT FILE CONTAINING LIST OF ANCIENT GREEK CITIES
    #Creating single column dataframe with all data within text file
    file='GR03-Ancient Greek Cities Before Hellenistic Period 20200131.txt'
    raw_df=pd.read_csv(file,sep='^',header=None)
    raw_df.columns=['Raw Data']
    #print(raw_df)


    #Create a list of out dataframe
    raw_df_list=raw_df['Raw Data'].tolist()

    #Create new list - each item being city code and name
    import re
    city_list = [re.findall(r'[A-Z]+[0-9]+\.\s[A-Za-z]+/?[A-Za-z]*?\s?[A-Za-z]*?',city) for city in raw_df_list]

    #Creating a flatlist out of city_list
    import itertools
    new_city_list= list(itertools.chain(*city_list))

    #Creating new dataframe
    clean_df=pd.DataFrame(new_city_list)
    clean_df.columns=['City Code and Name']


    #Breaking down string
    clean_df['City Code']= clean_df['City Code and Name'].str.split('.').str.get(0).str.strip()
    clean_df['Country Code']= clean_df['City Code and Name'].str.extract('([A-Z]+)',expand=True)
    clean_df['City Name']= clean_df['City Code and Name'].str.split('.').str.get(1).str.strip()

    # Load csv containing the mapping country code - country name
    mapping_df=pd.read_csv('GR03-Country Code Mapping.csv')

    #Converting each column into lists
    country_code= mapping_df['Key'].tolist()
    country_name= mapping_df['Value'].tolist()

    #Converting lists into a dictionary
    map_dict=dict(zip(country_code,country_name))

    clean_df['Country Name']= clean_df['Country Code'].map(map_dict)

    return clean_df


def create_df_for_viz():
    clean_df=txt_to_dataframe()

    city_count_geo_df=clean_df['Country Name'].value_counts().rename_axis('Country').reset_index(name='No of Cities')

    #Importing Geo-Coordinates
    geo_df=pd.read_csv('GR03-Selected Capital Geo Coordinates Modified.csv')

    #Converting each column into lists
    country_list= geo_df['CountryName'].tolist()
    latitude_list= geo_df['CapitalLatitude'].tolist()
    longitude_list= geo_df['CapitalLongitude'].tolist()

    #Converting lists into a dictionary
    lat_dict=dict(zip(country_list,latitude_list))
    long_dict=dict(zip(country_list,longitude_list))


    #Adding latitude & longitude to city_count_geo_df
    city_count_geo_df['Latitude']= city_count_geo_df['Country'].map(lat_dict)
    city_count_geo_df['Longitude']= city_count_geo_df['Country'].map(long_dict)

    #Drop the following countries
    city_count_geo_df=city_count_geo_df[city_count_geo_df.Country != 'Serbia']

    # Create function to assign category based on number of cities
    def assign_category(row):
        value=row['No of Cities']
        if value > 90:
            category='90+ colonies'

        elif value > 60 and value < 90:
            category='60 - 90 colonies'

        elif value > 30 and value < 60:
            category='30 - 60 colonies'

        elif value > 10 and value < 20:
            category='10 - 20 colonies'

        else:
            category='Less than 10 colonies'

        return category

    # Assign category using function above
    city_count_geo_df['Category']= city_count_geo_df.apply(assign_category,axis=1)

    # Text to display on Bubble map for each trace
    city_count_geo_df['Trace_Text']= city_count_geo_df.Country+'<br>'+\
     (city_count_geo_df['No of Cities']).astype(str)+' colonies'


    return city_count_geo_df
