# global_map_gif
Constructing a longitudinal global GeoDataFrame.


Be sure you have a pandas datetime column, as well as cowcode identifier named 'ccode'.

Example Code:

		geo_data_frame = make_poly(df, 'ccode', 'date')

<h1>Argument Key: </h1>

* make_poly (df, country_id, time_unit) :: Will create GeoDataFrame with historical global country boundaries

		1. df = DataFrame (country-date unit of analysis)
		2. country_id = currently accepting only COW codes as 'ccode'.
		3. time_unit = any feature in Pandas datetime format (for more info see: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html)




Shape files are primarily derived (with some minor adjustments and updates) from the R cshapes files.
Citation: Weidmann, Nils B., Doreen Kuse, and Kristian Skrede Gleditsch. 2010. The Geography of the International System: The CShapes Dataset. International Interactions 36 (1).
