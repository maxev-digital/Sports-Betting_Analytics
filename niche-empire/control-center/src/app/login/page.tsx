'use client';

import { useState, useEffect, Suspense } from 'react';
import { signIn } from 'next-auth/react';
import { useRouter, useSearchParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showRegisteredMessage, setShowRegisteredMessage] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    if (searchParams.get('registered') === 'true') {
      setShowRegisteredMessage(true);
    }
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await signIn('credentials', {
        email,
        password,
        redirect: false,
      });

      if (result?.error) {
        setError('Invalid email or password');
      } else {
        // Check for callbackUrl, otherwise go to dashboard
        const callbackUrl = searchParams.get('callbackUrl') || '/dashboard';
        router.push(callbackUrl);
        router.refresh();
      }
    } catch {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Hero Image */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-black items-center justify-center">
        {/* Background Image */}
        <Image
          src="/logos/apw-max-media-hero.png"
          alt="MAX Media"
          fill
          className="object-contain"
          priority
        />
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-black/40 via-transparent to-black"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black/50"></div>

        {/* Floating Content */}
        <div className="absolute bottom-12 left-12 right-12 z-10">
          <h2 className="text-4xl font-black text-white mb-4 drop-shadow-lg">
            AI-Powered Video Production
          </h2>
          <p className="text-lg text-slate-200 drop-shadow-md">
            Generate scripts, voiceovers, and thumbnails in minutes. Transform trending content into engaging videos.
          </p>
        </div>

        {/* Animated glow effects */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-red-600/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-48 h-48 bg-amber-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center relative overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-black">
          <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-red-600/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-1/4 left-1/4 w-80 h-80 bg-amber-600/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
          {/* Grid overlay */}
          <div
            className="absolute inset-0 opacity-[0.02]"
            style={{
              backgroundImage: 'linear-gradient(rgba(255,255,255,.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.1) 1px, transparent 1px)',
              backgroundSize: '50px 50px',
            }}
          ></div>
        </div>

        {/* Mobile Hero Banner */}
        <div className="lg:hidden absolute top-0 left-0 right-0 h-48 overflow-hidden">
          <Image
            src="/logos/apw-max-media-hero.png"
            alt="MAX Media"
            fill
            className="object-cover object-top"
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black"></div>
        </div>

        {/* Login Card */}
        <div className="w-full max-w-md p-6 relative z-10 lg:mt-0 mt-32">
          <div className="bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-3xl p-8 shadow-2xl shadow-black/50">
            {/* Logo and Branding */}
            <div className="text-center mb-8">
              <Link href="/welcome" className="inline-block">
                <Image
                  src="/logos/max-media-header-logo.png"
                  alt="MAX Media"
                  width={100}
                  height={100}
                  className="mx-auto mb-4 drop-shadow-lg hover:scale-105 transition-transform"
                  priority
                />
              </Link>
              <h1 className="text-2xl font-black text-white uppercase tracking-tight">
                MAX Studio
              </h1>
              <p className="text-slate-400 text-sm mt-1">Sign in to your dashboard</p>
            </div>

            {/* Success Message for New Registrations */}
            {showRegisteredMessage && (
              <div className="bg-green-900/30 border border-green-700/50 text-green-200 px-4 py-3 rounded-xl mb-6 text-sm flex items-center gap-2">
                <span className="w-5 h-5 bg-green-600 rounded-full flex items-center justify-center text-xs">✓</span>
                Account created! Please sign in to continue.
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="bg-red-900/30 border border-red-700/50 text-red-200 px-4 py-3 rounded-xl mb-6 text-sm flex items-center gap-2">
                <span className="w-5 h-5 bg-red-600 rounded-full flex items-center justify-center text-xs">!</span>
                {error}
              </div>
            )}

            {/* Login Form */}
            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-600/50 focus:border-red-600/50 transition-all"
                  placeholder="you@example.com"
                  required
                  autoComplete="email"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-slate-300 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-600/50 focus:border-red-600/50 transition-all"
                  placeholder="Enter your password"
                  required
                  autoComplete="current-password"
                />
              </div>

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center gap-2 text-slate-400 cursor-pointer">
                  <input type="checkbox" className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-red-600 focus:ring-red-600/50" />
                  Remember me
                </label>
                <Link href="/forgot-password" className="text-red-400 hover:text-red-300 transition-colors">
                  Forgot password?
                </Link>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 px-4 bg-gradient-to-r from-red-700 to-amber-600 hover:from-red-600 hover:to-amber-500 disabled:from-red-900 disabled:to-red-800 disabled:cursor-not-allowed text-white font-bold rounded-xl transition-all shadow-lg shadow-red-900/30 uppercase tracking-wide flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Signing in...
                  </>
                ) : (
                  'Sign In'
                )}
              </button>
            </form>

            {/* Divider */}
            <div className="flex items-center gap-4 my-6">
              <div className="flex-1 h-px bg-slate-700"></div>
              <span className="text-slate-500 text-xs uppercase">New to MAX Studio?</span>
              <div className="flex-1 h-px bg-slate-700"></div>
            </div>

            {/* Register Link */}
            <Link
              href="/register"
              className="block w-full py-3 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl transition-colors text-center border border-slate-700"
            >
              Create an Account
            </Link>

            {/* Footer */}
            <div className="mt-6 text-center">
              <Link href="/welcome" className="text-slate-500 hover:text-slate-400 text-xs transition-colors">
                ← Back to Home
              </Link>
            </div>
          </div>

          {/* Terms Footer */}
          <p className="text-center text-slate-600 text-xs mt-6">
            By signing in, you agree to our{' '}
            <Link href="/terms" className="text-slate-400 hover:text-white transition-colors">Terms</Link>
            {' '}and{' '}
            <Link href="/privacy" className="text-slate-400 hover:text-white transition-colors">Privacy Policy</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

// Loading fallback component
function LoginLoading() {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="w-12 h-12 border-4 border-red-600/30 border-t-red-600 rounded-full animate-spin"></div>
    </div>
  );
}

// Main page component with Suspense boundary for useSearchParams
export default function LoginPage() {
  return (
    <Suspense fallback={<LoginLoading />}>
      <LoginForm />
    </Suspense>
  );
}
