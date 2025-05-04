#Imports
from flexytg.sessions.create_session import create_session
from flexytg.sessions.analyze_session import analyze_session

# Creating sql Session From Information
session = create_session(module_name='hydrogram',session_type='sql',file_name='test.session',dc_id=4,auth_key="G1D2ptIr....",user_id=7682429075,api_id=123)
print(session)

# Analyzing Session To Information
Information = analyze_session(module_name='hydrogram',session_type='sql', sql_session='test.session')
print(Information)
