    filename_common: string
        Common part of the filename
    postfix_index: string
        Postfix of the filename
    file_format: string, optional
        Default is None
        
    If the targeted file is eta0.dat and the fields attributes are 'x' and 'eta', seperated by comma, 
    filename_common = 'eta', postfix_index = 0, table_delimiter = ',', table_headers = ['x', 'eta']
    file_format = '.dat'.