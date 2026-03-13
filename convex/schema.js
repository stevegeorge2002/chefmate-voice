import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  orders: defineTable({
    orderId: v.string(),
    tableNumber: v.number(),
    items: v.any(),
    status: v.string(),
    createdAt: v.string(),
    estimatedReadyAt: v.string(),
    urgency: v.string(),
    language: v.string()
  }),
  
  inventory: defineTable({
    item: v.string(),
    quantity: v.number(),
    lastUpdated: v.string()
  }),
  
  conversation: defineTable({
    timestamp: v.string(),
    speaker: v.string(),
    language: v.string(),
    transcript: v.string()
  })
});