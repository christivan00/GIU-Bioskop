-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 07, 2025 at 11:10 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uas_bioskop`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id_cs` int(5) NOT NULL,
  `nama` varchar(20) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `no_hp` varchar(15) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id_cs`, `nama`, `email`, `no_hp`, `password`) VALUES
(10, '1', '1', '1', '1'),
(11, 'chamdan', 'camdan mubarok', '081321', 'camdan123'),
(12, 'ibnu', 'dshghjgdhgd@gmail.com', '082139337602', 'budi01gaming'),
(13, 'christivan', 'chr@gmail.com', '081332', '1234'),
(14, 'rahmatt', 'rahmadgaming', '09888', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `film`
--

CREATE TABLE `film` (
  `id_film` int(5) NOT NULL,
  `nama_film` varchar(30) DEFAULT NULL,
  `genre` varchar(50) DEFAULT NULL,
  `harga` decimal(10,2) DEFAULT NULL,
  `durasi` varchar(50) DEFAULT NULL,
  `gambar_film` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `film`
--

INSERT INTO `film` (`id_film`, `nama_film`, `genre`, `harga`, `durasi`, `gambar_film`) VALUES
(1, 'mr.bean', 'comedi', 50000.00, '1 jam 30 menit', 'H:/UAS -----/BIOSKOP/GIU-Bioskop/gambar/mrbean.jpg'),
(2, 'Joker', 'horor', 60000.00, '2 jam', 'H:/UAS -----/BIOSKOP/GIU-Bioskop/gambar/joker.jpg'),
(3, 'Kimi no Na wa', 'drama', 70000.00, '1 jam 48 menit', 'H:/UAS -----/BIOSKOP/GIU-Bioskop/gambar/kimino_na_wa.jpg'),
(4, 'Avengers Endgame', 'fantasi', 100000.00, '3 jam 1 menit', 'H:/UAS -----/BIOSKOP/GIU-Bioskop/gambar/avengers_endgame.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal`
--

CREATE TABLE `jadwal` (
  `id_jadwal` int(11) NOT NULL,
  `id_film` int(11) NOT NULL,
  `hari` date NOT NULL,
  `jam` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jadwal`
--

INSERT INTO `jadwal` (`id_jadwal`, `id_film`, `hari`, `jam`) VALUES
(1, 1, '2024-12-31', '14:00:00'),
(2, 2, '2024-12-31', '16:30:00'),
(3, 3, '2024-12-31', '19:00:00'),
(4, 4, '2024-12-31', '21:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `pemesanan`
--

CREATE TABLE `pemesanan` (
  `id_pemesanan` int(11) NOT NULL,
  `id_customer` int(11) DEFAULT NULL,
  `id_film` int(11) DEFAULT NULL,
  `hari_tayang` varchar(20) DEFAULT NULL,
  `jam_tayang` varchar(10) DEFAULT NULL,
  `nomor_kursi` varchar(10) DEFAULT NULL,
  `metode_pembayaran` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id_cs`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `film`
--
ALTER TABLE `film`
  ADD PRIMARY KEY (`id_film`);

--
-- Indexes for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD PRIMARY KEY (`id_jadwal`),
  ADD KEY `id_film` (`id_film`);

--
-- Indexes for table `pemesanan`
--
ALTER TABLE `pemesanan`
  ADD PRIMARY KEY (`id_pemesanan`),
  ADD KEY `fk_customer` (`id_customer`),
  ADD KEY `fk_film` (`id_film`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id_cs` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `film`
--
ALTER TABLE `film`
  MODIFY `id_film` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `jadwal`
--
ALTER TABLE `jadwal`
  MODIFY `id_jadwal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `pemesanan`
--
ALTER TABLE `pemesanan`
  MODIFY `id_pemesanan` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD CONSTRAINT `jadwal_ibfk_1` FOREIGN KEY (`id_film`) REFERENCES `film` (`id_film`) ON DELETE CASCADE;

--
-- Constraints for table `pemesanan`
--
ALTER TABLE `pemesanan`
  ADD CONSTRAINT `fk_customer` FOREIGN KEY (`id_customer`) REFERENCES `customer` (`id_cs`),
  ADD CONSTRAINT `fk_film` FOREIGN KEY (`id_film`) REFERENCES `film` (`id_film`),
  ADD CONSTRAINT `pemesanan_ibfk_1` FOREIGN KEY (`id_customer`) REFERENCES `customer` (`id_cs`),
  ADD CONSTRAINT `pemesanan_ibfk_2` FOREIGN KEY (`id_film`) REFERENCES `film` (`id_film`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
