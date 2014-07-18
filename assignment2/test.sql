drop VIEW TransFreq;

drop VIEW SimilarityMatrix;

-- Create the transopse of Frequency
CREATE VIEW TransFreq 
AS SELECT term, docid, count FROM Frequency;

-- Do the matrix multiplication
CREATE VIEW SimilarityMatrix
AS
SELECT Frequency.docid,TransFreq.term, SUM(Frequency.count * TransFreq.count)
  FROM Frequency, TransFreq
 WHERE 
	Frequency.docid in ('10080_txt_crude' ,'17035_txt_earn') and
	Frequency.docid = TransFreq.docid
 GROUP BY Frequency.docid,TransFreq.term;
/*
select 
	a.docid var_id1, b.term var_id2, SUM(a.count * b.count) correl 
from 
	Frequency a, TransFreq b 
where a.docid in ('10080_txt_crude' ,'17035_txt_earn') and
	a.docid=b.docid and
	a.var_id1<=b.var_id2
group by a.var_id1, b.var_id2 ; 
*/
