import pandas as pd

def results_to_excel(time, temp, res):
    
    number_of_measurements = len(time) + 1
    
    # Create a Pandas dataframe from the data and write it to an Excel file
    df = pd.DataFrame({'time': time, 'temperature': temp, 'resistance': res})
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name = 'Results', index=False)

    # Create a new sheet for the plot
    workbook = writer.book
    worksheet = writer.sheets['Results']
    
    # Create a chart object
    chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})
    
    # Add our measurements to the chart
    chart.add_series({'name': 'temperature', 'categories': '=Results!$A$2:$A${}','values': '=Results!$B$2:$B${}'.format(number_of_measurements)})
    chart.add_series({'name': 'resistance', 'categories': '=Results!$A$2:$A${}','values': '=Results!$C$2:$C${}'.format(number_of_measurements), 'y2_axis': 1})
    
    # Set chart title and axis titles
    chart.set_title({'name': 'Resistance and temperature over time'})
    chart.set_x_axis({'name': 'time'})
    chart.set_y_axis({"name": "°C", "major_gridlines": {"visible": 1}})
    chart.set_y2_axis({"name": "\u2126"})
    
    # Insert the chart into the worksheet
    worksheet.insert_chart('E2', chart, {'x_scale': 2, 'y_scale': 2})
    
    # Close the Pandas Excel writer and save the Excel file
    writer._save()