"""
Scoring algorithms for doctors and sorting algorithm based on score.
"""
import os
import sys

from sqlalchemy import MetaData, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

def calculate_score_using_orm(db_conn, disease_name):
    meta = MetaData(db_conn)
    meta.reflect()
    dpi = meta.tables['disease_params_importance']
    diseases = meta.tables['diseases']
    doctors = meta.tables['doctors']
    session = sessionmaker(db_conn)()

    # All the parameter importance values associated with the input disease.
    Y = select([dpi.c.importance.label('i')], diseases.c.type == disease_name) \
        .select_from(dpi.join(diseases)) \
        .alias('Y')
    X = doctors.alias('X')
    hcp_rank = select([X, Y]).alias('hcp_rank')

    # Get each doctor's score for the specified disease.
    score = func.sum(hcp_rank.c.i * hcp_rank.c.weight).label('score')
    hcp_score = select([hcp_rank.c.hcp_number, score]) \
        .group_by(hcp_rank.c.hcp_number) \
        .alias('hcp_score')

    # Get each doctor's weightage factors as separate tables.
    # We know that there are exactly 5 weightages factors that are used for each
    # doctor.
    WEIGHTAGE_NO = 5
    weights = []
    for i in range(WEIGHTAGE_NO):
        query = select([doctors.c.hcp_number, doctors.c.weight.label(f'w{i+1}')]) \
            .where(doctors.c.weight_no == i) \
            .alias(f'weight_{i+1}')
        weights.append(query)

    # Multilevel sorting of diseases; first by score, then w1, w2, w3, w4, w5.
    hcp_score_and_weights = hcp_score \
        .join(weights[0], hcp_score.c.hcp_number == weights[0].c.hcp_number) \
        .join(weights[1], hcp_score.c.hcp_number == weights[1].c.hcp_number) \
        .join(weights[2], hcp_score.c.hcp_number == weights[2].c.hcp_number) \
        .join(weights[3], hcp_score.c.hcp_number == weights[3].c.hcp_number) \
        .join(weights[4], hcp_score.c.hcp_number == weights[4].c.hcp_number) \
        .alias('Z')

    hcp_scores_sorted = select([hcp_score_and_weights.c.hcp_score_hcp_number,
                                hcp_score_and_weights.c.hcp_score_score,
                                hcp_score_and_weights.c.weight_1_w1,
                                hcp_score_and_weights.c.weight_2_w2,
                                hcp_score_and_weights.c.weight_3_w3,
                                hcp_score_and_weights.c.weight_4_w4,
                                hcp_score_and_weights.c.weight_5_w5],
                               distinct=True) \
        .order_by(hcp_score_and_weights.c.hcp_score_score.desc(),
                  hcp_score_and_weights.c.weight_1_w1.desc(),
                  hcp_score_and_weights.c.weight_2_w2.desc(),
                  hcp_score_and_weights.c.weight_3_w3.desc(),
                  hcp_score_and_weights.c.weight_4_w4.desc(),
                  hcp_score_and_weights.c.weight_5_w5.desc())

    res = session.execute(hcp_scores_sorted)
    return [row[0:2] for row in res] 

if __name__ == '__main__':
    sys.path.append(sys.path[0] + '/model')
    
    from model.db_connection import get_db_connection
    db_conn = get_db_connection().connect()
    disease_name = 'test disease 3'
    res = calculate_score_using_db(db_conn, disease_name)
    
    for row in res:
        print(row)
