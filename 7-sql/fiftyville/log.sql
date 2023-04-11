-- Keep a log of any SQL queries you execute as you solve the mystery.

/*
Case fiftyville: "The CS50 Duck has been stolen.
Authorities believe that the thief stole the duck and then, shortly afterwards,
took a flight out of town with the help of an accomplice. "

Information: The theft took place on July 28, 2021 and that it took place on Humphrey Street.
*/

---------------------------------------------------------------------------------------------------------------------
-- 1. What can you tell me about the Humphrey Street crime scene reports from July 28, 2021?
---------------------------------------------------------------------------------------------------------------------
SELECT description FROM crime_scene_reports
WHERE day = 28
AND month = 7
AND year = 2021
AND street = 'Humphrey Street';

/*  Information gained:
    • Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
    • Interviews were conducted today with three witnesses who were present at the time -
      each of their interview transcripts mentions the bakery.
    • Littering took place at 16:36. No known witnesses.
*/
---------------------------------------------------------------------------------------------------------------------
-- 2. The transcripts for the three witnesses who were present at the time of the incident...
-- at the Humphrey Street bakery need to be obtained.
---------------------------------------------------------------------------------------------------------------------
SELECT name, transcript FROM interviews
WHERE day = 28
AND month = 7
AND year = 2021
AND transcript LIKE '%bakery%';

/*
    Information gained:
    1. Ruth: "Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and
              drive away. If you have security footage from the bakery parking lot, you might want to look for cars that
              left the parking lot in that time frame."

    2. Eugene: "I don't know the thief's name, but it was someone I recognized.
                Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and
                saw the thief there withdrawing some money."

    3. Raymond: "As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
                In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
                The thief then asked the person on the other end of the phone to purchase the flight ticket."

    Keyword clues:
    1. security footage from the bakery parking lot
    2. ATM on Leggett Street
    3. the earliest flight out of Fiftyville tomorrow
*/
---------------------------------------------------------------------------------------------------------------------
-- 3. What cars left the bakery?
---------------------------------------------------------------------------------------------------------------------
SELECT license_plate, activity FROM bakery_security_logs
WHERE day = 28
AND month = 7
AND year = 2021
AND hour = 10
AND minute > 15 AND minute < 25;

/*
    Information gained: The following are the vehicle license plates that left the bakery
    • 5P2BI95   |   exit
    • 94KL13X   |   exit
    • 6P58WS2   |   exit
    • 4328GD8   |   exit
    • G412CB7   |   exit
    • L93JTIZ   |   exit
    • 322W7JE   |   exit
    • 0NTHK55   |   exit
*/
---------------------------------------------------------------------------------------------------------------------
-- 4. I need the ATM logs from Leggett Street before the theft occurred.
---------------------------------------------------------------------------------------------------------------------
SELECT account_number, amount FROM atm_transactions
WHERE day = 28
AND month = 7
AND year = 2021
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

/*
    Information gained: The following are the account numbers and amounts that were withdrawn from the ATM
    • 28500762  |   48
    • 28296815  |   20
    • 76054385  |   60
    • 49610011  |   50
    • 16153065  |   80
    • 25506511  |   20
    • 81061156  |   30
    • 26013199  |   35
*/
---------------------------------------------------------------------------------------------------------------------
-- 5. I need you to find the earliest flight out of Fiftyville on July 29, 2021.
-- This is critical information in our investigation.
---------------------------------------------------------------------------------------------------------------------
SELECT abbreviation, full_name, city, hour, minute, flights.id
FROM airports
JOIN flights ON airports.id = destination_airport_id
WHERE (
    SELECT destination_airport_id FROM flights
    WHERE (
        SELECT id FROM airports
        WHERE city = 'Fiftyville'
    ) = origin_airport_id AND day = 29 AND month = 7 AND year = 2021
    ORDER BY hour ASC, minute ASC LIMIT 1
) = airports.id ORDER BY hour ASC, minute ASC LIMIT 1;

/*
    Information gained: The following is the flight that the thief planned to fly

    LGA | LaGuardia Airport | New York City | 8 | 20 | 36

    • The flight was from the airport in the city of Fiftyville to the airport in the city of New York.
    • The flight took place at 8:20am.
    • The flight was ID'd as ID #36.

    • The city the thief ESCAPED TO: New York City
*/
---------------------------------------------------------------------------------------------------------------------
-- 6. I compared the vehicle's license plate to the ATM account number and flight information and there are matches.
---------------------------------------------------------------------------------------------------------------------
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE license_plate = '5P2BI95'
    OR license_plate = '94KL13X'
    OR license_plate = '6P58WS2'
    OR license_plate = '4328GD8'
    OR license_plate = 'G412CB7'
    OR license_plate = 'L93JTIZ'
    OR license_plate = '322W7JE'
    OR license_plate = '0NTHK55'
