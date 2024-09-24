-- Diff code generated with pgModeler (PostgreSQL Database Modeler)
-- pgModeler version: 0.9.3
-- Diff date: 2022-04-13 19:36:42
-- Source model: metadata
-- Database: metadata-1.2.0
-- PostgreSQL version: 13.0

-- [ Diff summary ]
-- Dropped objects: 0
-- Created objects: 0
-- Changed objects: 1
-- Truncated tables: 0

SET search_path=public,pg_catalog;
-- ddl-end --


-- [ Changed objects ] --
ALTER TABLE public.replays ALTER COLUMN ignore_list TYPE json;
-- ddl-end --
