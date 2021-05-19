--DELETE FROM  public.dataset
--SELECT count(*) FROM public.dataset
SELECT * FROM public.dataset ORDER BY id ASC LIMIT 100;
SELECT count(*) FROM public.dataset;

--DELETE FROM  public.authors
SELECT * FROM public.authors ORDER BY author_id ASC LIMIT 100;
SELECT count(*) FROM public.authors;

--DELETE FROM  public.categories
SELECT * FROM public.categories ORDER BY category_id ASC LIMIT 100;
SELECT count(*) FROM public.categories;

--DELETE FROM  public.formats
SELECT * FROM public.formats ORDER BY format_id ASC LIMIT 100;
SELECT count(*) FROM public.formats;

select version();




--
insert into public.dataset --('author','bestsellers_rank','categorie','description','dimension_x','dimension_y','dimension_z','edition','edition_statement','for_ages','format','id','illustrations_note','image_checksum','image_path','image_url','imprint','index_date','isbn10','isbn13','lang','publication_date','publication_place','rating_avg','rating_count','title','url','weight')
	values 
	('{1, 2,7}','2038','{334, 335, 352, 2626}','A seminal work of dystopian fiction that foreshadowed the worst excesses of Soviet Russia, Yevgeny Zamyatins We is a powerfully inventive vision that has influenced writers from George Orwell to Ayn Rand. This Penguin Classics edition is translated from the Russian with an introduction by Clarence Brown.','134.0','196.0','11.0',NULL,'Revised ed.',NULL,'1','978014018585000',NULL,'1313c5d22d95cce5e94a49750e15e43f','full/5/7/3/5734a259853e631e8011cef8dba816df47570a4d.jpg','https://d1w7fb2mkkr3kw.cloudfront.net/assets/images/book/lrg/9780/1401/9780140185850.jpg','PENGUIN CLASSICS',NULL,'140185852','9780140185850','en','1993-11-25 00:00:00',NULL,'3.91','70619','We','/We-Yevgeny-Zamyatin/9780140185850','182.0');


