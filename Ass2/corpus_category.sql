-- Table: public.Category

-- DROP TABLE IF EXISTS public."Category";

CREATE TABLE IF NOT EXISTS public."Category"
(
    id integer NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Category_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Category"
    OWNER to postgres;