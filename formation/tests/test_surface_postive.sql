select *
from {{ ref('formattage' )}}
where contenance < 0