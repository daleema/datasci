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
