'use client';

import { useState } from 'react';
import { useUser } from '@auth0/nextjs-auth0/client';
import { useRouter } from 'next/navigation';
import LoginOverlay from './LoginOverlay';

export default function LoginButton({
  variant = 'primary',
  children,
}: {
  variant?: 'primary' | 'ghost';
  children?: React.ReactNode;
}) {
  const { user, isLoading } = useUser();
  const router = useRouter();
  const [open, setOpen] = useState(false);

  const label = user ? 'Open Memoray' : children ?? 'Get Started';

  function handleClick() {
    if (isLoading) return;
    if (user) router.push('/dashboard');
    else setOpen(true); // shows the zoom and then redirects
  }

  const base =
    'inline-flex items-center justify-center rounded-full px-6 py-3 font-semibold transition focus:outline-none';
  const styles = variant === 'primary' ? 'btn-primary' : 'glass text-white/90 hover:bg-white/10';

  return (
    <>
      <button onClick={handleClick} className={`${base} ${styles}`}>{label}</button>
      {open && <LoginOverlay returnTo="/dashboard" />}
    </>
  );
}
