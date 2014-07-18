select count(term) from 
(select term
from Frequency 
where docid = '10398_txt_earn'
 and count = 1
UNION
select term
from Frequency
where docid = '925_txt_trade'
 and count=1);
