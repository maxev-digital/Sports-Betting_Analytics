'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // Validate password strength
    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || 'Registration failed');
        return;
      }

      setSuccess(true);
      // Redirect to login with redirect to onboarding after successful registration
      setTimeout(() => {
        router.push('/login?registered=true&callbackUrl=/onboarding');
      }, 2000);
    } catch {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Hero Image */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        {/* Background Image */}
        <Image
          src="/logos/apw-max-media-hero.png"
          alt="MAX Media"
          fill
          className="object-cover"
          priority
        />
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-black/40 via-transparent to-black"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black/50"></div>

        {/* Floating Content */}
        <div className="absolute bottom-12 left-12 right-12 z-10">
          <h2 className="text-4xl font-black text-white mb-4 drop-shadow-lg">
            Join the Creator Revolution
          </h2>
          <p className="text-lg text-slate-200 drop-shadow-md">
            25+ pre-built studios, 18+ AI voices, 101 API endpoints. Start creating professional videos in minutes.
          </p>
          <div className="flex gap-6 mt-6">
            <div className="text-center">
              <p className="text-2xl font-bold text-white">25+</p>
              <p className="text-sm text-slate-300">Studios</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-white">18+</p>
              <p className="text-sm text-slate-300">AI Voices</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-white">Free</p>
              <p className="text-sm text-slate-300">To Start</p>
            </div>
          </div>
        </div>

        {/* Animated glow effects */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-red-600/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-48 h-48 bg-amber-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* Right Side - Register Form */}
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
        <div className="lg:hidden absolute top-0 left-0 right-0 h-40 overflow-hidden">
          <Image
            src="/logos/apw-max-media-hero.png"
            alt="MAX Media"
            fill
            className="object-cover object-top"
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black"></div>
        </div>

        {/* Registration Card */}
        <div className="w-full max-w-md p-6 relative z-10 lg:mt-0 mt-28">
          <div className="bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-3xl p-8 shadow-2xl shadow-black/50">
            {/* Logo and Branding */}
            <div className="text-center mb-6">
              <Link href="/welcome" className="inline-block">
                <Image
                  src="/logos/max-media-header-logo.png"
                  alt="MAX Media"
                  width={80}
                  height={80}
                  className="mx-auto mb-3 drop-shadow-lg hover:scale-105 transition-transform"
                  priority
                />
              </Link>
              <h1 className="text-xl font-black text-white uppercase tracking-tight">
                Create Account
              </h1>
              <p className="text-slate-400 text-sm mt-1">Start creating amazing videos</p>
            </div>

            {/* Success Message */}
            {success && (
              <div className="bg-green-900/30 border border-green-700/50 text-green-200 px-4 py-3 rounded-xl mb-6 text-sm flex items-center gap-2">
                <span className="w-5 h-5 bg-green-600 rounded-full flex items-center justify-center text-xs">✓</span>
                Account created! Redirecting to login...
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="bg-red-900/30 border border-red-700/50 text-red-200 px-4 py-3 rounded-xl mb-6 text-sm flex items-center gap-2">
                <span className="w-5 h-5 bg-red-600 rounded-full flex items-center justify-center text-xs">!</span>
                {error}
              </div>
            )}

            {/* Registration Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-slate-300 mb-1.5">
                  Full Name
                </label>
                <input
                  type="text"
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-600/50 focus:border-red-600/50 transition-all text-sm"
                  placeholder="John Doe"
                  required
                  autoComplete="name"
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-1.5">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-600/50 focus:border-red-600/50 transition-all text-sm"
                  placeholder="you@example.com"
                  required
                  autoComplete="email"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-slate-300 mb-1.5">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-600/50 focus:border-red-600/50 transition-all text-sm"
                  placeholder="At least 8 characters"
                  required
                  autoComplete="new-password"
                  minLength={8}
                />
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-slate-300 mb-1.5">
                  Confirm Password
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-600/50 focus:border-red-600/50 transition-all text-sm"
                  placeholder="Confirm your password"
                  required
                  autoComplete="new-password"
                  minLength={8}
                />
              </div>

              <div className="flex items-start gap-2 text-sm text-slate-400">
                <input
                  type="checkbox"
                  id="terms"
                  required
                  className="w-4 h-4 mt-0.5 rounded border-slate-600 bg-slate-800 text-red-600 focus:ring-red-600/50"
                />
                <label htmlFor="terms" className="cursor-pointer text-xs">
                  I agree to the{' '}
                  <Link href="/terms" className="text-red-400 hover:text-red-300 transition-colors">
                    Terms of Service
                  </Link>{' '}
                  and{' '}
                  <Link href="/privacy" className="text-red-400 hover:text-red-300 transition-colors">
                    Privacy Policy
                  </Link>
                </label>
              </div>

              <button
                type="submit"
                disabled={loading || success}
                className="w-full py-3 px-4 bg-gradient-to-r from-red-700 to-amber-600 hover:from-red-600 hover:to-amber-500 disabled:from-red-900 disabled:to-red-800 disabled:cursor-not-allowed text-white font-bold rounded-xl transition-all shadow-lg shadow-red-900/30 uppercase tracking-wide flex items-center justify-center gap-2 mt-5"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Creating Account...
                  </>
                ) : (
                  'Create Account'
                )}
              </button>
            </form>

            {/* Divider */}
            <div className="flex items-center gap-4 my-5">
              <div className="flex-1 h-px bg-slate-700"></div>
              <span className="text-slate-500 text-xs uppercase">Already have an account?</span>
              <div className="flex-1 h-px bg-slate-700"></div>
            </div>

            {/* Login Link */}
            <Link
              href="/login"
              className="block w-full py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl transition-colors text-center border border-slate-700 text-sm"
            >
              Sign In Instead
            </Link>

            {/* Footer */}
            <div className="mt-5 text-center">
              <Link href="/welcome" className="text-slate-500 hover:text-slate-400 text-xs transition-colors">
                ← Back to Home
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
