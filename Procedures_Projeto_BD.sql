----------------------- PROCEDURES ---------------------------

------- ADICIONAR PACIENTE ------------
create or replace procedure add_paciente(in s_nome varchar(512),
					 in s_cc integer,
				     in s_datanascimento date,
					 in s_sexo varchar(10),
					 in s_telemovel integer,
			         in s_gmail varchar(20),
					 in s_morada varchar(50),
				     in s_tipo_sangue varchar(512),
					 in s_altura float(8),
					 in s_peso float(8),
					 in s_password varchar(512),
				     out resultado integer)
language plpgsql
as $$
begin
	-- inicializar variavel de retorno
	resultado := 0;

	-- verificar se o paciente ja existe:
	if exists (
		select 1 from pessoa
		where cc = s_cc)
	then
		raise exception 'Pessoa com CC % ja existe', s_cc;
	end if;
	
	-- verificar se o email do paciente e unico
	if exists (
			select 1 from pessoa
			where gmail = s_gmail)
	then
		raise exception 'Pessoa com gmail % ja existe', s_gmail;
	end if;
			
	insert into pessoa(nome, cc, datanascimento, sexo, telemovel, gmail, morada, "password")
	values(s_nome, s_cc, s_datanascimento, s_sexo, s_telemovel, s_gmail, s_morada, s_password)
	returning cc into resultado;

	insert into paciente(tiposangue, altura, peso, pessoa_cc)
	values(s_tipo_sangue, s_altura, s_peso, s_cc);
	resultado :=1;

	exception
		when others then
			-- Se ocorrer um erro, chamar a exceção
			raise;
end;
$$;

----- ADICIONAR ASSISTENTE ----------------------

create or replace procedure add_assistente(in s_nome varchar(512),
				           in s_cc integer,
				           in s_datanascimento date,
				           in s_sexo varchar(10),
				           in s_telemovel integer,
				           in s_gmail varchar(20),
				           in s_morada varchar(50),
					       in s_datacontratacao date,
					       in s_horastrabalho integer,
					       in s_finalcontratacao date,
					       in s_cedula integer,
					       in s_funcao varchar(512),
					       in s_password varchar(512),
				           out resultado integer)
language plpgsql
as $$
begin
	-- inicializar variavel de retorno
	resultado := 0;
	
	-- verificar se o CC do assistente ja existe nos empregados
	if exists (
		select 1 from empregado
		where pessoa_cc = s_cc)
	then
		raise exception 'Empregado com CC % ja existe', s_cc;
	end if;
	
	-- verificar se o gmail do assistente ja existe
	if exists (
		select 1 from pessoa
		where gmail = s_gmail)
	then
		raise exception 'Pessoa com gmail % ja existe', s_gmail;
	end if;
	
	-- verificar se s_cedula é um valor novo
	if exists (
		select 1 from assistente
		where cedula = s_cedula)
	then
		raise exception 'Numero de cedula % ja existe', s_cedula;
	end if;
	
	insert into pessoa(nome, cc, datanascimento, sexo, telemovel, gmail, morada, "password")
	values(s_nome, s_cc, s_datanascimento, s_sexo, s_telemovel, s_gmail, s_morada, s_password);
	--returning cc into resultado;

	insert into empregado(horastrabalho, datacontratacao, finalcontratacao, pessoa_cc)
	values(s_horastrabalho, s_datacontratacao, s_finalcontratacao, s_cc)
	returning id into resultado;

	insert into assistente(cedula, funcao, empregado_pessoa_cc)
	values (s_cedula, s_funcao, s_cc);
					
exception
	when others then
		-- Se ocorrer um erro, chamar a exceção
		raise;
end;
$$;

------ ADICIONAR MEDICO ------------------------

create or replace procedure add_medico(in s_nome varchar(512),
				       in s_cc integer,
			           in s_datanascimento date,
				       in s_sexo varchar(10),
				       in s_telemovel integer,
				       in s_gmail varchar(20),
				       in s_morada varchar(50),
				       in s_datacontratacao date,
				       in s_horastrabalho integer,
				       in s_finalcontratacao date,
				       in s_cedula integer,
				       in s_seccao varchar(512),
				       in s_info_adicional text,
				       in s_password varchar(512),
				       out resultado integer)
