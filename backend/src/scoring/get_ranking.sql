select hcp_no, sum(w * i) as score from (
 	select d.hcp_number as hcp_no, d.weight as w 
 	from doctors as d) as X
cross join (
	select dpi.importance as i 
	from disease_params_importance as dpi
	inner join diseases as d
	on d.id = dpi.disease_id
	where d.type = 'test disease 1') as Y
group by hcp_no
order by score desc;
