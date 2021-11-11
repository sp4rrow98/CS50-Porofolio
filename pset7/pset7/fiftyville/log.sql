-- SELECT description
-- FROM crime_scene_reports
-- WHERE year = 2020
-- AND month = 07
-- AND day = 28;

-- SELECT transcript
-- FROM interviews
-- WHERE year = 2020
-- AND month = 07
-- AND day = 28;

-- -- SUSPECTS THAT WITHDRAW MONEY FROM THAT ATM

-- SELECT DISTINCT name
-- FROM people
-- JOIN bank_accounts
-- ON people.id = bank_accounts.person_id
-- JOIN atm_transactions
-- ON bank_accounts.account_number = atm_transactions.account_number
-- WHERE atm_transactions.year = 2020
-- AND atm_transactions.month = 07
-- AND atm_transactions.day = 28
-- AND atm_transactions.atm_location = "Fifer Street"
-- AND atm_transactions.transaction_type = "withdraw";

-- -- SUSPECTS WHO CALLED SOMEONE LESS THAN 1 MINUTE

-- SELECT DISTINCT name
-- FROM people
-- JOIN phone_calls
-- ON people.phone_number = phone_calls.caller
-- WHERE year = 2020
-- AND month = 07
-- AND day = 28
-- AND duration < 60;

-- -- SUSPECTS THAT LEFT THE PARKING SPACE

-- SELECT DISTINCT name
-- FROM people
-- JOIN courthouse_security_logs
-- ON people.license_plate = courthouse_security_logs.license_plate
-- WHERE year = 2020
-- AND  month = 07
-- AND day = 28
-- AND hour = 10
-- AND minute BETWEEN 15 and 25
-- AND activity = "exit";

-- -- SUSPECTS OF THE FIRST FLIGHT

-- SELECT name FROM people
-- JOIN passengers ON people.passport_number = passengers.passport_number
-- WHERE flight_id =
--     (
--     SELECT id
--     FROM flights
--     WHERE day = "29"
--     AND year = "2020"
--     AND month = "7"
--     ORDER BY hour, minute
--     LIMIT 1
--     );

    -- Who did it ?

SELECT name FROM people
JOIN bank_accounts
ON people.id = bank_accounts.person_id
JOIN atm_transactions
ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2020
AND atm_transactions.month = 07
AND atm_transactions.day = 28
AND atm_transactions.atm_location = "Fifer Street"
AND atm_transactions.transaction_type = "withdraw"

    INTERSECT

SELECT DISTINCT name
FROM people
JOIN phone_calls
ON people.phone_number = phone_calls.caller
WHERE year = 2020
AND month = 07
AND day = 28
AND duration < 60

    INTERSECT

SELECT DISTINCT name
FROM people
JOIN courthouse_security_logs
ON people.license_plate = courthouse_security_logs.license_plate
WHERE year = 2020
AND month = 07
AND day = 28
AND hour = 10
AND minute BETWEEN 15 and 25
AND activity = "exit"

    INTERSECT

SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id =
(
SELECT id
FROM flights
WHERE day = "29"
AND year = "2020"
AND month = "7"
ORDER BY
hour,
minute
LIMIT 1
);

-- Accomplice who helped :

SELECT name FROM people
JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE year = 2020
AND month = 07
AND day = 28
AND duration < 60
AND caller =
(
SELECT phone_number FROM people
WHERE name = "Ernest"
);

-- Where did he escape :

SELECT city FROM airports
JOIN flights ON airports.id = destination_airport_id
JOIN passengers ON passengers.flight_id = flights.id
WHERE year = 2020
AND month = 07
AND day = 29
AND passengers.passport_number = 
(
SELECT passport_number FROM people
WHERE name = "Ernest"
)
LIMIT 1;

--  SEAT he had

SELECT seat FROM passengers
JOIN flights ON flights.id = passengers.flight_id
WHERE passport_number =
(
SELECT passport_number FROM people
WHERE name = "Ernest"
)
AND month = 07
AND day = 29;