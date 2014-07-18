DROP TABLE IF EXISTS "docTermCounts";
CREATE VIEW "docTermCounts" AS select docid, sum(term) as termcount from Frequency where termcount > 300;
