SELECT section,
        count(*) as nb_parcelles,
        sum(contenance) as surface_section
FROM {{ ref("formattage") }}
GROUP BY section