language plpgsql
as $$
begin
	-- inicializar variavel de retorno
	resultado := 0;

	-- verificar se o medico ja existe:
	if exists (
		select 1 from pessoa
		where cc = s_cc)
	then
		raise exception 'Pessoa com CC % ja existe', s_cc;
	end if;
	
	-- verificar se o gmail do medico e unico
	if exists (
			select 1 from pessoa
			where gmail = s_gmail)
	then
		raise exception 'Pessoa com gmail % ja existe', s_gmail;
	end if;

	-- verificar se s_cedula é um valor novo
	if exists (
		select 1 from medico
		where cedula = s_cedula)
	then
		raise exception 'Numero de cedula % ja existe', s_cedula;
	end if;

	insert into pessoa(nome, cc, datanascimento, sexo, telemovel, gmail, morada, "password")
	values(s_nome, s_cc, s_datanascimento, s_sexo, s_telemovel, s_gmail, s_morada, s_password);

	insert into empregado(horastrabalho, datacontratacao, finalcontratacao, pessoa_cc)
	values(s_horastrabalho, s_datacontratacao, s_finalcontratacao, s_cc)
	returning id into resultado;

	insert into medico(cedula, seccao, info_adicional, empregado_pessoa_cc)
	values (s_cedula, s_seccao, s_info_adicional, s_cc);
	
exception
	when others then
		-- Se ocorrer um erro, chamar a exceção
		raise;
end;
$$;

---- ADICIONAR ENFERMEIRO ----------

create or replace procedure add_enfermeiro(in s_nome varchar(512),
				           in s_cc integer,
				           in s_datanascimento date,
				           in s_sexo varchar(10),
				           in s_telemovel integer,
				           in s_gmail varchar(20),
					   	   in s_morada varchar(50),
				           in s_datacontratacao date,
				           in s_horastrabalho integer,
				           in s_finalcontratacao date,
				           in s_cedula integer,
				           in s_seccao varchar(512),
				           in s_cargo varchar(512),
					  	   in s_password varchar(512),
				           out resultado integer)
language plpgsql
as $$
begin
	-- inicializar variavel de retorno
	resultado := 0;
	
	-- verificar se o email do enfermeiro e unio
	if exists (
			select 1 from pessoa
			where gmail = s_gmail)
	then
		raise exception 'Pessoa com gmail % ja existente', s_gmail;
	end if;
	
	-- verificar se o cc do enfermeiro ja existe:
	if exists (
			select 1 from empregado
			where pessoa_cc = s_cc)
	then
		raise exception 'Empregado com CC % ja existe', s_cc;
	end if;
				
	-- verificar se s_cedula é um valor novo
	if exists (
		select 1 from enfermeiro
		where cedula = s_cedula)
	then
		raise exception 'Numero de cedula % ja existe', s_cedula;
	end if;
	
	insert into pessoa(nome, cc, datanascimento, sexo, telemovel, gmail, morada, "password")
	values(s_nome, s_cc, s_datanascimento, s_sexo, s_telemovel, s_gmail, s_morada, s_password);

	insert into empregado(horastrabalho, datacontratacao, finalcontratacao, pessoa_cc)
	values(s_horastrabalho, s_datacontratacao, s_finalcontratacao, s_cc)
	returning id into resultado;

	insert into enfermeiro(cedula, seccao, cargo, empregado_pessoa_cc)
	values (s_cedula, s_seccao, s_cargo, s_cc);

exception
	when others then
		-- Se ocorrer um erro, chamar a exceção
		raise;
end;
$$;

---- ADICIONAR ESPECIALIDADE -------------

create or replace procedure add_especialidade(in s_empregado_pessoa_cc integer,
											  in s_nome varchar(512),
											  out resultado integer)
language plpgsql
as $$
begin
	-- inicializar variavel de saida
	resultado := 0;
	
	-- verificar se o empregado existe
	if exists (
			select 1 from pessoa
			where cc = s_empregado_pessoa_cc)
	then
		
		-- verificar se especialidade existe
		begin
			if not exists (
				select 1 from especialidade
				where nome = s_nome)
			then
				insert into especialidade(nome)
				values (s_nome);
			end if;
				
			insert into empregado_especialidade(empregado_pessoa_cc, especialidade_nome)
			values(s_empregado_pessoa_cc, s_nome);

			resultado := 1;
		end;
	else
		raise exception 'Pessoa com CC % inexistente', s_empregado_pessoa_cc;
	end if;
	
exception
	when others then
		-- Se ocorrer um erro, chamar a exceção
		raise;
end;
$$;

----- ADICIONAR SUBESPECIALIDADE --------

