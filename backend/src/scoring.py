"""
Scoring algorithms for doctors and sorting algorithm based on score.
"""
import os
import sys

def calculate_score_using_db(db_conn, disease):
    print('TO DO')
    query_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              'model/get_ranking.sql')
    with open(query_file, 'r') as get_ranking_query_ptr:
        query = ' '.join(get_ranking_query_ptr).replace('\n', ' ')

    res = db_conn.execute(query)
    return [row[0:2] for row in res] 

if __name__ == '__main__':
    sys.path.append(sys.path[0] + '/model')
    
    from model.db_connection import get_db_connection
    db_conn = get_db_connection().connect()
    disease_name = 'Test Disease 1'
    print(calculate_score_using_db(db_conn, disease_name))
