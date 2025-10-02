INSERT INTO readings (sensor_id, timestamp, temperature, target)
SELECT 1, NOW() - (i || ' minutes')::interval, 20 + (random()*10), 20 + (random()*10)
FROM generate_series(0, 199) AS s(i);