create or replace procedure add_subespecialidade(in s_cc integer,
						  in s_nome varchar(512),
					      in s_nome_especialidade varchar(512),
					      out resultado integer)
language plpgsql
as $$
begin
	-- inicializar variavel de saida
	resultado := 0;
	
	-- verificar se o empregado existe
	if exists (
			select 1 from pessoa
			where cc = s_empregado_pessoa_cc)
	then
		
		-- verificar se especialidade existe
		begin
			if exists (
				select 1 from especialidade
				where nome = s_nome)
			then
				-- verificar se subespecialidade existe
				if exists (
					select 1 from subespecialidade
					where nome = s_nome)
				then
					raise exception 'Subespecialidade % ja esta inserida', s_nome;
				else

				-- verificar que empregado tem especialidade
				if not exists(
					select 1 from empregado_especialidade
					where empregado_pessoa_cc = s_cc and nome = s_nome
				) then
					raise exception 'Empregado % nao tem especialidade %', s_cc, s_nome;
				end if;
				
				-- se houver um empregado com a especialidade e sem esta subespecialidade, inserir na tabela
				insert into subespecialidade(empregado_pessoa_cc, nome)
				values (s_empregado_pessoa_cc, s_nome);
				resultado := 1;

			else
				raise exception 'Especialidade % nao existe', s_nome_especialidade;
			end if;
		end;
	else
		raise exception 'Empregado de CC % não existe', s_especialidade_empregado_pessoa_cc;
	end if;
			
	exception
		when others then
			-- Se ocorrer um erro, chamar a exceção
			raise;			
end;
$$;

---- ADICIONAR RECEITA ---------------------

create or replace procedure adicionar_receita(in s_entrada_conta_id integer,
					      in s_tipo varchar(512),
					      in s_validade date,
					      in cur_time timestamp,
					      out resultado integer)
language plpgsql
as $$
declare
	cursor_medicamento cursor for
		select entrada_conta_id
			from prescricao pres
			inner join entrada_conta as e on e.id = pres.entrada_conta_id
			where e.id = s_entrada_conta_id
				and e.datahoraentrada < cur_time
				and (e.datahorasaida is null or e.datahorasaida > cur_time);
	rec RECORD;
	ultimo_id_entrada entrada_conta.id%type;
begin
	-- inicializar variavel saida
	resultado := 0;
	
	-- abrir cursor
	open cursor_medicamento;
	
	-- buscar primeira linha
	fetch cursor_medicamento into rec;
	
	-- se não encontrou registos:
	if not found then
	
		-- verificar se a entrada corrresponde ao tipo (hospitalizacao/consulta) existe
		begin
			if exists (
				select 1 from entrada_conta e
					full join consulta as co on e.id = co.entrada_conta_id
					full join hospitalizacao as ho on e.id = ho.entrada_conta_id
					where "id" = s_entrada_conta_id)
			then
				begin
						
					-- verificar se consulta/hospitalizaçao está a ocorrer
					if exists(
						select 1
							from entrada_conta e
								full join consulta as co on e.id = co.entrada_conta_id
								full join hospitalizacao as ho on e.id = ho.entrada_conta_id
								where e.id = s_entrada_conta_id
									and e.datahoraentrada < cur_time
									and (e.datahorasaida is null or e.datahorasaida > cur_time)
					)
					then
						begin
							-- inserir em prescricao
							insert into prescricao(validade, tipo, entrada_conta_id)
							values(s_validade, s_tipo, s_entrada_conta_id)
							returning numpresc into resultado;
						end;
					else
						raise exception 'A consulta/hospitalizacao nao esta a ocorrer';
					end if;
				end;
			else
				raise exception 'O id % nao corresponde a nenhuma consulta ou hospitalizacao', s_entrada_conta_id;
			end if;
		end;
	end if;
	
	-- fechar cursor
	close cursor_medicamento;

	exception
		when others then
			-- Se ocorrer um erro, chamar a exceção
			raise;
end;
$$;

---- ADICIONAR DESCRIÇAO DOSAGEM -----------------

create or replace procedure add_descricaodosagem(in s_id_receita integer,
						 in s_entrada_conta_id integer,
						 in s_medicamento_id integer,
					 	 in s_frequencia varchar(512),
						 in s_periodo varchar(512),
						 in s_quantidade integer,
						 out resultado integer)
