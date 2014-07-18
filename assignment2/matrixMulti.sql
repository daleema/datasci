--===== Transform matrix A into array A ======
;WITH arr_A AS
(SELECT row# AS Row,
            Col,
                    Val
                    FROM A
                    UNPIVOT (Val 
                        FOR Col IN ([1],[2],[3],[4],[5],[6],[7],[8])) unpvt
                ),
                --===== Transform matrix B into array B ======
                arr_B AS
                (SELECT row# AS Row,
                            Col,
                                    Val
                                    FROM B
                                    UNPIVOT (Val 
                                        FOR Col IN ([1],[2],[3],[4],[5],[6],[7],[8],[9])) unpvt
                                ),
                                --===== Calculate Product A*B =================
                                product AS
                                (
                                    SELECT rowA as Row, colB as Col, sum(product) Val
                                    FROM
                                    (SELECT arr_A.row rowA, arr_A.col colA, 
                                                 arr_B.row rowB, arr_B.col colB, 
                                                        arr_A.val * arr_B.val as product 
                                                             FROM arr_A INNER JOIN arr_B 
                                                                 ON arr_A.col = arr_B.row) t1
                                                            GROUP BY colB, rowA
                                                        )
                                                        --===== Back to matrix form (reverse transformation) =======
                                                        SELECT 
                                                         Row, 
                                                         [1], 
                                                         [2],
                                                         [3],
                                                         [4],
                                                         [5],
                                                         [6],
                                                         [7],
                                                         [8],
                                                         [9]
                                                        FROM
                                                          (SELECT Row, Col, Val FROM product) t1
                                                        PIVOT (MAX(Val) 
                                                              FOR Col IN ([1],[2],[3],[4],[5],[6],[7],[8],[9])
                                                        ) AS pvt
                                                        ORDER BY Row;
