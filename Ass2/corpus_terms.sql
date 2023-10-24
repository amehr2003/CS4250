-- Table: public.Terms

-- DROP TABLE IF EXISTS public."Terms";

CREATE TABLE IF NOT EXISTS public."Terms"
(
    term character varying COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    CONSTRAINT "Terms_pkey" PRIMARY KEY (term),
    CONSTRAINT term FOREIGN KEY (term)
        REFERENCES public."Terms" (term) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Terms"
    OWNER to postgres;