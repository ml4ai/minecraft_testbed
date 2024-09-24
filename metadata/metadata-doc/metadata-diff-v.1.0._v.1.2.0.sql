-- Diff code generated with pgModeler (PostgreSQL Database Modeler)
-- pgModeler version: 0.9.3
-- Diff date: 2021-04-15 12:15:19
-- Source model: metadata
-- Database: metadata
-- PostgreSQL version: 13.0

-- [ Diff summary ]
-- Dropped objects: 0
-- Created objects: 2
-- Changed objects: 3
-- Truncated tables: 0

SET search_path=public,pg_catalog;
-- ddl-end --


-- [ Created objects ] --
-- object: public.replaytype | type: TYPE --
-- DROP TYPE IF EXISTS public.replaytype CASCADE;
CREATE TYPE public.replaytype AS
 ENUM ('TRIAL','REPLAY');
-- ddl-end --
ALTER TYPE public.replaytype OWNER TO postgres;
-- ddl-end --

-- object: public.replays | type: TABLE --
-- DROP TABLE IF EXISTS public.replays CASCADE;
CREATE TABLE public.replays (
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	replay_id uuid NOT NULL,
	replay_parent_id uuid NOT NULL,
	replay_parent_type public.replaytype NOT NULL,
	date timestamp NOT NULL,
	ignore_list text[],
	CONSTRAINT replay_history_pk PRIMARY KEY (id),
	CONSTRAINT replay_id_uq UNIQUE (replay_id)

);
-- ddl-end --
COMMENT ON COLUMN public.replays.id IS E'The replay database id.';
-- ddl-end --
COMMENT ON COLUMN public.replays.replay_id IS E'The uuid of the replay.';
-- ddl-end --
COMMENT ON COLUMN public.replays.replay_parent_id IS E'The parent trial or replay uuid of the replay.';
-- ddl-end --
COMMENT ON COLUMN public.replays.replay_parent_type IS E'The parent type of replay, trial or replay.';
-- ddl-end --
COMMENT ON COLUMN public.replays.date IS E'The date and time the replay was run.';
-- ddl-end --
COMMENT ON COLUMN public.replays.ignore_list IS E'List of names to ignore during replay.';
-- ddl-end --
ALTER TABLE public.replays OWNER TO postgres;
-- ddl-end --



-- [ Changed objects ] --
COMMENT ON COLUMN public.trials.trial_id IS E'The trial uuid.';
-- ddl-end --
COMMENT ON COLUMN public.trials.experiment_id_experiments IS E'The uuid of the experiment used in the trial.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.experiment_id IS E'The experiment uuid.';
-- ddl-end --
