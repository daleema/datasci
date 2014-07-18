/*
(f) two words: Write a SQL statement to count the number of unique 
documents that contain both the word 'transactions' and the word 'world'.

What to turn in: Run your query against your local database and 
determine the number of records returned as described above. On 
the assignment page, upload a text file two_words.txt with a single 
line containing the number of records.

Then you should create a table with the results of the docid's 
where the corrresponding term is 'transactions', and create another 
one where the term is 'world'. What you need is the intersection of 
the 2 tables on the docid's from the two resulting tables. 
Hope this helps.
*/

select 
    freq.docid, freq.term, a.termCount
from
    Frequency freq,
(
    select 
        docid, sum(count) as termCount
    from    
        Frequency
    group by   
        docid
) a
    where freq.docid = a.docid
     and termCount > 300
    group by 
        a.docid
    order by
        termCount;