AND account_number = '28500762'
    OR account_number = '28296815'
    OR account_number = '76054385'
    OR account_number = '49610011'
    OR account_number = '16153065'
    OR account_number = '25506511'
    OR account_number = '81061156'
    OR account_number = '26013199'
INTERSECT
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.id = 36;

/*
    Information gained: The following are possible suspects:
    • Bruce
    • Kenny
    • Luca
    • Taylor
*/
---------------------------------------------------------------------------------------------------------------------
-- 7. I'll need to compare the suspects to the flight information to see if there's a match for double checking.
---------------------------------------------------------------------------------------------------------------------
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.id = 36
    AND (
        name = 'Bruce'
        OR name = 'Kenny'
        OR name = 'Luca'
        OR name = 'Taylor'
    );
/*
    Information gained: The following are double checked as possible suspects:
    • Bruce
    • Kenny
    • Luca
    • Taylor
*/
---------------------------------------------------------------------------------------------------------------------
-- 8. I need the phone numbers of the suspects.
---------------------------------------------------------------------------------------------------------------------
SELECT name, phone_number FROM people
WHERE name = 'Bruce'
    OR name = 'Kenny'
    OR name = 'Luca'
    OR name = 'Taylor';
/*
    Information gained: The following are the phone numbers of the suspects
    • Bruce: (367) 555-5533
    • Kenny: (826) 555-1652
    • Luca: (389) 555-5198
    • Taylor: (286) 555-6063
*/
---------------------------------------------------------------------------------------------------------------------
-- 9. I need to compare the phone numbers in the call logs to see if there are any matches.
---------------------------------------------------------------------------------------------------------------------
SELECT people.name, caller, receiver, duration, day
FROM phone_calls
JOIN people on phone_calls.caller = people.phone_number
WHERE (
    people.name = 'Bruce'
    OR people.name = 'Kenny'
    OR people.name = 'Luca'
    OR people.name = 'Taylor'
)
AND day = 28
AND month = 7
AND year = 2021
AND duration < 60;
/*
    Information gained: The following are the phone calls that were made by the suspects
        Caller            |     Receiver    | Duration  |   Day
    Bruce  (367) 555-5533 | (375) 555-8161  |   45      |   28
    Taylor (286) 555-6063 | (676) 555-6554  |   43      |   28
    Kenny  (826) 555-1652 | (066) 555-9701  |   55      |   28

    Down to three suspects:
    1. Bruce
    2. Kenny
    3. Taylor
*/
---------------------------------------------------------------------------------------------------------------------
-- 10. I need the names of the receivers.
---------------------------------------------------------------------------------------------------------------------
SELECT name FROM people
WHERE phone_number = '(375) 555-8161'
    OR phone_number = '(676) 555-6554'
    OR phone_number = '(066) 555-9701';

/*
    Information gained: The following are the names of the receivers
    • James
    • Robin
    • Doris
*/
---------------------------------------------------------------------------------------------------------------------
-- 11. What was the earliest flight to New York City, and who was on it?
---------------------------------------------------------------------------------------------------------------------
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.id = 36
    AND (
        name = 'Bruce'
        OR name = 'Kenny'
        OR name = 'Luca'
        OR name = 'Taylor'
    );

/*
    Information gained: It appears Bruce is the first on the list, I can pin
    Bruce as the passenger of the earliest flight out to New York City
    • Bruce

    The THIEF is: Bruce
*/
---------------------------------------------------------------------------------------------------------------------
-- 12. Who was the accomplice that helped Bruce escape?
---------------------------------------------------------------------------------------------------------------------
SELECT name FROM people
WHERE phone_number IN (
    SELECT receiver FROM phone_calls
    WHERE caller IN (
        SELECT phone_number FROM people
        WHERE name = 'Bruce'
    )
    AND day = 28
    AND month = 7
    AND year = 2021
    AND duration < 60
);
/*
    Information gained: The following is the accomplice
    • Robin
*/
---------------------------------------------------------------------------------------------------------------------
-- 13. The case leads to the following suspects:
---------------------------------------------------------------------------------------------------------------------
-- The THIEF is: Bruce
-- The city the thief ESCAPED TO: New York City
-- The ACCOMPLICE is: Robin
