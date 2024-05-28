call add_paciente('José Andrade', 100200300, '1976-07-12', 'M', 933333333,
			 'andrada@gmail.com', 'Covões', 'A+', 1.81, 75,
			 '$2b$12$LhSlIyDutn.DgblushQ..Ov.P8a/P5frMAWuELxR7bWutGuihyDYG', null);

call add_medico('Afonsa Cinza', 111222333, '1980-09-12', 'F', 943333333,
				'cinzenta@gmail.com', 'Alcabideque', '1997-01-01', 45, '2030-12-03',
				1234, 'CENTRO', null, '$2b$12$qz6nfJrtkR5sr1RQx4pAA.bMNs1kdU6PA1S.6ahxPPiL6nxHylIq2', null);
call add_especialidade(111222333, 'Ortopedia', null);

call add_medico('Gabriela', 300300300, '2004-11-02', 'F', 929292929,
				'gabi_ela@gmail.com', 'Porto', '2024-04-11', 12, '2030-12-03',
			    2345, 'NORTE', null, '$2b$12$6UgmeQ1gRm8jMGUYL.QBUefTZi1l3aL42pll36p9KWjQUTQp2c2DK', null);
call add_especialidade(300300300, 'Ortopedia', null);
call add_especialidade(300300300, 'Cardiologia', null);

--call add_subespecialidades(300300300, 'Arritmia', 'Cardiologia', null);

call add_enfermeiro('Ernesto Questo', 333222111, '1985-05-24', 'M', 945333333, 
				   'estoesto@gmail.com', 'Veneza', '2023-01-02', 15, '2030-12-03',
				   1111, 'CENTRO', 'Chefe', '$2b$12$v3JZSEmG86RlTIwaznzvgegAu.1PV28eud9wzWq9sqKIfWElfcH5G', null);

call add_enfermeiro('Diana Raquel', 101202303, '1980-05-04', 'F', 937333333,
					'dianel@gmail.com', 'Faro', '2022-02-01', 17, '2030-12-03',
				   2222, 'SUL', 'Sub-chefe', '$2b$12$ZkF/.UbO9.IJdos0CxjXk.mNaQvobJ0/FH1cFRe7Td6lLQokhAZZ.', null);

call add_assistente('Sofia João', 101202101, '1983-03-03', 'F', 937833333, 
				   'sjota@gmail.com', 'Lituania', '2021-01-02', 19, '2030-12-03',
				   3333, 'Banhos', '$2b$12$z8G.uRxUUGBhlgdjCnd1COHrvbAuwIbFpxNgLbtY7LMXmKJyF69ty', null);