language plpgsql
as $$
begin
	
	-- inicializar variavel de retorno
	resultado := 0;
	
	-- verificar se receita existe
	if exists (
		select 1 from prescricao
		where numpresc = s_id_receita)
	then
		begin
			
			-- verificar se medicamento existe
			if exists (
				select 1 from medicamento
				where "id" = s_medicamento_id)
			then
				begin
					-- inserir descricaodosagem
					insert into descricaodosagem(prescricao_entrada_conta_id, medicamento_id, quantidade, periodo, frequencia)
					values (s_entrada_conta_id, s_medicamento_id, s_quantidade, s_periodo, s_frequencia)
					returning s_id_receita into resultado;
				end;
			else
				raise exception 'Medicamento com id % nao existe', s_medicamento_id;
			end if;
		end;
	else
		raise exception 'Prescricao com id % nao existe', s_id_receita;
	end if;
	
	exception
		when others then
			-- Se ocorrer um erro, chamar a exceção
			raise;
end;
$$;

---- ADICIONAR CONSULTA --------------

CREATE OR REPLACE PROCEDURE addAppointment(
    IN gab smallint,
    IN m_id bigint,
    IN con_time timestamp,
	IN con_time_end timestamp,
    IN descript varchar,
    IN pacient_cc bigint,
    IN preco real,
    OUT var integer)
LANGUAGE plpgsql
AS $$
DECLARE
    cursor_appointment CURSOR FOR
        SELECT emp.id, c.gabinete, ent.datahoraentrada
        FROM medico m
        INNER JOIN consulta AS c ON m.empregado_pessoa_cc = c.medico_empregado_pessoa_cc
        INNER JOIN empregado AS emp ON m.empregado_pessoa_cc = emp.pessoa_cc
        INNER JOIN entrada_conta AS ent ON c.entrada_conta_id = ent.id
        WHERE (c.gabinete = gab AND ent.datahoraentrada < con_time_end and ent.datahorasaida > con_time) 
            OR (emp.id = m_id AND ent.datahoraentrada = con_time);
    rec RECORD;
    ultimo_id entrada_conta.id%TYPE;
    medico_cc pessoa.cc%TYPE;
BEGIN
    -- Inicializar a variável de saída
    var := 0;

    -- Abrir o cursor
    OPEN cursor_appointment;

    -- Buscar a primeira linha
    FETCH cursor_appointment INTO rec;

    -- Verificar se não encontrou registros
    IF NOT FOUND THEN
        -- Buscar o CC do médico & Verificar se o médico existe
		BEGIN
			SELECT pessoa_cc INTO medico_cc
				FROM empregado emp
				INNER JOIN medico m on emp.pessoa_cc = m.empregado_pessoa_cc
				WHERE id = m_id;
				IF NOT FOUND THEN
					RAISE EXCEPTION 'Médico com ID % não encontrado', m_id;
				END IF;
		END;
		
		-- Buscar o CC do paciente e verificar se ele existe
        BEGIN
            PERFORM cc
            FROM pessoa
            WHERE cc = pacient_cc;
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Paciente com CC % não encontrado', pacient_cc;
            END IF;
        END;

        -- Inserir em entrada_conta
        INSERT INTO entrada_conta (datahoraentrada, datahorasaida, descricao, conta_valortotal, conta_valorpago, paciente_pessoa_cc) 
        VALUES (con_time, con_time_end, descript, preco, 0, pacient_cc) 
        RETURNING id INTO ultimo_id;

        -- Inserir em consulta
        INSERT INTO consulta (gabinete, medico_empregado_pessoa_cc, entrada_conta_id) 
        VALUES (gab, medico_cc, ultimo_id);

        -- Definir a variável de saída para 1
        var := 1;
    END IF;

    -- Fechar o cursor
    CLOSE cursor_appointment;
EXCEPTION
    WHEN OTHERS THEN
        -- Se ocorrer um erro, relançar a exceção
        RAISE;
END;
$$;

---- ADICIONAR HOSPITALIZACAO ----------------

CREATE OR REPLACE PROCEDURE addHosp(
    IN nova_cama smallint,
    IN enf_id bigint,
    IN hosp_time timestamp,
	IN hosp_time_end timestamp,
    IN descript varchar(512),
    IN paciente_cc bigint,
    IN preco real,
    OUT out_var integer)
LANGUAGE plpgsql
AS $$
DECLARE
    cursor_hosp CURSOR FOR
        SELECT cama
		FROM hospitalizacao h
		INNER JOIN entrada_conta e ON e.id = h.entrada_conta_id
		WHERE h.cama = nova_cama
		  AND e.datahoraentrada < hosp_time_end
		  AND (e.datahorasaida IS NULL OR e.datahorasaida > hosp_time);	-- NULL significa q n se sabe quando vai sair
    rec RECORD;
    ultimo_id entrada_conta.id%TYPE;
    enf_cc pessoa.cc%TYPE;
