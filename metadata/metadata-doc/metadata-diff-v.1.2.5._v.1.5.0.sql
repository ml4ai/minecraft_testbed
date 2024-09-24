-- Diff code generated with pgModeler (PostgreSQL Database Modeler)
-- pgModeler version: 0.9.3
-- Diff date: 2022-04-13 19:38:03
-- Source model: metadata
-- Database: metadata
-- PostgreSQL version: 13.0

-- [ Diff summary ]
-- Dropped objects: 0
-- Created objects: 3
-- Changed objects: 0
-- Truncated tables: 0

SET search_path=public,pg_catalog;
-- ddl-end --


-- [ Dropped objects ] --
ALTER TABLE public.replays DROP COLUMN IF EXISTS ignore_list CASCADE;
-- ddl-end --


-- [ Created objects ] --
-- object: ignore_message_list | type: COLUMN --
-- ALTER TABLE public.replays DROP COLUMN IF EXISTS ignore_message_list CASCADE;
ALTER TABLE public.replays ADD COLUMN ignore_message_list json;
-- ddl-end --

COMMENT ON COLUMN public.replays.ignore_message_list IS E'List of messages to ignore during replay.';
-- ddl-end --


-- object: ignore_source_list | type: COLUMN --
-- ALTER TABLE public.replays DROP COLUMN IF EXISTS ignore_source_list CASCADE;
ALTER TABLE public.replays ADD COLUMN ignore_source_list json;
-- ddl-end --

COMMENT ON COLUMN public.replays.ignore_source_list IS E'List of sources to ignore during replay.';
-- ddl-end --


-- object: ignore_topic_list | type: COLUMN --
-- ALTER TABLE public.replays DROP COLUMN IF EXISTS ignore_topic_list CASCADE;
ALTER TABLE public.replays ADD COLUMN ignore_topic_list json;
-- ddl-end --

COMMENT ON COLUMN public.replays.ignore_topic_list IS E'List of topics to ignore during replay.';
-- ddl-end --


