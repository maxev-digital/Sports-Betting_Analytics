import NextAuth from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import bcrypt from 'bcryptjs';
import prisma from '@/lib/db';

// Fallback admin credentials (for emergency access if DB is down)
const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'admin@maxholdings.com';
const ADMIN_PASSWORD_HASH = process.env.ADMIN_PASSWORD_HASH ||
  // Default password: "maxstudio2024" - CHANGE THIS IN PRODUCTION
  '$2b$10$VytNbhHxH1h3VjVNN40ZNujZdfZhwWrn2yY3XBHujIh43mRVzIXO.';

export const { handlers, signIn, signOut, auth } = NextAuth({
  trustHost: true,
  providers: [
    Credentials({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        const email = (credentials.email as string).toLowerCase();
        const password = credentials.password as string;

        try {
          // Try to find user in database
          const user = await prisma.user.findUnique({
            where: { email },
          });

          if (user) {
            const isValid = await bcrypt.compare(password, user.passwordHash);
            if (isValid) {
              // Update last login time
              await prisma.user.update({
                where: { id: user.id },
                data: { lastLoginAt: new Date() },
              });

              return {
                id: user.id,
                email: user.email,
                name: user.name || 'User',
                role: user.role,
                plan: user.plan,
              };
            }
          }
        } catch (error) {
          console.error('Database auth error:', error);
          // Fall through to admin check if DB is unavailable
        }

        // Fallback: Check against hardcoded admin credentials
        if (email === ADMIN_EMAIL.toLowerCase()) {
          const isValid = await bcrypt.compare(password, ADMIN_PASSWORD_HASH);
          if (isValid) {
            return {
              id: 'admin-1',
              email: ADMIN_EMAIL,
              name: 'Admin',
              role: 'ADMIN',
              plan: 'ENTERPRISE',
            };
          }
        }

        return null;
      },
    }),
  ],
  pages: {
    signIn: '/login',
    newUser: '/onboarding', // Redirect new users to onboarding
  },
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = (user as { role?: string }).role || 'CREATOR';
        token.plan = (user as { plan?: string }).plan || 'FREE';
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        (session.user as { role?: string }).role = token.role as string;
        (session.user as { plan?: string }).plan = token.plan as string;
      }
      return session;
    },
  },
});
