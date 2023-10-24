-- Table: public.Documents

-- DROP TABLE IF EXISTS public."Documents";

CREATE TABLE IF NOT EXISTS public."Documents"
(
    "DocNumber" integer NOT NULL,
    text character varying COLLATE pg_catalog."default" NOT NULL,
    title character varying COLLATE pg_catalog."default" NOT NULL,
    date date NOT NULL,
    num_chars integer NOT NULL,
    id integer NOT NULL,
    CONSTRAINT "Documents_pkey" PRIMARY KEY ("DocNumber"),
    CONSTRAINT id FOREIGN KEY (id)
        REFERENCES public."Category" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Documents"
    OWNER to postgres;