
-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    email character varying COLLATE pg_catalog."default",
    password character varying COLLATE pg_catalog."default",
    status smallint,
    added_date timestamp without time zone DEFAULT now(),
    updated_date timestamp without time zone DEFAULT now(),
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;

-- Table: public.user_token

-- DROP TABLE IF EXISTS public.user_token;

CREATE TABLE IF NOT EXISTS public.user_token
(
    id integer NOT NULL DEFAULT nextval('user_token_id_seq'::regclass),
    user_id integer NOT NULL,
    token character varying COLLATE pg_catalog."default",
    user_device character varying COLLATE pg_catalog."default",
    ip character varying COLLATE pg_catalog."default",
    status smallint,
    added_date timestamp without time zone DEFAULT now(),
    updated_date timestamp without time zone DEFAULT now(),
    CONSTRAINT user_token_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_token
    OWNER to postgres;