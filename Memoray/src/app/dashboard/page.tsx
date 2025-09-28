// src/app/dashboard/page.tsx
import { getSession } from "@auth0/nextjs-auth0";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await getSession();

  if (!session?.user) {
    redirect("/api/auth/login?returnTo=/dashboard");
  }

  const user = session.user as {
    name?: string;
    email?: string;
    picture?: string;
  };

  return (
    <main className="section py-20">
      <div className="glass p-8">
        <div className="flex items-center gap-4">
          {user.picture && (
            <img
              src={user.picture}
              alt={user.name ?? "User"}
              className="h-12 w-12 rounded-full object-cover"
            />
          )}
          <div>
            <h1 className="text-2xl font-semibold">Welcome back{user.name ? `, ${user.name}` : ""}.</h1>
            <p className="text-white/60">{user.email}</p>
          </div>
        </div>

        <div className="mt-8">
          <a
            className="glass rounded-full px-5 py-3 hover:bg-white/10 transition"
            href="/api/auth/logout"
          >
            Log out
          </a>
        </div>
      </div>
    </main>
  );
}
