"""
Django management command to seed demo data for StoryAfrika.
Run with: python manage.py seed_demo_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from stories.models import Story
from taxonomy.models import Country, Category, Theme, Era
from editorial.models import FeaturedStory, ContentGuideline

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with demo African stories and related data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting demo data seed...'))

        # Create demo users
        users = self.create_users()

        # Create taxonomy
        countries = self.create_countries()
        categories = self.create_categories()
        themes = self.create_themes()
        eras = self.create_eras()

        # Create stories
        stories = self.create_stories(users, countries, categories, themes, eras)

        # Feature some stories
        self.create_featured_stories(stories, users)

        # Create content guidelines
        self.create_guidelines()

        self.stdout.write(self.style.SUCCESS('✓ Demo data seeded successfully!'))
        self.stdout.write(self.style.WARNING('  To clear demo data, run: python manage.py clear_demo_data'))

    def create_users(self):
        self.stdout.write('Creating demo users...')

        users = []

        # Create writers
        writer_data = [
            {
                'email': 'kwame@storyafrika.com',
                'full_name': 'Kwame Mensah',
                'biography': 'Ghanaian storyteller and cultural historian specializing in Akan folklore and traditions.',
                'is_writer': True,
            },
            {
                'email': 'amara@storyafrika.com',
                'full_name': 'Amara Okonkwo',
                'biography': 'Nigerian writer passionate about preserving Igbo mythology and contemporary African narratives.',
                'is_writer': True,
            },
            {
                'email': 'zola@storyafrika.com',
                'full_name': 'Zola Mabaso',
                'biography': 'South African author documenting Zulu history and oral traditions.',
                'is_writer': True,
            },
            {
                'email': 'fatima@storyafrika.com',
                'full_name': 'Fatima Hassan',
                'biography': 'Egyptian writer exploring ancient North African civilizations and their modern legacy.',
                'is_writer': True,
            },
        ]

        for data in writer_data:
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'full_name': data['full_name'],
                    'biography': data['biography'],
                    'is_writer': data['is_writer'],
                }
            )
            if created:
                user.set_password('demo1234')
                user.save()
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(users)} writers'))
        return users

    def create_countries(self):
        self.stdout.write('Creating countries...')

        country_data = [
            {'name': 'Nigeria', 'description': 'Home to over 250 ethnic groups with rich oral traditions'},
            {'name': 'Ghana', 'description': 'Ancient kingdom of gold with vibrant Akan folklore'},
            {'name': 'South Africa', 'description': 'Rainbow nation with diverse cultural heritage'},
            {'name': 'Egypt', 'description': 'Ancient civilization with millennia of recorded history'},
            {'name': 'Kenya', 'description': 'East African nation with Maasai and Swahili traditions'},
            {'name': 'Ethiopia', 'description': 'Ancient kingdom with unique Christian and Islamic heritage'},
            {'name': 'Morocco', 'description': 'North African crossroads of Berber, Arab, and African cultures'},
            {'name': 'Senegal', 'description': 'West African nation with Wolof and Serer storytelling traditions'},
        ]

        countries = []
        for data in country_data:
            country, _ = Country.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            countries.append(country)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(countries)} countries'))
        return countries

    def create_categories(self):
        self.stdout.write('Creating categories...')

        category_data = [
            {'name': 'Folklore', 'description': 'Traditional tales passed down through generations'},
            {'name': 'Mythology', 'description': 'Sacred stories and creation myths'},
            {'name': 'History', 'description': 'True stories from African history'},
            {'name': 'Contemporary', 'description': 'Modern African narratives and urban legends'},
            {'name': 'Proverbs', 'description': 'Wisdom and sayings from African cultures'},
        ]

        categories = []
        for data in category_data:
            category, _ = Category.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            categories.append(category)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(categories)} categories'))
        return categories

    def create_themes(self):
        self.stdout.write('Creating themes...')

        theme_names = [
            'Wisdom', 'Courage', 'Cunning', 'Community', 'Family',
            'Justice', 'Love', 'Betrayal', 'Transformation', 'Nature',
            'Ancestors', 'Magic', 'Survival', 'Unity', 'Pride'
        ]

        themes = []
        for name in theme_names:
            theme, _ = Theme.objects.get_or_create(name=name)
            themes.append(theme)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(themes)} themes'))
        return themes

    def create_eras(self):
        self.stdout.write('Creating eras...')

        era_names = [
            'Ancient',
            'Medieval',
            'Pre-Colonial',
            'Colonial',
            'Contemporary',
            'Traditional',
        ]

        eras = []
        for name in era_names:
            era, _ = Era.objects.get_or_create(name=name)
            eras.append(era)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(eras)} eras'))
        return eras

    def create_stories(self, users, countries, categories, themes, eras):
        self.stdout.write('Creating stories...')

        stories_data = self.get_stories_data()
        stories = []

        for i, story_data in enumerate(stories_data):
            story, created = Story.objects.get_or_create(
                slug=story_data['slug'],
                defaults={
                    'title': story_data['title'],
                    'excerpt': story_data['excerpt'],
                    'content': story_data['content'],
                    'author': users[i % len(users)],
                    'category': next(c for c in categories if c.name == story_data['category']),
                    'country': next(c for c in countries if c.name == story_data['country']),
                    'era': next(e for e in eras if e.name == story_data['era']),
                    'status': 'published',
                }
            )

            if created:
                # Add themes
                theme_objs = [t for t in themes if t.name in story_data['themes']]
                story.themes.set(theme_objs)

            stories.append(story)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(stories)} stories'))
        return stories

    def create_featured_stories(self, stories, users):
        self.stdout.write('Creating featured stories...')

        # Feature the first 3 stories
        featured_count = 0
        for story in stories[:3]:
            _, created = FeaturedStory.objects.get_or_create(
                story=story,
                defaults={'featured_by': users[0]}
            )
            if created:
                featured_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Featured {featured_count} stories'))

    def create_guidelines(self):
        self.stdout.write('Creating content guidelines...')

        guideline, _ = ContentGuideline.objects.get_or_create(
            slug='writing-guidelines',
            defaults={
                'title': 'Writing Guidelines',
                'description': 'Our mission is to preserve African stories, folklore, and cultural heritage for future generations. Stories must be well-researched, authentic, and respect cultural sensitivities.',
                'good_examples': 'Traditional folklore with proper citations, well-researched historical narratives, contemporary stories rooted in African culture.',
            }
        )

        self.stdout.write(self.style.SUCCESS('  ✓ Created content guidelines'))

    def get_stories_data(self):
        """Complete African stories with full content"""
        return [
            {
                'slug': 'anansi-and-the-sky-gods-stories',
                'title': 'Anansi and the Sky God\'s Stories',
                'excerpt': 'The legendary tale of how Anansi the spider won all the stories in the world from Nyame, the Sky God.',
                'category': 'Folklore',
                'country': 'Ghana',
                'era': 'Traditional',
                'themes': ['Cunning', 'Wisdom', 'Determination'],
                'content': '''# Anansi and the Sky God's Stories

Long ago, in the time before time, all the stories in the world belonged to Nyame, the Sky God. He kept them locked away in a golden box at the highest point of the heavens, where no mortal creature could reach them.

## The Challenge

Anansi the spider, known throughout the land for his wit and cunning, desired these stories more than anything. He wanted to own them, to share them, to make them his own. So one day, he spun a thread up to the sky and climbed to Nyame's palace.

"Great Sky God," Anansi said, bowing low, "I wish to buy your stories. Name your price."

Nyame laughed, a sound like thunder rolling across the heavens. "Many have tried to buy my stories, little spider. Warriors, kings, even other gods. All have failed. But if you truly wish to try, bring me:

- Onini, the python who could swallow an elephant
- Osebo, the leopard whose teeth are like spears
- The Mmoboro hornets whose sting brings death
- And Mmoatia, the fairy whom no one can see"

Anansi bowed again and descended to earth, his mind already working on a plan.

## The Python

First, Anansi went to Onini's favorite pool. He cut a long bamboo pole and placed it beside the python's path. When Onini appeared, Anansi shook his head sadly.

"My friend," said Anansi, "my wife and I have been arguing. She says you are not as long as this bamboo pole. I say you are longer. Would you help us settle our dispute?"

Onini, who was proud of his length, readily agreed. He stretched himself alongside the pole. "See?" said Anansi, "But you're not keeping still. Let me tie you to the pole so we can measure properly."

The moment Onini was tied, Anansi carried him to the Sky God.

## The Leopard

Next, Anansi went to where Osebo the leopard prowled. He dug a deep pit on the leopard's path and covered it with branches. When night fell, Osebo fell into the trap.

In the morning, Anansi appeared at the edge of the pit. "Oh, Osebo! How did you fall in? Here, I've woven a strong web. I'll lower it down so you can climb out."

But the moment Osebo grabbed the web, Anansi pulled it tight, binding the leopard. He then carried Osebo to the Sky God.

## The Hornets

For the hornets, Anansi filled a calabash gourd with water and walked to their nest. He poured some water on the hornets and some on himself, then held a large leaf over his head.

"Foolish hornets!" he called out. "Don't you know it's raining? Come into my gourd where it's dry!"

The hornets, seeing Anansi "wet" from the "rain," flew into the gourd to escape. Anansi quickly plugged it and carried it to Nyame.

## The Fairy

Finally, Anansi carved a small wooden doll and covered it with sticky gum from a tree. He placed a bowl of mashed yams in front of it and hid nearby.

When Mmoatia the fairy appeared, attracted by the food, she saw the doll. "May I have some?" she asked politely. The doll said nothing. "I asked you a question!" Still nothing. Angry, Mmoatia slapped the doll and her hand stuck. She slapped with the other hand, kicked with her feet, even butted with her head—until she was completely stuck.

Anansi emerged and carried her to the Sky God.

## The Reward

When Anansi presented all four captives to Nyame, the Sky God was amazed. "What many powerful beings could not do, you, a small spider, have accomplished through wit and wisdom. The stories are now yours."

From that day forward, all stories were called "Spider Stories"—Anansi stories. They belonged not to the powerful, but to the clever. Not to the mighty, but to those who use their minds.

And so Anansi brought stories to the world, teaching us that wisdom and cunning are greater than strength, and that with determination, even the smallest creature can achieve the impossible.

## Moral

This tale reminds us that intelligence and creativity can overcome any obstacle. In many West African cultures, Anansi stories teach children problem-solving, wit, and the power of the mind over brute force.
'''
            },
            {
                'slug': 'the-tortoise-and-the-birds',
                'title': 'The Tortoise and the Birds',
                'excerpt': 'A Nigerian fable about greed and its consequences, featuring the clever but greedy tortoise.',
                'category': 'Folklore',
                'country': 'Nigeria',
                'era': 'Traditional',
                'themes': ['Wisdom', 'Greed', 'Justice'],
                'content': '''# The Tortoise and the Birds

In the days when animals still spoke to one another and shared the same language, there lived a tortoise named Ijapa. He was known throughout the forest for his cunning—and his insatiable greed.

## The Great Feast

One season, food became scarce on the ground. The animals grew hungry, but the birds were invited to a great feast in the sky by the Sky People. The birds began to prepare for their journey, preening their feathers and practicing their songs.

Ijapa the tortoise watched them with envious eyes. His stomach growled, and his mind schemed. "How can I get to this feast?" he wondered. He had no wings, no ability to fly, yet his greed drove him to find a way.

## The Clever Plan

Approaching the birds with false humility, Ijapa spoke: "My dear friends, I couldn't help but overhear about the feast in the sky. The Sky People are known for their wisdom, and I'm sure they would want someone eloquent to speak on behalf of all earth's creatures. I volunteer to be that speaker."

The birds, knowing Ijapa's reputation, were suspicious. But Ijapa was so persuasive, so smooth with his words, that eventually they agreed. Each bird would give him one feather so he could fly with them.

## A New Name

As they prepared to depart, Ijapa announced: "In the sky, it is customary to take a new name for special occasions. I shall be called 'All of You.'"

The birds thought this was strange but accepted it. They all took flight together, Ijapa wearing his borrowed plumage, flying toward the clouds.

## The Feast Begins

When they arrived at the Sky Kingdom, the hosts had prepared a magnificent banquet. Tables groaned under the weight of pounded yam, egusi soup, jollof rice, fried plantains, grilled fish, and countless delicacies.

As they sat down, the Sky People announced: "Welcome, our honored guests! This feast is prepared for 'All of You.'"

Ijapa immediately stood up. "Did you hear that? They said the feast is for 'All of You'—and that is my name! This feast is mine!"

## Greed's Triumph

Before the shocked birds could protest, Ijapa began eating. He ate and ate, moving from dish to dish, sampling everything, gorging himself while the birds watched in dismay and anger. The Sky People, confused by this display, could only watch as Ijapa consumed the majority of the feast.

The birds ate only the scraps that Ijapa left behind, and their anger grew with every morsel he swallowed.

## The Reckoning

When it was time to return to earth, the birds took back their feathers, one by one. Ijapa, realizing what was happening, begged them to stop.

"Please, my friends! How will I get down? I'll die from the fall!"

But the birds, remembering his greed and trickery, showed no mercy. They took every feather back.

Desperate, Ijapa called down to his wife: "Please, bring all the soft things from our house and pile them beneath me! Bring all the mattresses, pillows, and cushions!"

His wife began gathering soft items, but Parrot, who was still angry, flew down first and told her: "Your husband says to bring all the hard things from your house—all the stones, mortars, and iron pots!"

The wife, trusting Parrot, did as told.

## The Fall

When Ijapa's feathers were all gone, he plummeted from the sky. He fell and fell, the wind whistling past his ears, and crashed into the pile of hard objects below.

His shell, which had been smooth and beautiful, shattered into many pieces. Though he survived, his wife had to painstakingly glue his shell back together.

## Why Tortoise Has a Broken Shell

This is why, to this day, the tortoise's shell is not smooth but divided into many segments—a permanent reminder of the consequences of greed and deception.

## Moral

This Igbo tale teaches us that greed leads to downfall, that tricks played on others often return to harm us, and that our actions have consequences. It reminds us to be content with our portion and to treat others with fairness and respect.

In Nigerian culture, this story is often told to children to teach them about the dangers of excessive greed and the importance of community sharing.
'''
            },
            {
                'slug': 'the-girl-who-married-a-snake',
                'title': 'The Girl Who Married a Snake',
                'excerpt': 'A Zulu love story about looking beyond appearances and honoring one\'s commitments.',
                'category': 'Folklore',
                'country': 'South Africa',
                'era': 'Traditional',
                'themes': ['Love', 'Courage', 'Transformation'],
                'content': '''# The Girl Who Married a Snake

In a small Zulu village, there lived a beautiful girl named Nomkhosi. She was the daughter of the chief, and many young men came from far and wide seeking her hand in marriage. But Nomkhosi turned them all away, for she believed in waiting for true love.

## The Drought

A terrible drought came to the land. The rivers dried up, the crops withered, and the people began to suffer. The village elders consulted with the sangoma, the spiritual healer, who delivered a troubling prophecy:

"The drought will only end when the chief's daughter is given in marriage to the one who finds water."

Days passed with no rain. The young men of the village searched everywhere for water, but found none. The people grew desperate.

## The Mysterious Stranger

One evening, a stranger arrived at the village. He was tall and handsome, with smooth skin that seemed to shimmer in the moonlight. He wore elegant beaded ornaments and spoke with a voice as smooth as honey.

"I have found water," he announced to the chief. "A spring that flows pure and clear, enough for the entire village. But I ask for your daughter's hand in marriage, as the prophecy stated."

The chief was overjoyed, and Nomkhosi, seeing her people's need and feeling drawn to the stranger's kind eyes, agreed to the marriage.

## The Wedding

The wedding was celebrated with great joy. The stranger had indeed shown them a hidden spring, and water flowed again through the village. But Nomkhosi noticed something strange about her new husband—he would not eat during the day, and at night, he would disappear for hours.

On their third night together, Nomkhosi's curiosity overcame her. She pretended to sleep and watched as her husband rose. In the moonlight, she witnessed an incredible transformation: his human form melted away, revealing a great serpent, beautiful and terrible, with scales that gleamed like precious stones.

## The Truth Revealed

Nomkhosi gasped, and the serpent turned to her. In a voice filled with sorrow, he spoke:

"Now you know the truth, my wife. I am the King of Serpents, cursed to take human form only during daylight. I saved your village because I had fallen in love with you from afar, watching you by the riverside. But now that you've seen my true form, you will surely flee."

Nomkhosi's heart raced with fear, but also with something else—a deep compassion. She remembered his kindness, his gentle words, the way he had saved her people.

"My husband," she said, her voice steady, "I made a vow before my ancestors and the gods. I will not break it. Tell me your story."

## The Ancient Curse

The Serpent King told her of an ancient curse placed upon him by a jealous witch doctor whose advances he had refused. He could only break the curse if someone loved him in both his forms and stayed with him for one full year without fleeing.

Many had tried before, but all had run away in fear when they discovered the truth.

"I will stay," Nomkhosi declared. "Not out of obligation, but because I choose to see beyond appearances. You have shown me kindness. That is the true measure of a person."

## The Year of Testing

The year that followed was not easy. Nomkhosi faced ridicule from some villagers who discovered her secret. Her own family questioned her decision. But she remained steadfast.

Each night, her husband would transform into the serpent, and each night, Nomkhosi would sit with him, talking, learning about his world beneath the earth, the ancient wisdom of serpents, and the magic that flowed through the land.

She came to see that his serpent form was as beautiful as his human one, just different. His scales caught the moonlight like stars, and his eyes held depths of wisdom and kindness.

## The Breaking of the Curse

On the final night of the year, as midnight approached, a brilliant light filled their dwelling. The Serpent King's form began to change—but this time, it did not shift back to his human day-form. Instead, the curse itself shattered like broken glass.

He stood before Nomkhosi in his true form: a being of both human and serpent, able to choose his shape at will, the curse broken by the power of genuine love and acceptance.

"You stayed," he whispered, his voice filled with wonder. "You looked beyond the surface and saw who I truly am."

## The Blessing

From that day forward, the Serpent King brought prosperity to the village. He taught the people where to find water even in drought, which plants could heal, and how to live in harmony with the earth.

Nomkhosi became a wise counselor to her people, teaching them that true beauty lies not in appearances but in character, and that courage means standing by those we love even when others do not understand.

Their children were said to have special gifts—the ability to speak with animals and understand the language of the earth.

## Moral

This Zulu tale teaches us about the courage to look beyond appearances, the importance of keeping our commitments, and the transformative power of acceptance and love. It reminds us that true partnership requires seeing and accepting our partner's full self.

In Zulu culture, this story is part of a larger tradition of tales about transformation and the importance of looking beneath the surface to find true value.
'''
            },
            {
                'slug': 'osiris-and-the-gift-of-civilization',
                'title': 'Osiris and the Gift of Civilization',
                'excerpt': 'The ancient Egyptian myth of Osiris, who brought agriculture, law, and culture to humanity.',
                'category': 'Mythology',
                'country': 'Egypt',
                'era': 'Ancient',
                'themes': ['Wisdom', 'Betrayal', 'Transformation'],
                'content': '''# Osiris and the Gift of Civilization

In the beginning, when the world was young and the gods walked among mortals, Egypt was a land of chaos. The people lived as wanderers, hunting and gathering, knowing neither law nor culture. Then came Osiris, the god-king who would change everything.

## The Divine Teacher

Osiris, son of Geb (the Earth) and Nut (the Sky), was chosen by Ra, the sun god, to bring order to Egypt. Unlike other gods who ruled through fear, Osiris governed through wisdom and compassion.

He taught humanity the sacred art of agriculture. He showed them how to plant wheat and barley along the fertile banks of the Nile, how to harvest grain, and how to make bread and beer. No longer would they need to wander in search of food.

But Osiris's gifts went far beyond agriculture. He gave them:

- Laws to govern themselves fairly
- Music and art to elevate their spirits
- Religious rites to honor the gods
- The institution of marriage and family
- Architecture to build lasting monuments
- Writing to record their knowledge

Under Osiris's guidance, Egypt transformed from a scattered people into a great civilization. The people loved him, and his wife, Isis, the goddess of magic, stood beside him in all things.

## The Jealous Brother

But not everyone rejoiced in Osiris's success. His brother Set, god of chaos and the desert, burned with jealousy. Set represented everything Osiris was not—violence, disorder, and destruction.

"Why should Osiris receive all the glory?" Set brooded. "Why should the people love him while they fear me?"

Set's envy grew into hatred, and hatred into a terrible plot.

## The Treacherous Banquet

Set organized a magnificent feast, inviting Osiris and seventy-two co-conspirators. The wine flowed freely, and entertainment filled the night. Then Set unveiled his masterpiece—a beautiful chest, ornately decorated with gold and precious stones.

"This chest," Set announced, "will be a gift to whoever fits inside it perfectly."

The guests tried one by one, but none fit. Finally, Osiris, encouraged by the crowd, stepped into the chest. It fit him perfectly—for Set had secretly measured it to Osiris's exact dimensions.

The moment Osiris lay down, Set and his conspirators slammed the lid shut, nailed it closed, and sealed it with molten lead. Before Isis or any loyal gods could react, they threw the chest into the Nile.

## Isis's Quest

Heartbroken, Isis searched the length of Egypt for her husband. She cut off her hair in mourning and wandered the land, asking everyone if they had seen the chest. Finally, she learned that it had floated to the land of Byblos and become embedded in a tamarisk tree.

The king of Byblos, not knowing what the tree contained, had cut it down and made it into a pillar for his palace. Isis traveled to Byblos, befriended the queen, and eventually revealed her identity. The royal couple, amazed and honored, gave her the pillar.

Isis extracted the chest and returned to Egypt, hiding it in the papyrus marshes while she prepared the sacred rites to resurrect Osiris.

## Set's Final Betrayal

But Set, hunting in the marshes, discovered the chest. His rage knew no bounds. He tore Osiris's body apart into fourteen pieces and scattered them across Egypt, from the Delta to the cataracts of the Nile.

Once again, Isis began her search, this time with her sister Nephthys. They traveled the length of the Nile, finding each piece. Wherever they found a piece, the local people helped them, and Isis blessed those places with fertility and abundance.

## The Resurrection

Though Isis found thirteen pieces, one remained lost—taken by an oxyrhynchus fish. Using her powerful magic, Isis reconstructed Osiris, fashioning a replacement for the missing piece. With the help of Anubis, the god of embalming (who was Osiris's son), she performed the first mummification.

Through sacred rites and magical words of power, Isis brought Osiris back to life—but he could no longer remain in the world of the living. He had been transformed. Osiris descended to the Duat, the realm of the dead, where he became the Lord of the Underworld and Judge of Souls.

## The Divine Heir

Before leaving the world of the living, Osiris and Isis conceived a son: Horus. Isis hid the infant in the marshes, protecting him from Set while he grew strong. When Horus came of age, he challenged Set for the throne of Egypt.

The battle between Horus and Set raged for eighty years. They fought in every form—as men, as hippopotami, as gods of terrible power. Finally, the gods assembled and judged in favor of Horus. Set was banished to the desert, where his rage would manifest as sandstorms.

## The Eternal Role

From his throne in the Duat, Osiris took on his most important role: judge of the dead. When a soul arrived in the afterlife, Osiris would oversee the weighing of their heart against Ma'at's feather of truth. Those who had lived justly would be welcomed into paradise. Those who had been evil would be devoured by Ammit, the soul-eater.

Osiris had transformed from a god of civilization to a god of resurrection and eternal life. His journey from life to death to rebirth became the model that every Egyptian hoped to follow.

## The Promise of Resurrection

The myth of Osiris gave the Egyptian people something precious: hope. It showed them that death was not the end, that through proper preparation and righteous living, they too could achieve eternal life.

The annual flooding of the Nile, which brought life to Egypt, was seen as Osiris's blessing—the god of resurrection bringing life from death, just as crops would rise from the seemingly dead earth.

## Legacy

The cult of Osiris became one of the most important in Egyptian religion, lasting for thousands of years. His myth taught:

- The value of civilization and order over chaos
- The power of love and loyalty (as shown by Isis)
- The promise of resurrection and eternal life
- The importance of justice and moral living
- The cyclical nature of life, death, and rebirth

Osiris's gifts—agriculture, law, culture, and the hope of resurrection—formed the foundation of Egyptian civilization, one of the greatest the world has ever known.

## Moral

The story of Osiris teaches us that civilization requires constant vigilance against the forces of chaos, that love and loyalty can overcome even death, and that our actions in life echo into eternity. It reminds us that true leadership serves the people, and that from death and suffering can come transformation and new life.
'''
            },
            {
                'slug': 'the-lion-and-the-hare',
                'title': 'The Wise Hare Outsmarts the Lion',
                'excerpt': 'An Ethiopian fable about a clever hare who saves his community from a tyrannical lion using wit and wisdom.',
                'category': 'Folklore',
                'country': 'Ethiopia',
                'era': 'Traditional',
                'themes': ['Wisdom', 'Courage', 'Community'],
                'content': '''# The Wise Hare Outsmarts the Lion

In the highlands of Ethiopia, there once lived a powerful lion who ruled over all the animals. His name was Anbessa, and he was feared throughout the land—not for his justice, but for his cruelty and insatiable hunger.

## The Tyrant's Decree

One day, Anbessa gathered all the animals of the highland and made a terrible proclamation:

"From this day forward, one of you will come to me each day to be my meal. If you do not obey, I will hunt down and destroy your entire families."

The animals were horrified, but what could they do? Anbessa was the strongest among them, and his claws were sharp. So they agreed, and each day, one animal would sadly make the journey to the lion's den, never to return.

Days turned to weeks, and weeks to months. The animal population dwindled. Families mourned. And still, Anbessa demanded his daily tribute.

## The Hare's Turn

Finally, the lot fell to the hares, and a small, elderly hare named Ketetegn was chosen. The other hares wept, for Ketetegn was wise and beloved, a keeper of stories and solver of problems.

But Ketetegn did not weep. His eyes sparkled with thought.

"Do not mourn for me yet, my friends," he said. "Sometimes the smallest creature can topple the mightiest opponent, if they use the weapon that the big can never match."

"What weapon is that?" asked the young hares.

"The mind," Ketetegn replied, tapping his head.

## The Delayed Arrival

Ketetegn did not hurry to the lion's den. Instead, he took his time, pausing to eat clover, watching the clouds, and thinking carefully. By the time he arrived, the sun was setting, and Anbessa was furious.

"You dare make me wait?" roared the lion. "I should eat you slowly for this disrespect!"

Ketetegn bowed low, his body trembling—though whether from fear or suppressed laughter, who could say?

"Great King," he said, "please forgive me. I set out on time, but on the way, I encountered another lion who claimed to be the true king of this land. He even tried to eat me himself, saying that you were a false king and that he should receive the daily tribute."

## Pride and Fury

Anbessa's mane bristled with rage. Another lion? In his territory? Claiming his throne?

"Take me to this imposter immediately!" he roared. "I will tear him apart and show all the animals who the true king is!"

Ketetegn bowed again. "As you wish, great king. Follow me."

The hare led the lion across the highland, over rocks and through valleys, until they came to a deep well. The well's water was clear and still, perfectly reflecting the sky.

"He is down there, mighty king," Ketetegn said, pointing into the well. "He is hiding in his den below."

## The Final Trick

Anbessa approached the well and looked down. There, in the water's reflection, he saw a lion looking back at him—his own reflection, though he did not know it.

"There you are, imposter!" Anbessa roared.

The reflection seemed to roar back (his own echo bouncing from the well's walls).

"How dare you challenge me!" Anbessa roared louder.

The echo roared louder too.

Anbessa's rage overwhelmed his reason. With a mighty leap, he jumped into the well to attack his rival. The splash was tremendous, but when the water settled, Anbessa was gone, drowned in the deep well.

## Freedom

Ketetegn returned to the other animals and told them what had happened. Joy spread throughout the highland like wildfire. The animals were free from Anbessa's tyranny.

They celebrated for seven days and seven nights. And from that day forward, they made a new agreement: they would live as equals, with wisdom valued as highly as strength, and the small protected alongside the large.

Ketetegn the hare was honored as a hero and became an advisor to the new council of animals, where all species had a voice.

## The Moral

The animals learned that tyranny cannot last forever, that courage comes in many sizes, and that intelligence can overcome brute force. They learned to value wisdom over strength and to protect the vulnerable rather than exploiting them.

## Cultural Significance

This Ethiopian tale is often told to teach children that:
- Intelligence and wit are as valuable as physical strength
- Tyrants contain the seeds of their own destruction (Anbessa's pride led to his downfall)
- Even the smallest can contribute to the community's welfare
- Courage means acting for others, not just oneself

In Ethiopian culture, the hare is a trickster figure similar to Anansi in West African tradition—a small creature who uses intelligence to overcome larger, more powerful opponents. These stories celebrate the triumph of mind over might and encourage people to think creatively when faced with seemingly impossible challenges.

The story also reflects Ethiopian values of community cooperation and the belief that true leadership serves the people rather than exploiting them.
'''
            },
        ]
