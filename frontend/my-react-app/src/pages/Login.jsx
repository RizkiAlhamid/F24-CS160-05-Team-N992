import { useState } from 'react'
import { Leaf } from "lucide-react"
import { Link } from "react-router-dom" // Replace with your router's Link

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess(false)

    try {
      // Simulating an API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      setSuccess(true)
    } catch (err) {
      setError('Login failed. Please check your credentials and try again.')
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-green-50 to-green-100">
      
      <header className="bg-green-600 text-white">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold flex items-center">
            <Leaf className="mr-2" />
            EcoAlerts
          </Link>
        </div>
      </header>

      <main className="flex-grow flex items-center justify-center px-4 py-8">
        <div className="w-full max-w-md bg-white shadow-lg rounded-lg p-6">
          <header className="text-center mb-4">
            <h2 className="text-3xl text-green-800 font-bold">Welcome Back!</h2>
            <p className="text-green-600 mt-3">Log in to your EcoAlerts account</p>
          </header>
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
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
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
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            {/* <button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-md">
              Log In
            </button> */} 

            <Link to="/home" className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-md">
              Log In
            </Link>   
            {/* Just for the demo */}
            
          </form>
          <footer className="flex flex-col space-y-2 mt-4">
            <p className="text-sm text-green-700 text-center">
              Don't have an account?{" "}
              <Link to="/register" className="text-green-600 hover:underline">
                Sign up
              </Link>
            </p>
          </footer>
        </div>
      </main>

      {error && (
        <div className="fixed bottom-4 right-4 max-w-md bg-red-100 border border-red-400 text-red-800 p-4 rounded-md">
          {error}
        </div>
      )}

      {success && (
        <div className="fixed bottom-4 right-4 max-w-md bg-green-100 border border-green-400 text-green-800 p-4 rounded-md">
          Login successful! Redirecting to your dashboard...
        </div>
      )}

        <footer className="bg-green-800 text-white py-8">
          <div className="container mx-auto px-4 text-center">
            <p>&copy; 2024 EcoAlerts. All rights reserved.</p>
          </div>
        </footer>
    </div>
  )
}
