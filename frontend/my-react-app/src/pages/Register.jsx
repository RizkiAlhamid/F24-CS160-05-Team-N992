import { useState } from 'react';
import { Leaf } from "lucide-react"
import { Link } from 'react-router-dom';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    // Simulate API call
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      setSuccess(true);
      setEmail('');
      setPassword('');
    } catch (err) {
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-green-50 to-green-100">
        <header className="bg-green-600 text-white">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold flex items-center">
            <Leaf className="mr-2" />
            Particle
          </Link>
         
        </div>
      </header>
     

      <main className="flex-grow flex items-center justify-center px-4 py-8">
        <div className="w-full max-w-md bg-white shadow-md rounded-lg p-6">
          <h2 className="text-3xl text-center text-green-800 font-bold">Create an Account</h2>
          <p className="mt-3 text-center text-green-600 mb-5">Join Particle and start making a difference today!</p>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-3 py-2 border rounded focus:outline-none focus:border-green-500"
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-3 py-2 border rounded focus:outline-none focus:border-green-500"
              />
            </div>
            <button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded">
              Register
            </button>
          </form>
          <p className="text-center text-sm text-green-700 mt-4">
            Already have an account?{" "}
            <Link to="/login" className="text-green-600 hover:underline">Log in</Link>
          </p>
        </div>
      </main>

      {error && (
        <div className="fixed bottom-4 right-4 max-w-md bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {success && (
        <div className="fixed bottom-4 right-4 max-w-md bg-green-100 border border-green-400 text-green-800 px-4 py-3 rounded">
          Registration successful! You can now log in.
        </div>
      )}

        <footer className="bg-green-800 text-white py-8">
          <div className="container mx-auto px-4 text-center">
            <p>&copy; 2024 Particle. All rights reserved.</p>
          </div>
        </footer>
    </div>
  );
}

