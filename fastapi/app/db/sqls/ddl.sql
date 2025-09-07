-- もしpublicスキーマ自体を作成しようとするsqlが含まれていたら、docker compose up時にエラーになるので、消してください。
-- なお、publicスキーマはデフォルトで存在するものになるので、CREATE TABLE public.categoriesのように、publicスキーマを指定してテーブルを作成することは可能です。
-- また、CREATE TABLE categoriesのようにpublicスキーマを省略しても、publicスキーマにテーブルが作成されるので、問題ないです。(public以外のスキーマを利用することはないので。)

-- public.categories definition

-- Drop table

-- DROP TABLE users;

CREATE TABLE users (
	user_id int4 NOT NULL,
	mail_address varchar NOT NULL,
	hashed_password varchar NOT NULL,
	full_name varchar NULL,
	is_active bool DEFAULT true NOT NULL,
	is_superuser bool DEFAULT false NOT NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	updated_at timestamptz DEFAULT now() NOT NULL,
	CONSTRAINT users_mail_address_unique UNIQUE (mail_address),
	CONSTRAINT users_pk PRIMARY KEY (user_id)
);


-- public.categories definition

-- Drop table

-- DROP TABLE categories;

CREATE TABLE categories (
	category_id int4 NOT NULL,
	category_name varchar NOT NULL,
	created_by int4 NULL,
	updated_by int4 NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	updated_at timestamptz DEFAULT now() NOT NULL,
	CONSTRAINT categories_pk PRIMARY KEY (category_id),
	CONSTRAINT categoryies_unique UNIQUE (category_name),
	CONSTRAINT fk_users_pk1 FOREIGN KEY (created_by) REFERENCES users(user_id),
	CONSTRAINT fk_users_pk2 FOREIGN KEY (updated_by) REFERENCES users(user_id)
);


-- public.items definition

-- Drop table

-- DROP TABLE items;

CREATE TABLE items (
	item_id int4 NOT NULL,
	item_name varchar NOT NULL,
	created_by int4 NULL,
	updated_by int4 NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	updated_at timestamptz DEFAULT now() NOT NULL,
	CONSTRAINT item_pk PRIMARY KEY (item_id),
	CONSTRAINT fk_users_pk1 FOREIGN KEY (updated_by) REFERENCES users(user_id),
	CONSTRAINT fk_users_pk2 FOREIGN KEY (created_by) REFERENCES users(user_id)
);


-- public.item_category definition

-- Drop table

-- DROP TABLE item_category;

CREATE TABLE item_category (
	item_id int4 NOT NULL,
	category_id int4 NOT NULL,
	CONSTRAINT item_category_pk PRIMARY KEY (item_id, category_id),
	CONSTRAINT item_category_categories_fk FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE,
	CONSTRAINT item_category_items_fk FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);