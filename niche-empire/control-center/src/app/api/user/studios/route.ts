import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/auth';
import prisma from '@/lib/db';
import { randomUUID } from 'crypto';

// Niche-specific colors for visual consistency
const nicheColors: Record<string, string> = {
  'crypto': '#10b981',
  'max-ev': '#ef4444',
  'apw': '#dc2626',
  'foodie': '#f59e0b',
  'travel': '#3b82f6',
  'fitness': '#22c55e',
  'tech': '#6366f1',
  'daily-gamer-live': '#8b5cf6',
  'flow-state-coder': '#a855f7',
  'roast-wire': '#ef4444',
  'scorched-onion': '#f97316',
  'queen-rook': '#78716c',
  'austin': '#fb923c',
  'miami': '#14b8a6',
  'nashville': '#eab308',
  'nyc': '#60a5fa',
};

// GET: List user's studios
export async function GET() {
  try {
    const session = await auth();

    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const studios = await prisma.studio.findMany({
      where: {
        userId: session.user.id,
      },
      orderBy: {
        createdAt: 'desc',
      },
      include: {
        videoTypes: true,
      },
    });

    return NextResponse.json({
      studios,
      count: studios.length,
    });
  } catch (error) {
    console.error('Failed to fetch studios:', error);
    return NextResponse.json(
      { error: 'Failed to fetch studios', details: String(error) },
      { status: 500 }
    );
  }
}

// POST: Create a new studio
export async function POST(request: NextRequest) {
  try {
    const session = await auth();

    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const body = await request.json();
    const { nicheId, name, description, youtubeHandle, color } = body;

    // Validate required fields
    if (!nicheId || !name) {
      return NextResponse.json(
        { error: 'Niche and name are required' },
        { status: 400 }
      );
    }

    // Check if user already has a studio with this niche
    const existingStudio = await prisma.studio.findFirst({
      where: {
        userId: session.user.id,
        nicheId: nicheId,
      },
    });

    if (existingStudio) {
      return NextResponse.json(
        { error: 'You already have a studio for this niche' },
        { status: 409 }
      );
    }

    // Generate a unique studio ID
    const studioId = `${nicheId}-${randomUUID().substring(0, 8)}`;

    // Create the studio
    const studio = await prisma.studio.create({
      data: {
        id: studioId,
        userId: session.user.id,
        name: name.trim(),
        nicheId: nicheId,
        description: description?.trim() || null,
        color: color || nicheColors[nicheId] || '#dc2626',
        youtubeHandle: youtubeHandle?.trim() || null,
      },
    });

    // Create default video types for this niche
    const defaultVideoTypes = getDefaultVideoTypes(nicheId);
    if (defaultVideoTypes.length > 0) {
      await prisma.videoType.createMany({
        data: defaultVideoTypes.map((vt, index) => ({
          id: `${studioId}-${vt.id}`,
          studioId: studio.id,
          name: vt.name,
          description: vt.description,
          duration: vt.duration,
          icon: vt.icon,
          sortOrder: index,
        })),
      });
    }

    return NextResponse.json({
      success: true,
      studio,
    });
  } catch (error) {
    console.error('Failed to create studio:', error);
    return NextResponse.json(
      { error: 'Failed to create studio', details: String(error) },
      { status: 500 }
    );
  }
}

// Helper function to get default video types for a niche
function getDefaultVideoTypes(nicheId: string) {
  const videoTypesByNiche: Record<string, Array<{ id: string; name: string; description: string; duration: string; icon: string }>> = {
    'crypto': [
      { id: 'daily-rundown', name: 'Daily Rundown', description: 'Quick market update', duration: '5-10 min', icon: '📊' },
      { id: 'deep-dive', name: 'Deep Dive', description: 'Detailed analysis', duration: '15-30 min', icon: '🔍' },
      { id: 'breaking-news', name: 'Breaking News', description: 'Time-sensitive updates', duration: '3-5 min', icon: '🚨' },
    ],
    'max-ev': [
      { id: 'daily-picks', name: 'Daily Picks', description: "Today's best bets", duration: '5-10 min', icon: '🎯' },
      { id: 'analysis', name: 'Game Analysis', description: 'Deep game breakdowns', duration: '10-15 min', icon: '📈' },
      { id: 'live-show', name: 'Live Show', description: 'Real-time betting coverage', duration: '30-60 min', icon: '🔴' },
    ],
    'foodie': [
      { id: 'restaurant-review', name: 'Restaurant Review', description: 'Local spot reviews', duration: '5-10 min', icon: '🍽️' },
      { id: 'recipe-tutorial', name: 'Recipe Tutorial', description: 'Step-by-step cooking', duration: '10-20 min', icon: '👨‍🍳' },
      { id: 'food-news', name: 'Food News', description: 'Trending food stories', duration: '3-5 min', icon: '📰' },
    ],
    'tech': [
      { id: 'review', name: 'Product Review', description: 'Gadget reviews', duration: '10-15 min', icon: '📱' },
      { id: 'news', name: 'Tech News', description: 'Industry updates', duration: '5-10 min', icon: '📰' },
      { id: 'tutorial', name: 'Tutorial', description: 'How-to guides', duration: '10-20 min', icon: '🎓' },
    ],
  };

  return videoTypesByNiche[nicheId] || [];
}
