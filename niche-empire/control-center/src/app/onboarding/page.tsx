'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';

// Niche categories with icons
const NICHE_CATEGORIES = {
  'Finance & Betting': [
    { id: 'crypto', name: 'Crypto & Trading', icon: '📈', color: '#10b981' },
    { id: 'max-ev', name: 'Sports Betting', icon: '🏈', color: '#ef4444' },
    { id: 'apw', name: 'Advantage Play', icon: '🎰', color: '#dc2626' },
  ],
  'Lifestyle': [
    { id: 'foodie', name: 'Food & Cooking', icon: '🍳', color: '#f59e0b' },
    { id: 'travel', name: 'Travel & Deals', icon: '✈️', color: '#3b82f6' },
    { id: 'fitness', name: 'Fitness & Health', icon: '💪', color: '#22c55e' },
  ],
  'Tech & Gaming': [
    { id: 'tech', name: 'Tech Reviews', icon: '📱', color: '#6366f1' },
    { id: 'daily-gamer-live', name: 'Gaming', icon: '🎮', color: '#8b5cf6' },
    { id: 'flow-state-coder', name: 'Coding & Lo-fi', icon: '💻', color: '#a855f7' },
  ],
  'Entertainment': [
    { id: 'roast-wire', name: 'Comedy & Roasts', icon: '🔥', color: '#ef4444' },
    { id: 'scorched-onion', name: 'Satire News', icon: '📰', color: '#f97316' },
    { id: 'queen-rook', name: 'Chess', icon: '♟️', color: '#78716c' },
  ],
  'Local / City': [
    { id: 'austin', name: 'Austin, TX', icon: '🤠', color: '#fb923c' },
    { id: 'miami', name: 'Miami, FL', icon: '🌴', color: '#14b8a6' },
    { id: 'nashville', name: 'Nashville, TN', icon: '🎸', color: '#eab308' },
    { id: 'nyc', name: 'New York City', icon: '🗽', color: '#60a5fa' },
  ],
};

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [selectedNiche, setSelectedNiche] = useState<string | null>(null);
  const [studioName, setStudioName] = useState('');
  const [studioDescription, setStudioDescription] = useState('');
  const [youtubeHandle, setYoutubeHandle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCreateStudio = async () => {
    if (!selectedNiche || !studioName.trim()) {
      setError('Please select a niche and enter a studio name');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/user/studios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nicheId: selectedNiche,
          name: studioName.trim(),
          description: studioDescription.trim() || null,
          youtubeHandle: youtubeHandle.trim() || null,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to create studio');
      }

      // Redirect to the new studio
      router.push(`/studio/${selectedNiche}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create studio');
    } finally {
      setLoading(false);
    }
  };

  const getSelectedNicheInfo = () => {
    for (const niches of Object.values(NICHE_CATEGORIES)) {
      const found = niches.find(n => n.id === selectedNiche);
      if (found) return found;
    }
    return null;
  };

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-lg">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
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
              <h1 className="text-xl font-bold text-white">Create Studio</h1>
              <p className="text-slate-400 text-sm">Step {step} of 3</p>
            </div>
          </div>
          <Link
            href="/dashboard"
            className="text-slate-400 hover:text-white text-sm transition-colors"
          >
            Cancel
          </Link>
        </div>
      </header>

      {/* Progress Bar */}
      <div className="max-w-4xl mx-auto px-6 pt-6">
        <div className="flex gap-2">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`flex-1 h-1.5 rounded-full ${
                s <= step ? 'bg-red-600' : 'bg-slate-800'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-8">
        {error && (
          <div className="bg-red-900/30 border border-red-700/50 text-red-200 px-4 py-3 rounded-xl mb-6 text-sm flex items-center gap-2">
            <span className="w-5 h-5 bg-red-600 rounded-full flex items-center justify-center text-xs">!</span>
            {error}
          </div>
        )}

        {/* Step 1: Choose Niche */}
        {step === 1 && (
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">Choose Your Niche</h2>
            <p className="text-slate-400 mb-8">
              Select the category that best fits your content. You can always create more studios later.
            </p>

            <div className="space-y-8">
              {Object.entries(NICHE_CATEGORIES).map(([category, niches]) => (
                <div key={category}>
                  <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
                    {category}
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    {niches.map((niche) => (
                      <button
                        key={niche.id}
                        onClick={() => setSelectedNiche(niche.id)}
                        className={`p-4 rounded-xl border text-left transition-all ${
                          selectedNiche === niche.id
                            ? 'bg-slate-800 border-red-600'
                            : 'bg-slate-900/50 border-slate-700/50 hover:border-slate-600'
                        }`}
                      >
                        <span className="text-2xl mb-2 block">{niche.icon}</span>
                        <span className="text-white font-medium text-sm">{niche.name}</span>
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-end mt-8">
              <button
                onClick={() => selectedNiche && setStep(2)}
                disabled={!selectedNiche}
                className="px-6 py-3 bg-gradient-to-r from-red-700 to-amber-600 hover:from-red-600 hover:to-amber-500 disabled:from-slate-700 disabled:to-slate-600 disabled:cursor-not-allowed text-white font-bold rounded-xl transition-all"
              >
                Continue
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Studio Details */}
        {step === 2 && (
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">Name Your Studio</h2>
            <p className="text-slate-400 mb-8">
              Give your studio a memorable name and optional description.
            </p>

            {getSelectedNicheInfo() && (
              <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4 mb-6 flex items-center gap-4">
                <span className="text-3xl">{getSelectedNicheInfo()?.icon}</span>
                <div>
                  <p className="text-white font-medium">{getSelectedNicheInfo()?.name}</p>
                  <p className="text-slate-400 text-sm">Selected niche</p>
                </div>
                <button
                  onClick={() => setStep(1)}
                  className="ml-auto text-red-400 hover:text-red-300 text-sm"
                >
                  Change
                </button>
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label htmlFor="studioName" className="block text-sm font-medium text-slate-300 mb-2">
                  Studio Name *
                </label>
                <input
                  type="text"
                  id="studioName"
                  value={studioName}
                  onChange={(e) => setStudioName(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-600/50 focus:border-red-600/50 transition-all"
                  placeholder="e.g., My Crypto Channel"
                  maxLength={50}
                />
              </div>

              <div>
                <label htmlFor="studioDescription" className="block text-sm font-medium text-slate-300 mb-2">
                  Description (optional)
                </label>
                <textarea
                  id="studioDescription"
                  value={studioDescription}
                  onChange={(e) => setStudioDescription(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-600/50 focus:border-red-600/50 transition-all resize-none"
                  placeholder="What kind of content will you create?"
                  rows={3}
                  maxLength={200}
                />
              </div>
            </div>

            <div className="flex justify-between mt-8">
              <button
                onClick={() => setStep(1)}
                className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white font-medium rounded-xl transition-all"
              >
                Back
              </button>
              <button
                onClick={() => studioName.trim() && setStep(3)}
                disabled={!studioName.trim()}
                className="px-6 py-3 bg-gradient-to-r from-red-700 to-amber-600 hover:from-red-600 hover:to-amber-500 disabled:from-slate-700 disabled:to-slate-600 disabled:cursor-not-allowed text-white font-bold rounded-xl transition-all"
              >
                Continue
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Connect YouTube (Optional) */}
        {step === 3 && (
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">Connect YouTube (Optional)</h2>
            <p className="text-slate-400 mb-8">
              Link your YouTube channel to enable direct uploads. You can skip this and connect later.
            </p>

            <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-6 mb-6">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-red-600/20 rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-red-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z"/>
                    <path fill="white" d="M9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="text-white font-semibold mb-1">YouTube Channel Handle</h3>
                  <p className="text-slate-400 text-sm mb-4">
                    Enter your YouTube handle (e.g., @yourchannel) to link your channel.
                  </p>
                  <input
                    type="text"
                    value={youtubeHandle}
                    onChange={(e) => setYoutubeHandle(e.target.value)}
                    className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-600/50 focus:border-red-600/50 transition-all"
                    placeholder="@yourchannel"
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-between mt-8">
              <button
                onClick={() => setStep(2)}
                className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white font-medium rounded-xl transition-all"
              >
                Back
              </button>
              <div className="flex gap-3">
                <button
                  onClick={handleCreateStudio}
                  disabled={loading}
                  className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white font-medium rounded-xl transition-all"
                >
                  {loading ? 'Creating...' : 'Skip & Create Studio'}
                </button>
                <button
                  onClick={handleCreateStudio}
                  disabled={loading || !youtubeHandle.trim()}
                  className="px-6 py-3 bg-gradient-to-r from-red-700 to-amber-600 hover:from-red-600 hover:to-amber-500 disabled:from-slate-700 disabled:to-slate-600 disabled:cursor-not-allowed text-white font-bold rounded-xl transition-all"
                >
                  {loading ? 'Creating...' : 'Create Studio'}
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
