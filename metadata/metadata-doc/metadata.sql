-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.3
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- -- object: metadata | type: DATABASE --
-- -- DROP DATABASE IF EXISTS metadata;
-- CREATE DATABASE metadata
-- 	ENCODING = 'UTF8'
-- 	LC_COLLATE = 'English_United States.1252'
-- 	LC_CTYPE = 'English_United States.1252'
-- 	TABLESPACE = pg_default
-- 	OWNER = postgres;
-- -- ddl-end --
-- 

-- object: public.trials | type: TABLE --
-- DROP TABLE IF EXISTS public.trials CASCADE;
CREATE TABLE public.trials (
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	trial_id uuid NOT NULL,
	name text,
	date timestamp,
	experimenter text,
	subjects text[],
	trial_number text,
	group_number text,
	study_number text,
	condition text,
	notes text[],
	testbed_version text,
	experiment_id_experiments uuid,
	CONSTRAINT trial_pk PRIMARY KEY (id),
	CONSTRAINT trial_id_uq UNIQUE (trial_id)

);
-- ddl-end --
COMMENT ON COLUMN public.trials.id IS E'The trial database id.';
-- ddl-end --
COMMENT ON COLUMN public.trials.trial_id IS E'The trial uuid.';
-- ddl-end --
COMMENT ON COLUMN public.trials.name IS E'A user friendly name for the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.date IS E'The date and time the trial was run.';
-- ddl-end --
COMMENT ON COLUMN public.trials.experimenter IS E'A name of the experimenter performing the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.subjects IS E'A list of the names or ids of the subjects in the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.trial_number IS E'Sequentially numbered trial run.';
-- ddl-end --
COMMENT ON COLUMN public.trials.group_number IS E'Data organization identifier.';
-- ddl-end --
COMMENT ON COLUMN public.trials.study_number IS E'Study identifier.';
-- ddl-end --
COMMENT ON COLUMN public.trials.condition IS E'The experimental condition used for the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.notes IS E'A list of notes for the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.testbed_version IS E'The testbed version used for the trial.';
-- ddl-end --
COMMENT ON COLUMN public.trials.experiment_id_experiments IS E'The uuid of the experiment used in the trial.';
-- ddl-end --
ALTER TABLE public.trials OWNER TO postgres;
-- ddl-end --

-- -- object: public.trials_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS public.trials_id_seq CASCADE;
-- CREATE SEQUENCE public.trials_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 2147483647
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE public.trials_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: public.experiments | type: TABLE --
-- DROP TABLE IF EXISTS public.experiments CASCADE;
CREATE TABLE public.experiments (
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	experiment_id uuid NOT NULL,
	name text,
	date timestamp,
	author text,
	mission text,
	CONSTRAINT experiment_pk PRIMARY KEY (id),
	CONSTRAINT experiment_id_uq UNIQUE (experiment_id),
	CONSTRAINT name_uq UNIQUE (name)

);
-- ddl-end --
COMMENT ON COLUMN public.experiments.id IS E'The experiment database id.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.experiment_id IS E'The experiment uuid.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.name IS E'A user friendly name for the experiment.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.date IS E'The date and time the experiment was created.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.author IS E'The name of the author of the experiment.';
-- ddl-end --
COMMENT ON COLUMN public.experiments.mission IS E'The mission associated with this experiment.';
-- ddl-end --
ALTER TABLE public.experiments OWNER TO postgres;
-- ddl-end --

-- -- object: public.experiments_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS public.experiments_id_seq CASCADE;
-- CREATE SEQUENCE public.experiments_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 2147483647
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE public.experiments_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
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
	ignore_message_list json,
	ignore_source_list json,
	ignore_topic_list json,
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
COMMENT ON COLUMN public.replays.ignore_message_list IS E'List of messages to ignore during replay.';
-- ddl-end --
COMMENT ON COLUMN public.replays.ignore_source_list IS E'List of sources to ignore during replay.';
-- ddl-end --
COMMENT ON COLUMN public.replays.ignore_topic_list IS E'List of topics to ignore during replay.';
-- ddl-end --
ALTER TABLE public.replays OWNER TO postgres;
-- ddl-end --

-- object: experiments_fk | type: CONSTRAINT --
-- ALTER TABLE public.trials DROP CONSTRAINT IF EXISTS experiments_fk CASCADE;
ALTER TABLE public.trials ADD CONSTRAINT experiments_fk FOREIGN KEY (experiment_id_experiments)
REFERENCES public.experiments (experiment_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --


