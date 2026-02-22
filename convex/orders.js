import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const createOrder = mutation({
  args: {
    orderId: v.string(),
    tableNumber: v.number(),
    items: v.any(),
    estimatedReadyAt: v.string(),
    language: v.string()
  },
  handler: async (ctx, args) => {
    return await ctx.db.insert("orders", {
      ...args,
      status: "cooking",
      urgency: "normal",
      createdAt: new Date().toISOString()
    });
  }
});

export const getActiveOrders = query({
  handler: async (ctx) => {
    return await ctx.db
      .query("orders")
      .filter(q => q.neq(q.field("status"), "completed"))
      .collect();
  }
});

export const completeOrder = mutation({
  args: { orderId: v.string() },
  handler: async (ctx, args) => {
    const order = await ctx.db
      .query("orders")
      .filter(q => q.eq(q.field("orderId"), args.orderId))
      .first();
    
    if (order) {
      await ctx.db.patch(order._id, {
        status: "completed",
        completedAt: new Date().toISOString()
      });
    }
  }
});
```

**Save (Ctrl+S) and close.**

---

## 📊 Check Convex Terminal

**Look at your Convex terminal (the one that's still running).**

**You should see:**
```
✔ Functions synced
✔ Watching for changes...