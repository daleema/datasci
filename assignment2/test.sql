CREATE VIEW SimilarityMatrix
AS
SELECT Frequency.docid,TransFreq.term, SUM(Frequency.count * TransFreq.count)
  FROM Frequency, TransFreq
 WHERE Frequency.docid = TransFreq.docid
 GROUP BY Frequency.docid,TransFreq.term;
