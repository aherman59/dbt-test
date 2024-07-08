SELECT
        id AS idpar,
        CASE WHEN commune!~'^97' THEN substring(commune,1,2) ELSE substring(commune,1,3) END::varchar(3) AS code_dep,
        CASE WHEN commune!~'^97' THEN substring(commune,3,5) ELSE substring(commune,4,5) END::varchar(3) AS code_com,
        prefixe::varchar(3) AS com_abs,
        lpad(section,2,'0')::varchar(2) AS section,
        lpad(numero,4,'0')::varchar(4) AS numero,
        ST_SETSRID(geometry,4326) AS geompar,
        CASE WHEN contenance=0 THEN NULL ELSE contenance END::numeric(10,0) AS contenance,
        created AS date_creation,
        updated AS date_maj,
        NULL::varchar(14) AS idparref,
        'PCI'::text as source 
    FROM
        {{ source('public', generate_table_name(var("CODE_INSEE")) ) }}
    WHERE
        ST_ISVALID(geometry) AND (id IS NOT NULL OR id != '') AND numero~'^\d+$'