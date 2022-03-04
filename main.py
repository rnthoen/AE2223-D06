import pandas as pd
from import_data import import_data
from separate_sequences import separate_sequences

files = [['Data/L103/L1-03.csv', 'Data/L103/L1-03_0_2_4052.csv', 'Data/L103/L1-03_4054_2_8840', 'Data/L103/L1-03_8842_2_13994', 'Data/L103/L1-03_13996_2_16696'],
         ['Data/L104/L1-04.csv', 'Data/L104/L1-04_0_2_4160', 'Data/L104/L1-04_4162_2_8548', 'Data/L104/L1-04_8550_2_12242', 'Data/L104/L1-04_12244_2_16402', 'Data/L104/L1-04_16404_2_20098', 'Data/L104/L1-04_20100_2_23800', 'Data/L104/L1-04_23802_2_27262', 'Data/L104/L1-04_27264_2_30036', 'Data/L104/L1-04_30038_2_31422'],
         ['Data/L105/L1-05.csv', 'Data/L105/L1-05_0_2_4050', 'Data/L105/L1-05_4052_2_7978', 'Data/L105/L1-05_7980_2_12136', 'Data/L105/L1-05_12138_2_15722'],
         ['Data/L109/L1-09.csv', 'Data/L109/L1-09_0_2_4016', 'Data/L109/L1-09_4018_2_8288', 'Data/L109/L1-09_8290_2_12072', 'Data/L109/L1-09_12074_2_14760'],
         ['Data/L123/L1-23.csv', 'Data/L123/L1-23_0_2_4000', 'Data/L123/L1-23_4002_2_8080', 'Data/L123/L1-23_8082_2_12430', 'Data/L123/L1-23_12432_2_15850', 'Data/L123/L1-23_15852_2_20506', 'Data/L123/L1-23_20508_2_24236', 'Data/L123/L1-23_24238_2_28894', 'Data/L123/L1-23_28896_2_31384', 'Data/L123/L1-23_31386_2_35416', 'Data/L123/L1-23_35418_2_40390', 'Data/L123/L1-23_40392_2_42256']]

select_specimen = files[0]

df_data = import_data(select_specimen)

df_separated = separate_sequences(df_data)
df_separated.to_csv(f'separated_sequences_{select_specimen[5:9]}.csv')