-- LLM Wiki knowledge base schema
CREATE TABLE IF NOT EXISTS topics (
  id TEXT PRIMARY KEY,
  title TEXT,
  summary TEXT,
  tags TEXT,
  updated TEXT
);
CREATE TABLE IF NOT EXISTS entities (
  id TEXT PRIMARY KEY,
  name TEXT,
  type TEXT,
  source TEXT
);
CREATE TABLE IF NOT EXISTS claims (
  id TEXT PRIMARY KEY,
  text TEXT,
  type TEXT,
  source TEXT,
  date TEXT
);
CREATE TABLE IF NOT EXISTS triples (
  subject TEXT,
  predicate TEXT,
  object TEXT,
  source TEXT
);
