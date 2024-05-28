import flask
import logging
import psycopg2
import time

app = flask.Flask(__name__)

StatusCodes = {
    'success': 200,
    'api_error': 400,
    'internal_error': 500
}

##########################################################
## DATABASE ACCESS
##########################################################

def db_connection():
    db = psycopg2.connect(
        user='aulaspl',
        password='aulaspl',
        host='127.0.0.1',
        port='5432',
        database='ProjetoBD'
    )

    return db


@app.route('/dbproj/top3', methods=['GET'])
def get_top_3_patients():
    logger.info('GET /dbproj/top3')

    conn = db_connection()
    cur = conn.cursor()

    try:
        query = '''
            SELECT 
                pe.nome AS patient_name, 
                SUM(ec.conta_valortotal) AS amount_spent,
                c.numconsulta AS id,
                c.medico_empregado_pessoa_cc AS doctor_id,
                ec.datahoraentrada AS date
            FROM 
                entrada_conta ec
            JOIN 
                paciente pa ON ec.paciente_pessoa_cc = pa.pessoa_cc
            JOIN 
                pessoa pe ON pa.pessoa_cc = pe.cc
            LEFT JOIN 
                consulta c ON ec.id = c.entrada_conta_id
            WHERE 
                DATE_TRUNC('month', ec.datahoraentrada) = DATE_TRUNC('month', CURRENT_DATE)
            GROUP BY 
                pe.nome, c.numconsulta, c.medico_empregado_pessoa_cc, ec.datahoraentrada
            ORDER BY 
                amount_spent DESC
            LIMIT 3;
        '''
        cur.execute(query)
        rows = cur.fetchall()

        # Parsing the results
        patients = {}
        for row in rows:
            patient_name = row[0]
            amount_spent = row[1]
            procedure = {
                'id': row[2],
                'doctor_id': row[3],
                'date': row[4]
            }
            if patient_name not in patients:
                patients[patient_name] = {
                    'patient_name': patient_name,
                    'amount_spent': amount_spent,
                    'procedures': []
                }
            patients[patient_name]['procedures'].append(procedure)

        results = list(patients.values())

        response = {'status': 'success', 'results': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /dbproj/top3 - error: {error}')
        response = {'status': 'error', 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)


if __name__ == '__main__':
    # set up logging
    logging.basicConfig(filename='log_file.log')
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    host = '127.0.0.1'
    port = 8080
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API v1.0 online: http://{host}:{port}')