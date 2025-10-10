// TypeScript augmentation for Nuxt app injections used across templates
import { NuxtApp } from '#app'
import { ComponentCustomProperties } from 'vue'

type AnyRecord = Record<string, any>

declare module '#app' {
  interface NuxtApp {
    $formatCurrency: (value: number, currency?: string) => string
    $formatDate: (date: string | number | Date) => string

    $analyticsUi?: { kpiIcon?: string; kpiCard?: string; listIcon?: string }
    $productsUi?: { thumb?: string; placeholder?: string; price?: string }
    $catalogUi?: { card?: string; badgeCategory?: string; btnAdd?: string }
  }

  interface PageMeta {
    middleware?: 'auth' | 'admin' | 'client' | MiddlewareKey | NavigationGuard
  }
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $formatCurrency: (value: number, currency?: string) => string
    $formatDate: (date: string | number | Date) => string

    $analyticsUi?: { kpiIcon?: string; kpiCard?: string; listIcon?: string }
    $productsUi?: { thumb?: string; placeholder?: string; price?: string }
    $catalogUi?: { card?: string; badgeCategory?: string; btnAdd?: string }
  }
}


