---
description: Create a LLM friendly index for the specified docs folder
argument-hint: [The docs folder to index]
---

- Create an LLM friendly index for the following docs folder : ARGUMENTS
- use `bash tree` to understand folder's structure (including nested content)
- use the template structure bellow
- right the file to the docs folder and name it `index.md`
- reference that file in "## Useful Documentation" in @CLAUDE.md"

<template>

# TanStack Query Documentation Index

This directory contains comprehensive documentation for TanStack Query (formerly React Query), organized for easy exploration and reference.

## Directory Structure

```
docs/llm/tanstack-query/
├── community/
│   ├── community-projects.md
│   └── tkdodos-blog.md
├── guides/
│   ├── advanced-ssr.md
│   ├── background-fetching-indicators.md
│   ├── caching.md
```

## Getting Started

- **Overview**: Start with `overview.md` for a high-level understanding
- **Quick Start**: Jump to `quick-start.md` for immediate implementation
- **Installation**: Check `installation.md` for setup instructions

## Key Documentation Sections

### Guides (`guides/`)

Comprehensive guides covering core concepts including queries, mutations, caching, infinite queries, SSR, and advanced patterns like optimistic updates and background fetching.

### Reference (`reference/`)

Complete API reference for all TanStack Query hooks, components, and utilities including `useQuery`, `useMutation`, `useInfiniteQuery`, and Suspense variants.

## Key Topics

- **Core Concepts**: Queries, mutations, caching, query keys
- **Data Fetching**: Background fetching, parallel queries, dependent queries
- **Advanced Features**: Infinite queries, optimistic updates, SSR support
- **Performance**: Render optimizations, request waterfalls, prefetching
- **Integration**: TypeScript support, React Native, GraphQL

## Files Count: 73 files across 5 directories

</template>
