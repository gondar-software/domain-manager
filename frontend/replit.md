# Domain Manager Application

## Overview

This is a full-stack web application for managing domain configurations with associated hosts and environments. The application features a React frontend with TypeScript, an Express.js backend, and uses PostgreSQL with Drizzle ORM for database operations. The UI is built with shadcn/ui components and Tailwind CSS for styling.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for development and production builds
- **UI Library**: shadcn/ui components built on Radix UI primitives
- **Styling**: Tailwind CSS with CSS custom properties for theming
- **State Management**: TanStack Query (React Query) for server state management
- **Form Handling**: React Hook Form with Zod validation
- **Routing**: Wouter for client-side routing
- **Theme System**: Custom theme provider supporting light/dark/system modes

### Backend Architecture
- **Runtime**: Node.js with Express.js framework
- **Language**: TypeScript with ESNext modules
- **Database**: PostgreSQL with Drizzle ORM
- **Database Provider**: Neon Database (serverless PostgreSQL)
- **Authentication**: Simple bearer token authentication (development-level)
- **API Style**: RESTful API with JSON responses

### Project Structure
- `client/` - React frontend application
- `server/` - Express.js backend application
- `shared/` - Shared TypeScript schemas and types
- `migrations/` - Database migration files

## Key Components

### Database Schema
The application uses a single main table `domains` with the following structure:
- `id` - Serial primary key
- `subdomain` - Unique text field for domain identification
- `environment` - Text field for environment classification (production, development, staging, testing)
- `hosts` - JSONB array containing host configurations with name, port, and prefix

### Authentication System
- Simple password-based authentication with bearer tokens
- Token storage in localStorage
- Route protection with authentication middleware
- Basic session management

### Data Models
- **Domain**: Main entity representing a domain configuration
- **Host**: Nested entity within domains containing service information
- **Environment**: Enumerated type for categorizing domains

### UI Components
- **DomainCard**: Display component for individual domain configurations
- **DomainModal**: Form modal for creating/editing domains
- **DeleteModal**: Confirmation dialog for domain deletion
- **ThemeToggle**: Theme switching component
- **Login**: Authentication form component

## Data Flow

1. **Authentication Flow**:
   - User submits password through login form
   - Backend validates and returns authentication token
   - Token stored in localStorage and used for subsequent requests

2. **Domain Management Flow**:
   - Dashboard fetches domains using TanStack Query
   - CRUD operations performed through REST API endpoints
   - Real-time UI updates via query cache invalidation
   - Form validation using Zod schemas

3. **State Management**:
   - Server state managed by TanStack Query
   - Local component state for UI interactions
   - Global theme state managed by React Context

## External Dependencies

### Frontend Dependencies
- **UI Framework**: React, React DOM
- **State Management**: TanStack Query
- **Form Handling**: React Hook Form, Hookform Resolvers
- **Validation**: Zod, Drizzle-Zod
- **UI Components**: Radix UI primitives, shadcn/ui
- **Styling**: Tailwind CSS, Class Variance Authority
- **Routing**: Wouter
- **Icons**: Lucide React

### Backend Dependencies
- **Framework**: Express.js
- **Database**: Drizzle ORM, Neon Database serverless driver
- **Validation**: Zod validation
- **Development**: TSX for TypeScript execution

### Development Tools
- **Build**: Vite, ESBuild
- **Database**: Drizzle Kit for migrations
- **TypeScript**: Strict mode enabled
- **Replit Integration**: Vite plugins for Replit environment

## Deployment Strategy

### Development Environment
- Vite dev server for frontend with HMR
- TSX for backend development with auto-restart
- Integrated development using Vite middleware

### Production Build
- Frontend: Vite build outputting to `dist/public`
- Backend: ESBuild bundling server code to `dist/index.js`
- Single process serving both static files and API

### Database Strategy
- PostgreSQL database configured via `DATABASE_URL` environment variable
- Drizzle migrations managed through `drizzle-kit`
- Schema-first approach with TypeScript type generation

### Environment Configuration
- Environment-specific configuration through environment variables
- Development/production mode detection
- Replit-specific integrations for hosted development

The application follows a modern full-stack TypeScript pattern with strong type safety, comprehensive validation, and a component-based architecture that supports both development and production deployment scenarios.