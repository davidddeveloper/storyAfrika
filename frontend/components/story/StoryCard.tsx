import Link from 'next/link';
import { motion } from 'framer-motion';

interface StoryCardProps {
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
    country: {
      name: string;
    };
    read_time: number;
    created_at: string;
  };
  index?: number;
}

export default function StoryCard({ story, index = 0 }: StoryCardProps) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4 }}
      className="group"
    >
      <Link href={`/stories/${story.slug}`} className="block">
        <div className="p-6 rounded-lg border border-border bg-card hover:shadow-md transition-all duration-300">
          {/* Meta */}
          <div className="flex items-center space-x-2 mb-3">
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-accent/10 text-accent">
              {story.category.name}
            </span>
            <span className="text-xs text-muted-foreground">
              {story.country.name}
            </span>
          </div>

          {/* Title */}
          <h3 className="text-xl font-semibold text-foreground mb-2 group-hover:text-accent transition-colors line-clamp-2">
            {story.title}
          </h3>

          {/* Excerpt */}
          <p className="text-muted-foreground text-sm mb-4 line-clamp-3 leading-relaxed">
            {story.excerpt}
          </p>

          {/* Footer */}
          <div className="flex items-center justify-between pt-4 border-t border-border">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-full bg-accent/10 flex items-center justify-center">
                <span className="text-xs font-medium text-accent">
                  {story.author.full_name.charAt(0)}
                </span>
              </div>
              <span className="text-sm text-muted-foreground">
                {story.author.full_name}
              </span>
            </div>
            <span className="text-xs text-muted-foreground">
              {story.read_time} min read
            </span>
          </div>
        </div>
      </Link>
    </motion.article>
  );
}
