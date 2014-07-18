/*
(g) multiply: Express A X B as a SQL query, referring 
to the class lecture for hints.

What to turn in: On the assignment page, turn in a 
text document multiply.txt with a single line 
containing the value of the cell (2,3)



CREATE VIEW MatrixC(i, j, element_value)
AS
SELECT i, j, SUM(MatrixA.element_value * MatrixB.element_value)
  FROM MatrixA, MatrixB
 WHERE MatrixA.k = MatrixB.k
 GROUP BY i, j;

*/
--CREATE VIEW c
--AS
SELECT 
    a.row_num, b.col_num, SUM(a.value * b.value)
FROM 
    a, b
WHERE 
    a.col_num = b.row_num
 GROUP BY a.row_num, b.col_num;
