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

##############     REGISTER      ##############
#
# PACIENTE
#

@app.route('/dbproj/register/patient', methods=['POST'])
def add_patient():
    route_string = 'POST /register/patient'
    logger.info(route_string)
    payload = flask.request.get_json()      # payload é um dicionario

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'{route_string} - payload: {payload}')

    # do not forget to validate every argument, e.g.,:
        # ⚠⚠ criar funçoes ⚠⚠
    #if 'ndep' not in payload:
        #response = {'status': StatusCodes['api_error'], 'results': 'ndep value not in payload'}
        #return flask.jsonify(response)
    if 'gmail' not in payload:
        payload['gmail'] = NULL

    # parameterized queries, good for security and performance
        # adicionar dados à tabela 'pessoa'
    statement1 = 'INSERT INTO pessoa (nome, cc, datanascimento, sexo, telemovel, gmail, morada) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    values1 = (payload['nome'], payload['cc'], payload['datanascimento'], payload['sexo'], payload['telemovel'], payload['gmail'], payload['morada'])
        # adicionar dados à tabela 'paciente'
    statement2 = 'INSERT INTO paciente (tiposangue, altura, peso, pessoa_cc) VALUES (%s, %s, %s, %s)'
    values2 = (payload['tiposangue'], payload['altura'], payload['peso'], payload['cc'])
    

    try:
        cur.execute(statement1, values1)

        # commit the transaction
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': f'Inserted person {payload["nome"]}'}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{route_string} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

        # an error occurred, rollback
        conn.rollback()
    try:
        cur.execute(statement2, values2)

        # commit the transaction
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': f'Inserted patient {payload["nome"]}'}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{route_string} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

#
# MEDICO
#



#
# ENFERMEIRO
#



#
# ASSISTENTE
#



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