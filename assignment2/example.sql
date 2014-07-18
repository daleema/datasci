drop TABLE Matrix;
drop VIEW MatrixT;

CREATE TABLE Matrix (
row INTEGER  NULL,
column INTEGER  NULL,
value INTEGER  NULL
);

INSERT Into Matrix VALUES (0,0,1);
INSERT Into Matrix VALUES (0,1,2);
INSERT Into Matrix VALUES (0,2,3);
INSERT Into Matrix VALUES (0,3,10);
INSERT Into Matrix VALUES (1,0,4);
INSERT Into Matrix VALUES (1,1,5);
INSERT Into Matrix VALUES (1,2,6);
INSERT Into Matrix VALUES (1,3,11);
INSERT Into Matrix VALUES (2,0,7);
INSERT Into Matrix VALUES (2,1,8);
INSERT Into Matrix VALUES (2,2,9);
INSERT Into Matrix VALUES (2,3,12);

-- Create the transopse of Matrix
CREATE VIEW MatrixT
AS SELECT column, row, value FROM Matrix
GROUP by column, row;

-- Multiply Matrix * MatrixT
/*SELECT A.row_number, B.column_number, SUM(A.value * B.value)
FROM A,B
WHERE A.column_number = B.row_number
GROUP BY A.row_number, B.column_number */
create view Answer
as select a.row, b.column, sum(a.value * b.value)
from Matrix a, MatrixT b
where a.column = b.row
group by a.row, b.column;
