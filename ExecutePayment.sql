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