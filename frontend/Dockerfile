# 1. Builder Stage: Install dependencies, build the app
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files and install all dependencies (incl. dev)
# Assumes package-lock.json is present and correct
COPY package.json package-lock.json* ./
RUN npm ci

# Copy the rest of the source code
COPY . .

# Disable Next.js telemetry
ENV NEXT_TELEMETRY_DISABLED 1

# Build the Next.js application
# This requires all dependencies, including devDependencies
RUN npm run build

# 2. Runner Stage: Create the final, small production image
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Create a non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy production-ready files from the builder stage
# This leverages Next.js's "standalone" output feature
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to the non-root user
USER nextjs

EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Start the Next.js server using the standalone output
CMD ["node", "server.js"]
