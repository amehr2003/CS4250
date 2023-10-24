-- Table: public.Index

-- DROP TABLE IF EXISTS public."Index";

CREATE TABLE IF NOT EXISTS public."Index"
(
    "DocNumber" integer NOT NULL,
    term character varying COLLATE pg_catalog."default" NOT NULL,
    count integer NOT NULL,
    CONSTRAINT "Index_pkey" PRIMARY KEY ("DocNumber", term),
    CONSTRAINT "DocNumber" FOREIGN KEY ("DocNumber")
        REFERENCES public."Documents" ("DocNumber") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "Term" FOREIGN KEY (term)
        REFERENCES public."Terms" (term) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Index"
    OWNER to postgres;