BEGIN
    -- Inicializar a variável de saída
    out_var := 0;

    -- Abrir o cursor
    OPEN cursor_hosp;

    -- Buscar a primeira linha
    FETCH cursor_hosp INTO rec;

    -- Verificar se não encontrou registros
    IF NOT FOUND THEN
        -- Buscar o CC do enfermeiro & Verificar se o enfermeiro existe
		BEGIN
			SELECT pessoa_cc INTO enf_cc
				FROM empregado emp
				INNER JOIN enfermeiro e on emp.pessoa_cc = e.empregado_pessoa_cc
				WHERE id = enf_id;
				IF NOT FOUND THEN
					RAISE EXCEPTION 'Enfermeiro com ID % não encontrado', enf_id;
				END IF;
		END;
		
		-- Buscar o CC do paciente e verificar se ele existe
        BEGIN
            PERFORM cc
            FROM pessoa
            WHERE cc = paciente_cc;
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Paciente com CC % não encontrado', paciente_cc;
            END IF;
        END;

        -- Inserir em entrada_conta
        INSERT INTO entrada_conta (datahoraentrada, datahorasaida, descricao, conta_valortotal, conta_valorpago, paciente_pessoa_cc) 
        VALUES (hosp_time, hosp_time_end, descript, preco, 0, paciente_cc) -- cc do paciente
		RETURNING id INTO out_var;

        -- Inserir em consulta
        INSERT INTO hospitalizacao (cama, enfermeiro_empregado_pessoa_cc, entrada_conta_id)
        VALUES (nova_cama, enf_cc, out_var);
		--RETURNING entrada_conta_id INTO var;

        --out_var := ultimo_id;
    END IF;

    -- Fechar o cursor
    CLOSE cursor_hosp;
EXCEPTION
    WHEN OTHERS THEN
        -- Se ocorrer um erro, relançar a exceção
        RAISE;
END;
$$;

------ ADICIONAR CIRURGIA ----------------------------

CREATE OR REPLACE PROCEDURE addSurg(
    IN nova_sala smallint, 
    IN med_id bigint,
    IN surg_time timestamp,
	IN surg_time_end timestamp,
    IN descript varchar(512),
    IN paciente_cc bigint,
    IN preco real,
	IN id_hosp integer,
    OUT var integer)
LANGUAGE plpgsql
AS $$
DECLARE
    cursor_surg CURSOR FOR
        SELECT sala
		FROM cirurgia c
		INNER JOIN entrada_conta e ON e.id = c.entrada_conta_id
		WHERE c.sala = nova_sala
		  AND e.datahoraentrada < surg_time_end
		  AND (e.datahorasaida IS NULL OR e.datahorasaida > surg_time);	-- NULL significa q n se sabe quando vai sair
    rec RECORD;
    --ultimo_id entrada_conta.id%TYPE;
    med_cc pessoa.cc%TYPE;
BEGIN
    -- Inicializar a variável de saída
    var := 0;

    -- Abrir o cursor
    OPEN cursor_surg;

    -- Buscar a primeira linha
    FETCH cursor_surg INTO rec;

    -- Verificar se não encontrou registros
    IF NOT FOUND THEN
        -- Buscar o CC do medico & Verificar se o enfermeiro existe
		BEGIN
			select pessoa_cc INTO med_cc
				FROM empregado emp
				INNER JOIN medico m on emp.pessoa_cc = m.empregado_pessoa_cc
				WHERE id = med_id;
				IF NOT FOUND THEN
					RAISE EXCEPTION 'Medico com ID % não encontrado', med_id;
				END IF;
		END;
		
		-- verificar se medico disponivel
		if exists(
			select 1 from entrada_conta e
			full join consulta co on e.id = co.entrada_conta_id
			full join cirurgia ci on e.id = ci.entrada_conta_id
				where (ci.medico_empregado_pessoa_cc = med_cc or co.medico_empregado_pessoa_cc = med_cc)
				AND e.datahoraentrada < surg_time_end AND (e.datahorasaida IS NULL OR e.datahorasaida > surg_time)
			)
		then
			RAISE EXCEPTION 'Medico ocupado neste horario';
		END if;
		
		-- Buscar o CC do paciente e verificar se ele existe
        BEGIN
            PERFORM cc
            FROM pessoa
            WHERE cc = paciente_cc;
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Paciente com CC % não encontrado', paciente_cc;
            END IF;
        END;

        -- Inserir em entrada_conta
        INSERT INTO entrada_conta (datahoraentrada, datahorasaida, descricao, conta_valortotal, conta_valorpago, paciente_pessoa_cc) 
        VALUES (surg_time, surg_time_end, descript, preco, 0, paciente_cc) -- cc do paciente
		RETURNING id INTO var;

        -- Inserir em cirurgia
        INSERT INTO cirurgia (sala, medico_empregado_pessoa_cc, entrada_conta_id)
        VALUES (nova_sala, med_cc, var);

		-- Inserir em cirurgia_hospitalizacao
		insert into cirurgia_hospitalizacao (cirurgia_entrada_conta_id, hospitalizacao_entrada_conta_id)
		values (var, id_hosp);
        
    END IF;

    -- Fechar o cursor
    CLOSE cursor_surg;
