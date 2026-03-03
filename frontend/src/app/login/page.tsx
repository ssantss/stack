"use client";

import { useState, FormEvent, useEffect } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { useGoogleOAuth } from "@react-oauth/google";
import { GoogleIcon } from "@/components/icons/google";
import { useAuth } from "../contexts/AuthContext";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Eye, EyeOff } from "lucide-react";

export default function LoginPage() {
  const { login, googleLogin, user, loading } = useAuth();
  const { clientId } = useGoogleOAuth();
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (!loading && user) {
      router.replace("/");
    }
  }, [loading, user, router]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await login(username, password);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        setError(err.response.data?.error || "Usuario o contraseña incorrectos");
      } else {
        setError("Error de conexión. Intenta de nuevo.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  async function handleGoogleLogin(credential: string) {
    setError("");
    try {
      await googleLogin(credential);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        setError(err.response.data?.error || "Error al iniciar sesión con Google");
      } else {
        setError("Error de conexión. Intenta de nuevo.");
      }
    }
  }

  if (loading || user) {
    return null;
  }

  return (
    <main className="flex min-h-svh items-center justify-center p-4">
      <Card className="w-full max-w-sm">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Stack</CardTitle>
          <CardDescription>Iniciar sesión</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <Label htmlFor="username">Usuario</Label>
              <Input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="password">Contraseña</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  onClick={() => setShowPassword(!showPassword)}
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            {error && (
              <p className="rounded-md bg-destructive/10 p-2 text-sm text-destructive">
                {error}
              </p>
            )}

            <Button type="submit" disabled={submitting} className="w-full">
              {submitting ? "Ingresando..." : "Iniciar sesión"}
            </Button>
          </form>

          <div className="my-4 flex items-center gap-3">
            <div className="h-px flex-1 bg-border" />
            <span className="text-sm text-muted-foreground">o</span>
            <div className="h-px flex-1 bg-border" />
          </div>

          <Button
            type="button"
            variant="outline"
            className="w-full"
            onClick={() => {
              if (!window.google?.accounts?.id) return;
              window.google.accounts.id.initialize({
                client_id: clientId,
                callback: (response: { credential?: string }) => {
                  if (response.credential) {
                    handleGoogleLogin(response.credential);
                  }
                },
              });
              window.google.accounts.id.prompt();
            }}
          >
            <GoogleIcon className="h-5 w-5" />
            Continuar con Google
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}
