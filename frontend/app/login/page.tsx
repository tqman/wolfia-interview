"use client";

import React, {useState} from 'react';
import {login} from "@/api/Auth";
import {useRouter} from "next/navigation";

export default function LoginRegister() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [orgName, setOrgName] = useState('');

  const router = useRouter();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (isLogin) {
      login({
        email: email,
        name: null,
        organization: null,
        internal_email: null
      }).then((res) => {
        router.push('/');
      })
    } else {
      login({
        email: email,
        name: name,
        organization: orgName,
        internal_email: null
      }).then((res) => {
        router.push('/');
      })
    }
  };

  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h2 className="text-center text-3xl font-extrabold text-black">
          {isLogin ? 'Login' : 'Register'}
        </h2>
        <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
          <label className="block">
            <span className="block text-sm font-medium text-black">Email:</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-black"
            />
          </label>
          {!isLogin && (
            <>
              <label className="block">
                <span className="block text-sm font-medium text-black">Name:</span>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-black"
                />
              </label>
              <label className="block">
                <span className="block text-sm font-medium text-black">Organization Name:</span>
                <input
                  type="text"
                  value={orgName}
                  onChange={(e) => setOrgName(e.target.value)}
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-black"
                />
              </label>
            </>
          )}
          <button
            type="submit"
            className="w-full py-2 px-4 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Submit
          </button>
        </form>
        <button
          onClick={toggleForm}
          className="w-full py-2 px-4 text-indigo-600 font-medium rounded-md hover:text-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          {isLogin ? 'Register here' : 'Login here'}
        </button>
      </div>
    </main>
  );
}
