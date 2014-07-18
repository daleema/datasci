-- Get a list of the count of terms for all docids
--select count (term)
--from Frequency
--where docid = '10398_txt_earn';

-- Now need to do this for all docids
--select docid, count (term) as new
--from Frequency 
--where docid in 
--    ( select docid 
--        from Frequency)
--group by docid
--HAVING new > 300
--ORDER BY new;
/*
You've probably got the group by and the filter 
correct, but remember that you need to add up 
the term frequencies rather than just count the terms.
*/
select docid, sum(count) as new
from Frequency 
where docid in 
    ( select docid 
        from Frequency)
group by docid
HAVING new > 300
ORDER BY new;
