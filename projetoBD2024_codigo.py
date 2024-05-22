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

price_appointment = 50
price_surgery = 80
gabinetes = [101, 102, 201, 202, 301, 302]
salas = [101, 102, 201, 202, 301, 302]
quartos = [101, 102, 201, 202, 301, 302]


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

##############  AUTHENTICATION   ##############





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
        payload['gmail'] = None

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


#################################################
############## SCHEDULE APPOINTMENT #############
#################################################


@app.route('/dbproj/appointment', methods=['POST'])
def add_appointment():
    route_string = 'POST /dbproj/appointment'
    logger.info(route_string)
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'{route_string} - payload: {payload}')

    # do not forget to validate every argument, e.g.,:
    if 'doctor_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'doctor_id value not in payload'}
        return flask.jsonify(response)
    if 'time_stamp' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'time_stamp not in payload'}
        return flask.jsonify(response)
    if 'cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cc not in payload'}
        return flask.jsonify(response)

    # parameterized queries, good for security and performance
    # statement = 'INSERT INTO dep (ndep, local, nome) VALUES (%s, %s, %s)'
    # values = (payload['ndep'], payload['localidade'], payload['nome'])

    doc_id = payload['doctor_id']
    time_stamp = payload['time_stamp']
    if 'descricao' in payload:
        descricao = payload['descricao']
    else:
        descricao = ''

    statement = "call addAppointment(%s::smallint, %s::bigint, %s::timestamp, %s::varchar, %s::bigint, %s::real, null)"
    gab_found = False
    excep = False

    # ----- PROCEDURE NO SERVER -----
    for gab in gabinetes:   
        values = (gab, payload['doctor_id'], payload['time_stamp'], payload['descricao'], payload['cc'], price_appointment)
        try:
            cur.execute(statement, values)
            rows = cur.fetchall()

            #print("rows[0][0]: ", rows[0][0])
            
            if rows[0][0] == 1:
                conn.commit()
                gab_found = True
                break

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'{route_string} - error: {error}')
            response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
            excep = True

            # an error occurred, rollback
            conn.rollback()
            break
    
    if gab_found:
        response = {'status': StatusCodes['success'], 'results': f'Consulta marcada com medico {doc_id} dia {time_stamp} - gabinete {gab}'}
    elif excep:
        #response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
        pass
    else:
        response = {'status': StatusCodes['internal_error'], 'results': 'não há gabinetes disponiveis ou o medico está ocupado nesta hora'}

    conn.close()

    return flask.jsonify(response)



#################################################
##############     MAIN      ####################
#################################################

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