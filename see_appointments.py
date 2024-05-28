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

##############     SEE APPOINTMENTS      ##############


@app.route('/dbproj/appointments/<int:patient_user_id>', methods=['GET'])
def get_all_appointments(patient_user_id):
    logger.info('GET /dbproj/appointments/{patient_user_id}')

    conn = db_connection()
    cur = conn.cursor()

    try:
        query = '''
                SELECT numconsulta, gabinete, piso, edificio, medico_empregado_pessoa_cc
                FROM consulta, entrada_conta
                WHERE paciente_pessoa_cc = %s
                '''
        cur.execute(query, (patient_user_id,))
        rows = cur.fetchall()

        logger.debug('GET /dbproj/appointments - parse')
        Results = []
        for row in rows:
            logger.debug(row)
            content = {'numconsulta': int(row[0]), 'gabinete': row[1], 'piso': row[2], 'edificio': row[3], 'medico_empregado_pessoa_cc':row[4]}
            Results.append(content)

        response = {'status': StatusCodes['success'], 'results': Results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /dbproj/appointments - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

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