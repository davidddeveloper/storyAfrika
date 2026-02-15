'use client';

import { useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import Button from '@/components/ui/Button';

export default function StoryDetailPage() {
  const params = useParams();
  const slug = params.slug;

  // Placeholder data - will be replaced with API call
  const story = {
    title: 'The Tale of Anansi the Spider',
    excerpt: 'A West African folklore about wisdom, cunning, and the power of storytelling.',
    content: `Once upon a time, in a small village nestled in the heart of West Africa, there lived a clever spider named Anansi. He was known throughout the land for his wit, his cunning, and his insatiable hunger for stories.

    ## The Quest for All Stories

    Anansi desired to own all the stories in the world. At that time, all stories belonged to Nyame, the Sky God, who kept them locked away in a golden box.

    One day, Anansi climbed up to the sky to speak with Nyame. "Great Sky God," said Anansi, "I wish to buy all your stories."

    Nyame laughed at the small spider. "Many have tried to buy my stories, but the price is too high. You must bring me:
    - Onini, the python who swallows men whole
    - Osebo, the leopard with teeth like spears
    - The Mmoboro hornets
    - Mmoatia, the invisible fairy

    Only then will the stories be yours."

    ## The Clever Solutions

    Anansi returned home, determined to complete the seemingly impossible tasks. Using his wit and cunning, he devised clever plans to capture each creature.

    For the python, he tricked it into measuring itself against a long branch. For the leopard, he dug a pit and covered it with branches. The hornets, he trapped in a gourd, and the fairy, he caught with a wooden doll covered in sticky gum.

    ## The Reward

    When Anansi presented all four to Nyame, the Sky God was amazed. True to his word, Nyame gave Anansi the golden box containing all the stories of the world.

    From that day forward, all stories were known as "Spider Stories" - Anansi Stories.

    And so, whenever you hear a tale that makes you laugh, or teaches you wisdom, or stirs your imagination, you are hearing an Anansi story - proof that cleverness and determination can achieve the impossible.`,
    author: {
      full_name: 'Kwame Mensah',
      biography: 'Cultural storyteller and folklore collector from Ghana.',
    },
    category: {
      name: 'Folklore',
    },
    country: {
      name: 'Ghana',
    },
    era: {
      name: 'Traditional',
    },
    themes: [
      { name: 'Wisdom' },
      { name: 'Cunning' },
      { name: 'Determination' },
    ],
    read_time: 8,
    created_at: '2024-01-15',
  };

  return (
    <>
      <Header />
      <main className="pt-24 pb-16 min-h-screen">
        {/* Story Header */}
        <article>
          <header className="bg-background py-16 border-b border-border">
            <div className="container-narrow">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                {/* Meta */}
                <div className="flex flex-wrap items-center gap-3 mb-6">
                  <span className="inline-flex items-center px-3 py-1 rounded-md text-sm font-medium bg-accent/10 text-accent">
                    {story.category.name}
                  </span>
                  <span className="text-sm text-muted-foreground">
                    {story.country.name}
                  </span>
                  <span className="text-sm text-muted-foreground">•</span>
                  <span className="text-sm text-muted-foreground">
                    {story.read_time} min read
                  </span>
                </div>

                {/* Title */}
                <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6 leading-tight">
                  {story.title}
                </h1>

                {/* Excerpt */}
                <p className="text-xl text-muted-foreground leading-relaxed mb-8">
                  {story.excerpt}
                </p>

                {/* Author & Date */}
                <div className="flex items-center justify-between flex-wrap gap-4 pt-6 border-t border-border">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center">
                      <span className="text-lg font-medium text-accent">
                        {story.author.full_name.charAt(0)}
                      </span>
                    </div>
                    <div>
                      <p className="font-medium text-foreground">
                        {story.author.full_name}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {new Date(story.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                        })}
                      </p>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex items-center space-x-2">
                    <button
                      className="p-2 rounded-md hover:bg-gray-100 transition-colors"
                      aria-label="Bookmark"
                    >
                      <svg
                        className="w-6 h-6 text-muted-foreground"
                        fill="none"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                      </svg>
                    </button>
                    <button
                      className="p-2 rounded-md hover:bg-gray-100 transition-colors"
                      aria-label="Share"
                    >
                      <svg
                        className="w-6 h-6 text-muted-foreground"
                        fill="none"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                      </svg>
                    </button>
                  </div>
                </div>
              </motion.div>
            </div>
          </header>

          {/* Story Content */}
          <div className="bg-white py-16">
            <div className="container-narrow">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.6 }}
                className="prose mx-auto"
              >
                {/* Parse markdown content - for now showing as is */}
                {story.content.split('\n\n').map((paragraph, index) => {
                  if (paragraph.startsWith('## ')) {
                    return (
                      <h2 key={index}>{paragraph.replace('## ', '')}</h2>
                    );
                  } else if (paragraph.startsWith('- ')) {
                    const items = paragraph.split('\n');
                    return (
                      <ul key={index}>
                        {items.map((item, i) => (
                          <li key={i}>{item.replace('- ', '')}</li>
                        ))}
                      </ul>
                    );
                  } else {
                    return <p key={index}>{paragraph}</p>;
                  }
                })}
              </motion.div>
            </div>
          </div>

          {/* Story Footer */}
          <footer className="bg-background border-t border-border py-12">
            <div className="container-narrow">
              {/* Tags/Themes */}
              <div className="mb-8">
                <h3 className="text-sm font-semibold text-muted-foreground mb-3">
                  Themes
                </h3>
                <div className="flex flex-wrap gap-2">
                  {story.themes.map((theme) => (
                    <span
                      key={theme.name}
                      className="px-3 py-1 rounded-md text-sm bg-card border border-border hover:border-accent transition-colors cursor-pointer"
                    >
                      {theme.name}
                    </span>
                  ))}
                  <span className="px-3 py-1 rounded-md text-sm bg-card border border-border">
                    {story.era.name}
                  </span>
                </div>
              </div>

              {/* Author Bio */}
              <div className="p-6 rounded-lg bg-card border border-border">
                <div className="flex items-start space-x-4">
                  <div className="w-16 h-16 rounded-full bg-accent/10 flex items-center justify-center flex-shrink-0">
                    <span className="text-2xl font-medium text-accent">
                      {story.author.full_name.charAt(0)}
                    </span>
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-foreground mb-1">
                      {story.author.full_name}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {story.author.biography}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </footer>
        </article>

        {/* Related Stories */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <h2 className="text-2xl font-bold text-foreground mb-8">
              More Stories from {story.country.name}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="p-6 rounded-lg border border-border bg-card hover:shadow-md transition-all duration-300"
                >
                  <div className="h-5 w-20 bg-accent/10 rounded skeleton mb-3" />
                  <div className="h-6 w-full bg-gray-200 rounded mb-2 skeleton" />
                  <div className="h-6 w-2/3 bg-gray-200 rounded mb-4 skeleton" />
                  <div className="space-y-2">
                    <div className="h-4 w-full bg-gray-200 rounded skeleton" />
                    <div className="h-4 w-3/4 bg-gray-200 rounded skeleton" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
