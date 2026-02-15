'use client';

import { useState } from 'react';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import Button from '@/components/ui/Button';

export default function StoriesPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedCountry, setSelectedCountry] = useState('all');

  // Placeholder data
  const categories = ['All', 'Folklore', 'History', 'Mythology', 'Contemporary'];
  const countries = ['All', 'Nigeria', 'Kenya', 'Ghana', 'South Africa', 'Ethiopia'];

  return (
    <>
      <Header />
      <main className="pt-24 pb-16 min-h-screen">
        {/* Hero Section */}
        <section className="bg-background py-16">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl">
              <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
                Explore Stories
              </h1>
              <p className="text-lg text-muted-foreground">
                Discover African stories, folklore, and cultural narratives from across the continent.
              </p>
            </div>
          </div>
        </section>

        {/* Filters & Search */}
        <section className="bg-white border-b border-border py-8">
          <div className="container mx-auto px-4">
            <div className="flex flex-col lg:flex-row gap-4">
              {/* Search */}
              <div className="flex-1">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search stories..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full px-4 py-3 pl-11 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent"
                  />
                  <svg
                    className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>

              {/* Category Filter */}
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-4 py-3 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent"
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat.toLowerCase()}>
                    {cat}
                  </option>
                ))}
              </select>

              {/* Country Filter */}
              <select
                value={selectedCountry}
                onChange={(e) => setSelectedCountry(e.target.value)}
                className="px-4 py-3 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent"
              >
                {countries.map((country) => (
                  <option key={country} value={country.toLowerCase()}>
                    {country}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </section>

        {/* Stories Grid */}
        <section className="py-12">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Placeholder Stories */}
              {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => (
                <article
                  key={i}
                  className="group p-6 rounded-lg border border-border bg-card hover:shadow-md transition-all duration-300"
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
                  <div className="flex items-center justify-between pt-4 border-t border-border">
                    <div className="h-4 w-24 bg-gray-200 rounded skeleton" />
                    <div className="h-4 w-16 bg-gray-200 rounded skeleton" />
                  </div>
                </article>
              ))}
            </div>

            {/* Load More */}
            <div className="text-center mt-12">
              <Button variant="outline" size="lg">
                Load More Stories
              </Button>
            </div>

            {/* Empty State (when no stories match filters) */}
            {/* <div className="text-center py-16">
              <p className="text-lg text-muted-foreground mb-4">No stories found</p>
              <p className="text-sm text-muted-foreground">Try adjusting your filters or search query</p>
            </div> */}
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
