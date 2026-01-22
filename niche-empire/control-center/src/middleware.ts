import { auth } from '@/auth';
import { NextResponse } from 'next/server';

// Public routes that don't require authentication
const PUBLIC_ROUTES = [
  '/welcome',
  '/login',
  '/register',
  '/forgot-password',
  '/terms',
  '/privacy',
  '/contact',
  '/niches',
  '/pricing',
];

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const pathname = req.nextUrl.pathname;

  // Check if this is a public route
  const isPublicRoute = PUBLIC_ROUTES.some(route =>
    pathname === route || pathname.startsWith(`${route}/`)
  );
  const isApiRoute = pathname.startsWith('/api/');

  // Allow all API routes
  if (isApiRoute) {
    return NextResponse.next();
  }

  // Root path handling
  if (pathname === '/') {
    if (isLoggedIn) {
      // Logged in users go to their dashboard
      return NextResponse.redirect(new URL('/dashboard', req.url));
    } else {
      // Non-logged in users see welcome page
      return NextResponse.redirect(new URL('/welcome', req.url));
    }
  }

  // Allow public routes without authentication
  if (isPublicRoute) {
    // Redirect logged-in users away from login/register to dashboard
    if ((pathname === '/login' || pathname === '/register') && isLoggedIn) {
      return NextResponse.redirect(new URL('/dashboard', req.url));
    }
    return NextResponse.next();
  }

  // Redirect non-logged-in users to welcome page
  if (!isLoggedIn) {
    return NextResponse.redirect(new URL('/welcome', req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: [
    // Match all routes except static files and assets
    '/((?!_next/static|_next/image|favicon.ico|logos|niches|sportsbook.png|bellagio-backdrop.png|audio|output|images|broll|.*\\.mp4$|.*\\.webm$|.*\\.mov$).*)',
  ],
};
