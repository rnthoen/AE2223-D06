import pandas as pd

def separate_sequences(dataframe):
    length = len(dataframe['count'])

    # Create lists
    cycle_number_list = []
    start_count_list = []
    end_count_list = []

    # Set first values
    cycle_number_list.append(500)
    start_count_list.append(dataframe['count'][0])

    # Define thresholds
    time_jump = 5 # [s]
    load_jump = 0 # [kN]
    displacement_jump = 0 # [mm]
    small_displacement_jump = 0.05 # [mm]
    large_displacement_jump = 0.8 # [mm]

    i = 0
    while (i < (length - 1)):
        test_results = []

        # Test for time jump
        if (dataframe['time'][i+1] - dataframe['time'][i]) > time_jump:
            test_results.append(True)
        else:
            test_results.append(False)

        # Test for load jump
        if (dataframe['load'][i+1] - dataframe['load'][i]) > load_jump:
            test_results.append(True)
        else:
            test_results.append(False)

        # Test for displacement jump
        if (dataframe['displacement'][i+1] - dataframe['displacement'][i]) > displacement_jump:
            test_results.append(True)
        else:
            test_results.append(False)

        # Check test results
        if sum(test_results) == 3:
            # Update previous end count
            end_count = dataframe['count'][i]
            end_count_list.append(end_count)

            # Add new cycle number
            j = len(cycle_number_list) - 1
            cycle_number = 500 + 500 * (j + 1) + 500 * ((j + 1) // 9)
            cycle_number_list.append(cycle_number)

            # Add new start count
            start_count = end_count + 1
            start_count_list.append(start_count)

        elif (sum(test_results) == 2) or (sum(test_results) == 1):
            # Check for type 1 error (FFT, second-last datapoint)
            if test_results == [False, False, True]:
                condition1 = abs(dataframe['displacement'][i+1] - dataframe['displacement'][i]) < small_displacement_jump
                condition2 = (dataframe['displacement'][i+2] - dataframe['displacement'][i]) > large_displacement_jump

                temp_displacement_jump = (dataframe['displacement'][i+2] - dataframe['displacement'][i])

                if (condition1 and condition2):
                    # Print error message
                    location = dataframe['count'][i]
                    #print(f'Type E1 error occured at count = {location}: {test_results}')

                else:
                    # Print error message
                    location = dataframe['count'][i]
                    #print(f'Error occured at count = {location}: {test_results} ({condition1}, {condition2}, {temp_displacement_jump})')

            else:
                # Print error message
                location = dataframe['count'][i]
                #print(f'Error occured at count = {location}: {test_results}')

        i += 1

    # Update end count of last entry
    end_count =  dataframe['count'][i]
    end_count_list.append(end_count)

    # Create dataframe
    sequences_dataframe = pd.DataFrame({'cycle_number': cycle_number_list, 'start_count': start_count_list, 'end_count': end_count_list})

    return sequences_dataframe
