"use client";

import { useAuth } from "./contexts/AuthContext";
import { Button } from "@/components/ui/button";

export default function Home() {
  const { user, loading, logout } = useAuth();

  if (loading || !user) {
    return null;
  }

  const displayName =
    user.first_name && user.last_name
      ? `${user.first_name} ${user.last_name}`
      : user.username;

  return (
    <main className="flex min-h-svh flex-col items-center justify-center">
      <h1 className="text-3xl font-bold">Stack</h1>
      <p className="mb-8 text-muted-foreground">Dashboard</p>
      <p className="mb-4">Hola, {displayName}</p>
      <Button variant="outline" onClick={logout}>
        Cerrar sesión
      </Button>
    </main>
  );
}
