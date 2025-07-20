-- もしpublicスキーマ自体を作成しようとするsqlが含まれていたら、docker compose up時にエラーになるので、消してください。
-- なお、publicスキーマはデフォルトで存在するものになるので、CREATE TABLE public.categoriesのように、publicスキーマを指定してテーブルを作成することは可能です。
-- また、CREATE TABLE categoriesのようにpublicスキーマを省略しても、publicスキーマにテーブルが作成されるので、問題ないです。(public以外のスキーマを利用することはないので。)

-- public.categories definition

-- Drop table

-- DROP TABLE public.categories;

CREATE TABLE public.categories (
	category_id int4 NOT NULL,
	category_name varchar NOT NULL,
	CONSTRAINT categories_pk PRIMARY KEY (category_id),
	CONSTRAINT categoryies_unique UNIQUE (category_name)
);


-- public.items definition

-- Drop table

-- DROP TABLE public.items;

CREATE TABLE public.items (
	item_id int4 NOT NULL,
	item_name varchar NOT NULL,
	CONSTRAINT item_pk PRIMARY KEY (item_id)
);


-- public.item_category definition

-- Drop table

-- DROP TABLE public.item_category;

CREATE TABLE public.item_category (
	item_id int4 NOT NULL,
	category_id int4 NOT NULL,
	CONSTRAINT item_category_pk PRIMARY KEY (item_id, category_id),
	CONSTRAINT item_category_categories_fk FOREIGN KEY (category_id) REFERENCES public.categories(category_id) ON DELETE CASCADE,
	CONSTRAINT item_category_items_fk FOREIGN KEY (item_id) REFERENCES public.items(item_id) ON DELETE CASCADE
);