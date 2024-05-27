import flask
import logging
import psycopg2
import time
from datetime import datetime, timedelta

app = flask.Flask(__name__) 

StatusCodes = {
    'success': 200,
    'api_error': 400,
    'internal_error': 500
}

# cada cirurgia e consulta dura 1 hora
price_appointment = 50
price_surgery = 80
gabinetes = [101, 102, 201, 202, 301, 302]
salas = [101, 102, 201, 202, 301, 302]
camas = [101, 102, 201, 202, 301, 302]


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

@app.route('/dbproj/user', methods=['PUT'])
def authentication():
    # autenticaçao feita a partir do mail
    route_string = 'PUT /dbproj/user'
    logger.info(route_string)
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'{route_string} - payload: {payload}')

    # do not forget to validate every argument, e.g.,:
    if 'username' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'username is required to update'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'password is required to update'}
        return flask.jsonify(response)


    # parameterized queries, good for security and performance
    statement = 'call verificar_usuario(%s::varchar, %s::varchar, null)'
    values = (payload['username'], payload['password'])

    try:
        res = cur.execute(statement, values)
        print("resposta: ", res)
        
        
        
        response = {'status': StatusCodes['success'], 'results': f'Login efetuado para: {cur.rowcount}', 'token': ''}

        # commit the transaction
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)


#############################################
############# REGISTER PATIENT ##############
#############################################


