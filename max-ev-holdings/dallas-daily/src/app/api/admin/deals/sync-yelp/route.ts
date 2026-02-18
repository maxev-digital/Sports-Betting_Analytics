import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

const YELP_API_KEY = process.env.YELP_API_KEY;
const YELP_FUSION_URL = 'https://api.yelp.com/v3/businesses/search';

interface YelpBusiness {
  id: string;
  name: string;
  image_url: string;
  url: string;
  review_count: number;
  rating: number;
  categories: { alias: string; title: string }[];
  location: {
    address1: string;
    city: string;
    zip_code: string;
    state: string;
  };
  phone: string;
  price?: string;
}

const DFW_CITIES = [
  { name: 'Dallas', lat: 32.7767, lng: -96.7970 },
  { name: 'Fort Worth', lat: 32.7555, lng: -97.3308 },
  { name: 'Plano', lat: 33.0198, lng: -96.6989 },
  { name: 'Arlington', lat: 32.7357, lng: -97.1081 },
  { name: 'Irving', lat: 32.8140, lng: -96.9489 },
  { name: 'Frisco', lat: 33.1507, lng: -96.8236 },
  { name: 'McKinney', lat: 33.1976, lng: -96.6154 },
  { name: 'Richardson', lat: 32.9483, lng: -96.7299 },
  { name: 'Garland', lat: 32.9126, lng: -96.6389 },
  { name: 'Allen', lat: 33.1031, lng: -96.6705 },
  { name: 'Carrollton', lat: 32.9537, lng: -96.8903 },
  { name: 'Grand Prairie', lat: 32.7459, lng: -96.9978 },
  { name: 'Lewisville', lat: 33.0462, lng: -96.9942 },
];

const DEAL_CATEGORIES = ['restaurants', 'shopping', 'nightlife', 'active', 'beautysvc'];

async function searchYelpDeals(city: string, lat: number, lng: number) {
  if (!YELP_API_KEY) throw new Error('YELP_API_KEY not configured');

  const deals: any[] = [];

  for (const category of DEAL_CATEGORIES) {
    try {
      const params = new URLSearchParams({
        latitude: String(lat),
        longitude: String(lng),
        categories: category,
        limit: '50',
        sort_by: 'rating',
      });

      const response = await fetch(`${YELP_FUSION_URL}?${params}`, {
        headers: {
          Authorization: `Bearer ${YELP_API_KEY}`,
          Accept: 'application/json',
        },
      });

      if (!response.ok) {
        console.error(`Yelp API error for ${category} in ${city}: ${response.status} ${response.statusText}`);
        continue;
      }

      const data = await response.json();
      const businesses: YelpBusiness[] = data.businesses || [];

      for (const biz of businesses) {
        if (biz.rating >= 4.0 && biz.review_count >= 20) {
          deals.push({
            title: `Special Offer at ${biz.name}`,
            description: `Highly rated ${biz.categories[0]?.title || 'business'} in ${city}. ${biz.review_count} reviews on Yelp.`,
            business_name: biz.name,
            category: biz.categories[0]?.title || 'General',
            city,
            image_url: biz.image_url || null,
            source_url: biz.url,
            source_name: 'yelp',
            is_active: true,
            dealType: 'yelp',
            expires_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
          });
        }
      }

      // Avoid rate limiting
      await new Promise((resolve) => setTimeout(resolve, 200));
    } catch (error) {
      console.error(`Error fetching ${category} for ${city}:`, error);
    }
  }

  return deals;
}

export async function POST(request: NextRequest) {
  if (!YELP_API_KEY) {
    return NextResponse.json(
      { success: false, error: 'YELP_API_KEY not configured' },
      { status: 503 }
    );
  }

  try {
    const body = await request.json().catch(() => ({}));
    const { cities } = body;
    const citiesToSync: string[] = cities || DFW_CITIES.map((c) => c.name);

    let totalFound = 0;
    let totalSaved = 0;
    const errors: string[] = [];

    for (const cityObj of DFW_CITIES) {
      if (!citiesToSync.includes(cityObj.name)) continue;

      try {
        const deals = await searchYelpDeals(cityObj.name, cityObj.lat, cityObj.lng);
        totalFound += deals.length;

        for (const deal of deals) {
          try {
            const existing = await prisma.deals.findFirst({
              where: {
                business_name: deal.business_name,
                city: deal.city,
                source_name: 'yelp',
              },
            });

            if (!existing) {
              await prisma.deals.create({ data: deal });
              totalSaved++;
            }
          } catch (err: any) {
            console.error(`Error saving deal for ${deal.business_name}:`, err.message);
          }
        }
      } catch (err: any) {
        errors.push(`${cityObj.name}: ${err.message}`);
      }
    }

    return NextResponse.json({
      success: true,
      dealsFound: totalFound,
      dealsSaved: totalSaved,
      errors: errors.length > 0 ? errors : null,
    });
  } catch (error: any) {
    console.error('Error syncing Yelp deals:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to sync Yelp deals', details: error.message },
      { status: 500 }
    );
  } finally {
    await prisma.$disconnect();
  }
}
