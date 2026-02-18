import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

/**
 * GET - Fetch all deals
 */
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const activeOnly = searchParams.get('active');
    const city = searchParams.get('city');
    const source = searchParams.get('source');
    const category = searchParams.get('category');
    const limit = parseInt(searchParams.get('limit') || '1000', 10);

    const where: any = {};

    if (activeOnly === 'true') {
      where.is_active = true;
    } else if (activeOnly === 'false') {
      where.is_active = false;
    }

    if (city && city !== 'all') {
      where.city = city;
    }

    if (source && source !== 'all') {
      where.source_name = source;
    }

    if (category && category !== 'all') {
      where.category = category;
    }

    const deals = await prisma.deals.findMany({
      where,
      orderBy: [{ created_at: 'desc' }],
      take: limit,
    });

    return NextResponse.json({
      success: true,
      deals,
      count: deals.length,
    });
  } catch (error: any) {
    console.error('Failed to fetch deals:', error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  } finally {
    await prisma.$disconnect();
  }
}

/**
 * POST - Create new deal
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      title,
      description,
      businessName,
      category,
      discount,
      originalPrice,
      discountedPrice,
      expiresAt,
      imageUrl,
      dealUrl,
      city,
      active = true,
    } = body;

    if (!title || !businessName || !expiresAt) {
      return NextResponse.json(
        { success: false, error: 'Missing required fields: title, businessName, expiresAt' },
        { status: 400 }
      );
    }

    const deal = await prisma.deals.create({
      data: {
        title,
        description: description || null,
        business_name: businessName,
        category: category || null,
        city: city || null,
        image_url: imageUrl || null,
        discount_amount: discount || null,
        original_price: originalPrice ? parseFloat(originalPrice) : null,
        discount_price: discountedPrice ? parseFloat(discountedPrice) : null,
        expires_at: new Date(expiresAt),
        source_url: dealUrl || null,
        source_name: 'manual',
        is_active: active,
        dealType: 'manual',
      },
    });

    return NextResponse.json({
      success: true,
      deal: { id: deal.id, title: deal.title, business_name: deal.business_name },
    });
  } catch (error: any) {
    console.error('Failed to create deal:', error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  } finally {
    await prisma.$disconnect();
  }
}

/**
 * PUT - Update existing deal
 */
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      id,
      title,
      description,
      businessName,
      category,
      city,
      discount,
      originalPrice,
      discountedPrice,
      expiresAt,
      imageUrl,
      dealUrl,
      active,
    } = body;

    if (!id) {
      return NextResponse.json(
        { success: false, error: 'Deal ID is required' },
        { status: 400 }
      );
    }

    const deal = await prisma.deals.update({
      where: { id },
      data: {
        title,
        description: description || null,
        business_name: businessName || null,
        category: category || null,
        city: city || null,
        image_url: imageUrl || null,
        discount_amount: discount || null,
        original_price: originalPrice ? parseFloat(originalPrice) : null,
        discount_price: discountedPrice ? parseFloat(discountedPrice) : null,
        expires_at: expiresAt ? new Date(expiresAt) : undefined,
        source_url: dealUrl || null,
        is_active: active !== undefined ? active : undefined,
        updated_at: new Date(),
      },
    });

    return NextResponse.json({
      success: true,
      deal: { id: deal.id, title: deal.title },
    });
  } catch (error: any) {
    console.error('Failed to update deal:', error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  } finally {
    await prisma.$disconnect();
  }
}

/**
 * DELETE - Delete deal
 */
export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');

    if (!id) {
      return NextResponse.json(
        { success: false, error: 'Deal ID is required' },
        { status: 400 }
      );
    }

    await prisma.deals.delete({ where: { id } });

    return NextResponse.json({ success: true, message: 'Deal deleted' });
  } catch (error: any) {
    console.error('Failed to delete deal:', error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  } finally {
    await prisma.$disconnect();
  }
}
