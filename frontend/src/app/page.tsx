'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-6 text-center">FastAPI + Next.js Application</h1>
        <p className="text-xl text-center mb-8">
          A full-stack application with FastAPI backend and Next.js frontend
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <Link href="/users">
          <Button size="lg" className="w-full">
            User Management
          </Button>
        </Link>

        <Link href="/items">
          <Button size="lg" className="w-full">
            Item Management
          </Button>
        </Link>

        <Link href="/orders">
          <Button size="lg" className="w-full">
            Order Management
          </Button>
        </Link>
      </div>
    </div>
  )
}