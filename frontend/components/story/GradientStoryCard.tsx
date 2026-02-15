'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';

interface GradientStoryCardProps {
  story: {
    id: string;
    title: string;
    excerpt: string;
    slug: string;
    author: {
      full_name: string;
    };
    category: {
      name: string;
    };
    read_time: number;
  };
  gradient: 'blue' | 'purple' | 'orange' | 'green' | 'cyan';
  index?: number;
}

export default function GradientStoryCard({ story, gradient, index = 0 }: GradientStoryCardProps) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
    >
      <Link href={`/stories/${story.slug}`}>
        <div className={`gradient-card gradient-${gradient} cursor-pointer`}>
          <div>
            {/* Category Badge */}
            <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-white/20 backdrop-blur-sm mb-4">
              {story.category.name}
            </span>

            {/* Title */}
            <h3 className="text-2xl md:text-3xl font-bold mb-3 line-clamp-3">
              {story.title}
            </h3>

            {/* Excerpt */}
            <p className="text-white/90 text-base md:text-lg line-clamp-3 mb-6">
              {story.excerpt}
            </p>
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium">{story.author.full_name}</span>
            <span className="text-white/80">{story.read_time} min read</span>
          </div>
        </div>
      </Link>
    </motion.article>
  );
}
