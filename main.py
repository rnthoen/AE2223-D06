from import_data import import_data

files = ['Data/L103/L1-03.csv',
         'Data/L104/L1-04.csv',
         'Data/L105/L1-05.csv',
         'Data/L109/L1-09.csv',
         'Data/L123/L1-23.csv']

select_specimen = files[1]

df_data = import_data(select_specimen)

