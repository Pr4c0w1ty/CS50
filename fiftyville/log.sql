-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';

SELECT license_plate
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour <= 11;

SELECT transcript
FROM interviews
WHERE month = 7 AND day = 28 AND year = 2023;

SELECT *
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
);


SELECT *
FROM phone_calls
WHERE caller IN (
SELECT phone_number
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
)) AND day = 28;

SELECT account_number
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Humphrey Lane';


SELECT *
FROM bank_accounts
WHERE account_number IN(SELECT account_number
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Humphrey Lane');


/* mala lista ludzi co i dzwonili i auto*/
SELECT *
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
) AND phone_number IN (SELECT caller
FROM phone_calls
WHERE caller IN (
SELECT phone_number
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
)) AND day = 28);

/* tu złodziej */
SELECT *
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
) AND phone_number IN (SELECT caller
FROM phone_calls
WHERE caller IN (
SELECT phone_number
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
)) AND day = 28) AND id IN (SELECT person_id
FROM bank_accounts
WHERE account_number IN(SELECT account_number
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street'));


SELECT *
FROM phone_calls
WHERE caller IN (SELECT phone_number
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
) AND phone_number IN (SELECT caller
FROM phone_calls
WHERE caller IN (
SELECT phone_number
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
)) AND day = 28) AND id IN (SELECT person_id
FROM bank_accounts
WHERE account_number IN(SELECT account_number
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street')) AND day = 28);

/* tu kolega */
SELECT *
FROM people
WHERE phone_number IN (SELECT receiver
FROM phone_calls
WHERE caller IN (SELECT phone_number
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
) AND phone_number IN (SELECT caller
FROM phone_calls
WHERE caller IN (
SELECT phone_number
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
)) AND day = 28) AND id IN (SELECT person_id
FROM bank_accounts
WHERE account_number IN(SELECT account_number
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street')) AND day = 28));

SELECT *
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour <= 11;

SELECT *
FROM flights
WHERE origin_airport_id = 8 AND year = 2023 AND month = 7 AND day = 29;

SELECT *
FROM passengers
WHERE flight_id IN(SELECT id
FROM flights
WHERE origin_airport_id = 8 AND year = 2023 AND month = 7 AND day > 27) AND passport_number IN(SELECT passport_number
FROM people
WHERE phone_number IN (SELECT receiver
FROM phone_calls
WHERE caller IN (SELECT phone_number
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
) AND phone_number IN (SELECT caller
FROM phone_calls
WHERE caller IN (
SELECT phone_number
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND hour <= 11
)) AND day = 28) AND id IN (SELECT person_id
FROM bank_accounts
WHERE account_number IN(SELECT account_number
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street')) AND day = 28)));

SELECT *
FROM passengers
WHERE passport_number = '';

SELECT *
FROM flights
WHERE id IN (SELECT flight_id
FROM passengers
WHERE passport_number = '');

SELECT *
FROM airports;

SELECT * FROM flights
WHERE origin_airport_id = 8 AND flights.year = 2023 AND flights.month = 7 AND flights.day = 29;

SELECT people.name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE airports.city = 'Fiftyville'
AND flights.year = 2023 AND flights.month = 7 AND flights.day = 29 AND flights.hour = 8 AND flights.minute = 20;

SELECT airports.city FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE flights.origin_airport_id = 8
AND flights.year = 2023 AND flights.month = 7 AND flights.day = 29 AND flights.hour = 8 AND flights.minute = 20;


SELECT people.name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2023 AND phone_calls.month = 7 AND phone_calls.day = 28
AND phone_calls.duration <= 60;
