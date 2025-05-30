import sqlite3
import pandas as pd


conn = sqlite3.connect('STAFF.db')

table_name = 'INSTRUCTOR'
dept_table = 'Departments'

attribute_list = ['ID', 'FNAME', 'LNAME', 'CITY', 'CODE']
dept_attribute_list = ['DEPT_ID', 'DEP_NAME', 'MANAGER_ID', 'LOC_ID']

file_path = '/home/project/INSTRUCTOR.csv'
dept_file_path = '/home/project/Departments.csv'
df = pd.read_csv(dept_file_path, names=dept_attribute_list)

# print(df.head(10))
df.to_sql(dept_table, conn, if_exists='replace', index=False)
# print('Table is ready')
query_statement = f"SELECT * FROM {dept_table}"
query_output = pd.read_sql(query_statement, conn)

print(query_statement)
print(query_output)

query_statement = f"SELECT COUNT(*) FROM {dept_table}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

data_dict = {'DEPT_ID' : [9],
            'DEP_NAME' : ['Quality Assurance'],
            'MANAGER_ID' : ['30010'],
            'LOC_ID' : ['l0010']}
data_append = pd.DataFrame(data_dict)

data_append.to_sql(dept_table, conn, if_exists = 'append', index=False)
print('Data appended successfully')

query_statement = f"SELECT * FROM {dept_table}"
query_output = pd.read_sql(query_statement, conn)

print(query_statement)
print(query_output)

conn.close()