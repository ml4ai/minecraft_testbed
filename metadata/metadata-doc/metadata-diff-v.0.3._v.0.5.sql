-- Diff code generated with pgModeler (PostgreSQL Database Modeler)
-- pgModeler version: 0.9.2
-- Diff date: 2020-05-27 18:25:42
-- Source model: metadata
-- Database: metadata
-- PostgreSQL version: 12.0

-- [ Diff summary ]
-- Dropped objects: 0
-- Created objects: 3
-- Changed objects: 0
-- Truncated tables: 0

SET search_path=public,pg_catalog;
-- ddl-end --


-- [ Dropped objects ] --
ALTER TABLE public.trials DROP COLUMN IF EXISTS id_experiments CASCADE;
-- ddl-end --

ALTER TABLE public.trials DROP CONSTRAINT IF EXISTS trials_uq;

ALTER TABLE public.trials DROP CONSTRAINT IF EXISTS experiments_fk;


-- [ Created objects ] --
-- object: experiment_id_experiments | type: COLUMN --
ALTER TABLE public.trials DROP COLUMN IF EXISTS experiment_id_experiments CASCADE;
ALTER TABLE public.trials ADD COLUMN experiment_id_experiments uuid;
-- ddl-end --


-- object: experiment_id | type: COLUMN --
ALTER TABLE public.experiments DROP COLUMN IF EXISTS experiment_id CASCADE;
ALTER TABLE public.experiments ADD COLUMN experiment_id uuid NOT NULL;
-- ddl-end --

-- [ Created constraints ] --
-- object: experiment_id_uq | type: CONSTRAINT --
ALTER TABLE public.experiments DROP CONSTRAINT IF EXISTS experiment_id_uq CASCADE;
ALTER TABLE public.experiments ADD CONSTRAINT experiment_id_uq UNIQUE (experiment_id);

ALTER TABLE public.trials ADD CONSTRAINT experiments_fk FOREIGN KEY (experiment_id_experiments)
REFERENCES public.experiments (experiment_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- ddl-end --

