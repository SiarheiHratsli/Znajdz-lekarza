-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Apr 26, 2025 at 11:16 AM
-- Wersja serwera: 8.0.35
-- Wersja PHP: 8.2.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `proj`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `appointments`
--

CREATE TABLE `appointments` (
  `id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `appointment_date` datetime NOT NULL,
  `patient_name` varchar(255) DEFAULT NULL,
  `status` enum('pending','confirmed','completed','cancelled') DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `doctor_id`, `appointment_date`, `patient_name`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, '2025-02-01 09:00:00', 'Jan Kowalski', 'confirmed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(2, 1, '2025-02-01 10:00:00', 'Anna Kowalska', 'pending', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(3, 2, '2025-02-02 14:00:00', 'Piotr Nowak', 'confirmed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(4, 2, '2025-02-02 15:00:00', 'Maria Zielińska', 'completed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(5, 3, '2025-02-03 08:30:00', 'Krzysztof Adamczyk', 'confirmed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(6, 3, '2025-02-03 09:30:00', 'Łukasz Lewandowski', 'pending', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(7, 4, '2025-02-04 13:00:00', 'Monika Szymańska', 'confirmed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(8, 4, '2025-02-04 14:00:00', 'Katarzyna Wójcik', 'completed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(9, 5, '2025-02-05 16:00:00', 'Zofia Nowakowska', 'confirmed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(10, 5, '2025-02-05 17:00:00', 'Tomasz Piotrowski', 'pending', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(11, 6, '2025-02-06 10:00:00', 'Julia Wójcik', 'confirmed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(12, 6, '2025-02-06 11:00:00', 'Aleksandra Nowak', 'pending', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(13, 7, '2025-02-07 09:30:00', 'Krzysztof Adamczyk', 'completed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(14, 7, '2025-02-07 10:30:00', 'Wojciech Szymański', 'pending', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(15, 8, '2025-02-08 12:00:00', 'Jan Kowalski', 'confirmed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(16, 8, '2025-02-08 13:00:00', 'Barbara Kowalska', 'completed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(17, 9, '2025-02-09 08:00:00', 'Tomasz Piotrowski', 'pending', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(18, 9, '2025-02-09 09:00:00', 'Dominik Kowalski', 'confirmed', '2025-01-23 00:57:56', '2025-01-23 00:57:56'),
(19, 10, '2025-02-10 11:00:00', 'Magdalena Nowakowska', 'confirmed', '2025-01-23 00:57:56', '2025-01-23 00:57:56');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `cities`
--

CREATE TABLE `cities` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cities`
--

INSERT INTO `cities` (`id`, `name`) VALUES
(1, 'Warszawa'),
(2, 'Kraków'),
(3, 'Wrocław'),
(4, 'Poznań'),
(5, 'Gdańsk'),
(6, 'Łódź'),
(7, 'Szczecin'),
(8, 'Bydgoszcz'),
(9, 'Lublin'),
(10, 'Katowice'),
(11, 'Białystok'),
(12, 'Gdynia'),
(13, 'Częstochowa'),
(14, 'Radom'),
(15, 'Toruń'),
(16, 'Kielce'),
(17, 'Zabrze'),
(18, 'Gliwice'),
(19, 'Olsztyn'),
(20, 'Rzeszów'),
(21, 'Opole'),
(22, 'Zielona Góra'),
(23, 'Tychy'),
(24, 'Koszalin'),
(25, 'Legnica'),
(26, 'Słupsk'),
(27, 'Chorzów'),
(28, 'Tarnów'),
(29, 'Siedlce'),
(30, 'Świętochłowice'),
(31, 'Gniezno'),
(32, 'Płock'),
(33, 'Nowy Sącz'),
(34, 'Rybnik'),
(35, 'Stalowa Wola'),
(36, 'Zamość'),
(37, 'Lubin'),
(38, 'Elbląg'),
(39, 'Jelenia Góra'),
(40, 'Sosnowiec'),
(41, 'Piotrków Trybunalski'),
(42, 'Kalisz'),
(43, 'Pabianice'),
(44, 'Ostrowiec Świętokrzyski'),
(45, 'Włocławek'),
(46, 'Mielec'),
(47, 'Grudziądz'),
(48, 'Gorzów Wielkopolski'),
(49, 'Świdnica'),
(50, 'Piekary Śląskie'),
(51, 'Jarosław'),
(52, 'Przemyśl'),
(53, 'Lębork'),
(54, 'Skierniewice'),
(55, 'Złotoryja'),
(56, 'Bielsko-Biała'),
(57, 'Racibórz'),
(58, 'Turek'),
(59, 'Chojnice'),
(60, 'Piła'),
(61, 'Będzin'),
(62, 'Kołobrzeg'),
(63, 'Słupsk'),
(64, 'Ciechanów'),
(65, 'Świebodzin');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `doctors`
--

CREATE TABLE `doctors` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `specialization_id` int DEFAULT NULL,
  `city_id` int DEFAULT NULL,
  `visit_type` enum('gabinet','online') NOT NULL,
  `address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`id`, `name`, `specialization_id`, `city_id`, `visit_type`, `address`) VALUES
(1, 'Jan Kowalski', 1, 1, 'gabinet', NULL),
(2, 'Anna Nowak', 2, 1, 'online', NULL),
(3, 'Marek Wiśniewski', 3, 2, 'gabinet', NULL),
(4, 'Ewa Kaczmarek', 4, 1, 'online', NULL),
(5, 'Paweł Zieliński', 5, 3, 'gabinet', NULL),
(6, 'Julia Wójcik', 2, 2, 'online', NULL),
(7, 'Krzysztof Adamczyk', 1, 4, 'gabinet', NULL),
(8, 'Monika Szymańska', 3, 4, 'online', NULL),
(9, 'Łukasz Lewandowski', 4, 3, 'gabinet', NULL),
(10, 'Magdalena Nowakowska', 5, 2, 'online', NULL),
(12, 'Anna Nowak', 2, 2, 'online', NULL),
(13, 'Marek Wiśniewski', 3, 3, 'gabinet', NULL),
(14, 'Ewa Kaczmarek', 4, 4, 'online', NULL),
(15, 'Paweł Zieliński', 5, 5, 'gabinet', NULL),
(16, 'Julia Wójcik', 6, 6, 'online', NULL),
(17, 'Krzysztof Adamczyk', 7, 7, 'gabinet', NULL),
(18, 'Monika Szymańska', 8, 8, 'online', NULL),
(19, 'Łukasz Lewandowski', 9, 9, 'gabinet', NULL),
(20, 'Magdalena Nowakowska', 10, 10, 'online', NULL),
(21, 'Michał Malinowski', 11, 11, 'gabinet', NULL),
(22, 'Natalia Zielińska', 12, 12, 'online', NULL),
(23, 'Wojciech Sierżant', 13, 13, 'gabinet', NULL),
(24, 'Aleksandra Nowak', 14, 14, 'online', NULL),
(25, 'Piotr Jankowski', 15, 15, 'gabinet', NULL),
(26, 'Szymon Kaczmarek', 16, 16, 'online', NULL),
(27, 'Karolina Nowakowska', 17, 17, 'gabinet', NULL),
(28, 'Łukasz Wiśniewski', 18, 18, 'online', NULL),
(29, 'Katarzyna Adamczak', 19, 19, 'gabinet', NULL),
(30, 'Tomasz Kwiatkowski', 20, 20, 'online', NULL),
(31, 'Zofia Wójcik', 21, 21, 'gabinet', NULL),
(32, 'Dariusz Dąbrowski', 22, 22, 'online', NULL),
(33, 'Marek Kaczmarek', 23, 23, 'gabinet', NULL),
(34, 'Olga Majewska', 24, 24, 'online', NULL),
(35, 'Grzegorz Nowak', 25, 25, 'gabinet', NULL),
(36, 'Julia Malinowska', 26, 26, 'online', NULL),
(37, 'Michał Kozłowski', 27, 27, 'gabinet', NULL),
(38, 'Andrzej Malinowski', 28, 28, 'online', NULL),
(39, 'Karolina Szymańska', 29, 29, 'gabinet', NULL),
(40, 'Piotr Kwiatkowski', 30, 30, 'online', NULL),
(41, 'Krzysztof Adamczak', 31, 31, 'gabinet', NULL),
(42, 'Patryk Wojciechowski', 32, 32, 'online', NULL),
(43, 'Martyna Zawisza', 33, 33, 'gabinet', NULL),
(44, 'Marek Kubicki', 34, 34, 'online', NULL),
(45, 'Natalia Kwiatkowska', 35, 35, 'gabinet', NULL),
(46, 'Wojciech Mazur', 36, 36, 'online', NULL),
(47, 'Monika Lewandowska', 37, 37, 'gabinet', NULL),
(48, 'Grzegorz Duda', 38, 38, 'online', NULL),
(49, 'Katarzyna Sierżant', 39, 39, 'gabinet', NULL),
(50, 'Piotr Zawisza', 40, 40, 'online', NULL),
(51, 'Ewa Kwiatkowska', 41, 41, 'gabinet', NULL);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `doctor_services`
--

CREATE TABLE `doctor_services` (
  `doctor_id` int NOT NULL,
  `service_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `doctor_services`
--

INSERT INTO `doctor_services` (`doctor_id`, `service_id`) VALUES
(1, 1),
(2, 1),
(6, 1),
(1, 2),
(4, 2),
(1, 3),
(3, 3),
(7, 3),
(2, 4),
(5, 4),
(2, 5),
(4, 5),
(6, 5),
(3, 6),
(5, 6),
(7, 6),
(4, 7),
(5, 7),
(7, 7);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `services`
--

CREATE TABLE `services` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `name`, `price`) VALUES
(1, 'Konsultacja ogólna', 150.00),
(2, 'Badanie krwi', 50.00),
(3, 'USG jamy brzusznej', 200.00),
(4, 'Ekg serca', 120.00),
(5, 'Konsultacja online', 100.00),
(6, 'Test alergiczny', 250.00),
(7, 'Wizyta kontrolna', 80.00);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `specializations`
--

