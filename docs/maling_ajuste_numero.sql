-- LIMPAR NUMEROS NO VOIP 
/*
Ela pega os três tipos de erro ao mesmo tempo, porque:
Número com traço (-): o REGEXP_REPLACE(FONE, '[^0-9]', '') remove o traço e qualquer outro símbolo.
Número incompleto: depois de limpar, se o número tiver menos de 10 dígitos, ele será pego.
Número com traço e incompleto: também será pego, porque o traço é removido e a contagem de dígitos será menor que 10.
*/
SELECT 
    c.*,
    LENGTH(REGEXP_REPLACE(c.FONE, '[^0-9]', '')) AS QTDE_DIGITOS
FROM AGE.CAMP_CHECKUP_SAUDE c
WHERE c.CAMPANHA = 'CHECK UP SAÚDE'
  AND LENGTH(REGEXP_REPLACE(c.FONE, '[^0-9]', '')) < 10;
  
  ---------------------------------------------
SELECT * FROM CAMP_CARDIOLOGIA c        -- OK
ORDER BY c.LIGAR_EM  ASC; -- CAMAPANHA = CARDIOLOGIA
---------------------------------------------
SELECT * FROM CAMP_CHECKUP_MULHER c     -- OK
ORDER BY c.LIGAR_EM  ASC; -- CAMAPANHA = CHECKUP MULHER
---------------------------------------------
SELECT * FROM CAMP_CHECKUP_SAUDE c      -- OK
ORDER BY c.LIGAR_EM  ASC; -- CAMAPANHA = CHECK UP SAÚDE
---------------------------------------------
SELECT * FROM CAMP_OFTALMOLOGIA c       -- OK
ORDER BY c.LIGAR_EM  ASC; -- CAMAPANHA  = OFTALMOLOGIA
---------------------------------------------
SELECT * FROM CAMP_PSICO_PSIQUI c       -- OK
ORDER BY c.LIGAR_EM  ASC; -- CAMAPANHA  = PSICOLOGIA E PSIQUIATRIA
---------------------------------------------
SELECT * FROM CAMP_CHECKUP_HOMEM c     --  XX
ORDER BY c.LIGAR_EM  ASC;  -- CAMAPANHA = CHECKUP HOMEM
---------------------------------------------
SELECT * FROM CAMP_ODONTO c            --  OK 
ORDER BY c.LIGAR_EM  ASC; -- CAMAPANHA = ODONTO
---------------------------------------------
SELECT * FROM CAMP_ODONTO_GERAL c       -- XX
ORDER BY c.LIGAR_EM  ASC; -- CAMAPANHA  =campanha_odonto_fluor
---------------------------------------------
  
 
  -- CARDIOLOGIA
DELETE FROM AGE.CAMP_CARDIOLOGIA
WHERE CAMPANHA = 'CARDIOLOGIA'
  AND LENGTH(REGEXP_REPLACE(FONE, '[^0-9]', '')) < 10;

-- CHECKUP MULHER
DELETE FROM AGE.CAMP_CHECKUP_MULHER
WHERE CAMPANHA = 'CHECKUP MULHER'
  AND LENGTH(REGEXP_REPLACE(FONE, '[^0-9]', '')) < 10;

-- CHECK UP SAÚDE
DELETE FROM AGE.CAMP_CHECKUP_SAUDE
WHERE CAMPANHA = 'CHECK UP SAÚDE'
  AND LENGTH(REGEXP_REPLACE(FONE, '[^0-9]', '')) < 10;

-- OFTALMOLOGIA
DELETE FROM AGE.CAMP_OFTALMOLOGIA
WHERE CAMPANHA = 'OFTALMOLOGIA'
  AND LENGTH(REGEXP_REPLACE(FONE, '[^0-9]', '')) < 10;

-- PSICOLOGIA E PSIQUIATRIA
DELETE FROM AGE.CAMP_PSICO_PSIQUI
WHERE CAMPANHA = 'PSICOLOGIA E PSIQUIATRIA'
  AND LENGTH(REGEXP_REPLACE(FONE, '[^0-9]', '')) < 10;

-- ODONTO
DELETE FROM AGE.CAMP_ODONTO
WHERE CAMPANHA = 'ODONTO'
  AND LENGTH(REGEXP_REPLACE(FONE, '[^0-9]', '')) < 10;
  
-- ODONTO_GERAL  
DELETE FROM AGE.CAMP_ODONTO_GERAL
WHERE CAMPANHA = 'campanha_odonto_fluor'
  AND LENGTH(REGEXP_REPLACE(FONE, '[^0-9]', '')) < 10;
  
COMMIT;