CREATE VIEW SimilarityMatrix
AS
SELECT Frequency.docid,TransFreq.term, SUM(Frequency.count * TransFreq.count)
  FROM Frequency, TransFreq
 WHERE 
	Frequency.docid in ('10080_txt_crude' ,'17035_txt_earn') and
	Frequency.docid = TransFreq.docid
 GROUP BY Frequency.docid,TransFreq.term;
