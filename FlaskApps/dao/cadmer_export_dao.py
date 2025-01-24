from flask import current_app
import MySQLdb

# Implementando o CRUD (Create, Read, Update, Delete)
class ProductDataAccess():
    def __init__ (self):
        # Esta chave foi definida em app.py
        '''
            This typically means that you attempted to use functionality that needed
            the current application. To solve this, set up an application context
            with app.app_context(). See the documentation for more information.

            read more at: https://flask.palletsprojects.com/en/stable/appcontext/
        '''

        self.mysql = current_app.extensions['mysql']
    
    # Considerando o caso mais simples
    def get_product_by_id (self, product_id: str):
        cursor = self.mysql.connection.cursor()

        # Define the query to fetch product details
        query = '''
            SELECT descricao, app_precovenda as venda
            FROM cadmer_exportacao
            WHERE codbarra = %s
        '''

        try:
            cursor.execute(query, (product_id,))  # Execute the query with the provided product_id
            result = cursor.fetchone()  # Fetch one result
        except MySQLdb.Error as e:
            print(f"Error fetching product by id: {e}")
            result = None
        finally:
            cursor.close()

        # Return the result, or None if no product was found
        return result