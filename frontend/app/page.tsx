"use client";

import React, {useEffect, useState} from 'react';
import {api} from "@/api";
import {UserResponse} from "@/api/data-contracts";

export default function Home() {
  const [currentUser, setCurrentUser] = useState<UserResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCurrentUser = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get<UserResponse>('/auth/me');
        setCurrentUser(response.data);
      } catch (error) {
        setError('Error fetching current user');
        console.error('Error fetching current user:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchCurrentUser();
  }, []);

  const handleLogout = async () => {
    try {
      await api.post<Response>('/auth/logout');
      window.location.href = '/login'; // Redirect to the login page
    } catch (err) {
      setError("Failed to log out");
    }
  };

  if (loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <div className="z-10 w-full max-w-5xl items-center justify-center font-mono text-sm lg:flex">
          <h2>Loading...</h2>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <div className="z-10 w-full max-w-5xl items-center justify-center font-mono text-sm lg:flex">
          <h2>{error}</h2>
        </div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        {currentUser && (
          <div>
            <h2><strong>Welcome home, {currentUser.name}!</strong></h2>
            <p><strong>Email:</strong> {currentUser.email}</p>
            <p><strong>Organization:</strong> {currentUser.organization_name}</p>
            <p><strong>Admin:</strong> {currentUser.is_internal ? 'Yes' : 'No'}</p>
            <p><strong>Member since:</strong> {new Date(currentUser.created_at).toLocaleDateString()}</p>
          </div>
        )}
      </div>
      <div>
          <p>Internal User: {currentUser.internal_email}</p>
          <button onClick={handleLogout}>Logout</button>
      </div>
    </main>
  );
}