@app.route('/dbproj/register/patient', methods=['POST'])
def add_patient():
    route_string = 'POST /dbproj/register/patient'
    logger.info(route_string)
    payload = flask.request.get_json()      # payload é um dicionario

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'{route_string} - payload: {payload}')
    

    # do not forget to validate every argument, e.g.,:
    if 'nome' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'person name (nome) not in payload'}
        return flask.jsonify(response)
    if 'cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cc not in payload'}
        return flask.jsonify(response)
    if 'datanascimento' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'datanascimento not in payload'}
        return flask.jsonify(response)
    if 'sexo' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'sexo value not in payload'}
        return flask.jsonify(response)
    if 'telemovel' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'telemovel not in payload'}
        return flask.jsonify(response)
    if 'morada' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'morada not in payload'}
        return flask.jsonify(response)
    if 'gmail' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'gmail not in payload'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'password not in payload'}
        return flask.jsonify(response)
    
    if 'tiposangue' not in payload:
        payload['tiposangue'] = None
    if 'altura' not in payload:
        payload['altura'] = None
    if 'peso' not in payload:
        payload['peso'] = None
        
    statement = "call add_paciente(%s::varchar, %s::integer, %s::date, %s::varchar, %s::integer, %s::varchar, %s::varchar, %s::varchar, %s::float, %s::float, %s::varchar, null)"
    excep = False
    success = False
    response = ""
    
    # --- ADICIONAR PACIENTE --------------
    values = (payload['nome'], payload['cc'], payload['datanascimento'], payload['sexo'], payload['telemovel'], payload['gmail'], payload['morada'], payload['tiposangue'], payload['altura'], payload['peso'], payload['password']);
    try:
        cur.execute(statement, values)
        rows = cur.fetchall()
        
        if rows[0][0] != 0: # significa que inseriu com sucesso
            
            # commit transaction
            conn.comit()
            id_paciente = rows[0][0]
            success = True

    except(Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{route_string} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
        excep = True

        # an error occurred, rollback
        conn.rollback()
        
    finally:
        if not excep and success:
            response = {'status': StatusCodes['success'], 'results': f'Paciente com id {id_paciente} inserido '}
        elif excep:
            pass
        else:
            response = {'status': StatusCodes['internal_error'], 'results': 'ja ha uma pessoa com o mesmo id'}
        if conn is not None:
            conn.close()

    return flask.jsonify(response)



#############################################
############# REGISTER DOCTOR ###############
#############################################


@app.route('/dbproj/register/doctor', methods=['POST'])
def add_doctor():
    route_string = 'POST /dbproj/register/doctor'
    logger.info(route_string)
    payload = flask.request.get_json()      # payload é um dicionario

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'{route_string} - payload: {payload}')
    

    # do not forget to validate every argument, e.g.,:
    if 'nome' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'person name (nome) not in payload'}
        return flask.jsonify(response)
    if 'cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cc not in payload'}
        return flask.jsonify(response)
    if 'datanascimento' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'datanascimento not in payload'}
        return flask.jsonify(response)
    if 'sexo' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'sexo value not in payload'}
        return flask.jsonify(response)
    if 'telemovel' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'telemovel not in payload'}
        return flask.jsonify(response)
    if 'morada' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'morada not in payload'}
        return flask.jsonify(response)
    if 'gmail' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'gmail not in payload'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'password not in payload'}
        return flask.jsonify(response)
    if 'datacontratacao' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'datacontratacao not in payload'}
        return flask.jsonify(response)
    if 'seccao' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'seccao not in payload'}
        return flask.jsonify(response)
    if 'cedula' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cedula not in payload'}
        return flask.jsonify(response)
    
    if 'horastrabalho' not in payload:
            payload['horastrabalho'] = None
    if 'finalcontratacao' not in payload:
            payload['finalcontratacao'] = None
    if 'infoadicional' not in payload:
            payload['infoadicional'] = None
    if 'especialidade' not in payload:
            payload['especialidade'] = None

    statement = "call add_medico(%s::varchar, %s::integer, %s::date, %s::varchar, %s::integer, %s::varchar, %s::varchar, %s::date, %s::integer, %s::date, %s::integer, %s::varchar, %s::text, %s::varchar, null)"
    excep = False
    success = False
    response = ""

    # --- ADICIONAR MEDICO --------------
    values = (payload['nome'], payload['cc'], payload['datanascimento'], payload['sexo'], payload['telemovel'], payload['gmail'], payload['morada'], payload['datacontratacao'], payload['horastrabalho'], payload['finalcontratacao'], payload['cedula'], payload['seccao'], payload['info_adicional'], payload['password']);
    try:
        cur.execute(statement, values)
        rows = cur.fetchall()
        
        if rows[0][0] != 0: # significa que inseriu com sucesso
            
            # commit transaction
            #conn.comit()
            id_medico = rows[0][0]
            success = True
    

    except(Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{route_string} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
        excep = True

        # an error occurred, rollback
        conn.rollback()
        
    # --- ADICIONAR ESPECIALIDADES --------------
    if not excep and success and payload['especialidade'] != None:
        statement = "call add_especialidade(%s::integer, %s::varchar)"
        # ADICIONA ESPECIALIDE AO MEDICO
        for it_especialidade in payload['especialidade']:
            values = (payload['cc'], it_especialidade['nome'])
            try:
                cur.execute(statement, values)
                #rows = cur.fetchall()

            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f'{route_string} - error: {error}')
                response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
                excep = True

                # an error occurred, rollback
                conn.rollback()
                break
            # --- ADICIONAR SUBESPECIALIDADES --------------
            if (len(it_especialidade['subespecialidade']) > 0):
                statement1 = "call add_subespecialidade(%s::varchar, %s::varchar, %s::integer)"
                # ADICIONA SUBESPECIALIDADE AO MEDICO
                for it_subespecialidade in it_especialidade['subespecialidade']:
                    values = (it_subespecialidade['nome'], it_especialidade['nome'], payload['cc'])
                    try:
                        cur.execute(statement1, values)
                        #rows = cur.fetchall()

                    except (Exception, psycopg2.DatabaseError) as error:
                        logger.error(f'{route_string} - error: {error}')
                        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
                        excep = True

                        # an error occurred, rollback
                        conn.rollback()
                        break
                else:
                    # continuar se nao haver break no inner loop
                    continue
                # se houver break no inner loop sair do outer loop
                break
                
    if not excep and success:
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': f'Medico com id {id_medico} registado '}
    elif excep:
        pass
    else:
        response = {'status': StatusCodes['internal_error'], 'results': 'ha um medico ja inserido com a mesma cedula, ou o seccao esta fora dos valores pre-definidos'}
    if conn is not None:
        conn.close()

    return flask.jsonify(response)



#############################################
############# REGISTER NURSE ################
#############################################


