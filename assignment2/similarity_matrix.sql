/*
(h) similarity matrix: Write a query to compute the similarity 
matrix DDT. (Hint: The transpose is trivial -- just join on 
columns to columns instead of columns to rows.) The query could 
take some time to run if you compute the entire result. But 
notice that you don't need to compute the similarity of both 
(doc1, doc2) and (doc2, doc1) -- they are the same, since 
similarity is symmetric. If you wish, you can avoid this 
wasted work by adding a condition of the form a.docid < b.docid 
to your query. (But the query still won't return immediately if you try to compute every result -- don't expect otherwise.)

What to turn in: On the assignment website, turn in a text 
document similarity_matrix.txt that contains a single line giving 
the similarity of the two documents '10080_txt_crude' and '17035_txt_earn'.
*/

/*Take the transposition of the Frequency table and multiply it 
by Frequency */

/*ANSWER*/
/*------*/
CREATE VIEW TransFreq 
AS SELECT term, docid, count FROM Frequency
order by term, docid;

CREATE VIEW SimilarityMatrix
AS
SELECT
  Frequency.term, TransFreq.docid, SUM(Frequency.count * TransFreq.count)
FROM Frequency, TransFreq 
WHERE Frequency.docid = TransFreq.docid and
	Frequency.docid in ('10080_txt_crude','17035_txt_earn')
GROUP BY Frequency.docid, Frequency.term;



/* From https://www.simple-talk.com/sql/t-sql-programming/matrix-math-in-sql/ 
CREATE VIEW SimilarityMatrix
AS
SELECT i, j, SUM(MatrixA.element_value * MatrixB.element_value)
  FROM MatrixA, MatrixB
 WHERE MatrixA.k = MatrixB.k
 GROUP BY i, j;

	Here: 	i: docid
		j: term
		k: docid
		MatrixA: Frequency
		MatrixB: TransFreq

*/