EXCEPTION
    WHEN OTHERS THEN
        -- Se ocorrer um erro, relançar a exceção
        RAISE;
END;
$$;

----- ADICIONAR ENFERMEIRO A CIRURGIA -----------

CREATE OR REPLACE PROCEDURE addEnfToSurg(
	IN enf_id bigint,
	IN surg_id integer,
	IN surg_time timestamp,
	IN surg_time_end timestamp
)
LANGUAGE plpgsql
AS $$
DECLARE
	enf_cc pessoa.cc%TYPE;
BEGIN
	-- Buscar o CC do enfermeiro & Verificar se o enfermeiro existe
	BEGIN
		SELECT pessoa_cc INTO enf_cc
			FROM empregado emp
			INNER JOIN enfermeiro e on emp.pessoa_cc = e.empregado_pessoa_cc
			WHERE id = enf_id;
			IF NOT FOUND THEN
				RAISE EXCEPTION 'Enfermeiro com ID % não encontrado', enf_id;
			END IF;
	END;
	
	if exists(
		select 1 from enfermeiro_cirurgia e_c
		inner join entrada_conta e on e_c.cirurgia_entrada_conta_id = e.id
		where enfermeiro_empregado_pessoa_cc = enf_cc
			AND e.datahoraentrada < surg_time_end
		  	AND (e.datahorasaida IS NULL OR e.datahorasaida > surg_time)
	) then
		RAISE EXCEPTION 'Enfermeiro % ocupado neste horario', enf_cc;
	END if;
	
	insert into enfermeiro_cirurgia(enfermeiro_empregado_pessoa_cc, cirurgia_entrada_conta_id)
	values(enf_cc, surg_id);
	
EXCEPTION
    WHEN OTHERS THEN
        -- Se ocorrer um erro, relançar a exceção
        RAISE;
END;
$$;

---- LOGIN ---------------------

CREATE OR REPLACE PROCEDURE addEnfToSurg(
	IN enf_id bigint,
	IN surg_id integer,
	IN surg_time timestamp,
	IN surg_time_end timestamp
)
LANGUAGE plpgsql
AS $$
DECLARE
	enf_cc pessoa.cc%TYPE;
BEGIN
	-- Buscar o CC do enfermeiro & Verificar se o enfermeiro existe
	BEGIN
		SELECT pessoa_cc INTO enf_cc
			FROM empregado emp
			INNER JOIN enfermeiro e on emp.pessoa_cc = e.empregado_pessoa_cc
			WHERE id = enf_id;
			IF NOT FOUND THEN
				RAISE EXCEPTION 'Enfermeiro com ID % não encontrado', enf_id;
			END IF;
	END;
	
	if exists(
		select 1 from enfermeiro_cirurgia e_c
		inner join entrada_conta e on e_c.cirurgia_entrada_conta_id = e.id
		where enfermeiro_empregado_pessoa_cc = enf_cc
			AND e.datahoraentrada < surg_time_end
		  	AND (e.datahorasaida IS NULL OR e.datahorasaida > surg_time)
	) then
		RAISE EXCEPTION 'Enfermeiro % ocupado neste horario', enf_cc;
	END if;
	
	insert into enfermeiro_cirurgia(enfermeiro_empregado_pessoa_cc, cirurgia_entrada_conta_id)
	values(enf_cc, surg_id);
	
EXCEPTION
    WHEN OTHERS THEN
        -- Se ocorrer um erro, relançar a exceção
        RAISE;
END;
$$;