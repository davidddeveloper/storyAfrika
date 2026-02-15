'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import Button from '@/components/ui/Button';

export default function HomePage() {
  return (
    <>
      <Header />
      <main>
        {/* Hero Section */}
        <section className="relative min-h-screen flex items-center justify-center px-4 overflow-hidden">
          {/* Background Pattern - Subtle */}
          <div className="absolute inset-0 -z-10">
            <div className="absolute top-20 left-10 w-72 h-72 bg-accent/5 rounded-full blur-3xl" />
            <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent/5 rounded-full blur-3xl" />
          </div>

          <div className="container mx-auto max-w-5xl text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
            >
              {/* Badge */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="inline-flex items-center px-3 py-1 rounded-full border border-border bg-card mb-8"
              >
                <span className="text-sm text-muted-foreground">
                  Preserving Cultural Heritage
                </span>
              </motion.div>

              {/* Main Headline */}
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-foreground mb-6 tracking-tight leading-tight">
                Stories That
                <br />
                <span className="text-accent">Shape Africa</span>
              </h1>

              {/* Subtitle */}
              <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
                Discover, preserve, and share African stories, folklore, and cultural heritage.
                A digital archive for future generations.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
                <Link href="/stories">
                  <Button size="lg" className="min-w-[160px]">
                    Explore Stories
                  </Button>
                </Link>
                <Link href="/apply">
                  <Button size="lg" variant="outline" className="min-w-[160px]">
                    Become a Writer
                  </Button>
                </Link>
              </div>

              {/* Stats */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
                className="flex flex-wrap items-center justify-center gap-8 text-sm text-muted-foreground"
              >
                <div className="flex items-center space-x-2">
                  <span className="text-2xl font-bold text-foreground">500+</span>
                  <span>Stories</span>
                </div>
                <div className="w-px h-4 bg-border" />
                <div className="flex items-center space-x-2">
                  <span className="text-2xl font-bold text-foreground">50+</span>
                  <span>Countries</span>
                </div>
                <div className="w-px h-4 bg-border" />
                <div className="flex items-center space-x-2">
                  <span className="text-2xl font-bold text-foreground">100+</span>
                  <span>Contributors</span>
                </div>
              </motion.div>
            </motion.div>
          </div>

          {/* Scroll Indicator */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, repeat: Infinity, duration: 1.5 }}
            className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
          >
            <div className="w-6 h-10 border-2 border-muted-foreground rounded-full flex items-start justify-center p-2">
              <motion.div
                animate={{ y: [0, 12, 0] }}
                transition={{ repeat: Infinity, duration: 1.5 }}
                className="w-1.5 h-1.5 bg-muted-foreground rounded-full"
              />
            </div>
          </motion.div>
        </section>

        {/* Featured Stories Section */}
        <section className="py-24 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
                Featured Stories
              </h2>
              <p className="text-lg text-muted-foreground">
                Handpicked stories from across the continent, carefully curated to bring you the
                best of African storytelling.
              </p>
            </div>

            {/* Placeholder for stories - will be populated with real data */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="p-6 rounded-lg border border-border bg-card hover:shadow-md transition-all duration-300"
                >
                  <div className="flex items-center space-x-2 mb-3">
                    <div className="h-5 w-20 bg-accent/10 rounded skeleton" />
                    <div className="h-4 w-16 bg-gray-200 rounded skeleton" />
                  </div>
                  <div className="h-6 w-full bg-gray-200 rounded mb-2 skeleton" />
                  <div className="h-6 w-2/3 bg-gray-200 rounded mb-4 skeleton" />
                  <div className="space-y-2 mb-4">
                    <div className="h-4 w-full bg-gray-200 rounded skeleton" />
                    <div className="h-4 w-full bg-gray-200 rounded skeleton" />
                    <div className="h-4 w-3/4 bg-gray-200 rounded skeleton" />
                  </div>
                </div>
              ))}
            </div>

            <div className="text-center mt-12">
              <Link href="/stories">
                <Button variant="outline" size="lg">
                  View All Stories
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Countries Section */}
        <section className="py-24 bg-background">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
                Explore by Country
              </h2>
              <p className="text-lg text-muted-foreground">
                Dive into stories from different African nations, each with its unique cultural heritage.
              </p>
            </div>

            {/* Country Grid - Placeholder */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 max-w-5xl mx-auto">
              {['Nigeria', 'Kenya', 'Ghana', 'South Africa', 'Ethiopia', 'Egypt', 'Morocco', 'Tanzania', 'Uganda', 'Senegal'].map((country) => (
                <Link
                  key={country}
                  href={`/countries/${country.toLowerCase()}`}
                  className="p-6 rounded-lg border border-border bg-card hover:shadow-md hover:border-accent transition-all duration-300 text-center group"
                >
                  <p className="font-medium text-foreground group-hover:text-accent transition-colors">
                    {country}
                  </p>
                </Link>
              ))}
            </div>

            <div className="text-center mt-12">
              <Link href="/countries">
                <Button variant="outline" size="lg">
                  View All Countries
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
                Become a Storyteller
              </h2>
              <p className="text-lg text-muted-foreground mb-8">
                Share your stories, preserve your culture, and contribute to Africa's digital heritage.
              </p>
              <Link href="/apply">
                <Button size="lg">
                  Apply to Write
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
