'use client';

import { useEffect } from 'react';

export default function LoginOverlay({ returnTo = '/dashboard' }: { returnTo?: string }) {
  useEffect(() => {
    const t = setTimeout(() => {
      window.location.href = `/api/auth/login?returnTo=${encodeURIComponent(returnTo)}`;
    }, 450); // wait for the zoom animation
    return () => clearTimeout(t);
  }, [returnTo]);

  return (
    <div
      className="fixed inset-0 z-[100] grid place-items-center bg-black/60"
      aria-live="polite"
      aria-busy="true"
    >
      {/* zoom bubble */}
      <div className="animate-[zoomIn_.45s_ease-out_forwards] w-24 h-24 rounded-full bg-violet-500 shadow-2xl" />
      <style jsx global>{`
        @keyframes zoomIn {
          from { transform: scale(0); opacity: .85; }
          to   { transform: scale(40); opacity: 1; }
        }
      `}</style>
    </div>
  );
}
