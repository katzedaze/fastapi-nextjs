# Next.js Frontend

This is the frontend application for the FastAPI-NextJS project.

## Technology Stack

- **Next.js**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Re-usable UI components built with Radix UI

## Project Structure

```
frontend/
├── public/             # Static files
└── src/
    ├── app/            # Next.js App Router pages
    ├── components/     # React components
    │   └── ui/         # UI components
    ├── contexts/       # React contexts
    ├── hooks/          # Custom React hooks
    ├── lib/            # Utility functions
    ├── services/       # API services
    ├── types/          # TypeScript type definitions
    └── utils/          # Helper utilities
```

## Development

### Local Setup

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:

   ```bash
   npm run dev
   ```

3. Build for production:

   ```bash
   npm run build
   ```

4. Start production server:

   ```bash
   npm start
   ```

## Environment Variables

Create a `.env.local` file in the frontend directory with the following variables:

```
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME="FastAPI NextJS App"
```

## Features

- User management (CRUD operations)
- Responsive design with Tailwind CSS
- Type-safe API requests with TypeScript
- Server-side rendering with Next.js
- Component library with shadcn/ui

## Available Pages

- Home Page: `/`
- User List: `/users`
- Create User: `/users/create`
- Edit User: `/users/edit/[id]`
