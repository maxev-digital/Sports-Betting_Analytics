'use client';

import { useSession } from 'next-auth/react';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';

interface Studio {
  id: string;
  name: string;
  nicheId: string;
  description: string | null;
  color: string;
  youtubeHandle: string | null;
  createdAt: string;
}

export default function DashboardPage() {
  const { data: session, status } = useSession();
  const [studios, setStudios] = useState<Studio[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (status === 'authenticated') {
      fetchStudios();
    }
  }, [status]);

  const fetchStudios = async () => {
    try {
      const response = await fetch('/api/user/studios');
      if (response.ok) {
        const data = await response.json();
        setStudios(data.studios || []);
      }
    } catch (error) {
      console.error('Failed to fetch studios:', error);
    } finally {
      setLoading(false);
    }
  };

  if (status === 'loading' || loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-red-600/30 border-t-red-600 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard">
              <Image
                src="/logos/max-media-header-logo.png"
                alt="MAX Studio"
                width={40}
                height={40}
                className="hover:scale-105 transition-transform"
              />
            </Link>
            <div>
              <h1 className="text-xl font-bold text-white">Dashboard</h1>
              <p className="text-slate-400 text-sm">Welcome back, {session?.user?.name || 'Creator'}</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link
              href="/onboarding"
              className="px-4 py-2 bg-gradient-to-r from-red-700 to-amber-600 hover:from-red-600 hover:to-amber-500 text-white font-semibold rounded-lg transition-all text-sm"
            >
              + Create Studio
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {studios.length === 0 ? (
          // Empty State
          <div className="flex flex-col items-center justify-center py-20">
            <div className="w-24 h-24 bg-slate-800 rounded-full flex items-center justify-center mb-6">
              <svg className="w-12 h-12 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">No Studios Yet</h2>
            <p className="text-slate-400 text-center max-w-md mb-6">
              Create your first studio to start generating AI-powered videos. Choose from 25+ niches or create a custom one.
            </p>
            <Link
              href="/onboarding"
              className="px-6 py-3 bg-gradient-to-r from-red-700 to-amber-600 hover:from-red-600 hover:to-amber-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-red-900/30"
            >
              Create Your First Studio
            </Link>

            {/* Quick Start Options */}
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-3xl">
              <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4 text-center">
                <div className="w-10 h-10 bg-blue-600/20 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <span className="text-xl">📺</span>
                </div>
                <h3 className="text-white font-semibold mb-1">Connect YouTube</h3>
                <p className="text-slate-400 text-sm">Link your existing channel</p>
              </div>
              <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4 text-center">
                <div className="w-10 h-10 bg-green-600/20 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <span className="text-xl">🎨</span>
                </div>
                <h3 className="text-white font-semibold mb-1">Pick a Niche</h3>
                <p className="text-slate-400 text-sm">25+ templates available</p>
              </div>
              <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4 text-center">
                <div className="w-10 h-10 bg-purple-600/20 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <span className="text-xl">🤖</span>
                </div>
                <h3 className="text-white font-semibold mb-1">Generate Content</h3>
                <p className="text-slate-400 text-sm">AI scripts & videos</p>
              </div>
            </div>
          </div>
        ) : (
          // Studios Grid
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Your Studios</h2>
              <span className="text-slate-400 text-sm">{studios.length} studio{studios.length !== 1 ? 's' : ''}</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {studios.map((studio) => (
                <Link
                  key={studio.id}
                  href={`/studio/${studio.nicheId}`}
                  className="group bg-slate-900/50 border border-slate-700/50 rounded-xl overflow-hidden hover:border-red-600/50 transition-all"
                >
                  <div
                    className="h-32 relative"
                    style={{ backgroundColor: studio.color + '20' }}
                  >
                    <div
                      className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-slate-900"
                    />
                    <div
                      className="absolute top-4 left-4 w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                      style={{ backgroundColor: studio.color }}
                    >
                      {studio.name.charAt(0).toUpperCase()}
                    </div>
                  </div>
                  <div className="p-4">
                    <h3 className="text-white font-bold mb-1 group-hover:text-red-400 transition-colors">
                      {studio.name}
                    </h3>
                    <p className="text-slate-400 text-sm line-clamp-2">
                      {studio.description || `${studio.nicheId} content studio`}
                    </p>
                    {studio.youtubeHandle && (
                      <div className="flex items-center gap-2 mt-3 text-xs text-slate-500">
                        <svg className="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z"/>
                          <path fill="white" d="M9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                        </svg>
                        {studio.youtubeHandle}
                      </div>
                    )}
                  </div>
                </Link>
              ))}

              {/* Add New Studio Card */}
              <Link
                href="/onboarding"
                className="group bg-slate-900/30 border-2 border-dashed border-slate-700/50 rounded-xl flex flex-col items-center justify-center min-h-[200px] hover:border-red-600/50 hover:bg-slate-900/50 transition-all"
              >
                <div className="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center mb-3 group-hover:bg-red-600/20 transition-colors">
                  <svg className="w-6 h-6 text-slate-400 group-hover:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </div>
                <p className="text-slate-400 font-medium group-hover:text-white transition-colors">Add New Studio</p>
              </Link>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
