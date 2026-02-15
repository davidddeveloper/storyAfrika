'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import Button from '@/components/ui/Button';
import GradientStoryCard from '@/components/story/GradientStoryCard';
import { storiesAPI } from '@/lib/api';
import type { Story } from '@/types';

export default function HomePage() {
  const [featuredStories, setFeaturedStories] = useState<Story[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadStories = async () => {
      try {
        const response = await storiesAPI.list({ page: 1 });
        setFeaturedStories(response.results.slice(0, 6));
      } catch (error) {
        console.error('Failed to load stories:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadStories();
  }, []);

  const gradients = ['blue', 'purple', 'orange', 'green', 'cyan', 'blue'] as const;

  return (
    <>
      <Header />
      <main className="bg-background">
        {/* Hero Section */}
        <section className="relative min-h-screen flex items-center justify-center px-4 pt-16">
          <div className="container mx-auto max-w-6xl text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              {/* Badge */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="inline-flex items-center px-4 py-1.5 rounded-full border border-border bg-surface/50 backdrop-blur-sm mb-8"
              >
                <span className="text-sm text-muted">Preserving African Stories</span>
              </motion.div>

              {/* Main Headline - Larger */}
              <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold mb-8 leading-tight">
                Stories That
                <br />
                <span className="text-gradient">Shape Africa</span>
              </h1>

              {/* Subtitle */}
              <p className="text-lg md:text-xl text-muted max-w-3xl mx-auto mb-12 leading-relaxed">
                Discover, preserve, and share African folklore, mythology, and cultural heritage.
                A digital archive for future generations.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link href="/stories">
                  <Button size="lg" className="min-w-[180px]">
                    Explore Stories
                  </Button>
                </Link>
                <Link href="/about">
                  <Button size="lg" variant="outline" className="min-w-[180px]">
                    Learn More
                  </Button>
                </Link>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Featured Stories Section */}
        <section className="py-32 px-4">
          <div className="container mx-auto">
            <div className="max-w-3xl mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-6">
                Featured Stories
              </h2>
              <p className="text-lg md:text-xl text-muted leading-relaxed">
                Handpicked narratives from across the continent, preserving the richness
                of African storytelling traditions.
              </p>
            </div>

            {/* Stories Grid with Gradient Cards */}
            {isLoading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                  <div
                    key={i}
                    className="surface-card h-[400px] skeleton"
                  />
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {featuredStories.map((story, index) => (
                  <GradientStoryCard
                    key={story.id}
                    story={story}
                    gradient={gradients[index % gradients.length]}
                    index={index}
                  />
                ))}
              </div>
            )}

            <div className="text-center mt-16">
              <Link href="/stories">
                <Button variant="outline" size="lg">
                  View All Stories
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-32 px-4 border-t border-border">
          <div className="container mx-auto max-w-5xl">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.1 }}
              >
                <div className="text-5xl md:text-6xl font-bold text-gradient mb-4">
                  500+
                </div>
                <p className="text-lg text-muted">African Stories</p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 }}
              >
                <div className="text-5xl md:text-6xl font-bold text-gradient mb-4">
                  50+
                </div>
                <p className="text-lg text-muted">Countries Represented</p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.3 }}
              >
                <div className="text-5xl md:text-6xl font-bold text-gradient mb-4">
                  100+
                </div>
                <p className="text-lg text-muted">Cultural Contributors</p>
              </motion.div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-32 px-4 border-t border-border">
          <div className="container mx-auto max-w-4xl text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Become a Storyteller
            </h2>
            <p className="text-lg md:text-xl text-muted mb-12 leading-relaxed max-w-2xl mx-auto">
              Share your stories, preserve your culture, and contribute to Africa's
              digital heritage for future generations.
            </p>
            <Link href="/apply">
              <Button size="lg" className="min-w-[200px]">
                Apply to Write
              </Button>
            </Link>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
