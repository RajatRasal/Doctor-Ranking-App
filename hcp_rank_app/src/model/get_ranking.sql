with hcp_rank as (
    select * from (
      select d.hcp_number as hcp_no, d.weight as w, d.weight_no as w_no 
      from doctors as d) as X
    cross join (
      select dpi.importance as i 
      from disease_params_importance as dpi
      inner join diseases as d
      on d.id = dpi.disease_id
      where d.type = 'test disease 3') as Y)
select distinct hcp_score.hcp_no as hcp_no, score, w_1, w_2, w_3, w_4, w_5
from (
  select hcp_no, sum(w * i) as score
  from hcp_rank
  group by hcp_no) hcp_score
inner join (
  select hcp_number, weight as w_1
  from doctors 
  where weight_no = 0) weight_1
on hcp_score.hcp_no = weight_1.hcp_number
inner join (
  select hcp_number, weight as w_2
  from doctors 
  where weight_no = 1) weight_2
on hcp_score.hcp_no = weight_2.hcp_number
inner join (
  select hcp_number, weight as w_3
  from doctors 
  where weight_no = 2) weight_3
on hcp_score.hcp_no = weight_3.hcp_number
inner join (
  select hcp_number, weight as w_4
  from doctors 
  where weight_no = 3) weight_4
on hcp_score.hcp_no = weight_4.hcp_number
inner join (
  select hcp_number, weight as w_5
  from doctors 
  where weight_no = 4) weight_5
on hcp_score.hcp_no = weight_5.hcp_number
order by score desc, w_1 desc, w_2 desc, w_3 desc, w_4 desc, w_5 desc;
