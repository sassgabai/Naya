import json
import psycopg2

def insert_postgres(secret, body):
    try:
        connection = psycopg2.connect(
            dbname= 'testpoc',
            user= secret['username'],
            password= secret['password'],
            host= 'noga-poc-1-instance-1.cocluqwjpuyf.us-east-1.rds.amazonaws.com',
            port= 5432
        )
        
        cursor = connection.cursor()
        
        
        #upsert
        cursor.execute(
            f'''
            INSERT INTO requests_table (user_id, action, lambda_name, status)
            VALUES ({body['user_id']}, \'{body['action']}\', \'{body['lambda_name']}\', \'{body['status']}\')
            ON CONFLICT (user_id)
            DO UPDATE SET action = \'{body['action']}\', lambda_name = \'{body['lambda_name']}\', status = \'{body['status']}\'
            ;
            
            '''
            )
        
        connection.commit()
        
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        raise e
        return '', ''
    
    
