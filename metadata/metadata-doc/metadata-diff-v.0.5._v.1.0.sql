-- Diff code generated with pgModeler (PostgreSQL Database Modeler)
-- pgModeler version: 0.9.2
-- Diff date: 2020-07-03 13:05:44
-- Source model: metadata
-- Database: metadata
-- PostgreSQL version: 12.0

-- [ Diff summary ]
-- Dropped objects: 0
-- Created objects: 5
-- Changed objects: 15
-- Truncated tables: 0

SET search_path=public,pg_catalog;
-- ddl-end --


-- [ Created objects ] --
-- object: trial_number | type: COLUMN --
-- ALTER TABLE public.trials DROP COLUMN IF EXISTS trial_number CASCADE;
ALTER TABLE public.trials ADD COLUMN trial_number text;
-- ddl-end --

COMMENT ON COLUMN public.trials.trial_number IS E'Sequentially numbered trial run.';
-- ddl-end --


-- object: group_number | type: COLUMN --
-- ALTER TABLE public.trials DROP COLUMN IF EXISTS group_number CASCADE;
ALTER TABLE public.trials ADD COLUMN group_number text;
-- ddl-end --

COMMENT ON COLUMN public.trials.group_number IS E'Data organization identifier.';
-- ddl-end --

-- object: study_number | type: COLUMN --
-- ALTER TABLE public.trials DROP COLUMN IF EXISTS study_number CASCADE;
ALTER TABLE public.trials ADD COLUMN study_number text;
-- ddl-end --

COMMENT ON COLUMN public.trials.study_number IS E'Study identifier.';
-- ddl-end --


-- object: condition | type: COLUMN --
-- ALTER TABLE public.trials DROP COLUMN IF EXISTS condition CASCADE;
ALTER TABLE public.trials ADD COLUMN condition text;
-- ddl-end --

COMMENT ON COLUMN public.trials.condition IS E'The experimental condition used for the trial.';
-- ddl-end --


-- [ Changed objects ] --
COMMENT ON COLUMN public.trials.id IS E'The trial database id.';
-- ddl-end --
COMMENT ON COLUMN public.trials.trial_id IS E'The trial id.';
-- ddl-end --
COMMENT ON COLUMN public.trials.name IS E'A user friendly name for the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.date IS E'The date and time the trial was run.';
-- ddl-end --
COMMENT ON COLUMN public.trials.experimenter IS E'A name of the experimenter performing the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.subjects IS E'A list of the names or ids of the subjects in the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.notes IS E'A list of notes for the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.testbed_version IS E'The testbed version used for the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.experiment_id_experiments IS E'The id of the experiment used in the trial.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.id IS E'The experiment database id.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.experiment_id IS E'The experiment id.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.name IS E'A user friendly name for the experiment.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.date IS E'The date and time the experiment was created.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.author IS E'The name of the author of the experiment.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.mission IS E'The mission associated with this experiment.';
-- ddl-end --

