/*
Navicat MySQL Data Transfer

Source Server         : blog
Source Server Version : 50528
Source Host           : 127.0.0.1:3306
Source Database       : movie

Target Server Type    : MYSQL
Target Server Version : 50528
File Encoding         : 65001

Date: 2018-05-28 22:46:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `actor`
-- ----------------------------
DROP TABLE IF EXISTS `actor`;
CREATE TABLE `actor` (
  `id` int(100) unsigned NOT NULL AUTO_INCREMENT,
  `movieId` int(100) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `link` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of actor
-- ----------------------------

-- ----------------------------
-- Table structure for `award`
-- ----------------------------
DROP TABLE IF EXISTS `award`;
CREATE TABLE `award` (
  `id` int(100) unsigned NOT NULL AUTO_INCREMENT,
  `movieId` int(100) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `type` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of award
-- ----------------------------

-- ----------------------------
-- Table structure for `comment`
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(100) unsigned NOT NULL AUTO_INCREMENT,
  `movieId` int(100) NOT NULL,
  `content` mediumtext CHARACTER SET utf8mb4 NOT NULL,
  `userName` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `time` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of comment
-- ----------------------------

-- ----------------------------
-- Table structure for `movie`
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `id` int(100) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `director` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `age` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `country` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `evaluationNum` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `score` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `note` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `link` mediumtext COLLATE utf8mb4_bin,
  `commentLink` mediumtext COLLATE utf8mb4_bin,
  `time` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `otherName` tinytext COLLATE utf8mb4_bin,
  `movieLength` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  `summary` mediumtext COLLATE utf8mb4_bin,
  `poster` mediumtext COLLATE utf8mb4_bin,
  `language` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of movie
-- ----------------------------