@app.route('/dbproj/register/doctor', methods=['POST'])
def add_nurse():
    route_string = 'POST /dbproj/register/nurse'
    logger.info(route_string)
    payload = flask.request.get_json()      # payload é um dicionario

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'{route_string} - payload: {payload}')
    

    # do not forget to validate every argument, e.g.,:
    if 'nome' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'person name (nome) not in payload'}
        return flask.jsonify(response)
    if 'cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cc not in payload'}
        return flask.jsonify(response)
    if 'datanascimento' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'datanascimento not in payload'}
        return flask.jsonify(response)
    if 'sexo' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'sexo value not in payload'}
        return flask.jsonify(response)
    if 'telemovel' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'telemovel not in payload'}
        return flask.jsonify(response)
    if 'morada' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'morada not in payload'}
        return flask.jsonify(response)
    if 'gmail' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'gmail not in payload'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'password not in payload'}
        return flask.jsonify(response)
    if 'datacontratacao' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'datacontratacao not in payload'}
        return flask.jsonify(response)
    if 'seccao' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'seccao not in payload'}
        return flask.jsonify(response)
    if 'cedula' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cedula not in payload'}
        return flask.jsonify(response)
    if 'cargo' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cargo not in payload'}
        return flask.jsonify(response)
    
    if 'horastrabalho' not in payload:
            payload['horastrabalho'] = None
    if 'finalcontratacao' not in payload:
            payload['finalcontratacao'] = None
    if 'especialidade' not in payload:
            payload['especialidade'] = None

    statement = "call add_enfermeiro(%s::varchar, %s::integer, %s::date, %s::varchar, %s::integer, %s::varchar, %s::varchar, %s::date, %s::integer, %s::date, %s::integer, %s::varchar, %s::varchar, %s::varchar, null)"
    excep = False
    success = False
    response = ""

    # --- ADICIONAR ENFERMEIRO --------------
    values = (payload['nome'], payload['cc'], payload['datanascimento'], payload['sexo'], payload['telemovel'], payload['gmail'], payload['morada'], payload['datacontratacao'], payload['horastrabalho'], payload['finalcontratacao'], payload['cedula'], payload['seccao'], payload['cargo'], payload['password']);
    try:
        cur.execute(statement, values)
        rows = cur.fetchall()
        
        if rows[0][0] != 0: # significa que inseriu com sucesso
            
            # commit transaction
            #conn.comit()
            id_enfermeiro = rows[0][0]
            success = True
    

    except(Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{route_string} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
        excep = True

        # an error occurred, rollback
        conn.rollback()
        
    # --- ADICIONAR ESPECIALIDADES --------------
    if not excep and success and payload['especialidade'] != None:
        statement = "call add_especialidade(%s::integer, %s::varchar)"
        # ADICIONA ESPECIALIDE AO ENFERMEIRO
        for it_especialidade in payload['especialidade']:
            values = (payload['cc'], it_especialidade['nome'])
            try:
                cur.execute(statement, values)
                #rows = cur.fetchall()

            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f'{route_string} - error: {error}')
                response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
                excep = True

                # an error occurred, rollback
                conn.rollback()
                break
            # --- ADICIONAR SUBESPECIALIDADES --------------
            if (len(it_especialidade['subespecialidade']) > 0):
                statement1 = "call add_subespecialidade(%s::varchar, %s::varchar, %s::integer)"
                # ADICIONA SUBESPECIALIDADE AO ENFERMEIRO
                for it_subespecialidade in it_especialidade['subespecialidade']:
                    values = (it_subespecialidade['nome'], it_especialidade['nome'], payload['cc'])
                    try:
                        cur.execute(statement1, values)
                        #rows = cur.fetchall()

                    except (Exception, psycopg2.DatabaseError) as error:
                        logger.error(f'{route_string} - error: {error}')
                        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
                        excep = True

                        # an error occurred, rollback
                        conn.rollback()
                        break
                else:
                    # continuar se nao haver break no inner loop
                    continue
                # se houver break no inner loop sair do outer loop
                break
                
    if not excep and success:
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': f'Medico com id {id_enfermeiro} registado '}
    elif excep:
        pass
    else:
        response = {'status': StatusCodes['internal_error'], 'results': 'ha um medico ja inserido com a mesma cedula, ou o seccao esta fora dos valores pre-definidos'}
    if conn is not None:
        conn.close()

    return flask.jsonify(response)


#############################################
############# REGISTER ASSISTENT ############
#############################################


