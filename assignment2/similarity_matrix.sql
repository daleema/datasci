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

This thread has been extremely helpful.  However I think I only saw 1 or 2 posts that refer back to the solution in g (multiply).  If have solved g then you have 90% of the solution for h. In g you are provided a and b.  In h you simply need to define a and b.

Still there are some excellent explanations here about *why* that works out.
*/

/*Take the transposition of the Frequency table and multiply it 
by Frequency */

--drop view TransFreq;
--drop view SimilarityMatrix;

/*ANSWER*/
/*------
CREATE VIEW TransFreq 
AS SELECT term, docid, count FROM Frequency
order by term, docid;*/
SELECT
  SUM(doc1.count * doc2.count)
FROM 
  ( select docid, term, count 
    from Frequency 
    where docid = ('10080_txt_crude')  ) doc1
    join
  ( select docid, term, count 
    from Frequency 
    where docid = ('17035_txt_earn') ) doc2
WHERE 
  doc1.term = doc2.term;

/*
Now take the dot product of the two matricies.
select sum(v1.value * v2.value)
select sum ( doc1.sum * doc2.sum)
from 
( select * from SimilarityMatrix 
where docid = '10080_txt_crude' ) doc1
join 
( select * from SimilarityMatrix 
where docid = '17035_txt_earn' ) doc2
where doc1.term = doc2.term and 
  doc1.term in (select term from SimilarityMatrix 
	where docid = '10080_txt_crude' );
*/
