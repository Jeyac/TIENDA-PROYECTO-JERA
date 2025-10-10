import type { NavigationGuard } from 'vue-router'
export type MiddlewareKey = "admin-redirect" | "admin" | "atencion" | "auth" | "client" | "user-only"
declare module 'nuxt/app' {
  interface PageMeta {
    middleware?: MiddlewareKey | NavigationGuard | Array<MiddlewareKey | NavigationGuard>
  }
}