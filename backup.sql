-- MySQL dump 10.13  Distrib 8.0.37, for Linux (x86_64)
--
-- Host: localhost    Database: storyafrika
-- ------------------------------------------------------
-- Server version	8.0.37-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bookmarks`
--

DROP TABLE IF EXISTS `bookmarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookmarks` (
  `story_id` varchar(60) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `story_id` (`story_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `bookmarks_ibfk_1` FOREIGN KEY (`story_id`) REFERENCES `stories` (`id`),
  CONSTRAINT `bookmarks_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookmarks`
--

LOCK TABLES `bookmarks` WRITE;
/*!40000 ALTER TABLE `bookmarks` DISABLE KEYS */;
INSERT INTO `bookmarks` VALUES ('e0e040fc-345d-4a80-8911-828db97a39e1','9ad31036-2e0b-4b12-b485-ee7340868d76','5889c208-37f4-4129-a0b7-112d1da7e5c4','2024-07-31 12:42:44','2024-07-31 12:42:44'),('e0e040fc-345d-4a80-8911-828db97a39e1','2c67e67f-147f-4b86-bc00-9bfa69175f6a','a3718b98-1b19-4201-982e-b1e3b729ad6c','2024-07-31 11:00:03','2024-07-31 11:00:03'),('8d628df3-97c1-4582-99bf-56e82321a499','9ad31036-2e0b-4b12-b485-ee7340868d76','dee0ab13-c0b0-443f-96a4-1012f87096a0','2024-07-31 13:06:04','2024-07-31 13:06:04');
/*!40000 ALTER TABLE `bookmarks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_likes`
--

DROP TABLE IF EXISTS `comment_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment_likes` (
  `comment_id` varchar(60) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_id` (`comment_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comment_likes_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`),
  CONSTRAINT `comment_likes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_likes`
--

LOCK TABLES `comment_likes` WRITE;
/*!40000 ALTER TABLE `comment_likes` DISABLE KEYS */;
INSERT INTO `comment_likes` VALUES ('6725b673-622b-4aec-9816-0ec249bfe5b7','2c67e67f-147f-4b86-bc00-9bfa69175f6a','3cf46698-f1e4-43ee-a92c-c687b3252ed2','2024-07-31 10:59:37','2024-07-31 10:59:37'),('6725b673-622b-4aec-9816-0ec249bfe5b7','9ad31036-2e0b-4b12-b485-ee7340868d76','d610c2db-bb06-4776-8afb-510d8d253eb9','2024-07-31 12:54:04','2024-07-31 12:54:04');
/*!40000 ALTER TABLE `comment_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_unlikes`
--

DROP TABLE IF EXISTS `comment_unlikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment_unlikes` (
  `comment_id` varchar(60) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_id` (`comment_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comment_unlikes_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`),
  CONSTRAINT `comment_unlikes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_unlikes`
--

LOCK TABLES `comment_unlikes` WRITE;
/*!40000 ALTER TABLE `comment_unlikes` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment_unlikes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `comment` text NOT NULL,
  `Story` varchar(60) NOT NULL,
  `User` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Story` (`Story`),
  KEY `User` (`User`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`Story`) REFERENCES `stories` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`User`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES ('Excellent story. Keep it up!','e0e040fc-345d-4a80-8911-828db97a39e1','2c67e67f-147f-4b86-bc00-9bfa69175f6a','6725b673-622b-4aec-9816-0ec249bfe5b7','2024-07-31 10:59:25','2024-07-31 10:59:25'),('Incredible!','8d628df3-97c1-4582-99bf-56e82321a499','9ad31036-2e0b-4b12-b485-ee7340868d76','f3f3f36e-639b-4514-ad45-872562eb539f','2024-07-31 12:55:35','2024-07-31 12:55:35');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `followers` (
  `follower_id` varchar(60) DEFAULT NULL,
  `followed_id` varchar(60) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `follower_id` (`follower_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`),
  CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `followers`
--

LOCK TABLES `followers` WRITE;
/*!40000 ALTER TABLE `followers` DISABLE KEYS */;
INSERT INTO `followers` VALUES ('2c67e67f-147f-4b86-bc00-9bfa69175f6a','869700c6-565c-46cd-ab18-e6bdac816480','22e94071-3c70-439c-98de-7430398dcc80','2024-07-31 10:09:05','2024-07-31 10:09:05'),('9ad31036-2e0b-4b12-b485-ee7340868d76','869700c6-565c-46cd-ab18-e6bdac816480','5acbf116-0a10-4dcd-96bb-a2fb196edd17','2024-07-31 11:24:14','2024-07-31 11:24:14');
/*!40000 ALTER TABLE `followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `story_id` varchar(60) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `story_id` (`story_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`story_id`) REFERENCES `stories` (`id`),
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES ('e0e040fc-345d-4a80-8911-828db97a39e1','2c67e67f-147f-4b86-bc00-9bfa69175f6a','2ff6ed42-4371-4612-9a62-8801f3907ae5','2024-07-31 11:40:12','2024-07-31 11:40:12'),('e0e040fc-345d-4a80-8911-828db97a39e1','9ad31036-2e0b-4b12-b485-ee7340868d76','4f76e480-2ef8-4fdf-9723-6004ffdaa16c','2024-07-31 12:42:47','2024-07-31 12:42:47'),('e0e040fc-345d-4a80-8911-828db97a39e1','869700c6-565c-46cd-ab18-e6bdac816480','cfeb81fa-f859-4801-934f-5a1ce737f749','2024-07-31 10:38:58','2024-07-31 10:38:58'),('8d628df3-97c1-4582-99bf-56e82321a499','9ad31036-2e0b-4b12-b485-ee7340868d76','e0f0eee9-574f-41ae-bc6d-0e7cee137c67','2024-07-31 12:41:08','2024-07-31 12:41:08'),('65b3951c-42ca-4e17-9965-d0c435284d61','2c67e67f-147f-4b86-bc00-9bfa69175f6a','f4cf8172-d33c-4c55-93da-68bef5f6964f','2024-07-31 11:11:23','2024-07-31 11:11:23');
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stories`
--

DROP TABLE IF EXISTS `stories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stories` (
  `title` varchar(200) NOT NULL,
  `text` text NOT NULL,
  `User` varchar(60) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `User` (`User`),
  CONSTRAINT `stories_ibfk_1` FOREIGN KEY (`User`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stories`
--

LOCK TABLES `stories` WRITE;
/*!40000 ALTER TABLE `stories` DISABLE KEYS */;
INSERT INTO `stories` VALUES ('How I make hundreds of dollars in Kenya purely online','[{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" contenteditable=\\\"false\\\" style=\\\"left: -35px; display: none;\\\">⇅</span>In the bustling city of Nairobi, Kenya, where the vibrant streets are filled with the sounds of honking matatus and lively conversations, lived a young entrepreneur named Alex. Alex had always been tech-savvy, fascinated by the endless possibilities of the internet. Determined to carve out a niche for himself, he set out to make a living purely online.\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" contenteditable=\\\"false\\\" style=\\\"left: -35px; display: none;\\\">⇅</span>Alex\'s journey began with a keen interest in e-commerce. He noticed a growing demand for locally made, sustainable products. With this insight, he decided to create an online store that showcased the unique handicrafts of Kenyan artisans. He partnered with local craftsmen and women, ensuring fair trade and highlighting the rich cultural heritage of Kenya.\"},{\"content\":\"<br />\"},{\"content\":\"Using his skills in web design, Alex built a sleek and user-friendly website. He took high-quality photos of the products and wrote engaging descriptions that told the stories behind each item. To drive traffic to his site, Alex leveraged social media platforms, sharing the artisans\' stories and the beauty of their craft. His authenticity resonated with people, and soon, orders started pouring in from all over the world.<span class=\\\"handle ui-sortable-handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" contenteditable=\\\"false\\\" style=\\\"left: -35px; display: none;\\\">⇅</span>In addition to his e-commerce venture, Alex explored the world of affiliate marketing. He created a blog where he reviewed tech gadgets, travel gear, and other products he was passionate about. By joining affiliate programs, he earned commissions for every sale made through his referral links. His honest and detailed reviews built trust with his audience, and his affiliate income steadily grew.\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" contenteditable=\\\"false\\\" style=\\\"left: -35px; display: none;\\\">⇅</span>Not stopping there, Alex tapped into the freelancing market. He offered his services as a graphic designer on various platforms, creating logos, social media graphics, and website layouts for clients globally. His reputation for delivering high-quality work on time earned him a steady stream of projects, further boosting his online income.\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" contenteditable=\\\"false\\\" style=\\\"left: -35px; display: none;\\\">⇅</span>To diversify his revenue streams, Alex also delved into online courses. He created a series of video tutorials on web design and e-commerce, sharing his expertise with aspiring entrepreneurs. These courses, hosted on popular e-learning platforms, provided him with a passive income as they continued to sell long after he had created them.\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" contenteditable=\\\"false\\\" style=\\\"left: -35px; display: none;\\\">⇅</span>Through dedication, innovation, and a keen understanding of the digital landscape, Alex managed to make hundreds of dollars every month, purely online. His success not only provided him with financial independence but also allowed him to support and uplift his community. The artisans he partnered with saw their crafts reach international markets, and Alex became a source of inspiration for many young Kenyans aspiring to make a mark in the digital world.\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" contenteditable=\\\"false\\\" style=\\\"left: -35px; display: none;\\\">⇅</span>Alex\'s story is a testament to the power of the internet and the endless opportunities it offers. In a world where connectivity knows no bounds, he turned his passion into profit, proving that with creativity and perseverance, one can truly thrive in the online realm.\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"}]','2c67e67f-147f-4b86-bc00-9bfa69175f6a','6883ad58-f6c5-4bb9-9e7b-656bf9e8b7d3.webp','65b3951c-42ca-4e17-9965-d0c435284d61','2024-07-31 11:01:09','2024-07-31 11:01:09'),('The Birth of the First Keke in Sierra Leone','[{\"content\":\"<br />\"},{\"content\":\"\"},{\"content\":\"<br />\"},{\"content\":\"In the heart of Freetown, Sierra Leone, I stood at the bustling intersection of Aberdeen and Lumley, watching the chaotic ballet of cars, motorcycles, and pedestrians. The city\'s vibrant energy pulsed around me, but amidst the commotion, I noticed a gap. The streets needed something more—something affordable, efficient, and uniquely suited to the city\'s needs. It was in that moment the idea of the first \\\"keke\\\" was born.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"I had always been an inventor at heart. Growing up, I spent countless hours dismantling and reassembling gadgets, much to my parents\' dismay. My fascination with mechanics led me to pursue engineering at Njala University, where I dreamt of creating something that would leave a lasting impact on my beloved country. But it wasn\'t until that day at the intersection that inspiration struck.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"The concept of the keke, a small three-wheeled vehicle, was not entirely new. They were popular in many parts of Asia and Africa, but Sierra Leone had yet to see one. I envisioned a keke that could navigate Freetown\'s narrow streets and heavy traffic, offering an affordable alternative to taxis and a safer option compared to motorcycles.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"With my savings, I purchased an old motorcycle and a rusted cart. Over the next few months, my small garage became a hub of activity. Friends and neighbors were skeptical at first, but their curiosity grew as they saw the progress. Using spare parts from local junkyards and custom-made components, I slowly transformed the motorcycle and cart into a prototype keke.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"The first test run was nerve-wracking. As I turned the key, the engine sputtered to life. My heart raced as I took the keke onto the streets of Freetown. People stared in disbelief, some even pointing and laughing. But I didn\'t care. The keke moved smoothly, navigating through traffic with ease. It was a success.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"News of the keke spread quickly. The local media dubbed it \\\"the people\'s vehicle,\\\" and soon, I was inundated with requests from individuals and businesses wanting their own. Recognizing the potential, I secured a small loan and established a workshop. I hired a team of young, enthusiastic engineers and mechanics, many of whom were unemployed youth looking for an opportunity to learn and grow.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Together, we refined the design, making it more durable and efficient. We added features like a sturdy roof for protection against the rain and a small luggage compartment. Our kekes became a common sight on Freetown\'s streets, providing affordable transportation and creating jobs.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"The impact of the keke went beyond transportation. It spurred economic growth, as people could now travel to markets, schools, and workplaces more easily. Women entrepreneurs, in particular, found the keke to be a game-changer, allowing them to transport goods safely and affordably. The keke also reduced the burden on the city\'s overtaxed public transportation system, easing congestion and pollution.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Years later, as I stood in front of our bustling workshop, watching the latest batch of kekes roll out, I felt a deep sense of pride. The keke had become more than just a vehicle; it was a symbol of innovation, resilience, and the power of dreams. Sierra Leone had embraced it wholeheartedly, and in turn, the keke had transformed the lives of countless people.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"The journey from that chaotic intersection to this moment had been challenging, but it was worth every struggle. I had developed the first keke in Sierra Leone, and in doing so, had helped steer my country toward a brighter, more connected future.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle ui-sortable-handle\\\" style=\\\"display: none;\\\">⇅</span>\"}]','9ad31036-2e0b-4b12-b485-ee7340868d76','keke.png','8d628df3-97c1-4582-99bf-56e82321a499','2024-07-31 12:33:38','2024-07-31 12:33:38'),('StoryAfrika: The Journey of Building My Portfolio Project','[{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle ui-sortable-handle\\\" style=\\\"display: none;\\\">⇅</span>Embarking on the creation of StoryAfrika, my capstone portfolio project, was a challenging yet immensely rewarding experience. StoryAfrika is a platform dedicated to sharing African stories with the world, and it has been a labor of love from start to finish.\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" contenteditable=\\\"false\\\" style=\\\"display: none;\\\">⇅</span>The Initial Spark\"},{\"content\":\"<br />\"},{\"content\":\"The inspiration for StoryAfrika came from my passion for storytelling and my desire to showcase the rich, diverse narratives of African life. I wanted to create a space where people from all walks of life could share their experiences, inspire others, and foster a greater understanding of our continent\'s heritage and culture.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Development Challenges<span class=\\\"handle ui-sortable-handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"One of the major challenges I faced was with Flask and <b>SQLAlchemy</b>. Unlike frameworks like Django, which come with many built-in features, Flask requires you to build from scratch. This meant handling everything from routing to session management, which was daunting at times. Managing sessions in particular was a tricky aspect, but through persistence and a lot of debugging, I eventually mastered it. This struggle, however, turned into a triumph when I saw my application running smoothly online.<span class=\\\"handle ui-sortable-handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Hosting Hurdles<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Hosting <b>StoryAfrika</b> presented its own set of obstacles. Many hosting providers, such as Digital Ocean, required payment, which was not feasible for me as a student. I turned to AWS, which offers a free tier. Initially, this seemed like a perfect solution, but after a few weeks, my account was inexplicably locked, and I could no longer access my resources. Creating new accounts yielded the same frustrating result.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"In the end, I found a solution by using the servers provided by my school. I hosted the main application at <i><b>stories.storyafrika.live</b></i> and the main site at <i><b>storyafrika.live,</b></i> both with HTTPS connections. Setting up Nginx and managing these servers was a complex task, but it was incredibly fulfilling to see everything come together.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Timeline and Execution<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"The entire project, from the research phase and project approval to the MVP and final hosting, took one month and one week. Every aspect of StoryAfrika was built and managed by me, including:<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<li><strong>Design:</strong> I used Figma to create detailed designs and prototypes.</li><li><strong>Hosting:</strong> I configured Nginx on Linux servers and used Gunicorn for the WSGI server.</li><li><strong>Backend Development:</strong> I developed the backend using Python, Flask, and MySQL.</li><li><strong>Frontend Development:</strong> I utilized HTML5 and TailwindCSS for the front end, ensuring a responsive and visually appealing design.</li><li><strong>SEO and Metadata:</strong> I implemented OG tags for better social media integration.</li><li><strong>JavaScript:</strong> I enhanced interactivity with JavaScript and jQuery.</li><span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Reflections and Future Prospects<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Looking back, the journey of creating StoryAfrika was filled with both challenges and successes. Each hurdle taught me valuable lessons and each success, no matter how small, was a stepping stone towards the final product. I am incredibly proud of what I have accomplished and excited about the potential of StoryAfrika to connect people through the power of storytelling.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Moving forward, I hope to continue improving and expanding the platform, incorporating more features and reaching a wider audience. The experience has not only honed my technical skills but also deepened my appreciation for the storytelling tradition that is so vital to our African heritage.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"Visit <a rel=\\\"noreferrer\\\" target=\\\"_new\\\" href=\\\"http://storyafrika.live\\\">StoryAfrika</a> and become a part of our community. Share your story, inspire others, and be inspired.<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle\\\" style=\\\"display: none;\\\">⇅</span>\"}]','869700c6-565c-46cd-ab18-e6bdac816480','Home_page_1.png','e0e040fc-345d-4a80-8911-828db97a39e1','2024-07-31 10:17:24','2024-07-31 10:17:24');
/*!40000 ALTER TABLE `stories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `story_topic_association`
--

DROP TABLE IF EXISTS `story_topic_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `story_topic_association` (
  `story_id` varchar(60) NOT NULL,
  `topic_id` varchar(60) NOT NULL,
  PRIMARY KEY (`story_id`,`topic_id`),
  KEY `topic_id` (`topic_id`),
  CONSTRAINT `story_topic_association_ibfk_1` FOREIGN KEY (`story_id`) REFERENCES `stories` (`id`),
  CONSTRAINT `story_topic_association_ibfk_2` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `story_topic_association`
--

LOCK TABLES `story_topic_association` WRITE;
/*!40000 ALTER TABLE `story_topic_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `story_topic_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic_followers`
--

DROP TABLE IF EXISTS `topic_followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topic_followers` (
  `user_id` varchar(60) NOT NULL,
  `topic_id` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `topic_id` (`topic_id`),
  CONSTRAINT `topic_followers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `topic_followers_ibfk_2` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_followers`
--

LOCK TABLES `topic_followers` WRITE;
/*!40000 ALTER TABLE `topic_followers` DISABLE KEYS */;
/*!40000 ALTER TABLE `topic_followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topics` (
  `name` varchar(80) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topics`
--

LOCK TABLES `topics` WRITE;
/*!40000 ALTER TABLE `topics` DISABLE KEYS */;
/*!40000 ALTER TABLE `topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(200) NOT NULL,
  `short_bio` varchar(160) DEFAULT NULL,
  `about` text,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `full_name` varchar(50) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('alfred','alfred@gmail.com','scrypt:32768:8:1$wX94epA6dA5w91Bb$58e33de70fce9bbbe93aca0dfb78a6b1b9578d03b8658ec81a07c56e7ce88167067eab7138841670be84d8c5d44ef8fe8c3638f4a57002ec2c25fe8d21b6f8c2',NULL,NULL,NULL,NULL,NULL,'background_py.jpg','2c67e67f-147f-4b86-bc00-9bfa69175f6a','2024-07-31 10:54:12','2024-07-31 10:54:12'),('David','benjamin@gmail.com','scrypt:32768:8:1$rxdDFiuChlvwdiCE$e7846014ff9a3647763d90b591a9be53a57bb3a58357b97bd70b1189074e34ca62eea860a63192a82052537f65e7876da326a1e9bf8f20368984eab43d92a68e',NULL,NULL,NULL,NULL,NULL,'profile-png.png','869700c6-565c-46cd-ab18-e6bdac816480','2024-07-31 10:11:11','2024-07-31 10:11:11'),('alusine','alusine@gmail.com','scrypt:32768:8:1$lSMo99ggVJ3wEKoP$1952a331e238606ba577257694c09c7001d851037b40172606186b6efd22703e025e89aec266a8c000e1aa93a3d50b49eb117c2133208eaddb6e83bd52ec7a94',NULL,NULL,NULL,NULL,NULL,'profile.jpg','9ad31036-2e0b-4b12-b485-ee7340868d76','2024-07-31 12:32:01','2024-07-31 12:32:01');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-31 13:09:10
