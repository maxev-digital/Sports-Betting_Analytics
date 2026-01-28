import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import fs from 'fs';
import path from 'path';

const SETTINGS_PATH = path.join(process.cwd(), 'data', 'revenue-settings.json');

interface YouTubeConnection {
  channelId: string;
  channelName: string;
  refreshToken: string;
  connected: boolean;
  studioId?: string;
}

interface RevenueSettings {
  stripeAccounts: any[];
  youtubeConnections: YouTubeConnection[];
}

function loadSettings(): RevenueSettings {
  try {
    if (!fs.existsSync(SETTINGS_PATH)) {
      return { stripeAccounts: [], youtubeConnections: [] };
    }
    const data = fs.readFileSync(SETTINGS_PATH, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('[Investor Revenue] Failed to load settings:', error);
    return { stripeAccounts: [], youtubeConnections: [] };
  }
}

/**
 * Extract YouTube revenue for a specific studio/product
 */
function getYouTubeRevenueForStudio(
  studioId: string,
  youtubeRevenueData: any
): number {
  if (!youtubeRevenueData.success || !youtubeRevenueData.byChannel) {
    return 0;
  }

  // Load settings to get channel-to-studio mapping
  const settings = loadSettings();
  const connection = settings.youtubeConnections.find(
    (conn) => conn.studioId === studioId && conn.connected
  );

  if (!connection) {
    return 0;
  }

  // Get revenue for this channel
  const channelData = youtubeRevenueData.byChannel[connection.channelId];
  return channelData?.revenue || 0;
}

export async function GET() {
  try {
    const BASE_URL = process.env.NEXTAUTH_URL || 'https://max-media-studio.com';

    // Fetch revenue data for different time periods (Stripe + YouTube)
    const [stripeMTD, stripeYTD, stripeAllTime, youtubeMTD, youtubeYTD, youtubeAllTime, channelsResponse] = await Promise.all([
      fetch(`${BASE_URL}/api/revenue/stripe?period=mtd`).then(r => r.json()),
      fetch(`${BASE_URL}/api/revenue/stripe?period=ytd`).then(r => r.json()),
      fetch(`${BASE_URL}/api/revenue/stripe?period=all`).then(r => r.json()),
      fetch(`${BASE_URL}/api/revenue/youtube?period=mtd`).then(r => r.json()),
      fetch(`${BASE_URL}/api/revenue/youtube?period=ytd`).then(r => r.json()),
      fetch(`${BASE_URL}/api/revenue/youtube?period=all`).then(r => r.json()),
      fetch(`${BASE_URL}/api/investor/channels`),
    ]);

    const channelsData = await channelsResponse.json();

    console.log('[Investor Revenue] YouTube Revenue - MRR:', youtubeMTD.grandTotal, 'YTD:', youtubeYTD.grandTotal, 'All Time:', youtubeAllTime.grandTotal);

    // Revenue products
    const revenue = [];
    const metrics = [];

    // Get revenue by product from Stripe API
    // Detection logic automatically classifies charges by product metadata/name
    // Sports charges (with "Starter" product) → MAX EV Sports
    // Charges without product data → APW (fallback for shared account)

    // APW Revenue by period
    const apwStripeMRR = stripeMTD.byNiche?.['advantage-player-workshop']?.total || 0;
    const apwStripeYTD = stripeYTD.byNiche?.['advantage-player-workshop']?.total || 0;
    const apwStripeAllTime = stripeAllTime.byNiche?.['advantage-player-workshop']?.total || 0;

    // APW YouTube Revenue by period
    const apwYoutubeMRR = getYouTubeRevenueForStudio('apw', youtubeMTD);
    const apwYoutubeYTD = getYouTubeRevenueForStudio('apw', youtubeYTD);
    const apwYoutubeAllTime = getYouTubeRevenueForStudio('apw', youtubeAllTime);

    // MAX EV Sports Revenue by period
    const maxevStripeMRR = stripeMTD.byNiche?.['max-ev-sports']?.total || 0;
    const maxevStripeYTD = stripeYTD.byNiche?.['max-ev-sports']?.total || 0;
    const maxevStripeAllTime = stripeAllTime.byNiche?.['max-ev-sports']?.total || 0;

    // MAX EV Sports YouTube Revenue by period
    const maxevYoutubeMRR = getYouTubeRevenueForStudio('max-ev-studio', youtubeMTD);
    const maxevYoutubeYTD = getYouTubeRevenueForStudio('max-ev-studio', youtubeYTD);
    const maxevYoutubeAllTime = getYouTubeRevenueForStudio('max-ev-studio', youtubeAllTime);

    // MAX Media Studio Revenue by period
    const maxStudioMRR = stripeMTD.byNiche?.['max-media-studio']?.total || 0;
    const maxStudioYTD = stripeYTD.byNiche?.['max-media-studio']?.total || 0;
    const maxStudioAllTime = stripeAllTime.byNiche?.['max-media-studio']?.total || 0;

    console.log(`[Investor Revenue] APW Stripe - MRR: $${apwStripeMRR}, YTD: $${apwStripeYTD}, All Time: $${apwStripeAllTime}`);
    console.log(`[Investor Revenue] APW YouTube - MRR: $${apwYoutubeMRR}, YTD: $${apwYoutubeYTD}, All Time: $${apwYoutubeAllTime}`);
    console.log(`[Investor Revenue] APW Combined - MRR: $${apwStripeMRR + apwYoutubeMRR}, YTD: $${apwStripeYTD + apwYoutubeYTD}, All Time: $${apwStripeAllTime + apwYoutubeAllTime}`);

    const apwChannel = channelsData.channels?.find((c: any) => c.id === 'apw') || {};

    revenue.push({
      id: 'apw',
      name: 'Advantage Player Workshop',
      youtubeRevenue: apwYoutubeMRR, // YouTube AdSense (current month)
      websiteRevenue: apwStripeMRR, // Stripe revenue (current month)
      mrr: apwStripeMRR + apwYoutubeMRR, // Combined MRR
      ytd: apwStripeYTD + apwYoutubeYTD, // Combined YTD
      allTime: apwStripeAllTime + apwYoutubeAllTime, // Combined all-time
      monthlyCost: 75, // Top 5 channel cost
      totalPnL: (apwStripeAllTime + apwYoutubeAllTime) - 75, // P&L based on combined all-time
      roi: (apwStripeAllTime + apwYoutubeAllTime) > 0 ? (((apwStripeAllTime + apwYoutubeAllTime) - 75) / 75) * 100 : 0,
    });

    metrics.push({
      id: 'apw',
      name: 'Advantage Player Workshop',
      ytSubscribers: apwChannel.subscribers || 9150,
      ytMembers: 0, // TODO: Get from YouTube membership API
      websiteVisits: 0, // TODO: Connect Google Analytics
      emailSubscribers: 0, // TODO: Connect Brevo/email platform
      totalEmailList: 0,
    });

    // MAX EV Sports Product
    revenue.push({
      id: 'max-ev-sports',
      name: 'MAX EV Sports',
      youtubeRevenue: maxevYoutubeMRR, // YouTube AdSense (current month)
      websiteRevenue: maxevStripeMRR, // Stripe revenue (current month)
      mrr: maxevStripeMRR + maxevYoutubeMRR, // Combined MRR
      ytd: maxevStripeYTD + maxevYoutubeYTD, // Combined YTD
      allTime: maxevStripeAllTime + maxevYoutubeAllTime, // Combined all-time
      monthlyCost: 75, // Top 5 channel cost
      totalPnL: (maxevStripeAllTime + maxevYoutubeAllTime) - 75,
      roi: (maxevStripeAllTime + maxevYoutubeAllTime) > 0 ? (((maxevStripeAllTime + maxevYoutubeAllTime) - 75) / 75) * 100 : 0,
    });

    const maxevChannel = channelsData.channels?.find((c: any) => c.id === 'max-ev-studio') || {};
    metrics.push({
      id: 'max-ev-sports',
      name: 'MAX EV Sports',
      ytSubscribers: maxevChannel.subscribers || 50,
      ytMembers: 0,
      websiteVisits: 0,
      emailSubscribers: 0,
      totalEmailList: 0,
    });

    // MAX Media Studio (the platform itself)
    revenue.push({
      id: 'max-media-studio',
      name: 'MAX Media Studio Platform',
      youtubeRevenue: 0,
      websiteRevenue: maxStudioMRR, // Current month Stripe revenue
      mrr: maxStudioMRR, // Monthly Recurring Revenue (current month)
      ytd: maxStudioYTD, // Year to Date
      allTime: maxStudioAllTime, // All time revenue
      monthlyCost: 75, // Top 5 channel cost
      totalPnL: maxStudioAllTime - 75,
      roi: maxStudioAllTime > 0 ? ((maxStudioAllTime - 75) / 75) * 100 : 0,
    });

    const users = await prisma.user.findMany({ select: { id: true } });
    metrics.push({
      id: 'max-media-studio',
      name: 'MAX Media Studio Platform',
      ytSubscribers: 0, // Platform doesn't have YT channel
      ytMembers: 0,
      websiteVisits: 0,
      emailSubscribers: 0,
      totalEmailList: users.length, // Platform users
    });

    // Vegas Player News (Top 5 channel #4)
    revenue.push({
      id: 'vegas-player-news',
      name: 'Vegas Player News',
      youtubeRevenue: 0,
      websiteRevenue: 0, // TODO: Connect Vegas Player Stripe when available
      mrr: 0,
      ytd: 0,
      allTime: 0,
      monthlyCost: 75, // Top 5 channel cost
      totalPnL: -75,
      roi: 0,
    });

    const vpnChannel = channelsData.channels?.find((c: any) => c.name.includes('Vegas')) || {};
    metrics.push({
      id: 'vegas-player-news',
      name: 'Vegas Player News',
      ytSubscribers: vpnChannel.subscribers || 0,
      ytMembers: 0,
      websiteVisits: 0, // TODO: Google Analytics
      emailSubscribers: 0, // TODO: Brevo
      totalEmailList: 0,
    });

    // All other YouTube channels (no revenue yet, but show them in the list)
    const allChannels = [
      { id: 'alpha-trader-news', name: 'Alpha Trader News', cost: 75 }, // Top 5 channel #5
      { id: 'travel-deals-daily', name: 'Travel Deals Daily', cost: 0 },
      { id: 'flavor-digest-daily', name: 'Flavor Digest Daily', cost: 0 },
      { id: 'daily-fit-digest', name: 'Daily Fit Digest', cost: 0 },
      { id: 'tech-wire-daily', name: 'Tech Wire Daily', cost: 0 },
      { id: 'roast-wire-daily', name: 'Roast Wire Daily', cost: 0 },
      { id: 'scorched-onion', name: 'The Scorched Onion', cost: 0 },
      { id: 'austin-studio', name: 'Austin Studio', cost: 0 },
      { id: 'miami-studio', name: 'Miami Studio', cost: 0 },
      { id: 'nashville-studio', name: 'Nashville Studio', cost: 0 },
      { id: 'nyc-studio', name: 'NYC Studio', cost: 0 },
      { id: 'golf-studio', name: 'Golf Studio', cost: 0 },
      { id: 'auto-studio', name: 'Auto Studio', cost: 0 },
      { id: 'vpn-reviews', name: 'VPN Reviews', cost: 0 },
      { id: 'queen-rook-cafe', name: 'Queen & Rook Gaming Cafe', cost: 0 },
      { id: 'daily-gamer-live', name: 'The Daily Gamer Live', cost: 0 },
      { id: 'flow-state-coder', name: 'Flow State Coder', cost: 0 },
    ];

    for (const channel of allChannels) {
      revenue.push({
        id: channel.id,
        name: channel.name,
        youtubeRevenue: 0,
        websiteRevenue: 0,
        mrr: 0,
        ytd: 0,
        allTime: 0,
        monthlyCost: channel.cost,
        totalPnL: -channel.cost,
        roi: 0,
      });

      const channelData = channelsData.channels?.find((c: any) =>
        c.id === channel.id || c.name.toLowerCase().includes(channel.name.toLowerCase().split(' ')[0])
      ) || {};

      metrics.push({
        id: channel.id,
        name: channel.name,
        ytSubscribers: channelData.subscribers || 0,
        ytMembers: 0,
        websiteVisits: 0,
        emailSubscribers: 0,
        totalEmailList: 0,
      });
    }

    // Calculate totals
    const totals = {
      totalYoutubeRevenue: revenue.reduce((sum, p) => sum + p.youtubeRevenue, 0),
      totalWebsiteRevenue: revenue.reduce((sum, p) => sum + p.websiteRevenue, 0),
      totalMRR: revenue.reduce((sum, p) => sum + p.mrr, 0),
      totalYTD: revenue.reduce((sum, p) => sum + p.ytd, 0),
      totalAllTime: revenue.reduce((sum, p) => sum + p.allTime, 0),
      totalMonthlyCost: revenue.reduce((sum, p) => sum + p.monthlyCost, 0),
      totalPnL: revenue.reduce((sum, p) => sum + p.totalPnL, 0),
      avgROI: revenue.length > 0 ? revenue.reduce((sum, p) => sum + p.roi, 0) / revenue.length : 0,
    };

    const metricTotals = {
      totalYTSubscribers: metrics.reduce((sum, p) => sum + p.ytSubscribers, 0),
      totalYTMembers: metrics.reduce((sum, p) => sum + p.ytMembers, 0),
      totalWebsiteVisits: metrics.reduce((sum, p) => sum + p.websiteVisits, 0),
      totalEmailSubscribers: metrics.reduce((sum, p) => sum + p.emailSubscribers, 0),
      totalEmailList: metrics.reduce((sum, p) => sum + p.totalEmailList, 0),
    };

    return NextResponse.json({
      revenue,
      metrics,
      totals,
      metricTotals,
    });
  } catch (error) {
    console.error('[Investor Revenue API] Error:', error);

    // Fallback to empty data if real data fails
    return NextResponse.json({
      revenue: [],
      metrics: [],
      totals: {
        totalYoutubeRevenue: 0,
        totalWebsiteRevenue: 0,
        totalMRR: 0,
        totalYTD: 0,
        totalAllTime: 0,
        totalMonthlyCost: 0,
        totalPnL: 0,
        avgROI: 0,
      },
      metricTotals: {
        totalYTSubscribers: 0,
        totalYTMembers: 0,
        totalWebsiteVisits: 0,
        totalEmailSubscribers: 0,
        totalEmailList: 0,
      },
      error: 'Using fallback data - check API connections',
    });
  }
}
