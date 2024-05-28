import flask
from flask import Flask, request,jsonify
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

##############     EXECUTE PAYMENT      ##############


@app.route('/dbproj/bills/<int:bill_id>', methods=['POST'])
def pay_bill(bill_id):
    logger.info(f'POST /dbproj/bills/{bill_id}')

    payload = request.json
    amount = payload.get('amount')
    patient_id = payload.get('patient_id')

    conn = db_connection()
    cur = conn.cursor()
    try:
        # Verifica se a conta existe
        cur.execute('SELECT 1 FROM entrada_conta WHERE id = %s', (bill_id,))
        row = cur.fetchone()
        if row is None:
            response = {'status': 'error', 'errors': 'Fatura inexistente'}
            return jsonify(response), 404

        # Verifica se a conta pertence ao paciente
        cur.execute('SELECT paciente_pessoa_cc FROM entrada_conta WHERE id = %s', (bill_id,))
        row = cur.fetchone()
        if row is None or row[0] != patient_id:
            response = {'status': 'error', 'errors': 'Acesso não autorizado'}
            return jsonify(response), 403

        # Executa a procedure para registrar o pagamento e atualizar o estado da conta
        cur.execute('CALL addPayment(%s, %s, %s)', (bill_id, amount, patient_id))
        conn.commit()

        # Verifica o valor restante da fatura
        cur.execute('SELECT conta_valortotal - conta_valorpago AS valor_restante FROM entrada_conta WHERE id = %s', (bill_id,))
        row = cur.fetchone()
        remaining_value = row[0]

        response = {'status': 'success', 'results': remaining_value}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /dbproj/bills/{bill_id} - error: {error}')
        response = {'status': 'error', 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)




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