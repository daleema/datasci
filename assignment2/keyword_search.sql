/*
What to turn in: On the assignment page, upload a text document keyword_search.txt that contains a single line giving the maximum similarity score between the query and any document. Your SQL query should return a list of (docid, similarity) pairs, but you will submit a file containing only a single number: the highest score in the list.

This is my approach :

1.- Create a new table that represents the query document as:
(SELECT 'q' as docid, 'washington' as term, 1 as count 
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION 
SELECT 'q' as docid, 'treasury' as term, 1 as count) t_q

Note that is the same as the proposal in the exercise but without the need to make a UNION with the frequency table (very fast this way!!!).

2.- Compute the product of t_q with the frequency table as in the previous exercise (join by term and grouping by docid) gives you the similarity between the t_q document table and the frequency table. Just order by similarity and get the results.
*/
Create view newdocterm
as
SELECT * FROM frequency
UNION
SELECT 'q' as docid, 'washington' as term, 1 as count 
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION 
SELECT 'q' as docid, 'treasury' as term, 1 as count;

SELECT
  doc1.docid, SUM(doc1.count * doc2.count * doc3.count)
FROM
  ( select docid, term, count
    from Frequency
    where term = 'washington' ) doc1
    join
  ( select docid, term, count
    from Frequency
    where term = 'taxes' )  doc2
    join
  ( select docid, term, count
    from Frequency
    where term = 'treasury' ) doc3
WHERE
  doc1.term = doc2.term and doc2.term = doc3.term;

