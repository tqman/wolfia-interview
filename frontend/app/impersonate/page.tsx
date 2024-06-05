"use client";

import React, {useState} from 'react';
import {login} from "@/api/Auth";
import {useRouter} from "next/navigation";

export default function LoginAsUser() {
  const [email, setEmail] = useState('');
  const [internal_email, setInternalEmail] = useState('');
  const [name, setName] = useState('');
  const [orgName, setOrgName] = useState('');

  const router = useRouter();

  const handleSubmit = (event) => {
    event.preventDefault();
    login({
      email: email,
      name: null,
      organization: null,
      internal_email: internal_email
    }).then((res) => {
      router.push('/');
    })
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h2 className="text-center text-3xl font-extrabold text-black">
          Login As A User
        </h2>
        <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
          <label className="block">
            <span className="block text-sm font-medium text-black">Email to Impersonate:</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-black"
            />
          </label>
          <label className="block">
            <span className="block text-sm font-medium text-black">Internal Email:</span>
            <input
              type="email"
              value={internal_email}
              onChange={(e) => setInternalEmail(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-black"
            />
          </label>
          
          <button
            type="submit"
            className="w-full py-2 px-4 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Submit
          </button>
        </form>
      </div>
    </main>
  );
}
