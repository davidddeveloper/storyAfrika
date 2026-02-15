'use client';

import Link from 'next/link';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/lib/context/AuthContext';

export default function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();

  const navigation = [
    { name: 'Stories', href: '/stories' },
    { name: 'Countries', href: '/countries' },
    { name: 'Categories', href: '/categories' },
    { name: 'About', href: '/about' },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-border bg-background/80 backdrop-blur-xl">
      <nav className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2 group">
            <span className="text-xl font-bold tracking-tight text-foreground group-hover:text-accent transition-colors">
              StoryAfrika
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="px-4 py-2 text-sm font-medium text-muted hover:text-foreground rounded-lg transition-colors"
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Auth Buttons / User Menu */}
          <div className="hidden md:flex items-center space-x-3">
            {isAuthenticated && user ? (
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-surface transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-gradient-blue flex items-center justify-center">
                    <span className="text-sm font-bold text-white">
                      {user.full_name.charAt(0)}
                    </span>
                  </div>
                  <span className="text-sm font-medium text-foreground">
                    {user.full_name.split(' ')[0]}
                  </span>
                </button>

                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-56 bg-surface rounded-lg shadow-lg border border-border py-2 z-50">
                    <Link
                      href="/dashboard"
                      className="block px-4 py-2 text-sm text-foreground hover:bg-background transition-colors"
                      onClick={() => setShowUserMenu(false)}
                    >
                      Dashboard
                    </Link>
                    {user.is_writer && (
                      <Link
                        href="/dashboard/stories"
                        className="block px-4 py-2 text-sm text-foreground hover:bg-background transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        My Stories
                      </Link>
                    )}
                    <Link
                      href="/bookmarks"
                      className="block px-4 py-2 text-sm text-foreground hover:bg-background transition-colors"
                      onClick={() => setShowUserMenu(false)}
                    >
                      Bookmarks
                    </Link>
                    <div className="border-t border-border my-2" />
                    <button
                      onClick={() => {
                        setShowUserMenu(false);
                        logout();
                      }}
                      className="w-full text-left px-4 py-2 text-sm text-error hover:bg-background transition-colors"
                    >
                      Sign out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link
                  href="/login"
                  className="px-4 py-2 text-sm font-medium text-muted hover:text-foreground transition-colors"
                >
                  Log in
                </Link>
                <Link
                  href="/register"
                  className="px-5 py-2 text-sm font-medium bg-accent text-white rounded-lg hover:bg-accent-hover transition-colors"
                >
                  Sign up
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-surface transition-colors"
            aria-label="Toggle menu"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              {isMobileMenuOpen ? (
                <path d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
              className="md:hidden border-t border-border overflow-hidden"
            >
              <div className="py-4 space-y-1">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className="block px-4 py-2 text-base font-medium text-muted hover:text-foreground hover:bg-surface rounded-lg transition-colors"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {item.name}
                  </Link>
                ))}
                <div className="pt-4 mt-4 border-t border-border space-y-2">
                  {isAuthenticated && user ? (
                    <>
                      <Link
                        href="/dashboard"
                        className="block px-4 py-2 text-base font-medium text-foreground hover:bg-surface rounded-lg transition-colors"
                        onClick={() => setIsMobileMenuOpen(false)}
                      >
                        Dashboard
                      </Link>
                      <button
                        onClick={() => {
                          setIsMobileMenuOpen(false);
                          logout();
                        }}
                        className="w-full text-left px-4 py-2 text-base font-medium text-error hover:bg-surface rounded-lg transition-colors"
                      >
                        Sign out
                      </button>
                    </>
                  ) : (
                    <>
                      <Link
                        href="/login"
                        className="block px-4 py-2 text-base font-medium text-muted hover:text-foreground hover:bg-surface rounded-lg transition-colors"
                        onClick={() => setIsMobileMenuOpen(false)}
                      >
                        Log in
                      </Link>
                      <Link
                        href="/register"
                        className="block mx-4 px-4 py-2 text-base font-medium bg-accent text-white rounded-lg hover:bg-accent-hover transition-colors text-center"
                        onClick={() => setIsMobileMenuOpen(false)}
                      >
                        Sign up
                      </Link>
                    </>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>
    </header>
  );
}
