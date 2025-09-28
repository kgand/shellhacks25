// src/lib/auth/getUser.ts
import { getSession } from '@auth0/nextjs-auth0';

export async function getUser() {
  const session = await getSession();
  return session?.user ?? null;
}
