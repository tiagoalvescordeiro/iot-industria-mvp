CREATE TABLE IF NOT EXISTS readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    temperature NUMERIC,
    target NUMERIC
);

CREATE INDEX IF NOT EXISTS idx_readings_ts ON readings (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_readings_sensor ON readings (sensor_id);
