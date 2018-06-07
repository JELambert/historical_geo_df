# global_map_gif
Constructing a longitudinal global GeoDataFrame.


Be sure you have a pandas datetime column, as well as cowcode identifier named 'ccode'. 

Example Code:

		geo_data_frame = make_poly(df, 'ccode', 'date')

<h1>Argument Key: </h1>
	
* make_poly (df, country_id, time_unit) :: Will create GeoDataFrame with historical global country boundaries
	
		1. df = DataFrame (country-date unit of analysis)
		2. country_id = currently accepting only COW codes as 'ccode', to be expanded.
		3. time_unit = any feature in Pandas datetime format (for more info see: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html)

* make_gwpoly(df, country_id, time_unit) :: Will create a GeoDataFrame with GW historical country boundaries
* make_name (df, country_id, time_unit) :: Will populate a field of Country Names
* make_gw (df, country_name, time_unit)	:: Will populate field with GW Codes, can be used with ^^country_names^^ created variable.
