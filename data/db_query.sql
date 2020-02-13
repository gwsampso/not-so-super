-- run query on ficsrv02
-- copy output to data.csv

USE [QSG_Dev]
GO

DECLARE @from_date datetime = '20180630'
DECLARE @to_date datetime = '20190630'

select i.investment_id, isnull(i.investment_shortname, i.investment_name) as fund_name, zst.superfund_type, icf.cashflow_value/1000000 as fund_assets,       
im.investment_id, im.investment_name, zac.asset_class,  isnull(p.lifecycle_in,0) as lifecycle_in, s.public_offer        
, return_1yr, return_3yr, return_5yr,  iis.investment_size/1000 as investment_size 
, ia_ret.attribute_value as targetreturn, ia_risk.attribute_value as risk, ia_fee.attribute_value as fee, sum(ia_ifee.attribute_value)/400 as invfee, sum(ia_afee.attribute_value)/400 as admin_fee  
from dc.investment i 
inner join dc.superfund s on i.investment_id=s.investment_id  
inner join dc.product p on p.parent_investment_id=s.investment_id    
inner join dc.mic_option m on m.parent_investment_id=p.investment_id and m.accumulation_in=1 and m.mysuper_in=1       
inner join dc.investment im on im.investment_id=m.investment_id      
inner join dc.z_superfund_type zst on zst.superfund_type_cd=s.superfund_type_cd   
inner join dc.investment_cashflow icf on icf.investment_id=i.investment_id and icf.cashflow_cd=22 and icf.financial_dt=2018      
left outer join dc.z_asset_class zac on zac.asset_class_cd=m.SR_asset_class_cd    
left outer join dc.investment_return irA on im.investment_id=irA.investment_id and irA.investment_dt=@to_date and irA.company_id=137 and irA.post_fee_in=1 and irA.post_tax_in=1       
inner join dc.investment_size iis on im.investment_id=iis.investment_id and iis.investment_dt=@to_date and iis.company_id=137     
left outer join dc.investment_attribute ia_ret on ia_ret.investment_id=im.investment_id and ia_ret.investment_dt=@to_date and ia_ret.attribute_cd=5   
left outer join dc.investment_attribute ia_risk on ia_risk.investment_id=im.investment_id and ia_risk.investment_dt=@to_date and ia_risk.attribute_cd=6 
left outer join dc.investment_attribute ia_fee on ia_fee.investment_id=im.investment_id and ia_fee.investment_dt=@to_date and ia_fee.attribute_cd=7   
left outer join dc.investment_attribute ia_ifee on ia_ifee.investment_id=im.investment_id and (ia_ifee.investment_dt<=@to_date and ia_ifee.investment_dt>@from_date) and ia_ifee.attribute_cd=11    
left outer join dc.investment_attribute ia_afee on ia_afee.investment_id=im.investment_id and (ia_afee.investment_dt<=@to_date and ia_afee.investment_dt>@from_date) and ia_afee.attribute_cd=12    
where i.active_in=1 
group by i.investment_id, i.investment_name, i.investment_shortname, im.investment_id, im.investment_name, zst.superfund_type, irA.return_1yr, irA.return_3yr, irA.return_5yr, iis.investment_size, ia_ret.attribute_value, ia_risk.attribute_value , ia_fee.attribute_value   
,  zac.asset_class   ,  icf.cashflow_value, im.investment_id, p.lifecycle_in, s.public_offer
order by im.investment_name