@app.route('/dbproj/register/assistent', methods=['POST'])
def add_assistent():
    route_string = 'POST /dbproj/register/assistent'
    logger.info(route_string)
    payload = flask.request.get_json()      # payload é um dicionario

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'{route_string} - payload: {payload}')
    

    # do not forget to validate every argument, e.g.,:
    if 'nome' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'person name (nome) not in payload'}
        return flask.jsonify(response)
    if 'cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cc not in payload'}
        return flask.jsonify(response)
    if 'datanascimento' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'datanascimento not in payload'}
        return flask.jsonify(response)
    if 'sexo' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'sexo value not in payload'}
        return flask.jsonify(response)
    if 'telemovel' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'telemovel not in payload'}
        return flask.jsonify(response)
    if 'morada' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'morada not in payload'}
        return flask.jsonify(response)
    if 'gmail' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'gmail not in payload'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'password not in payload'}
        return flask.jsonify(response)
    if 'datacontratacao' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'datacontratacao not in payload'}
        return flask.jsonify(response)
    if 'cedula' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cedula not in payload'}
        return flask.jsonify(response)
    
    if 'horastrabalho' not in payload:
            payload['horastrabalho'] = None
    if 'finalcontratacao' not in payload:
            payload['finalcontratacao'] = None
    if 'funcao' not in payload:
            payload['funcao'] = None
    

    statement = "call add_enfermeiro(%s::varchar, %s::integer, %s::date, %s::varchar, %s::integer, %s::varchar, %s::varchar, %s::date, %s::integer, %s::date, %s::integer, %s::varchar, %s::varchar, null)"
    excep = False
    success = False
    response = ""

    # --- ADICIONAR ASSISTENTE --------------
    values = (payload['nome'], payload['cc'], payload['datanascimento'], payload['sexo'], payload['telemovel'], payload['gmail'], payload['morada'], payload['datacontratacao'], payload['horastrabalho'], payload['finalcontratacao'], payload['cedula'], payload['funcao'], payload['password']);
    try:
        cur.execute(statement, values)
        rows = cur.fetchall()
        
        if rows[0][0] != 0: # significa que inseriu com sucesso
            
            # commit transaction
            #conn.comit()
            id_assistente = rows[0][0]
            success = True
    

    except(Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{route_string} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
        excep = True

        # an error occurred, rollback
        conn.rollback()
        
                  
    finally:
        if not excep and success:
            response = {'status': StatusCodes['success'], 'results': f'Paciente com id {id_assistente} inserido '}
        elif excep:
            pass
        else:
            response = {'status': StatusCodes['internal_error'], 'results': 'ja ha uma pessoa com o mesmo id ou a cedula ja existe'}
        if conn is not None:
            conn.close()      

    return flask.jsonify(response)


#################################################
############## ADD PRESCRIPTION #################
#################################################


@app.route('/dbproj/prescription/', methods=['POST'])
def add_prescription():
    route_string = 'POST /dbproj/prescription/'
    logger.info(route_string)
    payload = flask.request.get_json()      # payload é um dicionario

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'{route_string} - payload: {payload}')
    

    # do not forget to validate every argument, e.g.,:
    if 'validade' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'validade not in payload'}
        return flask.jsonify(response)
    if 'entrada_conta_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'event_id (nome) not in payload'}
        return flask.jsonify(response)
    if 'descricaodosagem' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'descricaodosagem not in payload'}
        return flask.jsonify(response)
    if 'tipo' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'event_type (tipo) not in payload'}
        return flask.jsonify(response)
    
    statement = "call adicionar_prescricao(%s::integer, %s::varchar, %s::date, %s::timestamp, null)"
    med_founs = False
    excep = False
    success = False
    response = ""
    data_hora_atual = datetime.today().strftime('%Y-%m-%d %H:%M')
    
    # --- ADICIONAR RECEITA --------------
    values = (payload['entrada_conta_id'], payload['tipo'], payload['validade'], data_hora_atual);
    try:
        cur.execute(statement, values)
        rows = cur.fetchall()
    
        if rows[0][0] != 0: # significa que inseriu com sucesso
        
            # commit transaction
            #conn.comit()
            id_receita = rows[0][0]
            success = True


    except(Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{route_string} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
        excep = True

        # an error occurred, rollback
        conn.rollback()
    
    # --- ADICIONAR MEDICAMENTOS --------------
    if not excep and success:
      statement = "call add_descricaodosagem(%s::integer, %s::integer, %s::integer, %s::varchar, %s::varchar, %s::integer, null)"
      # ADICIONA MEDICAMENTO A RECEITA
      for parcela_receita in payload['descricaodosagem']:
          values = (str(id_receita), payload['entrada_conta_id'], parcela_receita['medicamento_id'], parcela_receita['frequencia'], parcela_receita['periodo'], parcela_receita['quantidade'])
          try:
              cur.execute(statement, values)
              rows = cur.fetchall()
              if rows[0][0] != 0: # significa que inseriu com sucesso
                  med_founs = True

          except (Exception, psycopg2.DatabaseError) as error:
              logger.error(f'{route_string} - error: {error}')
              response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
              excep = True

              # an error occurred, rollback
              conn.rollback()
              break
      if not excep and med_founs and success:
          conn.commit()
          response = {'status': StatusCodes['success'], 'results': f'prescription_id: {id_receita}'}
      elif not excep and med_founs == False and success:
          response = {'status': StatusCodes['internal_error'], 'results': 'medicamento nao existe'}
      elif not excep and success == False:
          response = {'status': StatusCodes['internal_error'], 'results': 'Consulta/hospitalizacao nao existe ou nao esta a ocorrer'}
      else:
          pass
      
      if conn is not None:
          conn.close() 
          
      return flask.jsonify(response)



              
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
    
    response = ""

    # ----- PROCEDURE NO SERVER -----
    for gab in gabinetes:   
        values = (gab, payload['doctor_id'], payload['time_stamp'], payload['descricao'], payload['cc'], price_appointment) # colocamos o mm preço que a consulta
        try:
            cur.execute(statement, values)
            rows = cur.fetchall()

            #print("rows[0][0]: ", rows[0][0])
            
            if rows[0][0] == 0: # significa que inseriu com sucesso
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


#############################################
############## SCHEDULE SURGERY #############
#############################################

@app.route('/dbproj/surgery', defaults={'id_hosp': None}, methods=['POST'])
@app.route('/dbproj/surgery/<int:id_hosp>', methods=['POST'])
def add_Surgery(id_hosp):
    route_string = 'POST /dbproj/surgery/<id_hosp>'
    logger.info(route_string)
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'{route_string} - payload: {payload}')

    # do not forget to validate every argument, e.g.,:
    if 'doctor_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'doctor_id not in payload'}
        return flask.jsonify(response)
    if 'enf_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'enf_cc value not in payload'}
        return flask.jsonify(response)
    if 'time_stamp' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'time_stamp not in payload'}
        return flask.jsonify(response)
    if 'pacient_cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'pacient_cc value not in payload'}
        return flask.jsonify(response)
    if 'nurses' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'nurses not in payload'}
        return flask.jsonify(response)
    
    if 'descricao_hosp' in payload:
        descricao_hosp = payload['descricao_hosp']
    else:
        descricao_hosp = ''
    if 'descricao_surg' in payload:
        descricao_surg = payload['descricao_surg']
    else:
        descricao_surg = ''
    
    doc_id = payload['doctor_id']
    time_stamp = payload['time_stamp']

    cama_found = False
    sala_found = False
    excep = False
    hora_final = datetime.strptime(payload['time_stamp'], '%d-%m-%Y %H:%M') + timedelta(hours=1)
    str_hora_final = hora_final.strftime('%d-%m-%Y %H:%M')


    if id_hosp is None:     # temos de criar hospitalizacao
        logger.debug(f'id_hosp: {id_hosp}')

        # parameterized queries, good for security and performance
        # statement = 'INSERT INTO dep (ndep, local, nome) VALUES (%s, %s, %s)'
        # values = (payload['ndep'], payload['localidade'], payload['nome'])

        statement = "call addHosp(%s::smallint, %s::bigint, %s::timestamp, %s::timestamp, %s::varchar, %s::bigint, %s::real, null)"

        # --- ADICIONAR HOSPITALIZACAO, PROCURAR CAMA --------------
        for cama in camas: 
            print(f"cama: {cama}")
            values = (cama, payload['enf_id'], payload['time_stamp'],  str_hora_final, descricao_hosp, payload['pacient_cc'], price_appointment)
            try:
                cur.execute(statement, values)
                rows = cur.fetchall()

                #print("rows[0][0]: ", rows[0][0])
                
                if rows[0][0] != 0:
                    #conn.commit()           # aqui n faz comit, é mais a frente
                    id_hosp = rows[0][0]
                    cama_found = True
                    break

            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f'{route_string} - error: {error}')
                response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
                excep = True

                # an error occurred, rollback
                conn.rollback()
                break

        # --- ADICIONAR CIRURGIA, PROCURAR SALA --------------
        if not excep and cama_found:       # se n ocorreu excepçao
            # se do postman vier descricao_hosp vai ser ignorado, pq aqui a hospitalizacao ja existe
            
            statement = 'call addSurg(%s::smallint, %s::bigint, %s::timestamp, %s::timestamp, %s::varchar, %s::bigint, %s::real, %s::integer, null);'

            # ADICIONAR CIRURGIA, PROCURAR SALA DISPONIVEL
            for sala in salas:
                print(f"sala: {sala}")
                values = (sala, doc_id, payload['time_stamp'], str_hora_final, descricao_surg, payload['pacient_cc'], price_surgery, id_hosp)
                try:
                    cur.execute(statement, values)
                    rows = cur.fetchall()

                    #print("rows[0][0]: ", rows[0][0])

                    if rows[0][0] != 0:
                        #conn.commit()       # nao faz commit ja
                        entrada_surg_id = rows[0][0]
                        #print("entrada cirurgia: ", entrada_surg_id)
                        sala_found = True
                        break

                except (Exception, psycopg2.DatabaseError) as error:
                    logger.error(f'{route_string} - error: {error}')
                    response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
                    excep = True

                    # an error occurred, rollback
                    conn.rollback()
                    break

            # --- ADICIONAR ENFERMEIROS --------------
            if not excep and sala_found:
                print("a ir inserir enfs...")
                statement = "call addEnfToSurg(%s::bigint, %s::integer, %s::timestamp, %s::timestamp)"
                # ADICIONA ENFERMEIROS à CIRURGIA
                #print("nurses:", payload['nurses'])
                for nurse in payload['nurses']:
                    values = (nurse, entrada_surg_id, payload['time_stamp'], str_hora_final)
                    try:
                        cur.execute(statement, values)
                        #rows = cur.fetchall()

                    except (Exception, psycopg2.DatabaseError) as error:
                        logger.error(f'{route_string} - error: {error}')
                        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
                        excep = True

                        # an error occurred, rollback
                        conn.rollback()
                        break

        if not excep and sala_found:
            conn.commit()
            response = {'status': StatusCodes['success'], 'results': f'Cirurgia marcada com medico {doc_id} dia {time_stamp} - sala operatoria {sala}\nCama da hospitalizacao {cama}'}
        elif excep:
            #response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
            pass
        else:
            response = {'status': StatusCodes['internal_error'], 'results': 'não há salas disponiveis ou o medico está ocupado nesta hora'}

    else:       # HOSPITALIZACAO JA EXISTE - ADICIONAR CIRURGIA
        
        # ADICIONAR CIRURGIA -----------------
        statement = 'call addSurg(%s::smallint, %s::bigint, %s::timestamp, %s::timestamp, %s::varchar, %s::bigint, %s::real, %s::integer, null);'
        hora_final = datetime.strptime(payload['time_stamp'], '%d-%m-%Y %H:%M') + timedelta(hours=1)
        str_hora_final = hora_final.strftime('%d-%m-%Y %H:%M')

        # ADICIONAR CIRURGIA, PROCURAR SALA DISPONIVEL
        for sala in salas:
            print(f"sala: {sala}")
            values = (sala, doc_id, payload['time_stamp'], str_hora_final, descricao_surg, payload['pacient_cc'], price_surgery, id_hosp)
            try:
                cur.execute(statement, values)
                rows = cur.fetchall()

                #print("rows[0][0]: ", rows[0][0])

                if rows[0][0] != 0:
                    #conn.commit()       # nao faz commit ja
                    entrada_surg_id = rows[0][0]
                    #print("entrada cirurgia: ", entrada_surg_id)
                    sala_found = True
                    break

            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f'{route_string} - error: {error}')
                response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
                excep = True

                # an error occurred, rollback
                conn.rollback()
                break

        #print(excep, sala_found)
        # --- ADICIONAR ENFERMEIROS --------------
        if not excep and sala_found:
            print("a ir inserir enfs...")
            statement = "call addEnfToSurg(%s::bigint, %s::integer, %s::timestamp, %s::timestamp)"
            # ADICIONA ENFERMEIROS à CIRURGIA
            #print("nurses:", payload['nurses'])
            for nurse in payload['nurses']:
                values = (nurse, entrada_surg_id, payload['time_stamp'], str_hora_final)
                try:
                    cur.execute(statement, values)
                    #rows = cur.fetchall()

                except (Exception, psycopg2.DatabaseError) as error:
                    logger.error(f'{route_string} - error: {error}')
                    response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
                    excep = True

                    # an error occurred, rollback
                    conn.rollback()
                    break
    
        if not excep and sala_found:
            conn.commit()
            response = {'status': StatusCodes['success'], 'results': f'Cirurgia marcada com medico {doc_id} dia {time_stamp} - sala operatoria {sala}\nHospitalizacao {id_hosp}'}
        elif excep:
            #response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
            pass
        else:
            response = {'status': StatusCodes['internal_error'], 'results': 'não há salas disponiveis ou o medico está ocupado nesta hora'}

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
