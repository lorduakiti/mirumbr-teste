-- Qual a quantidade total de livros da base?
SELECT count(*) as qtd_livros FROM public.dataset;

-- Qual a quantidade de livros que possuí apenas 1 autor?
SELECT 
	count(*) as qtd_livros_com_um_autor 
FROM public.dataset
WHERE array_length(author, 1) = 1;

-- Quais os 5 autores com a maior quantidade de livros?
SELECT
	a.author_name,
	count(d.id) as qtd_livros_por_autor
FROM public.authors a
LEFT JOIN public.dataset d on a.author_id = ANY(d.author)
GROUP BY  a.author_name
ORDER BY  count(d.id) desc, a.author_name
LIMIT 5;

-- Qual a quantidade de livros por categoria?
SELECT
	c.category_name,
	count(d.id) as qtd_livros_por_categoria
FROM public.categories c
LEFT JOIN public.dataset d on c.category_id = ANY(d.categorie)
GROUP BY  c.category_name
ORDER BY  c.category_name;

-- Quais as 5 categorias com a maior quantidade de livros?
SELECT
	c.category_name,
	count(d.id) as qtd_livros_por_categoria
FROM public.categories c
LEFT JOIN public.dataset d on c.category_id = ANY(d.categorie)
GROUP BY  c.category_name
ORDER BY  count(d.id) desc, c.category_name
LIMIT 5;

-- Qual o formato com a maior quantidade de livros?
SELECT
	f.format_name,
	count(d.id) as qtd_livros_por_formato
FROM public.formats f
LEFT JOIN public.dataset d on f.format_id = d.format
GROUP BY  f.format_name
ORDER BY  count(d.id) desc, f.format_name
LIMIT 1;

-- Considerando a coluna “bestsellers-rank”, quais os 10 livros mais bem posicionados?
SELECT
	d.title,
	d.bestsellers_rank
FROM public.dataset d
WHERE bestsellers_rank IS NOT NULL
ORDER BY  bestsellers_rank desc
LIMIT 10;

-- Considerando a coluna “rating-avg”, quais os 10 livros mais bem posicionados?
SELECT
	d.title,
	d.rating_avg,
	d.rating_count
FROM public.dataset d
WHERE rating_avg IS NOT NULL
ORDER BY  rating_avg desc, d.rating_count
LIMIT 10;

-- Quantos livros possuem “rating-avg” maior do que 3,5?
SELECT
	count(d.id) as "qtd_livros_rating_maior_3,5"
FROM public.dataset d
WHERE rating_avg IS NOT NULL
AND rating_avg > 3.5;

-- Quantos livros tem data de publicação (publication-date) maior do que 01-01-2020?
SELECT
	count(d.id) as "qtd_livros_publicados"
FROM public.dataset d
WHERE publication_date > '01-01-2020 00:00:00';