CREATE TABLE `specializations` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `specializations`
--

INSERT INTO `specializations` (`id`, `name`) VALUES
(1, 'Kardiolog'),
(2, 'Dermatolog'),
(3, 'Okulista'),
(4, 'Dentysta'),
(5, 'Pediatra'),
(6, 'Neurolog'),
(7, 'Psychiatra'),
(8, 'Chirurg'),
(9, 'Ortopeda'),
(10, 'Ginekolog'),
(11, 'Endokrynolog'),
(12, 'Urolog'),
(13, 'Onkolog'),
(14, 'Stomatolog'),
(15, 'Laryngolog'),
(16, 'Alergolog'),
(17, 'Reumatolog'),
(18, 'Internista'),
(19, 'Psycholog'),
(20, 'Geriatra'),
(21, 'Fizjoterapeuta'),
(22, 'Masażysta'),
(23, 'Chirurg plastyczny'),
(24, 'Diabetolog'),
(25, 'Hematolog'),
(26, 'Radiolog'),
(27, 'Anestezjolog'),
(28, 'Dietetyk'),
(29, 'Proktolog'),
(30, 'Pulmonolog'),
(31, 'Farmaceuta'),
(32, 'Pediatra dermatolog'),
(33, 'Medycyna rodzinna'),
(34, 'Chirurg naczyniowy'),
(35, 'Mikrobiolog'),
(36, 'Terapia manualna'),
(37, 'Stomatologia dziecięca'),
(38, 'Pediatra kardiolog'),
(39, 'Bariatra'),
(40, 'Podolog'),
(41, 'Rehabilitant'),
(42, 'Fizjoterapeuta sportowy'),
(43, 'Endokrynolog dziecięcy'),
(44, 'Leczenie bólu'),
(45, 'Zabiegi estetyczne'),
(46, 'Chirurg ogólny'),
(47, 'Ortopeda dziecięcy'),
(48, 'Specjalista medycyny estetycznej'),
(49, 'Alergolog dziecięcy'),
(50, 'Immunolog'),
(51, 'Medycyna paliatywna'),
(52, 'Terapia zajęciowa'),
(53, 'Fizjoterapeuta dziecięcy'),
(54, 'Chirurgia stomatologiczna'),
(55, 'Klinika zdrowia'),
(56, 'Medycyna pracy'),
(57, 'Psychiatra dziecięcy'),
(58, 'Psychiatra młodzieżowy'),
(59, 'Pediatra nefrolog'),
(60, 'Otolaryngolog'),
(61, 'Leczenie uzależnień'),
(62, 'Chirurg plastyczny estetyczny'),
(63, 'Pediatra neurolog'),
(64, 'Hematologia kliniczna'),
(65, 'Urologia dziecięca');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `doctor_id` (`doctor_id`);

--
-- Indeksy dla tabeli `cities`
--
ALTER TABLE `cities`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id`),
  ADD KEY `specialization_id` (`specialization_id`),
  ADD KEY `city_id` (`city_id`);

--
-- Indeksy dla tabeli `doctor_services`
--
ALTER TABLE `doctor_services`
  ADD PRIMARY KEY (`doctor_id`,`service_id`),
  ADD KEY `service_id` (`service_id`);

--
-- Indeksy dla tabeli `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `specializations`
--
ALTER TABLE `specializations`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `cities`
--
ALTER TABLE `cities`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `specializations`
--
ALTER TABLE `specializations`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `doctors`
--
ALTER TABLE `doctors`
  ADD CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`specialization_id`) REFERENCES `specializations` (`id`),
  ADD CONSTRAINT `doctors_ibfk_2` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`);

--
-- Constraints for table `doctor_services`
--
ALTER TABLE `doctor_services`
  ADD CONSTRAINT `doctor_services_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `doctor_services_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE;
COMMIT;

CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `gender` ENUM('M', 'F', 'Other') NOT NULL,
  `birth_date` DATE NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
