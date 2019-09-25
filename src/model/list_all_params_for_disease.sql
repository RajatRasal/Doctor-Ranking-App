select type,
  case when d_type = '{disease}' then importance
       else 0
  end as i
from disease_params_importance dpi
inner join (
  select type d_type, id d_id 
  from diseases
  where type = '{disease}') d
  on d.d_id = dpi.disease_id
full outer join parameters p
  on dpi.parameter_id = p.id
