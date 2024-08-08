-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: storyafrika
-- ------------------------------------------------------
-- Server version	8.0.37

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
INSERT INTO `bookmarks` VALUES ('8dc042e8-5a92-4bb9-bbb0-02b489eb1ae8','929da5f1-d99c-474c-beb1-a6cab20ab263','86da63cd-675c-4cfd-92d9-4cee147c9ff6','2024-07-31 08:32:54','2024-07-31 08:32:54'),('386c6967-a0b0-4356-981e-dfeb7786fc77','f9231354-5fb8-4243-8e14-34add2d3d4c2','ed2ce570-8dd6-4e2d-8401-7f183e5b5b82','2024-08-03 19:05:02','2024-08-03 19:05:02');
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
INSERT INTO `comment_likes` VALUES ('a17aed69-251d-48bd-baba-7e307c7dfcea','237dce09-07d0-4c6f-9d36-bd9dc369bd82','582d6a40-7165-48f6-966d-85f09ae2fe78','2024-08-03 19:01:14','2024-08-03 19:01:14'),('a17aed69-251d-48bd-baba-7e307c7dfcea','f9231354-5fb8-4243-8e14-34add2d3d4c2','662bffe1-0554-4ab5-9717-310934d19acd','2024-08-03 19:05:00','2024-08-03 19:05:00'),('a8dd038e-7acc-4fe0-86a8-6546486d107f','f9231354-5fb8-4243-8e14-34add2d3d4c2','e90f54eb-e949-43fc-a95b-917895f1ac30','2024-08-03 04:03:04','2024-08-03 04:03:04');
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
INSERT INTO `comment_unlikes` VALUES ('fe6fdd8a-5bf8-4f3c-b862-251be253c39d','f9231354-5fb8-4243-8e14-34add2d3d4c2','0cb94514-b316-4c4f-99b5-ce6a26716e69','2024-08-03 04:02:45','2024-08-03 04:02:45'),('f53fd1a1-d413-4a06-a921-3c3520df0794','f9231354-5fb8-4243-8e14-34add2d3d4c2','d2ae3829-935b-419b-a88b-dd6e263bc979','2024-08-03 19:56:52','2024-08-03 19:56:52');
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
INSERT INTO `comments` VALUES ('your C game','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','20ecedea-34db-4cfb-82ab-9c6f79d01297','2024-08-03 15:36:20','2024-08-03 15:36:20'),('your D game','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','3fe92ef7-1f37-48c1-ac22-20bc8d67bad9','2024-08-03 15:36:46','2024-08-03 15:36:46'),('your b game','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','683264aa-a3e6-4693-9283-0e0a0e5e0e42','2024-08-03 15:36:07','2024-08-03 15:36:07'),('what is your name bro','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','6c73057e-7571-458c-9532-5c5ce60998f6','2024-08-03 15:28:29','2024-08-03 15:28:29'),('thequickbrownfox','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','96452086-679b-4d2e-9274-3ee147322f89','2024-08-03 15:28:00','2024-08-03 15:28:00'),('okay bro!','386c6967-a0b0-4356-981e-dfeb7786fc77','237dce09-07d0-4c6f-9d36-bd9dc369bd82','a17aed69-251d-48bd-baba-7e307c7dfcea','2024-08-03 18:56:33','2024-08-03 18:56:33'),('okay cool!','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','a8dd038e-7acc-4fe0-86a8-6546486d107f','2024-08-03 04:02:56','2024-08-03 04:02:56'),('the post have 6 comments in total','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','b5750769-aca5-4f00-ae8d-97c63e89536d','2024-08-03 15:29:58','2024-08-03 15:29:58'),('nice video','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','d169d696-2a96-49bc-80b4-74304857253a','2024-08-03 15:11:19','2024-08-03 15:11:19'),('Your Dad is indeed a hero. Inspiring story!','8dc042e8-5a92-4bb9-bbb0-02b489eb1ae8','929da5f1-d99c-474c-beb1-a6cab20ab263','e287f1ea-5827-4706-8b01-50f3bf834f94','2024-07-31 08:32:54','2024-07-31 08:32:54'),('Amazing story! I\'m truely inspired to know you actually work hard for your money. Which is in contrast to what people are saying. Continue doing what you do.','386c6967-a0b0-4356-981e-dfeb7786fc77','c46f79b2-5f36-4f16-b3cc-c54971aa30d5','f53fd1a1-d413-4a06-a921-3c3520df0794','2024-07-31 08:32:54','2024-07-31 08:32:54'),('your A game','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','fe45f436-caa3-4195-803d-46dfaf1e958d','2024-08-03 15:34:06','2024-08-03 15:34:06'),('nice story man','b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','fe6fdd8a-5bf8-4f3c-b862-251be253c39d','2024-07-31 08:50:33','2024-07-31 08:50:33');
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
INSERT INTO `followers` VALUES ('c46f79b2-5f36-4f16-b3cc-c54971aa30d5','50b9953f-7fa9-4812-8c44-7fd34ad6f2b8','08c0cdf8-a286-480e-a1ba-163627b610af','2024-08-03 18:41:58','2024-08-03 18:41:58'),('f9231354-5fb8-4243-8e14-34add2d3d4c2','929da5f1-d99c-474c-beb1-a6cab20ab263','1eee250f-b736-4e56-b000-2f854cd5a558','2024-08-03 17:56:21','2024-08-03 17:56:21'),('f9231354-5fb8-4243-8e14-34add2d3d4c2','c46f79b2-5f36-4f16-b3cc-c54971aa30d5','88c67ed0-e28f-4473-80af-4c4d42b58747','2024-08-03 18:21:35','2024-08-03 18:21:35');
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
INSERT INTO `likes` VALUES ('8dc042e8-5a92-4bb9-bbb0-02b489eb1ae8','929da5f1-d99c-474c-beb1-a6cab20ab263','2f1a8420-72e3-45b8-9cd9-c1a044275e9f','2024-07-31 08:32:54','2024-07-31 08:32:54'),('386c6967-a0b0-4356-981e-dfeb7786fc77','929da5f1-d99c-474c-beb1-a6cab20ab263','41e06bca-c64a-486b-b06b-6e5b3c71633e','2024-07-31 08:32:54','2024-07-31 08:32:54'),('386c6967-a0b0-4356-981e-dfeb7786fc77','f9231354-5fb8-4243-8e14-34add2d3d4c2','5eaf5413-9ffe-4ca8-86e7-0ad6a84eb6d2','2024-07-31 08:51:06','2024-07-31 08:51:06'),('386c6967-a0b0-4356-981e-dfeb7786fc77','c46f79b2-5f36-4f16-b3cc-c54971aa30d5','63289f2d-6dc2-4c51-a219-b469ef50cb27','2024-07-31 08:32:54','2024-07-31 08:32:54'),('386c6967-a0b0-4356-981e-dfeb7786fc77','237dce09-07d0-4c6f-9d36-bd9dc369bd82','81e20723-7c87-4c29-8a65-3c2f4390d0ad','2024-08-03 18:50:58','2024-08-03 18:50:58'),('b52c978e-27ae-4739-bf09-41aaf3c81de3','f9231354-5fb8-4243-8e14-34add2d3d4c2','9a695608-6f04-47eb-b5d3-86991d128950','2024-08-03 23:13:12','2024-08-03 23:13:12'),('386c6967-a0b0-4356-981e-dfeb7786fc77','50b9953f-7fa9-4812-8c44-7fd34ad6f2b8','ccd3a8a8-8104-4d47-99ab-7c77ec07f562','2024-07-31 08:32:54','2024-07-31 08:32:54');
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
INSERT INTO `stories` VALUES (' ','[{\"content\":\"xyzzzzzz\"}]','f9231354-5fb8-4243-8e14-34add2d3d4c2',NULL,'0a14e143-7546-4f37-8f57-8901ba945508','2024-08-03 23:14:01','2024-08-03 23:14:01'),('My journey to becoming the a successful enterpreneur in Afrika','My Journey to Becoming a Successful Entrepreneur in Africa\nMy name is Aliko Dangote, and my journey to becoming a successful entrepreneur in Africa is one of determination, vision, and unwavering perseverance. From humble beginnings to becoming one of the continent\'s most influential business magnates, my story is a testament to the boundless potential that lies within Africa.\n\nThe Early Years\nI was born in Kano, Nigeria, into a family with a rich history of trade and commerce. From a young age, I was fascinated by the world of business. I remember visiting my grandfather\'s small trading shop, where I would watch him meticulously handle transactions and interact with customers. Those early experiences planted the seeds of ambition and entrepreneurship in my heart.\n\nThe First Steps\nAfter completing my education, I decided to pursue my dreams in earnest. In 1977, with a modest loan from my uncle, I established the Dangote Group. It started as a small trading company, dealing primarily in cement and other basic commodities. The early days were challenging, but I was driven by a vision of creating a business that would not only succeed but also contribute significantly to Africa\'s economic development.\n\nOvercoming Challenges\nThe path to success was fraught with obstacles. The business environment in Nigeria and across Africa was often unpredictable and fraught with bureaucratic red tape. There were times when I faced significant financial setbacks, and moments when the future seemed uncertain. However, I remained steadfast, learning from every failure and using each setback as a stepping stone towards greater achievements.\n\nExpanding Horizons\nAs the Dangote Group grew, so did my ambitions. I began to see the potential for expanding beyond Nigeria and tapping into the broader African market. I diversified the company\'s operations, venturing into sectors such as sugar refining, flour milling, and later, cement manufacturing. Each new venture came with its own set of challenges, but I was determined to create a business empire that would stand the test of time.\n\nBuilding an Empire\nOne of the turning points in my journey was the establishment of Dangote Cement. Recognizing the immense demand for infrastructure development across Africa, I invested heavily in building state-of-the-art cement manufacturing plants. This decision not only revolutionized the construction industry in Nigeria but also positioned the Dangote Group as a key player in Africa\'s industrialization.\n\nGiving Back\nSuccess, to me, has always been about more than just personal wealth. I have always believed in the importance of giving back to society and contributing to the development of my community and continent. Through the Dangote Foundation, I have been able to support numerous initiatives in education, healthcare, and poverty alleviation, making a positive impact on the lives of millions of Africans.\n\nThe Road Ahead\nAs I reflect on my journey, I am filled with a sense of pride and gratitude. The road to becoming a successful entrepreneur in Africa has been anything but easy, but it has been immensely rewarding. I am humbled by the opportunities I have had to contribute to Africa\'s growth and development, and I am excited about the future.\n\nAfrica is a continent brimming with potential, and I believe that with the right vision, determination, and commitment, we can achieve extraordinary things. My journey is far from over, and I remain dedicated to building a legacy that will inspire future generations of African entrepreneurs to dream big and strive for greatness.\n\nIn the end, my story is not just about personal success; it is about the limitless possibilities that lie within Africa. It is a story of hope, resilience, and the enduring power of entrepreneurship to transform lives and shape the future of a continent.\n','f9231354-5fb8-4243-8e14-34add2d3d4c2',NULL,'386c6967-a0b0-4356-981e-dfeb7786fc77','2024-07-31 08:32:54','2024-07-31 08:32:54'),('My dad was protective during the civil ware in SL','In the heart of Sierra Leone, nestled among the rolling hills and lush, green forests, lay the small village of Makeni. The people of Makeni lived simple lives, farming the land and cherishing the tight-knit bonds of family and community. For young Mariama, the village was a paradise, a world filled with the laughter of children, the warmth of family, and the beauty of nature.\n\nMariama\'s father, Alpha, was a pillar of strength and wisdom in Makeni. A tall, broad-shouldered man with kind eyes that sparkled with a mix of wisdom and warmth, Alpha was respected by everyone in the village. He was known for his unwavering sense of justice and his deep love for his family. Mariama adored him and followed him everywhere, always eager to learn from his stories and teachings.\n<br>\n\nHowever, the peace and tranquility of Makeni were shattered when the civil war in Sierra Leone erupted. The conflict spread like wildfire, bringing with it tales of unimaginable horrors and despair. As the war crept closer to their village, fear began to grip the hearts of Makeni\'s residents.\n\nAlpha knew that they needed to protect their home and, most importantly, his family. He gathered the villagers one evening under the large baobab tree at the center of the village. With a calm yet commanding voice, he spoke to them about the importance of unity, vigilance, and preparation. He organized patrols, set up watch points, and made sure everyone knew what to do in case of an attack.\n\nDespite the looming threat, Alpha tried to maintain a sense of normalcy for Mariama and her younger brother, Kabba. He continued to tell them stories of their ancestors, of brave warriors and wise leaders, instilling in them a sense of hope and courage. Mariama could see the worry in her father\'s eyes, but she also felt his unwavering determination to protect them.\n<br>\n\nOne fateful night, the war finally reached their doorstep. Rebel soldiers, ruthless and armed, stormed into Makeni, their shouts and gunfire shattering the stillness of the night. Alpha had prepared for this moment, and he quickly sprang into action. He led Mariama, Kabba, and their mother to a hidden underground shelter he had constructed beneath their home.\n\nAs the sounds of chaos filled the air, Alpha held his family close, his strong arms wrapped around them protectively. Mariama clung to him, her heart pounding with fear. Alpha\'s calm voice reassured them, promising that they would get through this together.\n\nHours passed like an eternity. Eventually, the noises above began to fade, replaced by an eerie silence. Alpha carefully emerged from the shelter, his eyes scanning the surroundings for any sign of danger. He knew they couldn\'t stay in Makeni any longer; it was no longer safe.\n\nUnder the cover of darkness, Alpha led his family away from the village, moving swiftly and silently through the forest. He had a plan to reach a refugee camp near the border, a place where they might find safety. Mariama marveled at her father\'s resourcefulness and strength. Despite the danger, he remained a beacon of hope and protection.\n<br>\n\nThe journey was long and arduous. They traveled for days, avoiding rebel patrols and surviving on the little food they could carry. Alpha\'s determination never wavered, and his protective instincts kept them safe. He taught Mariama and Kabba how to move quietly, how to find safe paths through the wilderness, and how to stay hidden.\n\nFinally, after what felt like an eternity, they reached the refugee camp. It was a stark contrast to the vibrant life of Makeni, but it was a place of safety. Alpha\'s relief was palpable, and for the first time in weeks, Mariama saw him smile.\n<br>\n\nLife in the camp was difficult, but Alpha continued to be a pillar of strength for his family and the other refugees. He organized efforts to improve living conditions, provided guidance and support, and never lost his sense of hope. He became a leader among the displaced, his protective nature extending to all who needed help.\n\nYears passed, and the war eventually came to an end. Mariama grew up, her childhood shaped by the strength and resilience of her father. Alpha\'s protective nature had not only saved their lives but also taught her the importance of courage, unity, and unwavering love.\n\nWhen they finally returned to Makeni, the village was in ruins, but the spirit of its people remained unbroken. With Alpha\'s guidance, they began the slow process of rebuilding, piece by piece, brick by brick. Mariama, now a young woman, worked alongside her father, inspired by his unwavering determination and boundless love.\n\nAlpha\'s legacy of protection, strength, and hope lived on in Mariama and in the hearts of all those who had witnessed his courage. The village of Makeni, once torn apart by war, began to flourish once more, a testament to the enduring power of love and the indomitable spirit of its people.\n','c46f79b2-5f36-4f16-b3cc-c54971aa30d5',NULL,'8dc042e8-5a92-4bb9-bbb0-02b489eb1ae8','2024-07-31 08:32:54','2024-07-31 08:32:54'),('okay let\'s play the game','[{\"content\":\"<br />\"},{\"content\":\"play the game\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle ui-sortable-handle\\\" style=\\\"display: none;\\\">⇅</span>\"},{\"content\":\"<br />\"},{\"content\":\"<span class=\\\"handle ui-sortable-handle\\\" style=\\\"display: none;\\\">⇅</span>\"}]','f9231354-5fb8-4243-8e14-34add2d3d4c2','storyafrika.png','b52c978e-27ae-4739-bf09-41aaf3c81de3','2024-07-31 08:49:47','2024-07-31 08:49:47');
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
INSERT INTO `story_topic_association` VALUES ('8dc042e8-5a92-4bb9-bbb0-02b489eb1ae8','4b12fd08-7206-41eb-90c5-b8caae7d4490'),('386c6967-a0b0-4356-981e-dfeb7786fc77','6795c647-53ed-414e-a7aa-2f5270167913');
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
INSERT INTO `topics` VALUES ('Love','Love is patient and kind. It does not Jealous','4b12fd08-7206-41eb-90c5-b8caae7d4490','2024-07-31 08:32:54','2024-07-31 08:32:54'),('Business','Business focus on afrika','6795c647-53ed-414e-a7aa-2f5270167913','2024-07-31 08:32:54','2024-07-31 08:32:54'),('Education','Education is transformative','dad364b3-a90b-4427-924e-fd3fbd1e8dcd','2024-07-31 08:32:54','2024-07-31 08:32:54');
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
INSERT INTO `users` VALUES ('user','user@gmail.com','scrypt:32768:8:1$2gUBUwSNuwUaekPS$8fba13b19df0ad0ff89d045f815b7867123b5960a742dfee7fd2f521852fd4221add27090eddf4c4cfa770c3d5ab0d07c8907f641adfe50a3f0c1de7c0eea36d',NULL,NULL,NULL,NULL,NULL,'6883ad58-f6c5-4bb9-9e7b-656bf9e8b7d3.webp','237dce09-07d0-4c6f-9d36-bd9dc369bd82','2024-08-03 18:48:12','2024-08-03 18:48:12'),('david','david@gmail.com','scrypt:32768:8:1$zjZB2Xrvr6VmbVe6$bbab7ed99babb83ab8642a67d07508f8ffda80d9717edd6ed2fb75da662f7b045449c4fb50d795c166f12d557253d2bc5837f119e1b2020c03dd7a7faf4d3f3d','Software Engineer','I\"m a software engineer with two decades of experience',NULL,NULL,NULL,NULL,'50b9953f-7fa9-4812-8c44-7fd34ad6f2b8','2024-07-31 08:32:54','2024-07-31 08:32:54'),('paul','paul@gmail.com','scrypt:32768:8:1$QDvh1lnHGlrM577j$7e9e4def539f9229855664ef1611006c0561fab93ee785dd79ad7f4ba59ba4d0163a80da6edbe12b019feec2a211520d753cfcd423591e359d73be318e1f67be','Enterpreneur | Business man','I like to share the struggles I\"m personally face in the business industry',NULL,NULL,NULL,NULL,'929da5f1-d99c-474c-beb1-a6cab20ab263','2024-07-31 08:32:54','2024-07-31 08:32:54'),('alusine','alusine@gmail.com','scrypt:32768:8:1$3n0rwJIB6tUyBLZU$8d869e15be233d41f347c03c964c7a6f2af29dfe4d535b5b2aed3f003edce09a8b9a8602b3abfae10eefd77228197737b5005642451617492b6da4bf43ba0767','Teacher | Educator','I like to share how education have transformEducation have transform the lives of my student',NULL,NULL,NULL,NULL,'c46f79b2-5f36-4f16-b3cc-c54971aa30d5','2024-07-31 08:32:54','2024-07-31 08:32:54'),('alikodangote','alikodangote@gmail.com','scrypt:32768:8:1$7v0WgayubypYTB3T$c94e2c2fba56e7d132c414eac226c1728b0eeaec6b1bd4f28d9ac2cda6f86430a3a1c2202207514cc76ca122904ab686d995ab33b6f09932cbf58d77dcb18107','Enterpreneur | Successful Business man',NULL,NULL,NULL,NULL,'hassan001.png','f9231354-5fb8-4243-8e14-34add2d3d4c2','2024-07-31 08:32:54','2024-07-31 08:32:54');
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

-- Dump completed on 2024-08-03 23:30:33
